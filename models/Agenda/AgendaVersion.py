class AgendaVersion:
    def __init__(self, meeting_code, plaintext, status, intro_text, item_text, closing_text, links):
        self.meeting_code = meeting_code
        self.plaintext = plaintext
        self.status = status
        self.intro_text = intro_text
        self.item_text = item_text
        self.closing_text = closing_text
        self.links = links

    def __eq__(self, other):
        return self.meeting_code == other.meeting_code and self.plaintext == other.plaintext

    def should_save(self):
        return self.status == "NEW" or self.status == "UPDATED"

    def to_json(self):
        return {
            "meeting_code": self.meeting_code,
            "plaintext": self.plaintext,
            "intro_text": self.intro_text,
            "item_text": self.item_text,
            "closing_text": self.closing_text,
            "links": self.links
        }
