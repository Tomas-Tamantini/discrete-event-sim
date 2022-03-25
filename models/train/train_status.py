from enum import Enum


class TrainStatus(str, Enum):
    WAITING_IN_QUEUE = 'WAITING_IN_QUEUE'
    LOADING = 'LOADING'
    UNLOADING = 'UNLOADING'
    EN_ROUTE = 'EN_ROUTE'
