class AgendaVersion:
    def __init__(self, meeting_code, plaintext, status):
        self.meeting_code = meeting_code
        self.plaintext = plaintext
        self.status = status
    #     TODO add more fields

    def __eq__(self, other):
        return self.meeting_code == other.meeting_code and self.plaintext == other.plaintext

    def should_save(self):
        return self.status == "NEW" or self.status == "UPDATED"

    def to_json(self):
        return {
            "meeting_code": self.meeting_code,
            "plaintext": self.plaintext
        }
