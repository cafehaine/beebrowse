"""
A simple hypertext browser
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .tab import Tab


class BeeBrowse(toga.App):
    """The main app for Bee Browse"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tabs = []
        self._focused_tab = -1
        self.main_window: toga.MainWindow
        self.tab_box: toga.Box
        self.tab_contents_box: toga.Box

    def _close_tab(self, tab):
        # TODO
        print("TODO: close tab", tab)

    def _focus_tab(self, tab):
        # TODO
        print("TODO: focus tab", tab)

    def _update_tab_box(self):
        self.tab_box.remove(*self.tab_box.children)
        for tab in self._tabs:
            select_button = toga.Button(str(tab), on_press=lambda _: self._focus_tab(tab))
            close_button = toga.Button("x", on_press=lambda _: self._close_tab(tab))
            box = toga.Box(children=[select_button, close_button])
            self.tab_box.add(box)

    def _update_url_box(self):
        pass

    def _update_contents(self):
        self.tab_contents_box.remove(*self.tab_contents_box.children)
        self.tab_contents_box.add(*self._tabs[self._focused_tab].contents)

    def _update_title(self):
        pass

    def _new_tab(self, url=None, focus=False):
        self._tabs.insert(self._focused_tab + 1, Tab(url))
        if focus:
            self._focused_tab += 1
        self._update_tab_box()
        self._update_url_box()
        self._update_contents()
        self._update_title()

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.url_input = toga.TextInput()
        self.back_button = toga.Button("←")
        self.forward_button = toga.Button("→")
        refresh_button = toga.Button("🔁")
        downloads_button = toga.Button("⇓")
        url_box = toga.Box(children=[self.back_button, self.forward_button, self.url_input, refresh_button, downloads_button])

        new_tab_button = toga.Button("+", on_press=lambda _: self._new_tab())
        self.tab_box = toga.Box(style=Pack(direction=ROW))
        tab_scroll = toga.ScrollContainer(vertical=False, content=self.tab_box)
        tab_bar = toga.Box(children=[tab_scroll, new_tab_button], style=Pack(direction=ROW))

        self.tab_contents_box = toga.Box()

        main_box = toga.Box(children=[tab_bar, url_box, self.tab_contents_box], style=Pack(direction=COLUMN))

        self._new_tab(focus=True)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return BeeBrowse()
