from queue import Queue
from threading import Thread

from requests import Session, Response
import toga

class WorkerThread(Thread):
    """A worker that fetches pages in the background."""

    def __init__(self, session: Session) -> None:
        super().__init__()
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

    def _done_loading(self, response: Response):
        self.contents = [toga.Label(response.text)]
        # TODO use beautifulsoup and generate widgets based on page contents
        self._loaded_callback(self)
