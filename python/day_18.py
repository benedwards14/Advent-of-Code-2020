import dataclasses
import numpy
from typing import Optional, Tuple, Union

import utils


Parentheses = 'Stmt'
Value = Union[int, Parentheses]


@dataclasses.dataclass
class Operation:
    op: str
    value: Value = None


@dataclasses.dataclass
class Stmt:
    value: Union[Value, Operation]
    next: Optional['Stmt'] = None


def parse_equation(eq_str: str) -> Tuple[Stmt, str]:
    equation = None
    last_stmt = None
    remaining_str = eq_str

    while remaining_str:
        next_value = None
        next_op = None
        next_char, *remaining_str = remaining_str
        if next_char.isspace():
            continue

        if next_char == '(':
            next_value, remaining_str = parse_equation(remaining_str)
        elif next_char == ')':
            return equation, remaining_str

        elif next_char.isdigit():
            next_value = int(next_char)
        elif next_char in ['+', '*']:
            next_op = next_char

        if next_op is not None:
            next_stmt = Stmt(Operation(next_op))
            last_stmt.next = next_stmt
            last_stmt = next_stmt
        else:
            assert next_value is not None
            if equation is None:
                equation = Stmt(next_value)
                last_stmt = equation
            else:
                last_stmt.value.value = next_value

    return equation, None


def get_value(value: Value) -> int:
    return evaluate_equation(value) if isinstance(value, Stmt) else value


def evaluate_equation(equation: Stmt) -> int:
    total_value = get_value(equation.value)
    curr_stmt = equation.next

    while curr_stmt is not None:
        assert isinstance(curr_stmt.value, Operation)
        next_value = get_value(curr_stmt.value.value)
        if curr_stmt.value.op == '+':
            total_value += next_value
        else:
            assert curr_stmt.value.op == '*'
            total_value *= next_value
        curr_stmt = curr_stmt.next

    return total_value


def get_value2(value: Value) -> int:
    return evaluate_equation2(value) if isinstance(value, Stmt) else value


def evaluate_equation2(equation: Stmt) -> int:
    add_values = [get_value2(equation.value)]
    curr_stmt = equation.next

    while curr_stmt is not None:
        assert isinstance(curr_stmt.value, Operation)
        next_value = get_value2(curr_stmt.value.value)
        if curr_stmt.value.op == '+':
            add_values[-1] += next_value
        else:
            assert curr_stmt.value.op == '*'
            add_values.append(next_value)
        curr_stmt = curr_stmt.next

    return numpy.prod(add_values)


if __name__ == "__main__":
    equations = [
        parse_equation(equation)[0]
        for equation in utils.get_data(18).splitlines()
    ]
    assert sum(evaluate_equation(equation) for equation in equations) == 75592527415659
    assert sum(evaluate_equation2(equation) for equation in equations) == 360029542265462