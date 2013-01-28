#!/usr/bin/env python
"""
date system.
"""
import datetime
import calendar
import math

def real_datetime():
    """docstring for real_date"""
    dd = datetime.datetime.now()
    return dd.timetuple()

def insert_zero(value):
    """docstring for insert_zero"""
    return value if value >= 10 else "0%s" % (value)

def number_suffix(number):
    """docstring for num_suffix"""
    n = str(number)
    if n.endswith('1'):
        return "%s%s" % (number, 'st')
    elif n.endswith('2'):
        return "%s%s" % (number, 'nd')
    elif n.endswith('3'):
        return "%s%s" % (number, 'rd')
    else:
        return "%s%s" % (number, 'th')

def time_period(hour):
    """docstring for str_time"""
    if hour >= 7 and hour <= 14:
        return 'morning'
    elif hour >= 15 and hour <= 17:
        return 'noon'
    elif hour >= 18 and hour <= 21:
        return 'afternoon'
    elif hour >= 22 and hour <= 25:
        return 'evening'
    elif hour >= 26 and hour <= 29:
        return 'night'
    elif hour == 30 or hour == 0:
        return 'midnight'
    elif hour >= 1 and hour <= 6:
        return 'late night'
    else:
        pass

def mud_year():
    """docstring for mud_year"""
    start_year = 2013
    rd = real_datetime()
    current_year = rd.tm_year
    #. calculate past yeats
    days = 0
    while start_year < current_year:
        days += 366 if calendar.isleap(start_year) else 365
        start_year += 1
    days += rd.tm_yday
    days += 1 #. 2013/1/1 is tuesday
    return int(math.ceil(float(days)/7))

def mud_datetime():
    """
    1 secoind = 1 minute in game
    1 minute = 1 hour in game
    1 hour = 2 day(30 hour per day) in game
    1 day = 2 month(24 day per month) in game
    1 week = 1 year(14 month) in game
    """
    #. tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday
    rd = real_datetime()
    mud_min = rd.tm_sec
    mud_hour = rd.tm_min if rd.tm_min <= 30 else rd.tm_min - 30
    mud_mday = rd.tm_hour if rd.tm_hour <= 12 else rd.tm_hour - 12
    mud_mon = (rd.tm_wday+1) * 2  if rd.tm_hour > 12 else (rd.tm_wday+1) * 2 - 1
    return (mud_year(), mud_mon, mud_mday, mud_hour, mud_min)

def mud_format_time():
    """docstring for mud_format_time"""
    md = mud_datetime()
    return "%s:%s in the %s" % (
       insert_zero(md[3]), insert_zero(md[4]), time_period(md[3]))

def mud_format_datetime():
    """docstring for mud_datetime"""
    md = mud_datetime()
    return "%s/%s/%s %s:%s" % (
       insert_zero(md[0]), insert_zero(md[1]), insert_zero(md[2]),
       insert_zero(md[3]), insert_zero(md[4]))

def mud_string_datetime():
    """docstring for mud_str_datetime"""
    md = mud_datetime()
    return "%s year of boa age, %s day of %s month, %s:%s" % (
        number_suffix(md[0]), number_suffix(md[1]), number_suffix(md[2]), 
        insert_zero(md[3]), insert_zero(md[4]))

if __name__ == '__main__':
    print mud_format_time()
    print mud_format_datetime()
    print mud_string_datetime()


