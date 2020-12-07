import re
from typing import List, Pattern

import utils


class Bags:
    PATTERN: Pattern = r"(?P<count>[0-9 ]*)[ ]*(?P<colour>[a-z ]+) bag[s]{0,1}"

    def __init__(self, bag_strs: List[str]):
        self._bags = {}
        for bag_str in bag_strs:
            (_, outer_colour), *inner_bags = re.findall(
                self.PATTERN, bag_str
            )
            self._bags[outer_colour] = {
                inner_colour: int(count) for count, inner_colour in inner_bags
            }

    @property
    def colours(self):
        return set(self._bags.keys())

    def walk(self, start_colour: str):
        if start_colour in self._bags:
            for colour in self._bags[start_colour]:
                yield colour
                yield from self.walk(colour)

    def count_bags_in(self, start_colour):
        if start_colour not in self._bags:
            return 0
        return sum(
            count + count*self.count_bags_in(colour)
            for colour, count in self._bags[start_colour].items()
        )


if __name__ == "__main__":
    bags = Bags(utils.get_data(7).splitlines())

    assert sum(
        "shiny gold" in bags.walk(bag)
        for bag in bags.colours
    ) == 124
    assert bags.count_bags_in("shiny gold") == 34862