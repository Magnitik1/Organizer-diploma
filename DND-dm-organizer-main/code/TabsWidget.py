from __future__ import annotations

from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.event import EventDispatcher
from kivy.properties import (
    ObjectProperty,
    ListProperty,
    StringProperty,
    BooleanProperty,
    ColorProperty
)

from kivyutils import load_kv_for

import importlib as _importlib
import typing
import functools
from collections import OrderedDict

# The keys for the translated text used in tab name display
tabmodule_IDs = ["Campaign", "NPC", "Fight", "Notepad", "Music", "Spells", "Equipment"]


# The names of the folders fo the modules in ./tabmodules
def to_tabmodule_names(tabmodule_IDs):
    return map(lambda id: id.lower(), tabmodule_IDs)


load_kv_for(__file__)

from dataclasses import (dataclass, field)
import weakref
import abc


class _TabMenuBarButton(Button):
    def __init__(self, tabmodule_ID: str, **kwargs):
        self.tabmodule_ID = tabmodule_ID
        # Super after assignment, because otherwise the button tries to get text translation for an empty id
        super().__init__(**kwargs)


    tabmodule_ID: str = StringProperty()
    is_selected: bool = BooleanProperty(False)
    background_default = ColorProperty((0.3294, 0.4078, 0.2824, 1))
    background_selected = ColorProperty((0.5490, 0.6118, 0.4078, 1))
    background_color_pressed = ColorProperty((0.4941, 0.5506, 0.3670, 1))


@dataclass
class Tab:
    """A class that represents a single tab"""
    tabmodule_ID: str
    tabmodule_Screen: Screen

    # assigned by the loading TabsWidget
    _assigned_Button = typing.cast(_TabMenuBarButton, None)
    _tab_order_id = 0


class TabsWidget(BoxLayout, Widget):
    """Displays a menu for switching tabs,
       as well as the content of the selected one,
       content is represented by a `Widget`"""
    # Going through a fake cast, because
    # ListProperty doesn't have typing information
    tabs = typing.cast(list[Tab], ListProperty())
    # kv assigned
    ScreenManager = ObjectProperty()
    _tabs_by_IDs: dict[str, Tab]


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tabs_by_IDs = {}

    @staticmethod
    def on_tabs(inst, tabs: list[Tab]):
        menu_bar: Widget = inst.ids.tabs_menu_bar
        # Reset all
        menu_bar.clear_widgets()
        inst._tabs_by_IDs.clear()
        inst.tab_manager.clear_widgets()
        if not inst.tabs:
            return
        for tab, tab_order_id in zip(tabs, range(len(tabs))):
            # Add button to menu
            btn = _TabMenuBarButton(tab.tabmodule_ID)
            btn.on_press = functools.partial(inst.on_tabmenubarbutton_press, btn)
            menu_bar.add_widget(btn)
            # Backlink tab to button, and record tab order
            tab._assigned_Button = weakref.proxy(btn)
            tab._tab_order_id = tab_order_id
            inst._tabs_by_IDs[tab.tabmodule_ID] = tab

            inst.tab_manager.add_widget(tab.tabmodule_Screen)
        if inst.selected_tab is None:
            inst.selected_tab = inst.tabs[0]

    def on_tabmenubarbutton_press(self, btn):
        self.selected_tab = self._tabs_by_IDs[btn.tabmodule_ID]


    selected_tab = ObjectProperty(None)
    selected_tab_previous: Tab | None = None

    @staticmethod
    def on_selected_tab(inst: TabsWidget, tab: Tab):
        prev_order_id = 0
        # SwitchButtonColors
        if inst.selected_tab_previous is not None:
            inst.selected_tab_previous._assigned_Button.is_selected = False
            prev_order_id = inst.selected_tab_previous._tab_order_id
        tab._assigned_Button.is_selected = True
        # Tab switch
        now_order_id = tab._tab_order_id
        inst.tab_manager.transition.direction = "left" if now_order_id > prev_order_id else "right"

        inst.tab_manager.current = tab.tabmodule_ID
        # end
        inst.selected_tab_previous = tab



    def load_default_tabs(self):
        self.tabs = load_tabmodules(tabmodule_IDs)


def load_tabmodules(tabmodule_IDs=tabmodule_IDs):
    tabmodule_names = to_tabmodule_names(tabmodule_IDs)
    tabs: list[Tab] = []
    for [tabmodule_ID, tabmodule_name] in zip(tabmodule_IDs, tabmodule_names):
        module_path = "tabmodules." + tabmodule_name
        # load python module
        tabmodule_tab_export = _get_tabmodule_export(module_path) \
                               or _get_tabmodule_export(module_path + "." + tabmodule_name)
        # special case for .py file of same name as it's dir^
        if tabmodule_tab_export is None:
            raise Exception("Loaded module " + tabmodule_ID + " does not export tab")

        # instantiate the exported class
        tab_Screen = tabmodule_tab_export(name=tabmodule_ID)
        tabs.append(Tab(tabmodule_ID, tab_Screen))
    return tabs

# widget which responsible for each tab
def _get_tabmodule_export(tabmodule_path) -> typing.Optional[type[Screen]]:
    tabmodule = _importlib.import_module(tabmodule_path, package=None)
    if hasattr(tabmodule, "tabmodule_tab_export"):
        return getattr(tabmodule, "tabmodule_tab_export")
    else:
        return None

