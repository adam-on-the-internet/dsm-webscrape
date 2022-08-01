class CouncilMeetingSummary:
    def __init__(self, date, title, subtitle, heading_url, page_url, links):
        self.date = date
        self.title = title
        self.subtitle = subtitle
        self.heading_url = heading_url
        self.page_url = page_url
        self.links = links

    def get_message(self):
        return f"COUNCIL MEETING: {self.date} {self.title} ({self.page_url}) [{len(self.links)} link(s)]"
