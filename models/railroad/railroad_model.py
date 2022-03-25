from models.train import Train

from .flow import Flow


class RailroadModel:
    def __init__(self, flows: list[Flow], trains: list[Train]):
        origins = set([f.origin for f in flows])
        if len(origins) != 1:
            raise ValueError('All flows must share the same origin')
        self.__flows = flows
        self.__trains = trains
