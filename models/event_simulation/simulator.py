from .model import Model


class DiscreteEventSimulator:
    def __init__(self, model: Model) -> None:
        self.__model = model
        self.__current_time = 0.0

    @property
    def current_time(self) -> float:
        return self.__current_time
