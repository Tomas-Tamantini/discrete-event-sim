from dataclasses import dataclass


@dataclass(frozen=True)
class CycleTimes:
    loading: float
    trip_loaded: float
    unloading: float
    trip_empty: float
