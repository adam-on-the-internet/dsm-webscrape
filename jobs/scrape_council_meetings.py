from models.CouncilMeeting.CouncilMeetingHeading import CouncilMeetingHeading
from models.CouncilMeeting.CouncilMeetingSummary import CouncilMeetingSummary
from repo import council_meeting_repo
from util import soup_util, date_util


def get_council_meetings():
    new_council_meetings = find_new_council_meetings()
    save_council_meetings(new_council_meetings)

    updated_council_meetings = find_updated_council_meetings()
    update_council_meetings(updated_council_meetings)

    return new_council_meetings + updated_council_meetings


def save_council_meetings(council_meetings):
    for council_meeting in council_meetings:
        council_meeting_repo.save_council_meeting(council_meeting)
        print(f"  + {council_meeting.get_message()}")


def update_council_meetings(council_meetings):
    for council_meeting in council_meetings:
        council_meeting_repo.update_council_meeting(council_meeting)
        print(f"  + {council_meeting.get_message()}")


def find_new_council_meetings():
    council_meeting_headings = get_council_meeting_headings()
    found_headings = find_new_headings(council_meeting_headings)
    return get_summaries_for_headings(found_headings)


def find_updated_council_meetings():
    updated_meetings = []
    timely_council_meetings = get_timely_council_meetings()
    for existing_meeting in timely_council_meetings:
        current_meeting = build_council_meeting_summary(existing_meeting.url)
        if current_meeting is not None:
            if current_meeting != existing_meeting:
                current_meeting.meeting_id = existing_meeting.meeting_id
                updated_meetings.append(current_meeting)
                print(f"   + Checking {existing_meeting.get_shortname()} : Found Updates")
            else:
                print(f"   + Checking {existing_meeting.get_shortname()} : Found No Updates")
    return updated_meetings


def get_timely_council_meetings():
    # Pull Existing Data
    existing_council_meetings = council_meeting_repo.get_council_meetings()
    # Select Existing Council Meetings in Range (Use Range for Calendar Events with Month Offset -1, 0, 1)
    timely_council_meetings = []
    offset = 1
    month_year_stamps = date_util.pick_month_year_stamps(offset)
    for existing_council_meeting in existing_council_meetings:
        month_year_stamp = f"{existing_council_meeting.month}-{existing_council_meeting.year}"
        if month_year_stamp in month_year_stamps:
            timely_council_meetings.append(existing_council_meeting)
    return timely_council_meetings


def get_summaries_for_headings(council_meeting_headings):
    council_meeting_summaries = []
    for council_meeting_heading in council_meeting_headings:
        council_meeting_summary = build_council_meeting_summary(council_meeting_heading.url)
        if council_meeting_summary is not None:
            council_meeting_summaries.append(council_meeting_summary)
    return council_meeting_summaries


def build_council_meeting_summary(url):
    page = soup_util.convert_url_to_soup(url)
    breadcrumbs_element = get_breadcrumbs_element(page)
    if breadcrumbs_element is None:
        return None
    subtitle = get_subtitle_for_summary(breadcrumbs_element)
    full_title = soup_util.get_text_from_element(breadcrumbs_element)
    full_title_pieces = full_title.split("@")
    title = full_title_pieces[0].strip()
    time = get_time(full_title_pieces)
    agenda_detail_list = soup_util.get_elements_of_type_with_class(page, "div", "agendadetail")
    if len(agenda_detail_list) == 0:
        return None
    agenda_detail = agenda_detail_list[0]
    links = get_links(agenda_detail)
    date_pieces = get_date_pieces(agenda_detail)
    day = date_pieces[1]
    month = date_pieces[0]
    year = f"20{date_pieces[2]}"
    return CouncilMeetingSummary(day, month, year, time, title, subtitle, url, links, None)


def get_time(full_title_pieces):
    if len(full_title_pieces) > 1:
        return full_title_pieces[1].strip()
    else:
        return ""


def get_date_pieces(agenda_detail):
    date = soup_util.get_first_text_of_type_with_class(agenda_detail, "div", "agenda_date").replace("Date:", "").strip()
    date_piece = date.split(" ")[-1].replace("(", "").replace(")", "")
    date_pieces = date_piece.split("/")
    return date_pieces


def get_breadcrumbs_element(page):
    elements = soup_util.get_elements_of_type_with_id(page, "div", "breadcrumbs")
    if len(elements) > 0:
        breadcrumbs_element = elements[0]
        soup_util.remove_tags(breadcrumbs_element, "a")
        return breadcrumbs_element
    else:
        return None


def get_subtitle_for_summary(breadcrumbs_element):
    subtitle_result = soup_util.get_elements_of_type(breadcrumbs_element, "small")
    if len(subtitle_result) > 0:
        subtitle_element = subtitle_result[0]
        subtitle = soup_util.get_text_from_element(subtitle_element)
        subtitle_element.extract()
        return subtitle
    else:
        return ""


def get_links(agenda_detail):
    link_elements = soup_util.get_elements_of_type(agenda_detail, "a")
    links = []
    for link_element in link_elements:
        link_text = soup_util.get_text_from_element(link_element)
        link_href = soup_util.get_link_from_element(link_element)
        if "http" not in link_href:
            link_href = "https://www.dsm.city/" + link_href
        link_href = link_href.replace(" ", "%20")
        link = f"{link_text} :: {link_href}"
        links.append(link)
    return links


def find_new_headings(council_meeting_headings):
    found_council_meeting_headings = []
    existing_urls = council_meeting_repo.get_council_meeting_urls()

    for heading in council_meeting_headings:
        if heading.url not in existing_urls:
            found_council_meeting_headings.append(heading)

    return found_council_meeting_headings


def get_council_meeting_headings():
    council_meeting_elements = get_council_meeting_heading_elements()
    headings = []
    for council_meeting_element in council_meeting_elements:
        heading = build_council_meeting_heading(council_meeting_element)
        headings.append(heading)
    return headings


def get_council_meeting_heading_elements():
    council_meetings_url = 'https://www.dsm.city/government/council_meetings_and_agendas/index.php'
    soup = soup_util.convert_url_to_soup(council_meetings_url)
    soup_util.remove_script(soup)
    table_bodies = soup_util.get_elements_of_type(soup, "tbody")
    council_meeting_elements = soup_util.get_elements_of_type(table_bodies[0], "tr")
    return council_meeting_elements


def build_council_meeting_heading(council_meeting_element):
    title_element = soup_util.get_elements_of_type(council_meeting_element, "th")[0]
    subtitle = get_subtitle_for_heading(title_element)
    title_element_text = soup_util.get_text_from_element(title_element)
    date = title_element_text.split(" ", 1)[0].strip()
    title = title_element_text.split(" ", 1)[1].strip()
    url = get_url_for_heading(council_meeting_element)
    return CouncilMeetingHeading(date, title, subtitle, url)


def get_url_for_heading(council_meeting_element):
    link_element = soup_util.get_elements_of_type_with_text(council_meeting_element, "a", "More...")[0]
    partial_url = soup_util.get_link_from_element(link_element)
    return f"https://www.dsm.city/{partial_url}"


def get_subtitle_for_heading(title_element):
    subtitle_result = soup_util.get_elements_of_type(title_element, "small")
    if len(subtitle_result) > 0:
        subtitle_element = subtitle_result[0]
        subtitle = soup_util.get_text_from_element(subtitle_element)
        subtitle_element.extract()
        return subtitle
    else:
        return ""
