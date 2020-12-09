import collections
import itertools
from typing import List, Tuple

import utils


class PortData:
    def __init__(self, preamble: List[int]):
        self.combinations = collections.defaultdict(int)
        self.current_data = collections.deque(preamble)

        for first_num, second_num in itertools.combinations(preamble, 2):
            self.combinations[first_num + second_num] += 1

    def valid_entry(self, entry: int) -> bool:
        return entry in self.combinations and self.combinations[entry] > 0

    def add(self, new_entry):
        to_remove = self.current_data.popleft()
        for entry in self.current_data:
            self.combinations[entry + to_remove] -= 1
            self.combinations[entry + new_entry] += 1
        self.current_data.append(new_entry)


def parse_data_entries() -> Tuple[PortData, List[int]]:
    return [
        int(entry) for entry in utils.get_data(9).splitlines()
    ]


def get_invalid_entry(data_entries: List[int]) -> int:
    port_data, entries = PortData(data_entries[:25]), data_entries[25:]
    for entry in entries:
        if not port_data.valid_entry(entry):
            return entry
            break
        port_data.add(entry)


def get_encryption_weakness(data: List[int], invalid_entry: int) -> int:
    sum = 0
    current_set = collections.deque()
    for entry in data:
        current_set.append(entry)
        sum += entry

        while sum > invalid_entry:
            to_remove = current_set.popleft()
            sum -= to_remove

        if sum == invalid_entry:
            return min(current_set) + max(current_set)


if __name__ == "__main__":
    data_entries = parse_data_entries()
    invalid_entry = get_invalid_entry(data_entries)

    assert invalid_entry == 22477624
    assert get_encryption_weakness(data_entries, invalid_entry) == 2980044



