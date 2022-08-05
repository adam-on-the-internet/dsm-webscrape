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
    # return summaries #TODO return real value
    return []


def get_summaries_for_headings(headings):
    summaries = []
    for heading in headings:
        summary = get_summary_for_heading(heading)
        summaries.append(summary)
    return summaries


def get_summary_for_heading(heading):
    page_url = f"https://www.dsm.city/{heading.url}"
    soup = util.convert_url_to_soup(page_url)

    breadcrumbs_element = util.get_elements_of_type_with_id(soup, "div", "breadcrumbs")[0]
    util.remove_tags(breadcrumbs_element, "a")

    subtitle = ""
    subtitle_result = util.get_elements_of_type(breadcrumbs_element, "small")
    if len(subtitle_result) > 0:
        subtitle_element = subtitle_result[0]
        subtitle = util.get_text_from_element(subtitle_element)
        subtitle_element.extract()

    title = util.get_text_from_element(breadcrumbs_element)

    agenda_detail = util.get_elements_of_type_with_class(soup, "div", "agendadetail")[0]

    date = util.get_first_text_of_type_with_class(agenda_detail, "div", "agenda_date").replace("Date:", "").strip()

    link_elements = util.get_elements_of_type(agenda_detail, "a")
    links = []
    for link_element in link_elements:
        link_text = util.get_text_from_element(link_element)
        link_href = util.get_link_from_element(link_element)
        if "http" not in link_href:
            link_href = "https://www.dsm.city/" + link_href
        link_href = link_href.replace(" ", "%20")
        link = f"{link_text} :: {link_href}"
        links.append(link)

    summary = CouncilMeetingSummary(date, title, subtitle, heading.url, page_url, links)
    return summary


def get_headings_to_check(council_meeting_headings):
    headings_to_check = []
    existing_urls = get_existing_council_meeting_urls()

    for heading in council_meeting_headings:
        # Get New meetings
        if heading.url not in existing_urls:
            headings_to_check.append(heading)
        # Get Recent Existing meetings
        elif heading_is_recent(heading):
            headings_to_check.append(heading)

    # TODO remove hardcoding
    headings_to_check = [council_meeting_headings[0], council_meeting_headings[1], council_meeting_headings[2]]

    return headings_to_check


def heading_is_recent(heading):
    # TODO use heading date to check recency (TRUE for meetings with month offset -1/0/+1)
    return False


def get_existing_council_meeting_urls():
    # TODO use REAL existing data
    url = 'https://aoti-basic-express-app.herokuapp.com/dsmScrape/councilMeetingSummaries'
    # existing_news_posts = util.get_json(url)
    # return list(map(get_url, existing_news_posts))
    return []


def get_url(summary):
    return summary['heading_url']


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
