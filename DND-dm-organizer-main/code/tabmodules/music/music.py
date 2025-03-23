from kivy.uix.screenmanager import Screen
from kivyutils import load_kv_for

load_kv_for(__file__)

#exported to the tab loader, and instantiated only when accessed
class MusicTab(Screen):
  pass

#used by the tab module importer
#must be a `kivy.uix.screenmanager.Screen` subclass 
tabmodule_tab_export=MusicTab