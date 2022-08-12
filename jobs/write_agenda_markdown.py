from util import date_util


def write_agenda_markdown(agenda_version):
    meeting = agenda_version.meeting
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
