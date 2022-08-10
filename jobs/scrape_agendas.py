from jobs.scrape_council_meetings import get_timely_council_meetings
from util import file_util


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

    # Prepare directories
    file_util.make_directory_if_not_exists('data/agendas/')
    file_util.make_directory_if_not_exists(f'data/agendas/{meeting.get_meeting_code()}')

    # Download original PDF
    pdf_filename = f'data/agendas/{meeting.get_meeting_code()}.pdf'
    file_util.download_file_locally(agenda_url, f'data/agendas/{meeting.get_meeting_code()}/download.pdf')

    # Create local plaintext version of PDF
    plaintext_filename = f'data/agendas/{meeting.get_meeting_code()}/plaintext.txt'
    file_util.convert_pdf_to_plaintext(pdf_filename, plaintext_filename, meeting.get_shortname())

    # TODO can we fix the issue with certain characters showing as � in .txt?
    # TODO save plaintext
    # TODO compare plaintext to existing version to spot differences
    # TODO if updated, get update info. else, skip
    # TODO parse plaintext to useful object
    # TODO make debug markdown version?


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

