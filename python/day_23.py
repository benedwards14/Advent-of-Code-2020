import dataclasses
from typing import List

import utils


@dataclasses.dataclass
class Cup:
    value: int
    next: 'Cup' = None
    prev: 'Cup' = None

    def __iter__(self):
        yield self
        curr_cup = self.next
        while curr_cup is not None:
            if curr_cup == self:
                break
            yield curr_cup
            curr_cup = curr_cup.next


class Cups:
    def __init__(self, cup_values: List[int]):
        self._cups = {}
        self._min = min(cup_values)
        self._max = max(cup_values)
        self._destination_cup = None
        self._pickup = None
        self._current_cup = None

        prev_cup = None
        for cup_value in cup_values:
            new_cup = Cup(cup_value)
            new_cup.prev = prev_cup
            if prev_cup is not None:
                prev_cup.next = new_cup

            if self._current_cup is None:
                self._current_cup = new_cup

            self._cups[cup_value] = new_cup
            prev_cup = new_cup

        prev_cup.next = self._current_cup
        self._current_cup.prev = prev_cup

    def _pick_up(self):
        self._pickup = self._current_cup.next
        self._current_cup.next = None
        self._pickup.prev = None

        new_next = self._pickup.next.next.next
        new_next.prev.next = None
        new_next.prev = self._current_cup
        self._current_cup.next = new_next

    def _find_destination_cup(self):
        dest_value = self._current_cup.value - 1
        pickup_values = {cup.value for cup in self._pickup}
        while True:
            if dest_value < self._min:
                dest_value = self._max

            if dest_value not in pickup_values:
                self._destination_cup = self._cups[dest_value]
                return

            dest_value -= 1

    def _put_down(self):
        self._pickup.next.next.next = self._destination_cup.next
        self._destination_cup.next.prev = self._pickup.next.next

        self._destination_cup.next = self._pickup
        self._pickup.prev = self._destination_cup

        self._destination_cup = None
        self._pickup = None

    def round(self):
        self._pick_up()
        self._find_destination_cup()
        self._put_down()

        self._current_cup = self._current_cup.next

    def __getitem__(self, index: int) -> Cup:
        return self._cups[index]

    def __str__(self) -> str:
        values = []
        for cup in self._cups[1]:
            if cup == self._cups[1]:
                continue
            values.append(str(cup.value))

        return "".join(values)


def play(cups: Cups, rounds: int) -> str:
    for _ in range(rounds):
        cups.round()

    return cups


if __name__ == "__main__":
    cups = Cups([int(value) for value in utils.get_data(23)])
    assert str(play(cups, 100)) == "29385746"

    cups= Cups(
        [int(value) for value in utils.get_data(23)]
        + list(range(10, 1000000 + 1))
    )
    cups = play(cups, 10000000)
    assert cups[1].next.value * cups[1].next.next.value == 680435423892