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
