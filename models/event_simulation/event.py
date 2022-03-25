from typing import Callable, Iterator, Optional


class Event:
    def __init__(self, scheduled_time: float = 0.0,
                 callback: Optional[Callable] = None,
                 callback_args: Optional[tuple] = None) -> None:
        self.__scheduled_time = scheduled_time
        self.__callback = callback
        self.__callback_args = callback_args if callback_args else ()

    @property
    def scheduled_time(self) -> float:
        return self.__scheduled_time

    def __lt__(self, other: 'Event') -> bool:
        return self.__scheduled_time < other.__scheduled_time

    def fire(self) -> Optional[Iterator["Event"]]:
        if self.__callback:
            return self.__callback(self.__scheduled_time, *self.__callback_args)
