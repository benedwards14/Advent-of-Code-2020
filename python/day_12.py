import dataclasses
import enum
import math
import re

import utils


DIRECTION_PATTERN = r"(N|S|E|W|L|R|F)([0-9]*)"


class Direction(enum.Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    LEFT = "L"
    RIGHT = "R"
    FORWARD = "F"


@dataclasses.dataclass
class Point:
    latitude: int
    longitude: int


@dataclasses.dataclass
class Ship(Point):
    orientation: int


def move(ship: Ship, direction: Direction, distance: int):
    if direction == Direction.NORTH:
        ship.latitude += distance
    elif direction == Direction.SOUTH:
        ship.latitude -= distance

    elif direction == Direction.EAST:
        ship.longitude += distance
    elif direction == Direction.WEST:
        ship.longitude -= distance

    elif direction == Direction.LEFT:
        ship.orientation = (ship.orientation - distance) % 360
    elif direction == Direction.RIGHT:
        ship.orientation = (ship.orientation + distance) % 360

    elif direction == Direction.FORWARD:
        if ship.orientation == 0:
            ship.latitude += distance
        if ship.orientation == 90:
            ship.longitude += distance
        if ship.orientation == 180:
            ship.latitude -= distance
        if ship.orientation == 270:
            ship.longitude -= distance


def move2(ship: Ship, waypoint: Point, direction: Direction, distance: int):
    if direction == Direction.NORTH:
        waypoint.latitude += distance
    elif direction == Direction.SOUTH:
        waypoint.latitude -= distance

    elif direction == Direction.EAST:
        waypoint.longitude += distance
    elif direction == Direction.WEST:
        waypoint.longitude -= distance

    if direction in [Direction.LEFT, Direction.RIGHT]:
        longitude = waypoint.longitude
        latitude = waypoint.latitude
        if direction == Direction.RIGHT:
            distance = (360 - distance) % 360
        if distance == 90:
            waypoint.latitude = longitude
            waypoint.longitude = -latitude
        elif distance == 180:
            waypoint.latitude = -latitude
            waypoint.longitude = -longitude
        elif distance == 270:
            waypoint.latitude = -longitude
            waypoint.longitude = latitude

    elif direction == Direction.FORWARD:
        ship.latitude += waypoint.latitude * distance
        ship.longitude += waypoint.longitude * distance



def parse_directions():
    return [
        (Direction(direction), int(value))
        for direction, value in re.findall(
            DIRECTION_PATTERN, utils.get_data(12)
        )
    ]


if __name__ == "__main__":
    ship = Ship(0, 0, 90)
    ship2 = Ship(0, 0, 90)
    waypoint = Point(1, 10)
    for direction, value in parse_directions():
        move(ship, direction, value)
        move2(ship2, waypoint, direction, value)
    print(abs(ship.latitude) + abs(ship.longitude))
    print(abs(ship2.latitude) + abs(ship2.longitude))