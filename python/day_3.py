import enum
import numpy
from typing import Generator, List, Tuple

import utils


class Point(enum.Enum):
    CLEAR = "."
    TREE = "#"
    OFF_MAP = ""


Path = Generator[Point, None, Point]


class Map:
    def __init__(self, rows: List[str]):
        self._template = [
            [Point(col) for col in row]
            for row in rows 
        ]

    def __getitem__(self, x_y: Tuple[int, int]) -> Point:
        x, y = x_y
        try:
            row = self._template[y]
            return row [x % len(row)]
        except IndexError:
            return Point.OFF_MAP


def walk(map: Map, step_along: int, step_down:int) -> Path:
    x, y = 0, 0
    while map[x, y] is not Point.OFF_MAP:
        yield map[x, y]
        x += step_along
        y += step_down

    return Point.OFF_MAP


def count_trees(path: Path) -> int:
    return sum(point is Point.TREE for point in path)


if __name__ == "__main__":
    map = Map(utils.get_data(3).splitlines())

    paths = [
        count_trees(walk(map, 1, 1)),
        count_trees(walk(map, 3, 1)),
        count_trees(walk(map, 5, 1)),
        count_trees(walk(map, 7, 1)),
        count_trees(walk(map, 1, 2)),
    ]

    assert count_trees(walk(map, 3, 1)) == 176
    assert numpy.prod(paths) == 5872458240