from models import EventCalendar


def test_calendar_starts_out_empty():
    calendar = EventCalendar()
    assert calendar.is_empty
