class NewsPost:
    def __init__(self, url, heading_title, heading_date, page_title, page_content):
        self.url = url
        self.heading_title = heading_title
        self.heading_date = heading_date
        self.page_title = page_title
        self.page_content = page_content

    def get_message(self):
        return f"NEWS: {self.heading_title} ({self.url})"

    def to_json(self):
        return {
            "url": self.url,
            "heading_title": self.heading_title,
            "heading_date": self.heading_date,
            "page_title": self.page_title,
            "page_content": self.page_content,
        }
