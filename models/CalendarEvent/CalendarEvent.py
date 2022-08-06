class CalendarEvent:
    def __init__(self, raw_calendar_event, day, month, year):
        self.day = day
        self.month = month
        self.year = year

        self.name = raw_calendar_event.name
        self.time = raw_calendar_event.time_begin
        self.detail = raw_calendar_event.detail
        self.duration = raw_calendar_event.duration_formatted
        self.contact_name = raw_calendar_event.contact_name
        self.contact_email = raw_calendar_event.contact_email
        self.contact_phone = raw_calendar_event.contact_phone
        self.is_notable = raw_calendar_event.is_notable

        # TODO how to we get the event details url? usually in-site javascript
        # Should we link to month calendar?
        # https://www.dsm.city/calendar_app/calendar_event_detail.html?eventId=1320&date=8/2/2022&show=no

    def get_date_full(self):
        return f"{self.year}-{self.month}-{self.day}"

    def get_message(self):
        return f"CALENDAR EVENT: {self.get_date_full()} {self.time} {self.name}"

    def to_json(self):
        return {
            "day": self.day,
            "month": self.month,
            "year": self.year,
            "name": self.name,
            "time": self.time,
            "detail": self.detail,
            "duration": self.duration,
            "contact_name": self.contact_name,
            "contact_phone": self.contact_phone,
            "is_notable": 'true' if self.is_notable else 'false',
        }
