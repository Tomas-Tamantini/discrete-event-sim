from typing import Iterator, Protocol

from .event import Event


class Model(Protocol):
    def next_events(self) -> Iterator[Event]:
        ...
