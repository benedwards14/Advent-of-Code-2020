import dataclasses
import re
from typing import List

import utils


SINGLE_INSTRUCTION = r"(acc|nop|jmp) ((\+|-)[0-9]*)"


@dataclasses.dataclass
class Instruction:
    operation: str
    value: int
    executed: bool = False


@dataclasses.dataclass
class Programme:
    instructions: List[Instruction]
    next_index: int = 0
    accumulator: int = 0

    @property
    def next(self) -> Instruction:
        return self.instructions[self.next_index]


def load_programme() -> Programme:
    return Programme(
        [
            Instruction(operation, int(value))
            for operation, value, _ in re.findall(
                SINGLE_INSTRUCTION, utils.get_data(8)
            )
        ]
    )


def run(programme: Programme) -> Programme:
    while not programme.next.executed:
        programme.next.executed = True

        if programme.next.operation == "acc":
            programme.accumulator += programme.next.value
            programme.next_index += 1

        elif programme.next.operation == "jmp":
            programme.next_index += programme.next.value

        elif programme.next.operation == "nop":
            programme.next_index += 1
        else:
            assert False

    return programme


if __name__ == "__main__":
    programme = load_programme()
    programme = run(programme)
    assert programme.accumulator == 2080
