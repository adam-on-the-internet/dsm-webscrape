from util import request_util
from models.CouncilMeeting.CouncilMeetingSummary import CouncilMeetingSummary


datasource_url = 'https://aoti-basic-express-app.herokuapp.com/dsmScrape/councilMeeting'


def get_council_meeting_urls():
    council_meetings = get_council_meetings_json()
    return list(map(get_url_property, council_meetings))


def get_council_meetings_json():
    return request_util.get_json(datasource_url)


def get_council_meetings():
    json_list = get_council_meetings_json()
    council_meetings = []
    for item in json_list:
        council_meeting = build_council_meeting_from_json(item)
        council_meetings.append(council_meeting)
    return council_meetings


def build_council_meeting_from_json(item):
    day = item['day']
    month = item['month']
    year = item['year']
    time = item['time']
    title = item['title']
    subtitle = item['subtitle']
    links = item['links']
    url = item['url']
    __id = item['_id']
    return CouncilMeetingSummary(day, month, year, time, title, subtitle, url, links, __id)


def save_council_meeting(council_meeting):
    json_data = council_meeting.to_json()
    request_util.post_json(datasource_url, json_data)


def update_council_meeting(council_meeting):
    json_data = council_meeting.to_json()
    update_url = datasource_url + f"/{council_meeting.__id}/update"
    request_util.post_json(update_url, json_data)


def get_url_property(item):
    return item['url']

