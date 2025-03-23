from kivy.uix.screenmanager import Screen
from kivyutils import load_kv_for

load_kv_for(__file__)

#exported to the tab loader, and instantiated only when accessed
class NotepadTab(Screen):
  name = None
  subtext = None
  color = "#E4E181"


#used by the tab module importer
#must be a `kivy.uix.screenmanager.Screen` subclass 
tabmodule_tab_export=NotepadTab