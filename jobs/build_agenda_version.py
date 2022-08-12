from models.Agenda.AgendaVersion import AgendaVersion
from repo import agenda_version_repo
from util import file_util


def build_agenda_version(meeting):
    agenda_url = meeting.get_agenda_url()
    prepare_directories(meeting)
    file_util.download_file_locally(agenda_url, meeting.get_pdf_filename())
    current_plaintext = get_meeting_plaintext(meeting)
    status = get_agenda_status(current_plaintext, meeting)
    # parse_agenda(current_plaintext, meeting)  # TODO run parse agenda to get extra values
    return AgendaVersion(meeting.get_meeting_code(), current_plaintext, status)


def parse_agenda(current_plaintext, meeting):
    lines = current_plaintext.split("\n")
    if meeting.is_regular_meeting():
        # TODO break this down to useful info
        intro_lines = get_intro_lines(lines)
        closing_lines = get_closing_lines(lines)
        item_lines = get_item_lines(lines)
        links = get_links(lines)
    # TODO if not regular meeting, we can probably just take it all as "intro lines" or something...


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


def get_intro_lines(lines):
    intro_lines = []
    add_lines = False
    for index, line in enumerate(lines):
        if "1." in line.strip() and "ROLL CALL:" in lines[index + 1]:
            add_lines = False
        if add_lines:
            intro_lines.append(line)
        if "---- DOCUMENT START ----" in line:
            add_lines = True
    return intro_lines


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
    return item_lines


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
    return closing_lines


def get_agenda_status(current_plaintext, meeting):
    most_recent_plaintext = agenda_version_repo.get_most_recent_agenda_version(meeting.get_meeting_code())
    if most_recent_plaintext is None:
        print(f"     * New Plaintext Agenda found for {meeting.get_shortname()}")
        return "NEW"
    elif most_recent_plaintext != current_plaintext:
        print(f"     * Updated Plaintext Agenda found for {meeting.get_shortname()}")
        return "UPDATED"
    else:
        return "UNCHANGED"


def prepare_directories(meeting):
    file_util.make_directory_if_not_exists('data/agendas/')
    file_util.make_directory_if_not_exists(meeting.get_agenda_directory_name())


def get_meeting_plaintext(meeting):
    print(f"     * Converting to plaintext...")
    pdf_filename = meeting.get_pdf_filename()
    plaintext_filename = meeting.get_plaintext_filename()
    title = meeting.get_shortname()
    # TODO can we fix the issue with certain characters showing as � in .txt?
    return file_util.convert_pdf_to_plaintext(pdf_filename, plaintext_filename, title)
