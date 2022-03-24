from typing import Iterator, Optional


class Event:
    def __init__(self, scheduled_time: float = 0.0) -> None:
        self.__scheduled_time = scheduled_time

    @property
    def scheduled_time(self) -> float:
        return self.__scheduled_time

    def __lt__(self, other: 'Event') -> bool:
        return self.__scheduled_time < other.__scheduled_time

    def fire(self) -> Optional[Iterator["Event"]]:
        raise NotImplementedError('Subclasses must implement this method')
