class BaseCalendarEvent:
    def __init__(self, day, month, year, time, name):
        self.day = day
        self.month = month
        self.year = year
        self.time = time
        self.name = name

    def get_date_full(self):
        return f"{self.year}-{self.month}-{self.day}"

    def get_message(self):
        return f"CALENDAR EVENT FOUND: {self.get_date_full()} {self.time} {self.name}"
