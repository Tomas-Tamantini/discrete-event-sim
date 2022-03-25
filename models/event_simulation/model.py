from typing import Iterator, Protocol

from .event import Event


class Model(Protocol):
    def next_events(self, current_time: float = 0.0) -> Iterator[Event]:
        ...

    @property
    def state(self) -> str:
        ...
