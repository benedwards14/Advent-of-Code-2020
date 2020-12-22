from collections import Counter
import re
from typing import Dict, List, Set, Tuple

import utils


def parse_label(label: str) -> Tuple[List[str], List[str]]:
    match = re.match(r"([a-z ]*)\(contains ([a-z, ]*)\)", label)

    ingredients = match.group(1).strip().split()
    allegens = match.group(2).strip().split(", ")

    return ingredients, allegens


def parse_labels() -> Tuple[Counter, Dict[str, Set[str]]]:
    all_ingredients = Counter()
    allegen_map = {}
    for label in utils.get_data(21).splitlines():
        ingredients, allegens = parse_label(label)

        all_ingredients.update(ingredients)
        for allegen in allegens:
            if allegen not in allegen_map:
                allegen_map[allegen] = set(ingredients)
            else:
                allegen_map[allegen] &= set(ingredients)

    return all_ingredients, allegen_map


def count_non_allegen_ingredients(
    ingredient_count: Counter,
    allegens: Dict[str, Set[str]]
) -> int:
    ingedients = set(ingredient_count.elements())
    potential_allegens = set.union(
        *[ingredients for ingredients in allegens.values()]
    )

    non_allegen_ingredients = ingedients - potential_allegens

    return sum(
        ingredient_count[ingredient] for ingredient in non_allegen_ingredients
    )


def get_allegen_ingredients(allegens: Dict[str, Set[str]]) -> str:
    remaining_allegen_ingredients = set.union(
        *[ingredients for ingredients in allegens.values()]
    )
    allegen_to_ingredient = {}

    while remaining_allegen_ingredients:
        new_allegens = {}
        for allegen, potential_ingredients in allegens.items():
            potential_ingredients &= remaining_allegen_ingredients
            if len(potential_ingredients) == 1:
                remaining_allegen_ingredients -= potential_ingredients
                allegen_to_ingredient[allegen] = potential_ingredients.pop()
            else:
                new_allegens[allegen] = potential_ingredients

        allegens = new_allegens

    return ",".join(
        [
            allegen_to_ingredient[allegen]
            for allegen in sorted(allegen_to_ingredient.keys())
        ]
    )


if __name__ == "__main__":
    ingredients, allegens = parse_labels()

    assert count_non_allegen_ingredients(ingredients, allegens) == 2020
    assert (
        get_allegen_ingredients(allegens)
        == "bcdgf,xhrdsl,vndrb,dhbxtb,lbnmsr,scxxn,bvcrrfbr,xcgtv"
    )

