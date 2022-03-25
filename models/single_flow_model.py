from typing import Hashable, Optional

from models.train.train_status import TrainStatus

from .event_simulation import Event, EventCalendar
from .railroad import Flow
from .train import Train


class SingleFlowModel:
    def __init__(self, flow: Flow, trains: list[Train]) -> None:
        self.__flow = flow
        self.__trains = trains

    @property
    def __origin(self) -> Hashable:
        return self.__flow.origin

    def __terminal_is_free(self, terminal: Hashable) -> bool:
        bad_status = (TrainStatus.LOADING, TrainStatus.UNLOADING)
        for t in self.__trains:
            if t.location == terminal and t.status in bad_status:
                return False
        return True

    def __next_train_to_load(self) -> Optional[Train]:
        if self.__terminal_is_free(self.__origin):
            for t in self.__trains:
                if t.status == TrainStatus.WAITING_IN_QUEUE and\
                    t.location == self.__origin and \
                        not t.is_loaded:
                    return t

    def __start_loading(self, current_time: float, train: Train) -> None:
        train.status = TrainStatus.LOADING
        # Trigger end load event in future
        next_time = current_time + self.__flow.cycle_times.loading
        next_event = Event(scheduled_time=next_time,
                           callback=self.__end_loading,
                           callback_args=(train,))
        return (next_event,)

    def __end_loading(self, current_time: float, train: Train) -> None:
        train.is_loaded = True
        train.status = TrainStatus.WAITING_IN_QUEUE
        # Create start loaded trip event in future

    def initial_calendar(self) -> EventCalendar:
        ec = EventCalendar()
        t = self.__next_train_to_load()
        if t:
            event = Event(callback=self.__start_loading, callback_args=(t,))
            ec.schedule(event)
        return ec
