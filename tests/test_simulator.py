from models import DiscreteEventSimulator, Event, EventCalendar
from models.event_simulation import event


class EventSpy(Event):
    def __init__(self, scheduled_time: float = 0) -> None:
        super().__init__(scheduled_time)
        self.has_been_called = False

    def fire(self) -> None:
        self.has_been_called = True


class ModelStub:
    def __init__(self, events_in_inital_calendar: list[EventSpy] = None) -> None:
        self.__initial_calendar = EventCalendar()
        if events_in_inital_calendar:
            for e in events_in_inital_calendar:
                self.__initial_calendar.schedule(e)

    def initial_calendar(self) -> EventCalendar:
        return self.__initial_calendar


def test_simulator_current_time_starts_at_zero():
    simulator = DiscreteEventSimulator(ModelStub())
    assert simulator.current_time == 0


def test_simulator_fires_initial_events():
    event = EventSpy(scheduled_time=10.0)
    simulator = DiscreteEventSimulator(ModelStub([event]))
    simulator.run()
    assert simulator.current_time == 10.0
    assert event.has_been_called
