from jobs.write_agenda_markdown import write_agenda_markdown
from models.Agenda.AgendaVersion import AgendaVersion
from repo import plaintext_agenda_repo
from util import file_util


def build_agenda_version(meeting):
    agenda_url = meeting.get_agenda_url()
    prepare_directories(meeting)
    file_util.download_file_locally(agenda_url, meeting.get_pdf_filename())
    current_plaintext = get_meeting_plaintext(meeting)
    status = get_agenda_status(current_plaintext, meeting)
    agenda_version = AgendaVersion(meeting, current_plaintext, status)
    parse_plaintext_if_necessary(agenda_version)
    return agenda_version


def parse_plaintext_if_necessary(agenda_version):
    if agenda_version.meeting.title == "Regular Meeting":
        # TODO parse plaintext to useful object
        print(f"     * Parsing to markdown...")
        write_agenda_markdown(agenda_version)


def get_agenda_status(current_plaintext, meeting):
    most_recent_plaintext = plaintext_agenda_repo.get_most_recent_plaintext(meeting.get_meeting_code())
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
