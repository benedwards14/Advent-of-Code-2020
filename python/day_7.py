import dataclasses
import re
from typing import ClassVar, List, Pattern

import utils


@dataclasses.dataclass(frozen=True)
class Bag:
    colour: str

    PATTERN: ClassVar[Pattern] = r"[0-9 ]*(?P<colour>[a-z ]+) bag[s]{0,1}"


def parse_bags(bag_strs: List[str]):
    for bag_str in bag_strs:
        outer_bag_colour, *inner_bag_colours = re.findall(Bag.PATTERN, bag_str)
        yield (
            Bag(outer_bag_colour),
            {Bag(inner_bag_colour) for inner_bag_colour in inner_bag_colours}
        )


if __name__ == "__main__":
    bags = {
        outer_bag: inner_bags
        for outer_bag, inner_bags in parse_bags(utils.get_data(7).splitlines())
    }

    def contains_shiny_gold(outer_bag):
        if outer_bag not in bags:
            return False
        if Bag("shiny gold") in bags[outer_bag]:
            return True
        return any(
            contains_shiny_gold(inner_bag) for inner_bag in bags[outer_bag]
        )

    print(
        sum(contains_shiny_gold(outer_bags) for outer_bags in bags.keys())
    )