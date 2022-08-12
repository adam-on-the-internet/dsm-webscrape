class AgendaVersion:
    def __init__(self, meeting_code, plaintext, status):
        self.meeting_code = meeting_code
        self.plaintext = plaintext
        self.status = status
    #     TODO add more fields

    def should_save(self):
        return self.status == "NEW" or self.status == "UPDATED"
