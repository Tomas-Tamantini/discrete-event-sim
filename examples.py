import logging
import os

from models import (CycleTimes, DiscreteEventSimulator, Flow, RailroadModel,
                    Train, TrainStatus)

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


def single_flow_single_train():
    train = Train(train_id=1, location='Terminal 1', is_loaded=False,
                  status=TrainStatus.WAITING_IN_QUEUE)
    cycle_times = CycleTimes(loading=7, trip_loaded=20,
                             unloading=6, trip_empty=17)
    flow = Flow('Terminal 1', 'Terminal 2', 3_500, 1_000, cycle_times)
    model = RailroadModel([flow], [train])
    simulator = DiscreteEventSimulator(model)
    simulator.run(time_horizon=120)


def two_flows_two_trains():
    train_1 = Train(train_id=1, location='Terminal 2', is_loaded=True,
                    status=TrainStatus.WAITING_IN_QUEUE, flow_destination='Terminal 2')
    train_2 = Train(train_id=2, location='Terminal 3', is_loaded=True,
                    status=TrainStatus.WAITING_IN_QUEUE, flow_destination='Terminal 3')
    cycle_times_1_2 = CycleTimes(loading=7, trip_loaded=20,
                                 unloading=6, trip_empty=17)
    cycle_times_1_3 = CycleTimes(loading=7, trip_loaded=20,
                                 unloading=10, trip_empty=17)
    flow_1_2 = Flow('Terminal 1', 'Terminal 2', 14_000, 1_000, cycle_times_1_2)
    flow_1_3 = Flow('Terminal 1', 'Terminal 3', 3_000, 1_000, cycle_times_1_3)
    model = RailroadModel([flow_1_2, flow_1_3], [train_1, train_2])
    simulator = DiscreteEventSimulator(model)
    simulator.run(time_horizon=360)


if __name__ == '__main__':
    two_flows_two_trains()
