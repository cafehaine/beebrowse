class Tab:
    """A tab and it's history."""
    def __init__(self, url = None):
        if url is None:
            url = "https://duckduckgo.com/" # config.new_tab
        self.url = url
        self.history = [url]
