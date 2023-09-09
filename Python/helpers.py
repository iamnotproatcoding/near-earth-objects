import datetime

def cd_to_datetime(calendar_date):
    """ Converting a calender date given in cad.json into datetime object in Python"""
    return datetime.datetime.strptime(calendar_date, "%Y-%b-%d %H:%M")

def datetime_to_str(dt):
    """ Format the time attribute to a string (no seconds)"""
    return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M")