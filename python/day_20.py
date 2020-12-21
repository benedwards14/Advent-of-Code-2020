from collections import defaultdict, deque
import dataclasses
import numpy
import re
from typing import Dict, List, Set

import utils


@dataclasses.dataclass
class Edge:
    actual: str

    def _symetrical_string(self) -> str:
        return "".join(sorted([self.actual, self.actual[::-1]]))

    def __hash__(self):
        return hash(self._symetrical_string())

    def __eq__(self, other) -> bool:
        return self._symetrical_string() == other._symetrical_string()


@dataclasses.dataclass
class Image:
    tile_id: int
    _pixels: List[str]
    fixed = False

    @property
    def pixels(self) -> List[str]:
        return [row[1:-1] for row in self._pixels[1:-1]]

    @property
    def actual_pixels(self) -> List[str]:
        return self._pixels

    @property
    def edges(self) -> Set[Edge]:
        return {self.top, self.bottom, self.right, self.left}

    @property
    def top(self) -> Edge:
        return Edge(self._pixels[0])

    @property
    def bottom(self) -> Edge:
        return Edge(self._pixels[-1])

    @property
    def left(self) -> Edge:
        return Edge("".join([row[0] for row in self._pixels]))

    @property
    def right(self) -> Edge:
        return Edge("".join([row[-1] for row in self._pixels]))

    def rotate(self):
        new_pixels = []
        for i in range(len(self._pixels)):
            new_pixels.append([row[-i-1] for row in self._pixels])
        self._pixels = ["".join(row) for row in new_pixels]

    def flip_x(self):
        self._pixels = [
            row[::-1] for row in self._pixels
        ]

    def flip_y(self):
        self._pixels = self._pixels[::-1]


@dataclasses.dataclass
class Tiles:
    edge_to_tile: Dict[Edge, Image]
    id_to_tile: Dict[int, Image]

    def is_image_edge(self, edge: Edge) -> bool:
        return len(self.edge_to_tile[edge]) == 1

    def is_corner(self, tile: Image) -> bool:
        return sum(
            self.is_image_edge(edge) for edge in tile.edges
        ) == 2

    def get_next_right(self, tile: Image) -> Image:
        return [
            t
            for t in self.edge_to_tile[tile.right]
            if t.tile_id != tile.tile_id
        ][0]

    def get_next_below(self, tile: Image) -> Image:
        return [
            t
            for t in self.edge_to_tile[tile.bottom]
            if t.tile_id != tile.tile_id
        ][0]

    def __iter__(self):
        for tile in self.id_to_tile.values():
            yield tile


def parse_image(input_str: List[str]) -> Image:
    tile_id_str, *tile_str = input_str.splitlines()
    tile_id = int(re.match(r"Tile ([0-9]*):", tile_id_str).group(1))

    return Image(tile_id, tile_str)


def parse_tiles() -> Tiles:
    tile_strs = utils.get_data(20).split("\n\n")

    tiles = [parse_image(tile_str) for tile_str in tile_strs]

    id_to_tile = {
        tile.tile_id: tile for tile in tiles
    }
    edge_to_tile = defaultdict(list)

    for tile in tiles:
        for edge in tile.edges:
            assert edge not in edge_to_tile or len(edge_to_tile[edge]) < 2
            edge_to_tile[edge].append(tile)

    return Tiles(edge_to_tile, id_to_tile)


def get_corner(tiles: Tiles) -> Image:
    for tile in tiles:
        if tiles.is_corner(tile):
            corner_tile = tile
            break

    while not tiles.is_image_edge(corner_tile.top):
        corner_tile.rotate()

    if not tiles.is_image_edge(corner_tile.left):
        corner_tile.flip_x()

    return corner_tile


def get_edge(image: Image, tiles: Tiles) -> List[List[Image]]:
    images = [[image]]
    last_image = image
    while not tiles.is_image_edge(last_image.bottom):
        next_image = tiles.get_next_below(last_image)

        while next_image.top != last_image.bottom:
            next_image.rotate()
        if next_image.top.actual != last_image.bottom.actual:
            next_image.flip_x()
        assert next_image.top.actual == last_image.bottom.actual

        images.append([next_image])
        last_image = next_image

    return images


def get_row(images: List[Image], tiles: Tiles) -> List[Image]:
    last_image = images[0]
    while not tiles.is_image_edge(last_image.right):
        next_image = tiles.get_next_right(last_image)

        while next_image.left != last_image.right:
            next_image.rotate()
        if next_image.left.actual != last_image.right.actual:
            next_image.flip_y()
        assert next_image.left.actual == last_image.right.actual

        images.append(next_image)
        last_image = next_image

    return images


def build_image(tiles: Tiles) -> List[List[Image]]:
    image = get_corner(tiles)
    images = get_edge(image, tiles)
    images = [get_row(row, tiles) for row in images]

    return images


def combine_images(images: List[List[Image]]) -> List[str]:
    final_image = []
    for row in images:
        for pixels in zip(*[image.pixels for image in row]):
            final_image.append("".join(pixels))

    return Image(0, final_image)


def find_sea_monsters(image: Image) -> int:
    sea_monster = (
        "                  # \n"
        "#    ##    ##    ###\n"
        " #  #  #  #  #  #   "
    )
    sea_monster = sea_monster.replace(
        "\n", f".{{{len(image.actual_pixels[0]) - len(sea_monster)//3}}}"
    ).replace(" ", ".")

    pattern = re.compile(f"(?=({sea_monster}))")
    matches = pattern.findall("".join(image.actual_pixels))

    return (
        "".join(image.actual_pixels).count('#')
        - (len(matches) * sea_monster.count('#'))
    )


if __name__ == "__main__":
    tiles = parse_tiles()

    images = build_image(tiles)

    assert (
        images[0][0].tile_id
        * images[-1][0].tile_id
        * images[0][-1].tile_id
        * images[-1][-1].tile_id
    ) == 51214443014783

    final_image = combine_images(images)

    assert find_sea_monsters(final_image) == 2065