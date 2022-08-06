from util import date_util, soup_util
from repo import calendar_event_repo
from models.CalendarEvent.CalendarEvent import CalendarEvent
from models.CalendarEvent.RawCalendarEvent import RawCalendarEvent


def get_calendar_events():
    calendar_events = find_calendar_events()
    save_calendar_events(calendar_events)
    return calendar_events


def find_calendar_events():
    found_calendar_events = []
    calendar_events = get_timely_calendar_events()
    existing_event_messages = calendar_event_repo.get_calendar_events()
    for calendar_event in calendar_events:
        if calendar_event.get_message() not in existing_event_messages:
            found_calendar_events.append(calendar_event)
    return found_calendar_events


def save_calendar_events(calendar_events):
    for calendar_event in calendar_events:
        calendar_event_repo.save_calendar_event(calendar_event)
        print(f"  + {calendar_event.get_message()}")


def get_timely_calendar_events():
    raw_events = get_timely_raw_events()
    calendar_events = build_calendar_events(raw_events)
    date_util.sort_items_by_date(calendar_events)
    return calendar_events


def build_calendar_events(raw_events):
    calendar_events = []
    for raw_event in raw_events:
        for occurrence in raw_event.occurrences:
            date_pieces = occurrence.split("-")
            month = date_pieces[0]
            day = date_pieces[1]
            year = date_pieces[2]
            calendar_event = build_calendar_event(day, month, year, raw_event)
            calendar_events.append(calendar_event)
    return calendar_events


def build_calendar_event(day, month, year, raw_event):
    name = raw_event.name
    detail = raw_event.detail
    time = raw_event.time_begin
    if len(str(day)) == 1:
        day = f"0{day}"
    calendar_event = CalendarEvent(raw_event, day, month, year)
    return calendar_event


def get_timely_raw_events():
    raw_events = []
    offset = 1
    month_year_stamps = date_util.pick_month_year_stamps(offset)
    for month_year_stamp in month_year_stamps:
        monthly_raw_events = get_monthly_raw_events(month_year_stamp)
        raw_events = raw_events + monthly_raw_events
    return raw_events


def get_monthly_raw_events(month_year_stamp):
    stamp_pieces = month_year_stamp.split("-")
    month = stamp_pieces[0]
    year = stamp_pieces[1]
    return get_raw_calendar_events_for_month(month, year)


def get_raw_calendar_events_for_month(month, year):
    xml_events = get_xml_events_for_month(month, year)
    raw_calendar_events = []
    for xml_event in xml_events:
        raw_calendar_event = RawCalendarEvent(xml_event, month, year)
        raw_calendar_events.append(raw_calendar_event)
    return raw_calendar_events


def get_xml_events_for_month(month, year):
    # EX: https://www.dsm.city/calendar_app/db/calendar_1_activemonthsdata_2022-08.xml
    calendar_xml_url = f'https://www.dsm.city/calendar_app/db/calendar_1_activemonthsdata_{year}-{month}.xml'
    xml_file = soup_util.convert_url_to_soup(calendar_xml_url)
    return xml_file.find_all("event")
