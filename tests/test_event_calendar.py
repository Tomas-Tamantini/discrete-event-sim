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


def test_can_peek_time_of_next_scheduled_event():
    calendar = EventCalendar()
    assert calendar.time_of_next_event is None
    calendar.schedule(Event(scheduled_time=10))
    assert calendar.time_of_next_event == 10
    calendar.schedule(Event(scheduled_time=5))
    assert calendar.time_of_next_event == 5
    calendar.schedule(Event(scheduled_time=40))
    assert calendar.time_of_next_event == 5


def test_pop_returns_highest_priority_event():
    calendar = EventCalendar()
    e1 = Event(scheduled_time=10)
    e2 = Event(scheduled_time=5)
    e3 = Event(scheduled_time=40)
    for e in (e1, e2, e3):
        calendar.schedule(e)
    assert calendar.pop_event() == e2
    assert calendar.pop_event() == e1
    assert calendar.pop_event() == e3
