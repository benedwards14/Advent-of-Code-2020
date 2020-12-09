import copy
import dataclasses
import re
from typing import List, Optional

import utils


SINGLE_INSTRUCTION = r"(acc|nop|jmp) ((\+|-)[0-9]*)"


@dataclasses.dataclass
class Instruction:
    operation: str
    value: int
    index: int
    next_index: Optional[int] = None
    prev_indices: List[int] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Program:
    instructions: List[Instruction]

    def __iter__(self):
        curr = self.instructions[0]
        executed_indices = set()
        while curr is not None:
            yield curr
            executed_indices.add(curr.index)

            if curr.next_index is None or curr.next_index in executed_indices:
                break
            curr = self.instructions[curr.next_index]


def load_program() -> Program:
    instructions = [
        Instruction(operation, int(value), index)
        for index, (operation, value, _) in enumerate(
            re.findall(SINGLE_INSTRUCTION, utils.get_data(8))
        )
    ]

    for instruction in instructions:
        if instruction.operation == "jmp":
            next_index = instruction.index + instruction.value
        else:
            next_index = instruction.index + 1
        if next_index < len(instructions):
            instruction.next_index = next_index
            instructions[next_index].prev_indices.append(instruction.index)

    return Program(instructions)


def run(program: Program) -> int:
    return sum(
        instruction.value
        for instruction in program
        if instruction.operation == "acc"
    )


def get_correct_instruction_set(
    old_program: Program
) -> List[Instruction]:
    old_instructions = old_program.instructions
    def walk_back(instruction):
        yield instruction.index
        for index in instruction.prev_indices:
            yield from walk_back(old_instructions[index])
    end_indices = {
        index for index in walk_back(old_instructions[-1])
    }

    new_instructions = copy.deepcopy(old_instructions)
    new_program = Program(new_instructions)
    for instruction in new_program:
        change_to_index = None
        if instruction.operation == "jmp":
            if instruction.index + 1 in end_indices:
                instruction.operation = "nop"
                change_to_index = instruction.index + 1
        elif instruction.operation == "nop":
            if instruction.index + 1 in end_indices:
                instruction.operation = "jmp"
                change_to_index = instruction.index + instruction.value

        if change_to_index is not None:
            new_instructions[instruction.next_index].prev_indices.remove(
                instruction.index
            )
            instruction.next_index = change_to_index
            new_instructions[instruction.next_index].prev_indices.append(
                instruction.index
            )
            break

    return new_program


if __name__ == "__main__":
    program = load_program()
    assert run(program) == 2080

    new_program = get_correct_instruction_set(program)
    assert run(new_program) == 2477