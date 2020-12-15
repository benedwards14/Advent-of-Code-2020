from typing import Dict, List

import utils


def get_next(turn: int, last_number: int, cache: Dict[int, int]) -> int:
    if last_number in cache:
        next_number = (turn-1) - cache[last_number]
    else:
        next_number = 0

    cache[last_number] = turn - 1

    return next_number


def get_turn(target_turn: int, seed: List[int]) -> int:
    target_index = target_turn - 1
    try:
        return seed[target_index]
    except IndexError:
        pass

    cache = {num: turn_index for turn_index, num in enumerate(seed)}
    curr_turn_index = len(seed)
    next_num = seed[-1]

    while curr_turn_index != target_index:
        next_num = get_next(curr_turn_index, next_num, cache)
        curr_turn_index += 1

    return get_next(curr_turn_index, next_num, cache)


if __name__ == "__main__":
    seed = [
        int(number) for number in utils.get_data(15).split(',')
    ]
    assert get_turn(2020, seed) == 475
    assert get_turn(30000000, seed) == 11261