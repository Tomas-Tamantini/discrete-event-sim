from models import Event


def test_events_can_be_sorted_by_scheduled_time():
    event1 = Event(scheduled_time=15.0)
    event2 = Event(scheduled_time=5.0)
    event3 = Event(scheduled_time=10.0)

    events = [event1, event2, event3]
    events.sort()
    assert events == [event2, event3, event1]


def test_event_runs_callbacks_with_args_and_scheduled_time():
    spy_list = []

    def callback(time, lst, *args):
        lst.append(time)
        lst += list(args)

    callback_args = (spy_list, 'a', 'b', 'c')
    event = Event(scheduled_time=15.0,
                  callback=callback,
                  callback_args=callback_args)

    event.fire()
    assert spy_list == [15.0, 'a', 'b', 'c']
