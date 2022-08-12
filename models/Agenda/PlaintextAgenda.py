class PlaintextAgenda:
    def __init__(self, meeting_code, plaintext):
        self.meeting_code = meeting_code
        self.plaintext = plaintext

    def __eq__(self, other):
        return self.meeting_code == other.meeting_code and self.plaintext == other.plaintext

    def to_json(self):
        return {
            "meeting_code": self.meeting_code,
            "plaintext": self.plaintext
        }
