import utils


def loop(value: int, subject_num: int) -> int:
    return (value * subject_num) % 20201227


def get_public_key(public_key: int) -> int:
    value = 1
    count = 0
    while value != public_key:
        value = loop(value, 7)
        count += 1
    return count


if __name__ == "__main__":
    card_key, door_key = (int(value) for value in utils.get_data(25).splitlines())

    loop_num = get_public_key(card_key)
    encryption_key = pow(door_key, loop_num, 20201227)

    assert encryption_key == 8329514