from models.Generic.Section import Section
from util import plaintext_util


def parse_plaintext(plaintext, meeting):
    lines = plaintext_util.get_lines_from_plaintext(plaintext)

    sections = []

    if meeting.is_regular_meeting():

        intro_section = get_intro_section_for_regular(lines)
        sections.append(intro_section)

        items_section = get_items_section(lines)
        sections.append(items_section)

        closing_section = get_closing_section(lines)
        sections.append(closing_section)

    else:

        intro_section = get_intro_section_for_irregular(lines)
        sections.append(intro_section)

    link_section = get_links_section(lines)
    sections.append(link_section)

    return sections


def get_intro_section_for_irregular(lines):
    intro_lines = get_intro_lines_for_irregular_meeting(lines)
    return Section("Intro", intro_lines)


def get_intro_section_for_regular(lines):
    intro_lines = get_intro_lines_for_regular_meeting(lines)
    return Section("Intro", intro_lines)


def get_links_section(lines):
    links = get_links(lines)
    return Section("Links", links)


def get_closing_section(lines):
    lines = get_closing_lines(lines)
    return Section("Closing", lines)


def get_items_section(lines):
    lines = get_item_lines(lines)
    return Section("Items", lines)


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


def get_intro_lines_for_irregular_meeting(lines):
    clean_intro_lines = []
    add_lines = False
    for index, line in enumerate(lines):
        if "---- DOCUMENT END ----" in line:
            add_lines = False
        if add_lines:
            clean_intro_lines.append(line)
        if "---- DOCUMENT START ----" in line:
            add_lines = True
    return plaintext_util.remove_blank_lines_from_start_and_end(clean_intro_lines)


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


def get_item_lines(lines):
    item_lines = []
    # TODO initial "marks" here?
    add_lines = False
    for index, line in enumerate(lines):
        if "1." in line.strip() and "ROLL CALL:" in lines[index + 1]:
            add_lines = True
        if "MOTION TO ADJOURN" in line:
            add_lines = False
        if add_lines:
            item_lines.append(line)
    return plaintext_util.remove_blank_lines_from_start_and_end(item_lines)
