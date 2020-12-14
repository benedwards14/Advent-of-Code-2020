import dataclasses
import itertools
import re
from typing import Dict, Tuple, Union

import utils


class Mask:
    ALWAYS_ZERO = None
    ALWAYS_ONE = None

    def __init__(self, mask: str):
        self._and_num = int(
            "".join("0" if c == self.ALWAYS_ZERO else "1" for c in mask), base=2
        )
        self._or_num = int(
            "".join("1" if c == self.ALWAYS_ONE else "0" for c in mask), base=2
        )

    def _update_bits(self, num: int) -> int:
        return (num & self._and_num) | self._or_num

    def get_value(_, value: int) -> int:
        return value

    def get_registers(_, register: int) -> int:
        yield register


class Mask1(Mask):
    ALWAYS_ZERO = "0"
    ALWAYS_ONE = "1"

    def get_value(self, value: int) -> int:
        return self._update_bits(value)


class Mask2(Mask):
    ALWAYS_ZERO = "X"
    ALWAYS_ONE = "1"

    def __init__(self, mask: str):
        super().__init__(mask)

        self._x_values = [
            2 ** index for index, c in enumerate(mask[::-1]) if c == "X"
        ]

    def get_registers(self, register: int) -> int:
        reg = self._update_bits(register)
        yield reg
        for i in range(len(self._x_values)):
            for increments in itertools.combinations(self._x_values, i+1):
                yield reg + sum(increments)


@dataclasses.dataclass
class Program:
    mask: Mask
    memory: Dict[int, int] = dataclasses.field(default_factory=dict)

    def update(self, register: int, value: int):
        for reg in self.mask.get_registers(register):
            self.memory[reg] = self.mask.get_value(value)


def run(program: Program, steps: Union[Mask, Tuple[int, int]]) -> int:
    for step in steps:
        if isinstance(step, Mask):
            program.mask = step
        else:
            register, value = step
            program.update(register, value)

    return sum(program.memory.values())


def parse_step(input_str: str, mask_cls) -> Union[Mask, Tuple[int, int]]:
    if (match := re.match(r"mask = ([01X]*)", input_str)) is not None:
        return mask_cls(match.group(1))

    assert (
        match := re.match(r"mem\[([0-9]*)\] = ([0-9]*)", input_str)
    ) is not None
    return int(match.group(1)), int(match.group(2))


if __name__ == "__main__":
    first_mask, *steps = [
        parse_step(step_str, Mask1)
        for step_str in utils.get_data(14).splitlines()
    ]
    program = Program(first_mask)
    assert run(program, steps) == 7997531787333

    first_mask, *steps = [
        parse_step(step_str, Mask2)
        for step_str in utils.get_data(14).splitlines()
    ]
    program = Program(first_mask)
    assert run(program, steps) == 3564822193820
