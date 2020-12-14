import numpy
from typing import List, Optional, Tuple

import utils


def parse_data() -> Tuple[int, List[Optional[int]]]:
    timestamp, bus_ids = utils.get_data(13).splitlines()
    return int(timestamp), [
        int(bus_id) if bus_id != "x" else None for bus_id in bus_ids.split(',')
    ]


def get_wait_time(timestamp: int, bus_id: int) -> int:
    return -timestamp % bus_id


def get_next_bus(timestamp: int, bus_ids: List[Optional[int]]) -> int:
    wait_times = {
        get_wait_time(timestamp, bus_id): bus_id
        for bus_id in bus_ids
        if bus_id is not None
    }
    shortest_time = min(wait_times.keys())
    return wait_times[shortest_time], shortest_time


def combine(buses: List[Tuple[int, int]]) -> Tuple[int, int]:
    *buses_to_combine, (bus_time_period, wait_time) = buses

    if not buses_to_combine:
        return 0, bus_time_period

    curr_time, time_period = combine(buses_to_combine)
    while True:
        if get_wait_time(curr_time, bus_time_period) == wait_time:
            return curr_time, numpy.lcm(time_period, bus_time_period)
        curr_time += time_period


def get_competition_time(bus_ids: List[Optional[int]]) -> int:
    buses = [
        (time_period, wait_time % time_period)
        for wait_time, time_period in enumerate(bus_ids)
        if time_period is not None
    ]
    return combine(buses)[0]


if __name__ == "__main__":
    timestamp, bus_ids = parse_data()

    next_bus, wait_time = get_next_bus(timestamp, bus_ids)
    assert next_bus * wait_time == 410
    assert get_competition_time(bus_ids) == 600691418730595