class Event:
    def __init__(self, scheduled_time: float = 0.0) -> None:
        self.__scheduled_time = scheduled_time

    def __lt__(self, other: 'Event') -> bool:
        return self.__scheduled_time < other.__scheduled_time
