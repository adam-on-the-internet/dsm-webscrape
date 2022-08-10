from jobs.scrape_council_meetings import get_timely_council_meetings


def get_agendas():
    timely_council_meetings = get_timely_council_meetings()
    for meeting in timely_council_meetings:
        if "Regular Meeting" in meeting.title:
            agenda_url = None
            for link in meeting.links:
                if "https://councildocs.dsm.city/agendas/" in link:
                    agenda_url = link.split("::")[1].strip()
            if agenda_url is None:
                print(f"   + Agenda not found for {meeting.get_shortname()}")
            else:
                print(f"   + Agenda found for {meeting.get_shortname()}: {agenda_url}")
        else:
            print(f"   + Agenda not needed for {meeting.get_shortname()} (type not supported)")
    return []  # TODO really scrape agendas

