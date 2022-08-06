class RawCalendarEvent:
    def __init__(self, xml, name, date_begin, time_begin, detail, repeat):
        self.xml = xml
        self.name = name
        self.date_begin = date_begin
        self.time_begin = time_begin
        self.detail = detail
        self.repeat = repeat

    def is_repeat(self):
        return self.repeat != ""

    def get_occurrence_dates(self):
        raw_dates = self.xml.find("dates")
        dates = raw_dates.get_text().strip()
        return dates.split(",")
