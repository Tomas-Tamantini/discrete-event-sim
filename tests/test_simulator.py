from models import DiscreteEventSimulator


class ModelStub:
    pass


def test_simulator_current_time_starts_at_zero():
    simulator = DiscreteEventSimulator(ModelStub())
    assert simulator.current_time == 0
