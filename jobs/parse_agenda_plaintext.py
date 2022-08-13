from models.Agenda.ParsedAgendaPieces import ParsedAgendaPieces
from util import plaintext_util


def parse_agenda_plaintext(current_plaintext, meeting):
    lines = plaintext_util.get_lines_from_plaintext(current_plaintext)

    if meeting.is_regular_meeting():
        links = get_links(lines)
        intro_text = get_intro_text_for_regular_meeting(lines)
        closing_text = get_closing_text(lines)
        item_text = get_item_text(lines)

        # TODO parse items somehow
        # print_lines(item_lines, "item")
        return ParsedAgendaPieces(intro_text, item_text, closing_text, links)

    else:
        # For non-regular meetings, we can just capture links and the text as "intro"
        links = get_links(lines)
        intro_text = get_intro_text_for_non_regular_meeting(lines)
        item_text = ""
        closing_text = ""
        return ParsedAgendaPieces(intro_text, item_text, closing_text, links)


def get_links(lines):
    links = []
    add_lines = False
    for line in lines:
        if "---- LINKS END ----" in line.strip():
            add_lines = False
        if add_lines and line.strip() != "":
            links.append(line.strip())
        if "---- LINKS START ----" in line:
            add_lines = True
    return links


def get_intro_text_for_regular_meeting(lines):
    intro_lines = []
    add_lines = False
    for index, line in enumerate(lines):
        if "1." in line.strip() and "ROLL CALL:" in lines[index + 1]:
            add_lines = False
        if add_lines:
            intro_lines.append(line)
        if "---- DOCUMENT START ----" in line:
            add_lines = True
    clean_intro_lines = plaintext_util.remove_blank_lines_from_start_and_end(intro_lines)
    return convert_lines_to_text(clean_intro_lines)


def get_intro_text_for_non_regular_meeting(lines):
    clean_intro_lines = []
    add_lines = False
    for index, line in enumerate(lines):
        if "---- DOCUMENT END ----" in line:
            add_lines = False
        if add_lines:
            clean_intro_lines.append(line)
        if "---- DOCUMENT START ----" in line:
            add_lines = True
    clean_intro_lines = plaintext_util.remove_blank_lines_from_start_and_end(clean_intro_lines)
    return convert_lines_to_text(clean_intro_lines)


def convert_lines_to_text(lines):
    text = ""
    for index, line in enumerate(lines):
        if index > 0:
            text = text + "\n"
        text = text + line
    return text


def get_item_text(lines):
    item_lines = []
    add_lines = False
    for index, line in enumerate(lines):
        if "1." in line.strip() and "ROLL CALL:" in lines[index + 1]:
            add_lines = True
        if "MOTION TO ADJOURN" in line:
            add_lines = False
        if add_lines:
            item_lines.append(line)
    clean_item_lines = plaintext_util.remove_blank_lines_from_start_and_end(item_lines)
    return convert_lines_to_text(clean_item_lines)


def get_closing_text(lines):
    closing_lines = []
    add_lines = False
    for index, line in enumerate(lines):
        if "---- DOCUMENT END ----" in line:
            add_lines = False
        if "MOTION TO ADJOURN" in line:
            add_lines = True
        if add_lines:
            closing_lines.append(line)
    clean_closing_lines = plaintext_util.remove_blank_lines_from_start_and_end(closing_lines)
    return convert_lines_to_text(clean_closing_lines)


# TODO remove this, its just for debugging
def print_lines(lines, section):
    print(f" ~~~ start {section} ~~~ ")
    for line in lines:
        print(line)
    print(f" ~~~ end {section} ~~~ ")
