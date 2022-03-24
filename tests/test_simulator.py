import pytest
from models import DiscreteEventSimulator, Event, EventCalendar


class EventSpy(Event):
    def __init__(self, scheduled_time: float = 0, children: list["EventSpy"] = None) -> None:
        super().__init__(scheduled_time)
        self.has_been_called = False
        self.__children = children or []

    def fire(self):
        self.has_been_called = True
        return self.__children


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


def test_events_after_time_horizon_are_not_fired():
    event_1 = EventSpy(scheduled_time=10.0)
    event_2 = EventSpy(scheduled_time=4.0)
    simulator = DiscreteEventSimulator(ModelStub([event_1, event_2]))
    simulator.run(time_horizon=5.0)
    assert simulator.current_time == 4.0
    assert not event_1.has_been_called
    assert event_2.has_been_called


def test_event_children_are_fired():
    child_1 = EventSpy(scheduled_time=10.0)
    child_2 = EventSpy(scheduled_time=4.0)
    parent = EventSpy(scheduled_time=1.0, children=[child_1, child_2])
    simulator = DiscreteEventSimulator(ModelStub([parent]))
    simulator.run(time_horizon=8.0)
    assert simulator.current_time == 4.0
    assert not child_1.has_been_called
    assert child_2.has_been_called
    assert parent.has_been_called


def test_cannot_schedule_event_in_the_past():
    child_1 = EventSpy(scheduled_time=10.0)
    child_2 = EventSpy(scheduled_time=4.0)  # Child happening before parent
    parent = EventSpy(scheduled_time=5.0, children=[child_1, child_2])
    simulator = DiscreteEventSimulator(ModelStub([parent]))
    with pytest.raises(ValueError):
        simulator.run()
