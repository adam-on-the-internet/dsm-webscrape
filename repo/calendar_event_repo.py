from util import request_util
from models.CalendarEvent.BaseCalendarEvent import BaseCalendarEvent


datasource_url = 'https://aoti-basic-express-app.herokuapp.com/dsmScrape/calendarEvent'


def save_calendar_event(calendar_event):
    json_data = calendar_event.to_json()
    request_util.post_json(datasource_url, json_data)


def get_calendar_events():
    json_data = request_util.get_json(datasource_url)
    return list(map(convert_to_base_calendar_event_messages, json_data))


def convert_to_base_calendar_event_messages(item):
    base_calendar_event = BaseCalendarEvent(item['day'], item['month'], item['year'], item['time'], item['name'])
    return base_calendar_event.get_message()

