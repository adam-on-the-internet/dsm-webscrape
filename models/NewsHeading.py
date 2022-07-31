class NewsHeading:
    def __init__(self, title, url, date):
        self.title = title
        self.url = url
        self.date = date

    def print(self):
        print(f"Title: {self.title}")
        print(f"URL: {self.url}")
        print(f"Date: {self.date}")
