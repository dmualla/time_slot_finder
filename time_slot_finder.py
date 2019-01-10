# -*- coding: utf-8 -*-
"""
Time Slot Finder.

This script is used to find all slots (30 minutes interval) that are free between 9:00AM to 5:00PM
within the range of the provided input.

Example:
        assuming the input looks like this:
        input = [{"start_time": "04/03/2018T10:30", "end_time": "04/03/2018T17:00"},
                {"start_time": "04/04/2018T10:00", "end_time": "04/04/2018T15:30"}]
        the output is a list of all free 30 minutes time slots between the two dates 04/03/2018 and 04/04/2018
        and it looks like this
        output = [{'start_time': '04/03/2018T09:00', 'end_time': '04/03/2018T09:30'},
            {'start_time': '04/03/2018T09:30', 'end_time': '04/03/2018T10:00'},
            {'start_time': '04/03/2018T10:00', 'end_time': '04/03/2018T10:30'},
            {'start_time': '04/04/2018T09:00', 'end_time': '04/04/2018T09:30'},
            {'start_time': '04/04/2018T09:30', 'end_time': '04/04/2018T10:00'},
            {'start_time': '04/04/2018T15:30', 'end_time': '04/04/2018T16:00'},
            {'start_time': '04/04/2018T16:00', 'end_time': '04/04/2018T16:30'},
            {'start_time': '04/04/2018T16:30', 'end_time': '04/04/2018T17:00'}]

"""
import datetime
from datetime import timedelta


def parse_date(datetime_string):
    """
    Date Parsing Function

    Args:
        datetime_string: a string representation of a date  on format "%m/%d/%YT%H:%M"
    Returns:
        year, month, day, hour and minutes as integers
    """
    (token_start_date, token_start_time) = datetime_string.split("T")
    (month, day, year) = token_start_date.split("/")
    (hour, minute) = token_start_time.split(":")
    return int(year), int(month), int(day), int(hour), int(minute)


def get_reserved_time_list(input_time_list):
    """
    String format date list to date list transformer.

    This function takes a list of dictionaries with string represented date times and transform it into
    a list of pairs with start and end times as datetime objects.

    Args:
        input_time_list: a list of dictionaries with string represented date times of reserved times

    Returns:
        reserved_times_list: a list of pairs with start and end times as datetime objects.
    """
    reserved_times_list = []
    for item in input_time_list:
        (start_year, start_month, start_day, start_hour, start_minutes) = parse_date(item["start_time"])
        (end_year, end_month, end_day, end_hour, end_minutes) = parse_date(item["end_time"])
        start_slot_datetime = datetime.datetime(start_year, start_month, start_day, start_hour, start_minutes)
        end_slot_datetime = datetime.datetime(end_year, end_month, end_day, end_hour, end_minutes)
        reserved_times_list.append((start_slot_datetime, end_slot_datetime))
    return reserved_times_list


def get_start_end_dates(input_time_list):
    """
    Getting the range of dates from input.

    Args:
        input_time_list: a list of dictionaries with string represented date times of reserved times

    Returns:
        start_date, end_date: datetime objects representing the starting time and the ending time respectfully
    """
    (start_year, start_month, start_day, start_hour, start_minute) = parse_date(input_time_list[0]["start_time"])
    (end_year, end_month, end_day, end_hour, end_minute) = parse_date(input_time_list[-1]["end_time"])
    start_date = datetime.datetime(start_year, start_month, start_day, 9, 0)
    end_date = datetime.datetime(end_year, end_month, end_day, 17, 0)
    return start_date, end_date


def find_time_slots(input_time_list):
    """
    Finding the free time slots

    This function will find all the slots that are free without any event reserved

    Args:
        input_time_list: a list of dictionaries with string represented date times of reserved times

    Returns:
        output_list: a list of dictionaries with string represented date times of free time slots
    """
    (start_date, end_date) = get_start_end_dates(input_time_list)
    reserved_times_list = get_reserved_time_list(input_time_list)
    output_list = []
    while start_date < end_date:
        if start_date.hour >= 17:
            start_date = start_date + timedelta(days=1, hours=-8)
        slot_start = start_date
        slot_end = start_date + timedelta(minutes=30)
        available = True
        for time_pair in reserved_times_list:
            if (time_pair[0] < slot_start < time_pair[1]) or (time_pair[0] < slot_end < time_pair[1]):
                available = False
                break
        if available:
            time_slot_dict = {"start_time": slot_start.strftime("%m/%d/%YT%H:%M"),
                              "end_time": slot_end.strftime("%m/%d/%YT%H:%M")}
            output_list.append(time_slot_dict)
        start_date = slot_end
    return output_list
