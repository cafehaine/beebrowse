from queue import Queue
from threading import Thread
from typing import List, Optional

from bs4 import BeautifulSoup, Tag
from requests import Session, Response
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class WorkerThread(Thread):
    """A worker that fetches pages in the background."""

    def __init__(self, session: Session) -> None:
        super().__init__(daemon=True)
        self._session = session
        self._task_queue = Queue()

    def run(self) -> None:
        while True:
            url, callback = self._task_queue.get()
            results = self._session.get(url)
            callback(results)


    def fetch(self, url, callback):
        self._task_queue.put((url, callback))

class Tab:
    """A tab and it's history."""
    def __init__(self, session: Session, url = None, on_loaded = None):
        if url is None:
            url = "https://duckduckgo.com/" # config.new_tab
        self.url: str = url
        self._title: Optional[str] = None
        self.history = [url]
        self.contents: List[toga.Widget] = [toga.Label("LOADING")]
        self._loaded_callback = on_loaded
        self._worker_thread = WorkerThread(session)
        self._worker_thread.start()
        self._worker_thread.fetch(self.url, self._done_loading)

    @property
    def title(self) -> str:
        if self._title is None:
            return self.url
        return self._title

    def _recursively_build_page(self, tag: Tag) -> Optional[toga.Widget]:
        if tag.name in ("p", "span", "h1", "h2", "h3", "h4", "h5", "h6"):
            # TODO custom styling for titles
            # TODO hande em/i/b/…
            return toga.Label(tag.text)
        if tag.name == "a":
            # TODO handle navigation
            return toga.Button(tag.text)
        if tag.name == "script":
            return None
        if tag.name == "img":
            # TODO use an Image widget
            return toga.Label(tag.get("alt", "no description"))
        if tag.name == "hr":
            return toga.Divider()
        if tag.name in ("div", "main", "article", "section", "header", "footer", "body", "noscript"):
            children = [self._recursively_build_page(child) for child in tag.children]
            return toga.Box(children=[child for child in children if child is not None], style=Pack(direction=COLUMN))
        return toga.Label(str(tag)) # TODO proper support

    def _widgets_from_soup(self, soup: BeautifulSoup) -> List[toga.Widget]:
        head = soup.find("head")
        if head is not None:
            title = head.find("title")
            # TODO favicon, some meta?
            if title is not None:
                self._title = title.text

        output = None
        body = soup.find("body")
        if body is not None:
            element = self._recursively_build_page(body)
            if element is not None:
                output = [element]
        if not output:
            output = [toga.Label("Empty page.")]
        return output

    def _done_loading(self, response: Response):
        self.contents = self._widgets_from_soup(BeautifulSoup(response.text, features="lxml"))
        self._loaded_callback(self)
