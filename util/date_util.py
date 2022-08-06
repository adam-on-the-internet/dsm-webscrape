import datetime


def pick_month_year_stamps(offset_count):
    relative_start = offset_count * -1
    relative_end = offset_count + 1
    offsets = list(range(relative_start, relative_end))
    now = datetime.datetime.now()
    month_year_stamps = []
    for offset in offsets:
        month_year_stamp = pick_month_and_year(now, offset)
        month_year_stamps.append(month_year_stamp)
    return month_year_stamps


def pick_month_and_year(base_datetime, offset):
    base_year = base_datetime.year
    base_month = base_datetime.month
    return adjust_date(base_month + offset, base_year)


def adjust_date(month, year):
    if month == 0:
        month = 12
        year = year - 1
    elif month == 13:
        month = 1
        year = year + 1

    if len(str(month)) == 1:
        month = f"0{month}"

    return f'{month}-{year}'
