class CouncilMeetingSummary:
    def __init__(self, date, title, subtitle, details_url):
        self.date = date
        self.title = title
        self.subtitle = subtitle
        self.details_url = details_url

    def get_message(self):
        return f"COUNCIL MEETING: {self.date} {self.title} ({self.details_url})"
