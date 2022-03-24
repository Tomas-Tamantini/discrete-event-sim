from .event import Event


class EventCalendar:
    def __init__(self):
        self.__scheduled_events = []

    def schedule(self, event: Event) -> None:
        self.__scheduled_events.append(event)

    def pop_event(self) -> Event:
        if self.is_empty:
            raise self.UnderflowError('Cannot pop from empty calendar')
        return self.__scheduled_events.pop(0)

    @property
    def is_empty(self) -> bool:
        return len(self.__scheduled_events) == 0

    class UnderflowError(Exception):
        pass
