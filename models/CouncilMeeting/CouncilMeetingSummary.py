class CouncilMeetingSummary:
    def __init__(self, day, month, year, time, title, subtitle, url, links, __id):
        self.day = day
        self.month = month
        self.year = year
        self.time = time
        self.url = url
        self.title = title
        self.subtitle = subtitle
        self.links = links
        self.__id = __id

    def get_date_full(self):
        return f"{self.year}-{self.month}-{self.day}"

    def get_status(self):
        if self.__id is None:
            return "UPDATED"
        else:
            return "FOUND"

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

