from jobs.parse_agenda_plaintext import parse_agenda_plaintext
from models.Agenda.AgendaVersion import AgendaVersion
from repo import agenda_version_repo
from util import file_util


def build_agenda_version(meeting):
    agenda_url = meeting.get_agenda_url()
    prepare_directories(meeting)
    file_util.download_file_locally(agenda_url, meeting.get_pdf_filename())
    current_plaintext = get_meeting_plaintext(meeting)
    status = get_agenda_status(current_plaintext, meeting)
    parsed_agenda_pieces = parse_agenda_plaintext(current_plaintext, meeting)
    return merge_agenda_pieces(current_plaintext, meeting, parsed_agenda_pieces, status)


def merge_agenda_pieces(current_plaintext, meeting, parsed_agenda_pieces, status):
    meeting_code = meeting.get_meeting_code()
    links = parsed_agenda_pieces.links
    intro_text = parsed_agenda_pieces.intro_text
    item_text = parsed_agenda_pieces.item_text
    closing_text = parsed_agenda_pieces.closing_text
    return AgendaVersion(meeting_code, current_plaintext, status, intro_text, item_text, closing_text, links)


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
