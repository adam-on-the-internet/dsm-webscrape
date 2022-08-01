import util
from models.CouncilMeetingHeading import CouncilMeetingHeading
from models.CouncilMeetingSummary import CouncilMeetingSummary


def get_council_meetings():
    council_meeting_headings = get_council_meeting_headings()
    headings_to_check = get_headings_to_check(council_meeting_headings)
    summaries = get_summaries_for_headings(headings_to_check)
    for summary in summaries:
        print(f" - {summary.get_message()}")
        # TODO save
    return summaries


def get_summaries_for_headings(headings):
    summaries = []
    for heading in headings:
        summary = get_summary_for_heading(heading)
        summaries.append(summary)
    return summaries


def get_summary_for_heading(heading):
    # TODO get proper page context
    details_url = f"https://www.dsm.city/{heading.details_url}"
    summary = CouncilMeetingSummary(heading.date, heading.title, heading.subtitle, details_url)
    return summary


def get_headings_to_check(council_meeting_headings):
    # TODO actually pick which headings to check
    return [council_meeting_headings[0]]


def get_council_meeting_headings():
    council_meeting_elements = get_council_meeting_heading_elements()
    headings = []
    for council_meeting_element in council_meeting_elements:
        heading = refine_council_meeting_heading(council_meeting_element)
        headings.append(heading)
    return headings


def get_council_meeting_heading_elements():
    council_meetings_url = 'https://www.dsm.city/government/council_meetings_and_agendas/index.php'
    soup = util.convert_url_to_soup(council_meetings_url)
    util.remove_script(soup)
    table_bodies = util.get_elements_of_type(soup, "tbody")
    council_meeting_elements = util.get_elements_of_type(table_bodies[0], "tr")
    return council_meeting_elements


def refine_council_meeting_heading(council_meeting_element):
    title_element = util.get_elements_of_type(council_meeting_element, "th")[0]
    subtitle = ""
    subtitle_result = util.get_elements_of_type(title_element, "small")
    if len(subtitle_result) > 0:
        subtitle_element = subtitle_result[0]
        subtitle = util.get_text_from_element(subtitle_element)
        subtitle_element.extract()
    title_element_text = util.get_text_from_element(title_element)
    date = title_element_text.split(" ", 1)[0].strip()
    title = title_element_text.split(" ", 1)[1].strip()
    link_element = util.get_elements_of_type_with_text(council_meeting_element, "a", "More...")[0]
    link = util.get_link_from_element(link_element)
    heading = CouncilMeetingHeading(date, title, subtitle, link)
    return heading
