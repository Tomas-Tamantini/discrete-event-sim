from typing import Protocol

from .event_calendar import EventCalendar


class Model(Protocol):
    def initial_calendar(self) -> EventCalendar:
        ...
