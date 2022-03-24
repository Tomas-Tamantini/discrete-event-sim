from typing import Optional

from .model import Model


class DiscreteEventSimulator:
    def __init__(self, model: Model) -> None:
        self.__model = model
        self.__calendar = model.initial_calendar()
        self.__current_time = 0.0

    @property
    def current_time(self) -> float:
        return self.__current_time

    def run(self, time_horizon: float = float('inf')) -> None:
        while not self.__calendar.is_empty and self.__calendar.time_of_next_event <= time_horizon:
            next_event = self.__calendar.pop_event()
            self.__current_time = next_event.scheduled_time
            other_events = next_event.fire()
            if not other_events:
                continue
            for e in other_events:
                if e.scheduled_time < self.current_time:
                    raise ValueError('Cannot schedule events in the past')
                self.__calendar.schedule(e)
