class AgendaVersion:
    def __init__(self, meeting, plaintext, status):
        self.meeting = meeting
        self.plaintext = plaintext
        self.status = status
    #     TODO add more fields

    def should_save(self):
        return self.status == "NEW" or self.status == "UPDATED"
