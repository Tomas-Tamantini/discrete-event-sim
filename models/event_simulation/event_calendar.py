from .event import Event


class EventCalendar:
    def __init__(self):
        self.__scheduled_events = []

    def schedule(self, event: Event) -> None:
        self.__scheduled_events.append(event)

    @property
    def is_empty(self) -> bool:
        return len(self.__scheduled_events) == 0
