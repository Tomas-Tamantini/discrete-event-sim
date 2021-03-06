import logging
from typing import Hashable, Iterator, Optional

from models.event_simulation import Event
from models.train import Train, TrainStatus

from .flow import Flow


class RailroadModel:
    def __init__(self, flows: list[Flow], trains: list[Train]):
        origins = set([f.origin for f in flows])
        if len(origins) != 1:
            raise ValueError('All flows must share the same origin')
        for t in trains:
            if t.status != TrainStatus.WAITING_IN_QUEUE:
                raise ValueError(
                    'All trains must be waiting in queue initially')
        self.__flows = flows
        self.__trains = trains
        self.__operated_volumes = {
            f: {'loaded': 0, 'unloaded': 0} for f in flows}

    @property
    def __origin(self) -> Hashable:
        return self.__flows[0].origin

    def __terminal_is_free(self, terminal: Hashable) -> bool:
        occupied_status = (TrainStatus.LOADING, TrainStatus.UNLOADING)
        for t in self.__trains:
            if t.location == terminal and t.status in occupied_status:
                return False
        return True

    def __can_load(self, train) -> bool:
        if not self.__terminal_is_free(self.__origin):
            return False
        if train.location != self.__origin:
            return False
        if train.status != TrainStatus.WAITING_IN_QUEUE:
            return False
        return not train.is_loaded

    def __can_unload(self, train) -> bool:
        terminal = train.flow_destination
        if not self.__terminal_is_free(terminal):
            return False
        if train.location != terminal:
            return False
        if train.status != TrainStatus.WAITING_IN_QUEUE:
            return False
        return train.is_loaded

    def __can_start_loaded_trip(self, train) -> bool:
        if train.location != self.__origin:
            return False
        if train.status != TrainStatus.WAITING_IN_QUEUE:
            return False
        return train.is_loaded

    def __can_start_unloaded_trip(self, train) -> bool:
        terminal = train.flow_destination
        if train.location != terminal:
            return False
        if train.status != TrainStatus.WAITING_IN_QUEUE:
            return False
        return not train.is_loaded

    def __next_train_to_load(self) -> Optional[Train]:
        for t in self.__trains:
            if self.__can_load(t):
                return t

    def __assign_flow(self, train: Train) -> None:
        flow_to_choose = self.__flows[0]
        max_remaining_demand = -float('inf')
        for f, vol in self.__operated_volumes.items():
            remaining_demand = (f.demand - vol['unloaded']) / (1 + f.demand)
            if remaining_demand > max_remaining_demand:
                max_remaining_demand = remaining_demand
                flow_to_choose = f
        train.flow_destination = flow_to_choose.destination

    def __get_flow(self, train: Train) -> Flow:
        if train.flow_destination is None:
            self.__assign_flow(train)
        for f in self.__flows:
            if f.destination == train.flow_destination:
                return f

    def __start_loading(self, current_time: float, train: Train) -> list[Event]:
        if not self.__can_load(train):
            return
        train.status = TrainStatus.LOADING
        self.__assign_flow(train)
        next_time = current_time + self.__get_flow(train).cycle_times.loading
        next_event = Event(scheduled_time=next_time,
                           callback=self.__end_loading,
                           callback_args=(train,))
        self.__log_event(
            current_time, description=f'Loading train {train.train_id}')
        return [next_event]

    def __end_loading(self, current_time: float, train: Train) -> None:
        if train.location != self.__origin or train.status != TrainStatus.LOADING:
            return
        train.is_loaded = True
        train.status = TrainStatus.WAITING_IN_QUEUE
        flow = self.__get_flow(train)
        self.__operated_volumes[flow]['loaded'] += flow.train_capacity
        self.__log_event(
            current_time, description=f'Train {train.train_id} finshed loading')

    def __start_loaded_trip(self, current_time: float, train: Train) -> list[Event]:
        if not self.__can_start_loaded_trip(train):
            return
        train.status = TrainStatus.EN_ROUTE
        next_time = current_time + \
            self.__get_flow(train).cycle_times.trip_loaded
        next_event = Event(scheduled_time=next_time,
                           callback=self.__end_loaded_trip,
                           callback_args=(train,))
        self.__log_event(
            current_time, description=f'Train {train.train_id} started loaded trip')
        return [next_event]

    def __end_loaded_trip(self, current_time: float, train: Train) -> None:
        if train.location != self.__origin or train.status != TrainStatus.EN_ROUTE:
            return
        train.location = train.flow_destination
        train.status = TrainStatus.WAITING_IN_QUEUE
        self.__log_event(
            current_time, description=f'Train {train.train_id} finished loaded trip')

    def __start_unloading(self, current_time: float, train: Train) -> list[Event]:
        if not self.__can_unload(train):
            return
        train.status = TrainStatus.UNLOADING
        next_time = current_time + self.__get_flow(train).cycle_times.unloading
        next_event = Event(scheduled_time=next_time,
                           callback=self.__end_unloading,
                           callback_args=(train,))
        self.__log_event(
            current_time, description=f'Train {train.train_id} started unloading')
        return [next_event]

    def __end_unloading(self, current_time: float, train: Train) -> None:
        if train.location != train.flow_destination or train.status != TrainStatus.UNLOADING:
            return
        train.is_loaded = False
        train.status = TrainStatus.WAITING_IN_QUEUE
        flow = self.__get_flow(train)
        self.__operated_volumes[flow]['unloaded'] += flow.train_capacity
        self.__log_event(
            current_time, description=f'Train {train.train_id} finished unloading')

    def __start_unloaded_trip(self, current_time: float, train: Train) -> list[Event]:
        if not self.__can_start_unloaded_trip(train):
            return
        train.status = TrainStatus.EN_ROUTE
        next_time = current_time + \
            self.__get_flow(train).cycle_times.trip_empty
        next_event = Event(scheduled_time=next_time,
                           callback=self.__end_unloaded_trip,
                           callback_args=(train,))
        self.__log_event(
            current_time, description=f'Train {train.train_id} started empty trip')
        return [next_event]

    def __end_unloaded_trip(self, current_time: float, train: Train) -> None:
        if train.location != train.flow_destination or train.status != TrainStatus.EN_ROUTE:
            return
        train.location = self.__origin
        train.status = TrainStatus.WAITING_IN_QUEUE
        self.__log_event(
            current_time, description=f'Train {train.train_id} finished empty trip')

    def next_events(self, current_time: float = 0.0) -> Iterator[Event]:
        train_to_load = self.__next_train_to_load()
        if train_to_load:
            event = Event(callback=self.__start_loading,
                          callback_args=(train_to_load,),
                          scheduled_time=current_time)
            yield event
        for t in self.__trains:
            if self.__can_start_loaded_trip(t):
                event = Event(callback=self.__start_loaded_trip,
                              callback_args=(t,),
                              scheduled_time=current_time)
                yield event
            elif self.__can_unload(t):
                event = Event(callback=self.__start_unloading,
                              callback_args=(t,),
                              scheduled_time=current_time)
                yield event
            elif self.__can_start_unloaded_trip(t):
                event = Event(callback=self.__start_unloaded_trip,
                              callback_args=(t,),
                              scheduled_time=current_time)
                yield event

    @property
    def state(self) -> str:
        def op_vol_to_str(flow, vol):
            return str(flow) + f': <{vol["loaded"]}/{vol["unloaded"]}>'
        return '- ' + '\ -'.join(map(str, self.__trains)) + f' - Operated volume: ' + '|'.join([op_vol_to_str(f, v) for (f, v) in self.__operated_volumes.items()])

    def __log_event(self, current_time: float, description: str) -> None:
        logging.info(f'({current_time}h) Event: {description}')
        logging.info(f'({current_time}h) State: {self.state}')
