"""
A simple hypertext browser
"""
from requests import Session
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
        self.session = Session()
        self.session.headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", # Taken from Firefox Developer Edition on Wed 17 Feb 2021
            "User-Agent": "BeeBrowse 0.1",
            })

    def _close_tab(self, tab):
        tab_index = self._tabs.index(tab)
        if tab_index <= self._focused_tab:
            self._focused_tab -= 1
        self._tabs.pop(tab_index)
        if not self._tabs:
            self.main_window.close()
            return
        self._update_tab_box()
        self._update_url_box()
        self._update_contents()
        self._update_title()

    def _focus_tab(self, tab):
        self._focused_tab = self._tabs.index(tab)
        self._update_tab_box()
        self._update_url_box()
        self._update_contents()
        self._update_title()

    def _update_tab_box(self):
        self.tab_box.remove(*self.tab_box.children)
        for tab in self._tabs:
            select_button = toga.Button(tab.title, on_press=lambda _: self._focus_tab(tab))
            close_button = toga.Button("x", on_press=lambda _: self._close_tab(tab))
            box = toga.Box(children=[select_button, close_button])
            self.tab_box.add(box)

    def _update_url_box(self):
        self.url_input.value = self._tabs[self._focused_tab].url

    def _update_contents(self):
        self.tab_contents_box.remove(*self.tab_contents_box.children)
        self.tab_contents_box.add(*self._tabs[self._focused_tab].contents)

    def _update_title(self):
        tab_title = self._tabs[self._focused_tab].title
        self.main_window.title = f"{tab_title} − Bee Browse"

    def _new_tab(self, url=None, focus=False):
        self._tabs.insert(self._focused_tab + 1, Tab(self.session, url, on_loaded=self._tab_loaded))
        if focus:
            self._focused_tab += 1
        self._update_tab_box()
        self._update_url_box()
        self._update_contents()
        self._update_title()

    def _history_backward(self):
        print("TODO history backward")# TODO

    def _history_forward(self):
        print("TODO history forward")# TODO

    def _navigate_url(self):
        print("TODO navigate url")# TODO

    def _popup_downloads(self):
        print("TODO popup downloads") # TODO

    def _tab_loaded(self, tab: Tab) -> None:
        self._update_tab_box()
        self._update_contents()
        self._update_title()

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.url_input = toga.TextInput(placeholder="url")
        self.url_input.style.update(flex=1)
        self.back_button = toga.Button("←", on_press=lambda _: self._history_backward())
        self.forward_button = toga.Button("→", on_press=lambda _: self._history_forward())
        refresh_button = toga.Button("🔁", on_press=lambda _: self._navigate_url())
        downloads_button = toga.Button("⇓", on_press=lambda _: self._popup_downloads())
        url_box = toga.Box(children=[self.back_button, self.forward_button, self.url_input, refresh_button, downloads_button])

        new_tab_button = toga.Button("+", on_press=lambda _: self._new_tab())
        self.tab_box = toga.Box(style=Pack(direction=ROW))
        tab_scroll = toga.ScrollContainer(vertical=False, content=self.tab_box)
        tab_scroll.style.update(flex=1)
        tab_bar = toga.Box(children=[tab_scroll, new_tab_button], style=Pack(direction=ROW))

        self.tab_contents_box = toga.Box()
        contents_scroll = toga.ScrollContainer(content=self.tab_contents_box)
        contents_scroll.style.update(flex=1)

        main_box = toga.Box(children=[tab_bar, url_box, contents_scroll], style=Pack(direction=COLUMN))
        main_box.style.update(flex=1)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box

        self._new_tab(focus=True)
        self.main_window.show()


def main():
    return BeeBrowse()
