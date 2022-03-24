import pytest
from models import Event, EventCalendar


def test_calendar_starts_out_empty():
    calendar = EventCalendar()
    assert calendar.is_empty


def test_pop_with_empty_calendar_is_underflow():
    calendar = EventCalendar()
    with pytest.raises(EventCalendar.UnderflowError):
        _ = calendar.pop_event()


def test_after_push_calendar_is_not_empty():
    calendar = EventCalendar()
    event = Event()
    calendar.schedule(event)
    assert not calendar.is_empty


def test_after_push_and_pop_calendar_is_empty():
    calendar = EventCalendar()
    calendar.schedule(Event())
    calendar.pop_event()
    assert calendar.is_empty


def test_pop_returns_highest_priority_event():
    calendar = EventCalendar()
    e1 = Event(time_to_fire=10)
    e2 = Event(time_to_fire=5)
    e3 = Event(time_to_fire=40)
    for e in (e1, e2, e3):
        calendar.schedule(e)
    assert calendar.pop_event() == e2
    assert calendar.pop_event() == e1
    assert calendar.pop_event() == e3
