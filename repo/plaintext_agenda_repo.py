from util import request_util

datasource_url = 'https://aoti-basic-express-app.herokuapp.com/dsmScrape/plaintextAgenda'


def save_plaintext_agenda(plaintext_agenda):
    json_data = plaintext_agenda.to_json()
    request_util.post_json(datasource_url, json_data)


# Returns in order, most recent first
def get_plaintext_agendas(code):
    json_data = request_util.get_json(datasource_url + f"/{code}")
    return list(map(convert_to_plaintext, json_data))


def get_most_recent_plaintext(code):
    plaintexts = get_plaintext_agendas(code)
    if len(plaintexts) == 0:
        return None
    else:
        return plaintexts[0]


def convert_to_plaintext(item):
    return item['plaintext']
