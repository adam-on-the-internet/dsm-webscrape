from models.Agenda.AgendaItem import AgendaItem

SECTION_NAMES = [
    "LICENSES AND PERMITS",
    "PUBLIC IMPROVEMENTS",
    "SPECIAL ASSESSMENTS",
    "LAND/PROPERTY TRANSACTIONS",
    "BOARDS/COMMISSIONS/NEIGHBORHOODS ",
    "COMMUNICATIONS FROM PLANNING AND ZONING",
    "SETTING DATE OF HEARINGS",
    "LEGAL DEPARTMENT - CLAIM SETTLEMENTS & BILLINGS",
    "CITY MANAGER COMMUNICATIONS",
    "APPROVING",
    "APPROVING II",
    "APPROVING III",
    "ORDINANCES FIRST CONSIDERATION",
    "COMMUNICATIONS/REPORTS",
    "INFORMAL HEARINGS",
    "COUNCIL REQUESTS",
]


def parse_items(item_lines):
    items = []

    current_item_number = 0
    current_section = "OPENING"
    current_lines = []
    current_type = "ITEM"

    for index, line in enumerate(item_lines):
        clean_line = line.strip()
        first_piece = clean_line.split(" ")[0]

        # Check if new item has started
        next_item_number = current_item_number + 1
        if first_piece == f"{next_item_number}.":

            if current_item_number > 0:
                # Submit the previous item
                agenda_item = AgendaItem(current_item_number, current_section, current_lines, current_type)
                items.append(agenda_item)

            # Start the next item
            current_item_number = next_item_number
            current_lines = []
            abridged_line = line.replace(f"{first_piece} ", "")
            current_lines.append(abridged_line)
        elif "HEARINGS (OPEN " in clean_line:
            # Switch to Hearing section
            current_section = "HEARINGS"
            current_type = "HEARING ITEM"
        elif clean_line in SECTION_NAMES:
            # Switch to the new section
            current_section = clean_line
            current_type = "ITEM"
        else:
            # Add the line
            current_lines.append(line)

        print("~~")
        print(f"{index} {line}")

    # submit final item
    agenda_item = AgendaItem(current_item_number, current_section, current_lines, current_type)
    items.append(agenda_item)

    return items
