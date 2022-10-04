from models.Agenda.AgendaItem import AgendaItem
from util.plaintext_util import remove_blank_lines_from_end

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
    next_section = "OPENING"
    current_lines = []
    current_type = "ITEM"
    next_is_hearing_start = False
    next_is_consent_start = False
    next_is_hearings_end = False
    next_is_consent_end = False

    for index, line in enumerate(item_lines):
        clean_line = line.strip()
        first_piece = clean_line.split(" ")[0]

        if "APPROVING CONSENT AGENDA" in clean_line:
            next_is_consent_start = True

        # Check if new item has started
        next_item_number = current_item_number + 1
        if first_piece == f"{next_item_number}.":

            if current_item_number > 0:
                # Submit the previous item
                current_lines = remove_blank_lines_from_end(current_lines)
                agenda_item = AgendaItem(current_item_number, current_section, current_lines, current_type)
                items.append(agenda_item)

            # Start the next item

            current_section = next_section

            if next_is_hearing_start:
                next_section = "HEARINGS"
                current_type = "HEARING ITEM"
                next_is_hearing_start = False
                next_is_consent_end = False
            elif next_is_consent_start:
                current_type = "CONSENT ITEM"
                next_is_consent_start = False
            elif next_is_consent_end:
                current_type = "ITEM"
                next_is_consent_end = False
            elif next_is_hearings_end:
                current_type = "ITEM"
                next_is_hearings_end = False

            current_item_number = next_item_number
            current_lines = []
            abridged_line = line.replace(f"{first_piece} ", "")
            current_lines.append(abridged_line)
        elif "END CONSENT AGENDA" in clean_line:
            # Close out consent agenda
            next_is_consent_end = True
        elif "END HEARINGS AT" in clean_line or "END HEARTINGS AT" in clean_line:
            # Close out consent agenda
            next_is_hearings_end = True
        elif "HEARINGS (OPEN " in clean_line:
            # Switch to Hearing section
            next_is_hearing_start = True
        elif clean_line in SECTION_NAMES:
            # Record the new section
            next_section = clean_line
        else:
            # Add the line
            current_lines.append(line)

        print("~~")
        print(f"{index} {line}")

    # submit final item
    agenda_item = AgendaItem(current_item_number, current_section, current_lines, current_type)
    items.append(agenda_item)

    return items
