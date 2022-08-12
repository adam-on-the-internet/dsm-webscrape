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

    def get_meeting_code(self):
        return f"{self.year}_{self.month}_{self.day}_{self.title.replace(' ', '_')}"

    def get_date_full(self):
        return f"{self.year}-{self.month}-{self.day}"

    def get_status(self):
        if self.meeting_id is None:
            return "FOUND"
        else:
            return "UPDATED"

    def get_shortname(self):
        return f"{self.get_date_full()} {self.title}"

    def get_agenda_directory_name(self):
        return f'data/agendas/{self.get_meeting_code()}/'

    def get_pdf_filename(self):
        return f'{self.get_agenda_directory_name()}download.pdf'

    def get_plaintext_filename(self):
        return f'{self.get_agenda_directory_name()}plaintext.txt'

    def get_markdown_filename(self):
        return f'{self.get_agenda_directory_name()}markdown.md'

    def get_message(self):
        return f"COUNCIL MEETING {self.get_status()}: {self.get_shortname()} ({self.url}) [{len(self.links)} link(s)]"

    def get_agenda_url(self):
        for link in self.links:
            link_pieces = link.split("::")
            link_text = link_pieces[0].strip()
            if "Agenda" == link_text:
                return link_pieces[1].strip()
        return None

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

