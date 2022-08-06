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

    def get_message(self):
        return f"{self.year}-{self.month}-{self.day} {self.name}"
