from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (ObjectProperty)
import myconfig
import json
import TabsWidget
from kivy.core.window import Window


Window.size = (1000, 600)


class MyApp(App):
    def build(self):
        tabsWidget=TabsWidget.TabsWidget()
        tabsWidget.load_default_tabs()

        return tabsWidget


