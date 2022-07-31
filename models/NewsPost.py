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
