import fitz  # PyMuPDF
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.graphics.texture import Texture
from kivyutils import load_kv_for

load_kv_for(__file__)

NPC_NAMES = {"Tom", "Betty", "Violet", "Hannah", "Dee", "Larry"}

class PDFPageView(FloatLayout):
    def __init__(self, page, zoom=2.0, **kwargs):
        super().__init__(**kwargs)
        self.page = page

        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        orig_w, orig_h = pix.width, pix.height
        aspect = orig_h / orig_w

        self.size_hint_x = 1
        self.size_hint_y = None
        self.height = self.width * aspect
        self.bind(width=lambda inst, w: setattr(inst, 'height', w * aspect))

        tex = Texture.create(size=(orig_w, orig_h), colorfmt='rgb')
        tex.blit_buffer(pix.samples, colorfmt='rgb', bufferfmt='ubyte')
        tex.flip_vertical()
        img = Image(
            texture=tex,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.add_widget(img)

        rect = page.rect
        words = page.get_text("words")

        for x0, y0, x1, y1, word, *_ in words:
            subwords = word.replace(',', ' ').replace('—', ' ').replace('-', ' ').split()
            w_total = x1 - x0
            if len(subwords) > 1:
                word_width = w_total / len(subwords)
            else:
                word_width = w_total

            for idx, subword in enumerate(subwords):
                clean = subword.strip('.,:;"\'!?()[]')
                if clean in NPC_NAMES:
                    sub_x0 = x0 + idx * word_width
                    sub_x1 = sub_x0 + word_width

                    w_norm = (sub_x1 - sub_x0) / rect.width
                    h_norm = (y1 - y0) / rect.height
                    x_norm = sub_x0 / rect.width
                    y_norm = 1 - (y1 / rect.height)

                    btn = Button(
                        size_hint=(w_norm, h_norm),
                        pos_hint={'x': x_norm, 'y': y_norm},
                        background_color=(0, 1, 0, 0.4),
                        background_normal='',
                        background_down='',
                    )
                    btn.bind(on_press=lambda inst, t=clean: print("Clicked on:", t))
                    self.add_widget(btn)

class CampaignTab(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_enter=self.load_pdf)

    def load_pdf(self, *args):
        if getattr(self, '_pdf_loaded', False):
            return

        doc = fitz.open("code/Wiebe_TheHangover.pdf")
        container = self.ids.pdf_container
        for page in doc:
            container.add_widget(PDFPageView(page))
        self._pdf_loaded = True

tabmodule_tab_export = CampaignTab
