class PlaintextAgenda:
    def __init__(self, agenda_code, plaintext):
        self.agenda_code = agenda_code
        self.plaintext = plaintext

    def __eq__(self, other):
        return self.agenda_code == other.agenda_code and self.plaintext == other.plaintext

    def to_json(self):
        return {
            "agenda_code": self.agenda_code,
            "plaintext": self.plaintext
        }
