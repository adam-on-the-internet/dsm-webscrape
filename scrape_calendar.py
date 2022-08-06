from util import date_util, soup_util
from models.CalendarEvent.CalendarEvent import CalendarEvent
from models.CalendarEvent.RawCalendarEvent import RawCalendarEvent


def get_calendar_events():
    calendar_events = get_timely_calendar_events()

    # TODO filter off existing events
    existing_events = []

    # TODO save any found events
    for calendar_event in calendar_events:
        # calendar_event_repo.save_calendar_event(calendar_event)
        print(f"  + {calendar_event.get_message()}")

    return []  # TODO return actual events


def get_timely_calendar_events():
    # TODO validate this works as expected by comparing against real
    calendar_events = []
    offset = 1
    month_year_stamps = date_util.pick_month_year_stamps(offset)
    for month_year_stamp in month_year_stamps:
        monthly_events = get_monthly_calendar_events(month_year_stamp)
        calendar_events = calendar_events + monthly_events
    return calendar_events


def get_monthly_calendar_events(month_year_stamp):
    monthly_events = []
    stamp_pieces = month_year_stamp.split("-")
    month = stamp_pieces[0]
    year = stamp_pieces[1]

    raw_events = get_events_for_month(month, year)

    for raw_event in raw_events:
        if raw_event.is_repeat():
            for occurrence in raw_event.get_occurrence_dates():
                date_pieces = occurrence.split("-")
                date_month = date_pieces[0]
                date_year = date_pieces[2]
                if date_month == month and date_year == year:
                    day = date_pieces[1]
                    calendar_event = build_calendar_event(day, month, year, raw_event)
                    monthly_events.append(calendar_event)
        else:
            day = raw_event.date_begin.split(" ")[1].split(",")[0]
            calendar_event = build_calendar_event(day, month, year, raw_event)
            monthly_events.append(calendar_event)
    monthly_events.sort(key=lambda x: int(x.day), reverse=False)
    return monthly_events


def build_calendar_event(day, month, year, raw_event):
    name = raw_event.name
    detail = raw_event.detail
    time = raw_event.time_begin
    if len(str(day)) == 1:
        day = f"0{day}"
    calendar_event = CalendarEvent(name, day, month, year, time, detail)
    return calendar_event


def get_events_for_month(month, year):
    xml_events = get_xml_events_for_month(month, year)
    raw_calendar_events = []
    for xml_event in xml_events:
        raw_calendar_event = build_raw_calendar_event(xml_event)
        raw_calendar_events.append(raw_calendar_event)
    return raw_calendar_events


def build_raw_calendar_event(xml_event):
    name = soup_util.get_xml_attribute(xml_event, "name")
    date_begin = soup_util.get_xml_attribute(xml_event, "date_begin")
    time_begin = soup_util.get_xml_attribute(xml_event, "time_begin")
    detail = soup_util.get_xml_attribute(xml_event, "detail")
    repeat = soup_util.get_xml_attribute(xml_event, "repeat")
    raw_calendar_event = RawCalendarEvent(xml_event, name, date_begin, time_begin, detail, repeat)
    return raw_calendar_event


def get_xml_events_for_month(month, year):
    # EX: https://www.dsm.city/calendar_app/db/calendar_1_activemonthsdata_2022-08.xml
    calendar_xml_url = f'https://www.dsm.city/calendar_app/db/calendar_1_activemonthsdata_{year}-{month}.xml'
    xml_file = soup_util.convert_url_to_soup(calendar_xml_url)
    return xml_file.find_all("event")
