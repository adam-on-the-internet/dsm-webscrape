class CouncilMeetingSummary:
    def __init__(self, day, month, year, time, title, subtitle, url, links, meeting_id):
        self.day = day
        self.month = month
        self.year = year
        self.time = time
        self.url = url
        self.title = title
        self.subtitle = subtitle
        self.links = links
        self.meeting_id = meeting_id

    def __eq__(self, other):
        return self.day == other.day and self.month == other.month and self.year == other.year and \
               self.time == other.time and self.url == other.url and self.title == other.title and \
               self.subtitle == other.subtitle and self.links == other.links

    def get_date_full(self):
        return f"{self.year}-{self.month}-{self.day}"

    def get_status(self):
        if self.meeting_id is None:
            return "FOUND"
        else:
            return "UPDATED"

    def get_message(self):
        return f"COUNCIL MEETING {self.get_status()}: {self.get_date_full()} {self.title} ({self.url}) [{len(self.links)} link(s)]"

    def to_json(self):
        return {
            "day": self.day,
            "month": self.month,
            "year": self.year,
            "time": self.time,
            "title": self.title,
            "subtitle": self.subtitle,
            "url": self.url,
            "links": self.links,
        }

