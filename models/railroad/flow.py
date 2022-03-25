from dataclasses import dataclass
from typing import Hashable

from .cycle_times import CycleTimes


@dataclass(frozen=True)
class Flow:
    origin: Hashable
    destination: Hashable
    demand: float
    train_capacity: float
    cycle_times: CycleTimes
