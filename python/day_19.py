from collections import defaultdict
import itertools
import re
from typing import Dict, List, Optional, Set

import utils


def combine_ids(
    _, ids: List[int], rules: Dict[int, Set[str]],
):
    for strs in itertools.product(*[rules[id] for id in ids]):
        yield "".join(strs)


def create_rule(
    rule_id: int, rule_strs: Dict[int, str], rules: Dict[int, Set[str]]
) -> Dict[int, Set[str]]:
    if rule_id in rules:
        return rules
    rule_def = rule_strs[rule_id]

    if (match := re.match(r"\"(a|b)\"", rule_def)) is not None:
        rules[rule_id] = {match.group(1)}
        return rules

    rule_ids = [
        list(map(lambda id: int(id), ids.split()))
        for ids in rule_def.split(" | ")
    ]
    for ids in rule_ids:
        for id in ids:
            rules = create_rule(id, rule_strs, rules)

        for str in combine_ids(rule_id, ids, rules):
            rules[rule_id].add(str)

    return rules


def apply_loop_rules(
    input_str: str, starts_with: Set[str], ends_with: Set[str]
) -> bool:
    section_len = 8
    if len(input_str) % section_len != 0:
        return False

    input_sections = [
        input_str[i:i + section_len]
        for i in range(0, len(input_str), section_len)
    ]

    if (
        input_sections[0] not in starts_with
        or input_sections[1] not in starts_with
        or input_sections[-1] not in ends_with
    ):
        return False
    input_sections = input_sections[2:-1]

    while len(input_sections) > 1 and input_sections[-1] in ends_with:
        if input_sections[0] not in starts_with:
            return False

        input_sections = input_sections[1:-1]

    return all(section in starts_with for section in input_sections)


if __name__ == "__main__":
    rule_strs, input_strs, *_ = utils.get_data(19).split("\n\n")

    temp_rules = {
        int(rule_str.split(':')[0]): rule_str.split(':')[1].strip()
        for rule_str in rule_strs.splitlines()
    }
    rules = create_rule(0, temp_rules, defaultdict(set))

    assert sum(
        input_str in rules[0] for input_str in input_strs.splitlines()
    ) == 291
    assert sum(
        apply_loop_rules(input_str, rules[42], rules[31])
        for input_str in input_strs.splitlines()
    ) == 409