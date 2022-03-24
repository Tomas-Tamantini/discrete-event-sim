from dataclasses import dataclass

from models import Event, EventCalendar


def test_calendar_starts_out_empty():
    calendar = EventCalendar()
    assert calendar.is_empty


def test_after_push_calendar_is_not_empty():
    calendar = EventCalendar()
    event = Event()
    calendar.schedule(event)
    assert not calendar.is_empty
