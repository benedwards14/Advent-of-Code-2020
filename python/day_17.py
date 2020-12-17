import copy
import dataclasses
import itertools
from typing import Generator, List

import utils


DIMENSIONS = 3


@dataclasses.dataclass(frozen=True)
class Point:
    coords: tuple

    @classmethod
    def create(cls, *args) -> 'Point':
        assert len(args) <= DIMENSIONS
        coords = args
        if len(coords) < DIMENSIONS:
            extra_coords = [0] * (DIMENSIONS-len(args))
            coords = (*coords, *extra_coords)

        return cls(coords)

    def get_neighbours(self) -> Generator[int, None, None]:
        for deltas in itertools.product([-1, 0, 1], repeat=DIMENSIONS):
            if all(map(lambda x: x == 0, deltas)):
                continue
            yield Point(
                tuple(
                    [
                        coord + delta
                        for coord, delta in zip(self.coords, deltas)
                    ]
                )
            )


class PocketD:
    def __init__(self, start: List[List[str]]):
        self._active = {
            Point.create(x, y)
            for y, row in enumerate(start)
            for x, point in enumerate(row)
            if point == "#"
        }

    @property
    def active_cubes(self) -> int:
        return len(self._active)

    def step(self):
        new_active = set()
        active_to_evaluate = copy.copy(self._active)
        inactive_to_evaluate = set()

        for point in active_to_evaluate:
            active = 0
            for neighbour in point.get_neighbours():
                if neighbour in self._active:
                    active += 1
                else:
                    inactive_to_evaluate.add(neighbour)
            if active in [2,3]:
                new_active.add(point)

        for point in inactive_to_evaluate:
            active = 0
            for neighbour in point.get_neighbours():
                if neighbour in self._active:
                    active += 1
            if active == 3:
                new_active.add(point)

        self._active = new_active


def run(time: int):
    energy_source = PocketD(
        [
            [point for point in row]
            for row in utils.get_data(17).splitlines()
        ]
    )

    for _ in range(time):
        energy_source.step()

    return energy_source.active_cubes


if __name__ == "__main__":
    DIMENSIONS = 3
    assert run(6) == 333

    DIMENSIONS = 4
    assert run(6) == 2676