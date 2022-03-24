class Event:
    def __init__(self, time_to_fire: float = 0.0) -> None:
        self.__time_to_fire = time_to_fire

    def __lt__(self, other: 'Event') -> bool:
        return self.__time_to_fire < other.__time_to_fire
