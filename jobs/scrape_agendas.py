from jobs.build_agenda_version import build_agenda_version
from jobs.scrape_council_meetings import get_timely_council_meetings
from repo import agenda_version_repo


def get_agendas():
    return check_meetings_for_agendas()


def check_meetings_for_agendas():
    agendas = []
    meetings_to_check = get_meetings_to_check()
    for meeting in meetings_to_check:
        agenda = scan_agenda_url(meeting)
        if agenda is not None:
            agendas.append(agenda)
    return agendas


def scan_agenda_url(meeting):
    print(f"   + Scanning agenda {meeting.get_shortname()}: {meeting.get_agenda_url()}")
    agenda_version = build_agenda_version(meeting)
    return save_if_necessary(agenda_version)


def save_if_necessary(agenda_version):
    if agenda_version.should_save():
        agenda_version_repo.save_agenda_version(agenda_version)
        print(f"     * Saving Agenda Version... (Changes Found)")
        # TODO save agenda version instead of plaintext...
        return agenda_version
    else:
        return None


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
