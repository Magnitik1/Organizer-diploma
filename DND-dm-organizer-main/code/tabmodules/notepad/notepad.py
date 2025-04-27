from kivy.uix.screenmanager import Screen
from kivyutils import load_kv_for

load_kv_for(__file__)

#exported to the tab loader, and instantiated only when accessed
class NotepadTab(Screen):
  name = None
  subtext = None
  color = "#E4E181"


class Note():
  def __init__(self, text, name=None):
    if name is None:
      name = text[:20] + "..." if len(text) > 20 else text
    self.name = name
    self.text = text
 


tabmodule_tab_export=NotepadTab

