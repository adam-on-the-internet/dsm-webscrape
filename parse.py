from repo import council_meeting_repo
from repo import agenda_version_repo
from jobs.plaintext_parser import parse_plaintext
from util import file_util


def find_meeting(shortname):
    council_meetings = council_meeting_repo.get_council_meetings()
    for council_meeting in council_meetings:
        if council_meeting.get_shortname().strip() == shortname.strip():
            return council_meeting
    return None


def find_agenda(code):
    return agenda_version_repo.get_most_recent_agenda_version(code)


# TODO this format is not great...


# TODO Don't have meeting hardcoded. Maybe just get most recent unless a param is given.
selected_shortname = "2022-08-22 Regular Meeting"
print(f"# Looking for meeting: {selected_shortname}")
selected_council_meeting = find_meeting(selected_shortname)

if selected_council_meeting is None:
    print(f" - Could not find meeting, try again later")
else:
    print(f" - Found meeting")
    selected_code = selected_council_meeting.get_meeting_code()
    print(f"# Looking for most recent agenda: {selected_code}")
    selected_agenda_version = find_agenda(selected_code)
    if selected_agenda_version is None:
        print(f" - Could not find agenda, try again later")
    else:
        print(f" - Found agenda")
        print("# Downloading plaintext...")
        directory = f'data/parse/{selected_code}'
        file_util.make_directory_if_not_exists(directory)
        file_util.write_plaintext_doc(directory + '/original.txt', selected_agenda_version)
        print("# Splitting into sections...")
        sections = parse_plaintext(selected_agenda_version, selected_council_meeting)
        filename = directory + '/parsed.md'
        file_util.write_file_by_sections(filename, selected_shortname, sections)
#         TODO From here, we want to manually mark the "items" since those are not easy to auto-control
#         It may be preferable to have an initial pass at the item marking that we can fix as needed
#         After marking, we should be able to run another job that reads the parsed.txt and saves it to db
#         Instead of running another job, can we just wait? Or simply have a re-parsed -> save?

#         TODO remove original "parse" partial logic...

#         TODO put links where they belong
#         TODO prevent weird symbols?

