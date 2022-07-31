class NewsPost:
    def __init__(self, heading_title, heading_date, heading_url, page_title, page_url, page_content):
        self.heading_title = heading_title
        self.heading_date = heading_date
        self.heading_url = heading_url
        self.page_title = page_title
        self.page_url = page_url
        self.page_content = page_content

    def get_message(self):
        return f"NEWS: {self.heading_title} ({self.page_url})"

    def to_json(self):
        return {
            "heading_title": self.heading_title,
            "heading_url": self.heading_url,
            "page_url": self.page_url,
            "page_content": self.page_content,
            "page_title": self.page_title,
            "heading_date": self.heading_date
        }
