import toga

class Tab:
    """A tab and it's history."""
    def __init__(self, url = None):
        if url is None:
            url = "https://duckduckgo.com/" # config.new_tab
        self.url: str = url
        self._title: Optional[str] = None
        self.history = [url]
        self.contents: List[toga.Widget] = []
        self._load_contents()

    @property
    def title(self) -> str:
        if self._title is None:
            return self.url
        return self._title

    def _load_contents(self):
        # TODO download url
        # TODO fill contents
        self.contents = [toga.Label("Hello :)")]
