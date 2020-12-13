import enum
from typing import List, Tuple

import utils


class Seat(enum.Enum):
    EMPTY = "L"
    OCCUPIED = "#"
    FLOOR = "."


class Map:
    MAX_OCCUPIED = 4

    def __init__(self, seats: List[str]):
        self._width = len(seats[0])
        self._height = len(seats)
        self._seats = [
            Seat(seat) for row in seats for seat in row
        ]
        self._last_updated: List[Tuple[int, Seat]] = list(enumerate(self._seats))

    @property
    def occupied_seats(self) -> int:
        return sum(seat == Seat.OCCUPIED for seat in self._seats)

    def __getitem__(self, x_y: Tuple[int, int]) -> Seat:
        x, y = x_y
        if x < 0 or x >= self._width:
            raise IndexError
        if y < 0 or y >= self._height:
            raise IndexError
        return self._seats[y*self._width + x]

    def _get_neighbours(self, index: int):
        row, column = index // self._width, index % self._width
        for y in [row - 1, row, row + 1]:
            for x in [column - 1, column, column + 1]:
                if x == column and y == row:
                    continue
                else:
                    try:
                        yield self[x,y]
                    except IndexError:
                        pass

    def _evaluate(self, index: int) -> Seat:
        occupied_neighbours = sum(
            neighbour == Seat.OCCUPIED
            for neighbour in self._get_neighbours(index)
        )
        if self._seats[index] == Seat.OCCUPIED and occupied_neighbours >= self.MAX_OCCUPIED:
            return Seat.EMPTY
        if self._seats[index] == Seat.EMPTY and occupied_neighbours == 0:
            return Seat.OCCUPIED
        return self._seats[index]

    def _step(self):
        updated = []
        for index, _ in self._last_updated:
            new_seat = self._evaluate(index)
            if new_seat != self._seats[index]:
                updated.append((index, new_seat))

        for index, new_seat in updated:
           self._seats[index] = new_seat

        self._last_updated = updated

    def run(self) -> int:
        while self._last_updated:
            #print(str(self))
            self._step()

    def __str__(self) -> str:
        map = []
        for y in range(self._height):
            for x in range(self._width):
                map.append(self[x,y].value)
            map.append('\n')
        map.append('\n')
        return "".join(map)


class Map2(Map):
    MAX_OCCUPIED = 5

    def _get_neighbours(self, index: int):
        row, col = index % self._width, index // self._width
        directions = [
            (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)
        ]

        for x_step, y_step in directions:
            step = 1
            try:
                while True:
                    x = row + x_step*step
                    y = col + y_step*step
                    if self[x, y] != Seat.FLOOR:
                        yield self[x, y]
                        break
                    step += 1
            except IndexError:
                pass


if __name__ == "__main__":
    map = Map(utils.get_data(11).splitlines())
    map.run()
    assert map.occupied_seats == 2247

    map2 = Map2(utils.get_data(11).splitlines())
    map2.run()
    assert map2.occupied_seats == 2011

