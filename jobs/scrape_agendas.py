from jobs.scrape_council_meetings import get_timely_council_meetings
from models.Agenda.PlaintextAgenda import PlaintextAgenda
from models.Agenda.AgendaVersion import AgendaVersion
from repo import plaintext_agenda_repo
from util import file_util, date_util


def get_agendas():
    agendas = check_meetings_for_agendas()
    return []  # TODO once check-able, return agendas


def check_meetings_for_agendas():
    agendas = []
    meetings_to_check = get_meetings_to_check()
    for meeting in meetings_to_check:
        agenda = scan_agenda_url(meeting)
        if agenda is not None:
            agendas.append(agenda)
    return agendas


def scan_agenda_url(meeting):
    agenda_url = meeting.get_agenda_url()
    print(f"   + Scanning agenda {meeting.get_shortname()}: {agenda_url}")
    prepare_directories(meeting)
    file_util.download_file_locally(agenda_url, meeting.get_pdf_filename())
    current_plaintext = get_meeting_plaintext(meeting)
    status = get_agenda_status(current_plaintext, meeting)
    agenda_version = AgendaVersion(meeting.get_meeting_code(), current_plaintext, status)
    parse_plaintext_if_necessary(meeting)
    return save_if_necessary(agenda_version, current_plaintext, meeting)


def save_if_necessary(agenda_version, current_plaintext, meeting):
    if agenda_version.should_save():
        save_plaintext(meeting, current_plaintext)
        print(f"     * Saving Agenda Version... (Changes Found)")
        # TODO save agenda version instead of plaintext...
        return agenda_version
    else:
        return None


def get_meeting_plaintext(meeting):
    print(f"     * Converting to plaintext...")
    pdf_filename = meeting.get_pdf_filename()
    plaintext_filename = meeting.get_plaintext_filename()
    title = meeting.get_shortname()
    # TODO can we fix the issue with certain characters showing as � in .txt?
    return file_util.convert_pdf_to_plaintext(pdf_filename, plaintext_filename, title)


def parse_plaintext_if_necessary(meeting):
    if meeting.title == "Regular Meeting":
        # TODO parse plaintext to useful object
        print(f"     * Parsing to markdown...")
        write_markdown_file(meeting)


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


def save_plaintext(meeting, plaintext):
    plaintext_agenda = PlaintextAgenda(meeting.get_meeting_code(), plaintext)
    plaintext_agenda_repo.save_plaintext_agenda(plaintext_agenda)


def get_meetings_to_check():
    timely_council_meetings = get_timely_council_meetings()
    meetings_to_check = []
    for meeting in timely_council_meetings:
        agenda_url = meeting.get_agenda_url()
        if agenda_url is None:
            print(f"   + Agenda not found for {meeting.get_shortname()}")
        else:
            meetings_to_check.append(meeting)
    return meetings_to_check


def write_markdown_file(meeting):
    file = open(meeting.get_markdown_filename(), "w")

    # meeting info title & heading
    title = meeting.get_shortname() + " Council Agenda"
    file.write(f"# {title} \n\n")

    # agenda content
    # TODO write agenda content

    # metadata
    file.write(f"## Metadata \n\n")
    created_date = date_util.get_current_date()
    file.write(f"- file created at {created_date} \n\n")

    file.close()
