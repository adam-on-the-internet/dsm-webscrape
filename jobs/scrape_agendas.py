from jobs.scrape_council_meetings import get_timely_council_meetings
from util import file_util, date_util
from models.Agenda.PlaintextAgenda import PlaintextAgenda
from repo import plaintext_agenda_repo


def get_agendas():
    check_meetings_for_agendas()
    # TODO save new vs updates?
    return []  # TODO really scrape agendas


def check_meetings_for_agendas():
    meetings_to_check = get_meetings_to_check()
    for meeting in meetings_to_check:
        agenda_url = find_agenda_url_for_regular_meeting(meeting)
        scan_agenda_url(agenda_url, meeting)


def scan_agenda_url(agenda_url, meeting):
    print(f"   + Scanning agenda {meeting.get_shortname()}: {agenda_url}")
    prepare_directories(meeting)

    # Download original PDF
    file_util.download_file_locally(agenda_url, meeting.get_pdf_filename())

    # Create local plaintext version of PDF
    # TODO can we fix the issue with certain characters showing as � in .txt?
    plaintext = file_util.convert_pdf_to_plaintext(meeting.get_pdf_filename(), meeting.get_plaintext_filename(), meeting.get_shortname())

    # get plaintexts for meeting (sorted most recent first)
    plaintexts = plaintext_agenda_repo.get_plaintext_agendas(meeting.get_meeting_code())

    if len(plaintexts) == 0:
        print(f"     * New Plaintext Agenda found for {meeting.get_shortname()}")
        save_plaintext(meeting, plaintext)
    elif plaintexts[0] != plaintext:
        print(f"     * Updated Plaintext Agenda found for {meeting.get_shortname()}")
        save_plaintext(meeting, plaintext)
    else:
        print(f"     * Unchanged Plaintext Agenda found for {meeting.get_shortname()}")


def prepare_directories(meeting):
    file_util.make_directory_if_not_exists('data/agendas/')
    file_util.make_directory_if_not_exists(meeting.get_agenda_directory_name())


def save_plaintext(meeting, plaintext):
    plaintext_agenda = PlaintextAgenda(meeting.get_meeting_code(), plaintext)
    plaintext_agenda_repo.save_plaintext_agenda(plaintext_agenda)

    # TODO parse plaintext to useful object

    # TODO make debug markdown version?
    write_markdown_file(meeting)


def get_meetings_to_check():
    timely_council_meetings = get_timely_council_meetings()
    meetings_to_check = []
    for meeting in timely_council_meetings:
        # TODO can we support other meeting types?
        if "Regular Meeting" in meeting.title:
            agenda_url = find_agenda_url_for_regular_meeting(meeting)
            if agenda_url is None:
                print(f"   + Agenda not found for {meeting.get_shortname()}")
            else:
                meetings_to_check.append(meeting)
        else:
            print(f"   + Agenda not needed for {meeting.get_shortname()} (type not supported)")
    return meetings_to_check


def find_agenda_url_for_regular_meeting(meeting):
    agenda_url = None
    for link in meeting.links:
        link_pieces = link.split("::")
        link_text = link_pieces[0].strip()
        if "Agenda" == link_text:
            agenda_url = link_pieces[1].strip()
    return agenda_url


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

