from typing import Dict, Generator, List

import utils


combination_cache: Dict[int, int] = {}


def voltage_jumps(adapters: List[int]) -> Generator[int, None, None]:
    prev_joltage = 0
    for joltage in adapters:
        yield joltage - prev_joltage
        prev_joltage = joltage
    yield 3


def combine_three_forwards(joltage_jumps: List[int]) -> int:
    first_jump, second_jump, third_jump, *remaining_jumps = joltage_jumps
    if first_jump + second_jump + third_jump > 3:
        return 0
    return count_combinations(remaining_jumps)


def combine_two_forwards(joltage_jumps: List[int]) -> int:
    first_jump, second_jump, *remaining_jumps = joltage_jumps
    if first_jump + second_jump > 3:
        return 0
    return count_combinations(remaining_jumps)


def combine_one_forwards(joltage_jumps: List[int]) -> int:
    _, *remaining_jumps = joltage_jumps
    return count_combinations(remaining_jumps)


def count_combinations(joltage_jumps: List[int]) -> int:
    if len(joltage_jumps) in combination_cache:
        return combination_cache[len(joltage_jumps)]

    count = 0
    if len(joltage_jumps) >= 3:
        count += combine_three_forwards(joltage_jumps)
    if len(joltage_jumps) >= 2:
        count += combine_two_forwards(joltage_jumps)
    if len(joltage_jumps) >= 1:
        count += combine_one_forwards(joltage_jumps)
    else:
        count = 1

    combination_cache[len(joltage_jumps)] = count

    return count


if __name__ == "__main__":
    adapters = sorted(
        [int(joltage) for joltage in utils.get_data(10).splitlines()]
    )
    voltage_jumps = list(voltage_jumps(adapters))
    assert voltage_jumps.count(1) * voltage_jumps.count(3) == 2482
    assert count_combinations(voltage_jumps) == 96717311574016

