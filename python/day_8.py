import copy
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
class Program:
    instructions: List[Instruction]
    next_index: int = 0
    accumulator: int = 0

    @property
    def next(self) -> Instruction:
        return self.instructions[self.next_index]

    @property
    def finished(self) -> bool:
        return self.next_index == len(self.instructions)



def load_program() -> Program:
    return Program(
        [
            Instruction(operation, int(value))
            for operation, value, _ in re.findall(
                SINGLE_INSTRUCTION, utils.get_data(8)
            )
        ]
    )


def run(program: Program) -> int:
    while not program.finished:
        if program.next.executed:
            return program.accumulator
        program.next.executed = True

        if program.next.operation == "acc":
            program.accumulator += program.next.value
            program.next_index += 1

        elif program.next.operation == "jmp":
            program.next_index += program.next.value

        elif program.next.operation == "nop":
            program.next_index += 1
        else:
            assert False

    return program.accumulator


def get_alternative_programs(
    program: List[Program]
) -> List[Program]:
    alt_programs = []
    for index, instruction in enumerate(program.instructions):
        if instruction.operation == "acc":
            continue

        new_operation = "jmp" if instruction.operation == "nop" else "nop"
        alt_programs.append(
            Program(
                copy.deepcopy(program.instructions[:index])
                + [Instruction(new_operation, instruction.value)]+
                copy.deepcopy(program.instructions[index + 1:])
            )
        )

    return alt_programs


if __name__ == "__main__":
    program = load_program()
    alternative_programs = get_alternative_programs(program)

    assert run(program) == 2080

    for alt_prog in alternative_programs:
        accumulator = run(alt_prog)
        if alt_prog.finished:
            break
    assert accumulator == 2477
