from typing import Hashable

from models import CycleTimes, Flow, SingleFlowModel, Train, TrainStatus
from models.railroad import cycle_times


# Helper methods
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

# Tests


def test_if_single_train_starts_at_origin_empty_it_starts_loading():
    train = create_train(location='A',
                         status=TrainStatus.WAITING_IN_QUEUE,
                         is_loaded=False)
    flow = create_flow('A', 'B')
    model = SingleFlowModel(flow, [train])

    first_event = model.initial_calendar().pop_event()
    first_event.fire()

    assert first_event.scheduled_time == 0.0
    assert train.location == 'A'
    assert not train.is_loaded
    assert train.status == TrainStatus.LOADING


def test_start_load_triggers_end_load_in_future():
    train = create_train(location='A',
                         status=TrainStatus.WAITING_IN_QUEUE,
                         is_loaded=False)
    cycle_times = create_cycle_times(loading=13)
    flow = create_flow('A', 'B', cycle_times=cycle_times)
    model = SingleFlowModel(flow, [train])

    first_event = model.initial_calendar().pop_event()
    next_event, *_ = first_event.fire()
    next_event.fire()

    assert next_event.scheduled_time == 13.0
    assert train.location == 'A'
    assert train.is_loaded
    assert train.status == TrainStatus.WAITING_IN_QUEUE
