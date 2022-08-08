from util import request_util


datasource_url = 'https://aoti-basic-express-app.herokuapp.com/dsmScrape/councilMeeting'


def get_council_meeting_urls():
    council_meetings = get_council_meetings()
    return list(map(get_url_property, council_meetings))


def get_council_meetings():
    return request_util.get_json(datasource_url)


def save_council_meeting(council_meeting):
    json_data = council_meeting.to_json()
    request_util.post_json(datasource_url, json_data)


def update_council_meeting(council_meeting):
    json_data = council_meeting.to_json()
    update_url = datasource_url + f"/{council_meeting.id}/update"
    request_util.post_json(update_url, json_data)


def get_url_property(item):
    return item['url']

