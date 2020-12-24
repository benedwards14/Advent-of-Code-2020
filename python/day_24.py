import dataclasses
import re
from typing import ClassVar, Dict, Generator, List, Set, Tuple

import utils


@dataclasses.dataclass
class Vector:
    east: int = 0
    northeast: int = 0

    DIRECTIONS: ClassVar[Dict[str, Tuple[int, int]]] = {
        "e": (1, 0),
        "ne": (0, 1),
        "nw": (-1, 1),
        "w": (-1, 0),
        "sw": (0, -1),
        "se": (1, -1),
    }

    @property
    def neighbours(self) -> Generator['Vector', None, None]:
        for direction in self.DIRECTIONS.keys():
            yield self.move(direction)

    def move(self, direction: str):
        move_e, move_ne = self.DIRECTIONS[direction]
        return Vector(self.east + move_e, self.northeast + move_ne)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def __str__(self) -> str:
        return f"E:{self.east},NE:{self.northeast}"


def parse_tile(tile_str: str) -> Vector:
    tile = Vector()
    pattern = re.compile(f"({'|'.join(list(Vector.DIRECTIONS.keys()))})")
    for direction in pattern.findall(tile_str):
        tile = tile.move(direction)

    return tile


def parse_tiles() -> List[Vector]:
    return [
        parse_tile(tile_str) for tile_str in utils.get_data(24).splitlines()
    ]


def get_black_tiles(tiles: List[Vector]) -> Set[Vector]:
    black_tiles = set()
    for tile in tiles:
        if tile in black_tiles:
            black_tiles.remove(tile)
        else:
            black_tiles.add(tile)

    return black_tiles


def daily_flip(black_tiles: Set[Vector]) -> Set[Vector]:
    white_tiles = {
        tile
        for black_tile in black_tiles
        for tile in black_tile.neighbours
        if tile not in black_tiles
    }
    new_black_tiles = set()

    for tile in black_tiles:
        black_neighbours = sum(
            neighbour in black_tiles for neighbour in tile.neighbours
        )
        if black_neighbours in [1, 2]:
            new_black_tiles.add(tile)

    for tile in white_tiles:
        black_neighbours = sum(
            neighbour in black_tiles for neighbour in tile.neighbours
        )
        if black_neighbours == 2:
            new_black_tiles.add(tile)

    return new_black_tiles


def flip(black_tiles: Set[Vector], days: int) -> Set[Vector]:
    for _  in range(days):
        black_tiles = daily_flip(black_tiles)

    return black_tiles


if __name__ == "__main__":
    tiles = parse_tiles()

    black_tiles = get_black_tiles(tiles)
    assert len(black_tiles) == 277

    print(len(flip(black_tiles, 100)))


