import logging
import re

from django.utils import timezone, formats
from django.core.cache import cache

from ics import Calendar
import requests

logger = logging.getLogger(__name__)


def get_current_events(calendar: Calendar, limit: int = 5) -> list:
    """
    Get upcoming events from calendar
    :param calendar: The calendar object
    :param limit: Count of events
    :return: List of upcoming events
    """
    i: int = 0
    events: list = []
    for event in calendar.timeline.start_after(timezone.now()):
        # Check for limit
        if i >= limit:
            break
        i += 1

        # Create formatted dates and times for begin and end
        begin_date_formatted = formats.date_format(event.begin)
        end_date_formatted = formats.date_format(event.end)
        begin_time_formatted = formats.time_format(event.begin.time())
        end_time_formatted = formats.time_format(event.end.time())

        if event.begin.date() == event.end.date():
            # Event is only on one day
            formatted = begin_date_formatted

            if not event.all_day:
                # No all day event
                formatted += " " + begin_time_formatted

            if event.begin.time != event.end.time():
                # Event has an end time
                formatted += " – " + end_time_formatted

        else:
            # Event is on multiple days
            if event.all_day:
                # Event is all day
                formatted = "{} – {}".format(begin_date_formatted, end_date_formatted)
            else:
                # Event has begin and end times
                formatted = "{} {} – {} {}".format(begin_date_formatted, begin_time_formatted, end_date_formatted,
                                                   end_time_formatted)

        events.append({
            "name": event.name,
            "begin_timestamp": event.begin.timestamp,
            "end_timestamp": event.end.timestamp,
            "date_formatted": formatted,
        })

    return events


def get_current_events_with_cal(calendar_url: str, limit: int = 5) -> list:
    if not calendar_url:
        return []

    # Check if current events are cached
    current_events = cache.get("current_events")
    if current_events:
        # Return the if so
        return current_events

    # Get ICS
    try:
        calendar: Calendar = Calendar(requests.get(calendar_url, timeout=3).text)
    except requests.RequestException as e:
        logger.error(str(e))
        return []

    # Get events
    current_events = get_current_events(calendar, limit)
    cache.set("current_events", current_events, 60 * 5)
    return current_events
