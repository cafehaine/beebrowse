"""
A simple hypertext browser
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .tab import Tab


class BeeBrowse(toga.App):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tabs = []
        self._focused_tab = -1
        self.main_window: toga.MainWindow
        self.tab_box: toga.Box

    def _update_tab_box(self):
        self.tab_box.remove(*self.tab_box.children)
        for tab in self._tabs:
            self.tab_box.add(toga.Button(str(tab)))

    def _new_tab(self, url=None, focus=False):
        self._tabs.insert(self._focused_tab + 1, Tab(url))
        if focus:
            self._focused_tab += 1
        print("New tab:", url)
        self._update_tab_box()

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        new_tab_button = toga.Button("+", on_press=self._new_tab)
        self.tab_box = toga.Box()
        # TODO wrap in a scroll container
        tab_bar = toga.Box(children=[self.tab_box, new_tab_button])
        main_box = toga.Box(children=[tab_bar])

        self._new_tab(focus=True)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return BeeBrowse()
