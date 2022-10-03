from models.Generic.Section import Section


class AgendaItem:
    def __init__(self, number, section, lines, item_type):
        self.number = number
        self.section = section
        self.lines = lines
        self.item_type = item_type

    def to_section(self):
        intro_lines = []
        intro_lines.append(f"- Section: {self.section}")
        intro_lines.append("")

        all_lines = intro_lines + self.lines
        return Section(f"{self.item_type} #{self.number}", all_lines)
