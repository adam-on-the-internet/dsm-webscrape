from util import plaintext_util


def parse_agenda_plaintext(current_plaintext, meeting):
    lines = plaintext_util.get_lines_from_plaintext(current_plaintext)

    if meeting.is_regular_meeting():
        intro_lines = get_intro_lines_for_regular_meeting(lines)
        closing_lines = get_closing_lines(lines)
        links = get_links(lines)

        item_lines = get_item_lines(lines)
        # TODO parse items somehow
        # print_lines(item_lines, "item")
    else:
        # For non-regular meetings, we can just capture links and the text as "intro"
        intro_lines = get_intro_lines_for_non_regular_meeting(lines)
        links = get_links(lines)

    # TODO use details to add to Agenda Version


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


def get_intro_lines_for_regular_meeting(lines):
    intro_lines = []
    add_lines = False
    for index, line in enumerate(lines):
        if "1." in line.strip() and "ROLL CALL:" in lines[index + 1]:
            add_lines = False
        if add_lines:
            intro_lines.append(line)
        if "---- DOCUMENT START ----" in line:
            add_lines = True
    return plaintext_util.remove_blank_lines_from_start_and_end(intro_lines)


def get_intro_lines_for_non_regular_meeting(lines):
    intro_lines = []
    add_lines = False
    for index, line in enumerate(lines):
        if "---- DOCUMENT END ----" in line:
            add_lines = False
        if add_lines:
            intro_lines.append(line)
        if "---- DOCUMENT START ----" in line:
            add_lines = True
    return plaintext_util.remove_blank_lines_from_start_and_end(intro_lines)


def get_item_lines(lines):
    item_lines = []
    add_lines = False
    for index, line in enumerate(lines):
        if "1." in line.strip() and "ROLL CALL:" in lines[index + 1]:
            add_lines = True
        if "MOTION TO ADJOURN" in line:
            add_lines = False
        if add_lines:
            item_lines.append(line)
    return plaintext_util.remove_blank_lines_from_start_and_end(item_lines)


def get_closing_lines(lines):
    closing_lines = []
    add_lines = False
    for index, line in enumerate(lines):
        if "---- DOCUMENT END ----" in line:
            add_lines = False
        if "MOTION TO ADJOURN" in line:
            add_lines = True
        if add_lines:
            closing_lines.append(line)
    return plaintext_util.remove_blank_lines_from_start_and_end(closing_lines)


# TODO remove this, its just for debugging
def print_lines(lines, section):
    print(f" ~~~ start {section} ~~~ ")
    for line in lines:
        print(line)
    print(f" ~~~ end {section} ~~~ ")
