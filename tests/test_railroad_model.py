from typing import Hashable

import pytest
from models import CycleTimes, Flow, RailroadModel, Train, TrainStatus


def create_train(train_id: Hashable = 'T1',
                 location: Hashable = 'A',
                 is_loaded: bool = False,
                 status: TrainStatus = TrainStatus.WAITING_IN_QUEUE) -> Train:
    return Train(train_id, location, is_loaded, status)


def create_cycle_times(loading: float = 7,
                       trip_loaded: float = 20,
                       unloading: float = 6,
                       trip_empty: float = 17) -> CycleTimes:
    return CycleTimes(loading, trip_loaded, unloading, trip_empty)


def create_flow(origin: Hashable = 'A',
                destination: Hashable = 'B',
                demand: float = 100_000,
                train_capacity: float = 5_000,
                cycle_times: CycleTimes = None) -> Flow:
    if not cycle_times:
        cycle_times = create_cycle_times()
    return Flow(origin, destination, demand, train_capacity, cycle_times)


def test_all_flows_must_share_same_origin():
    f1 = create_flow(origin='A')
    f2 = create_flow(origin='B')
    with pytest.raises(ValueError):
        RailroadModel(flows=[f1, f2], trains=[])
