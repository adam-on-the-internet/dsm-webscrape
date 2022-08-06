class CalendarEvent:
    def __init__(self, name, day, month, year, time, detail):
        self.name = name
        self.day = day
        self.month = month
        self.year = year
        self.time = time
        self.detail = detail
        self.checked = False
        self.found_date = None

        # TODO how to we get the event details url? usually in-site javascript
        # Should we link to month calendar?
        # https://www.dsm.city/calendar_app/calendar_event_detail.html?eventId=1320&date=8/2/2022&show=no

    def get_date_full(self):
        return f"{self.year}-{self.month}-{self.day}"

    def get_message(self):
        return f"{self.get_date_full()} {self.name}"
