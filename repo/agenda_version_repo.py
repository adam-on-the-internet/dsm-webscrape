from util import request_util

datasource_url = 'https://aoti-basic-express-app.herokuapp.com/dsmScrape/agendaVersion'


def save_agenda_version(agenda_version):
    json_data = agenda_version.to_json()
    request_util.post_json(datasource_url, json_data)


# Returns in order, most recent first
def get_agenda_versions(code):
    json_data = request_util.get_json(datasource_url + f"/{code}")
    return list(map(convert_to_plaintext, json_data))


def get_most_recent_agenda_version(code):
    agenda_versions = get_agenda_versions(code)
    if len(agenda_versions) == 0:
        return None
    else:
        return agenda_versions[0]


def convert_to_plaintext(item):
    return item['plaintext']
