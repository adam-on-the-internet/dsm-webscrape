from util import soup_util, date_util


class RawCalendarEvent:
    def __init__(self, xml_event, month, year):
        # XML Meta
        self.xml_event = xml_event
        self.event_id = soup_util.get_element_attr(self.xml_event, "id")
        self.calendar_id = soup_util.get_element_attr(self.xml_event, "calendarid")

        # Useful XML fields
        self.name = self.get_attr("name")
        self.date_begin = self.get_attr("date_begin")
        self.date_end = self.get_attr("date_end")
        self.time_begin = self.get_attr("time_begin")
        self.detail = self.get_attr("detail")
        self.repeat = self.get_attr("repeat")
        self.dates = self.get_attr("dates").split(",")

        # Unused XML fields
        self.duration = self.get_attr("duration")
        self.duration_formatted = self.get_attr("duration_formatted")
        self.is_notable = self.get_attr("notable") == "yes"
        self.repeat_units = self.get_attr("repeatUnits")
        self.repeat_count = self.get_attr("repeatCount")
        self.repeat_other = self.get_attr("repeatOther")
        self.repeat_description = self.get_attr("repeatDesc")
        self.summary = self.get_attr("summary")
        self.contact_name = self.get_attr("contact_name")
        self.contact_email = self.get_attr("contact_email")
        self.contact_phone = self.get_attr("contact_phone")
        self.signup_form = self.get_attr("signup_form")
        self.signup_form_url = self.get_attr("signup_form_url")
        self.event_coordinator_name = self.get_attr("event_coordinator_name")
        self.event_coordinator_email = self.get_attr("event_coordinator_email")
        self.event_coordinator_phone = self.get_attr("event_coordinator_phone")
        self.supervisor_email = self.get_attr("supervisor_email")
        self.date_time_stamp = self.get_attr("date_time_stamp")
        self.rollup = self.get_attr("rollup")

        # More complicated calculations
        self.occurrences = self.get_occurrences(month, year)

    def get_occurrences(self, month, year):
        if self.does_event_repeat():
            occurrences = []
            for date in self.dates:
                if date_util.is_date_in_month_and_year(date, month, year):
                    occurrences.append(date)
            return occurrences
        else:
            day = self.date_begin.split(" ")[1].split(",")[0]
            single_date = f"{month}-{day}-{year}"
            return [single_date]

    def does_event_repeat(self):
        return self.repeat != ""

    def get_attr(self, attribute):
        return soup_util.get_xml_attr(self.xml_event, attribute)
