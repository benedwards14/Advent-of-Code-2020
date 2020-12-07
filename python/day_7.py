from collections import defaultdict
import dataclasses
import re
from typing import Dict, Generator, List, Pattern, Set, Tuple

import utils


BAG_PATTERN: Pattern = r"(?P<count>[0-9 ]*)[ ]*(?P<colour>[a-z ]+) bag[s]{0,1}"
LEAF_EDGE = Tuple[int, str]


@dataclasses.dataclass
class Leaf:
    parents: Set[str] = dataclasses.field(default_factory=set)
    children: List[LEAF_EDGE] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Tree:
    leaves: Dict[str, Leaf] = dataclasses.field(
        default_factory=lambda: defaultdict(Leaf)
    )

    def add_leaf(self, name: str, children: List[Tuple[str, str]]):
        for child_count, child_name in children:
            self.leaves[name].children.append((int(child_count), child_name))
            self.leaves[child_name].parents.add(name)

    def walk_parents(self, leaf_name: str) -> Generator[str, None, None]:
        for parent in self.leaves[leaf_name].parents:
            yield parent
            yield from self.walk_parents(parent)

    def count_parents(self, leaf_name: str) -> int:
        return len(set(self.walk_parents(leaf_name)))

    def count_children(self, leaf_name: str) -> int:
        return sum(
            count + count*self.count_children(name)
            for count, name in self.leaves[leaf_name].children
        )


def parse_bags() -> Tree:
    bag_tree = Tree()
    for bag_str in utils.get_data(7).splitlines():
        (_, bag_colour), *inner_bags = re.findall(BAG_PATTERN, bag_str)
        bag_tree.add_leaf(bag_colour, inner_bags)

    return bag_tree


if __name__ == "__main__":
    bags = parse_bags()

    assert bags.count_parents("shiny gold") == 124
    assert bags.count_children("shiny gold") == 34862