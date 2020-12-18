import dataclasses
import numpy
from typing import List, Optional, Tuple, Union

import utils


@dataclasses.dataclass
class SyntaxNode:
    _value: Union[int, 'SyntaxTree']

    def evaluate(self) -> int:
        if isinstance(self._value, int):
            return self._value
        assert isinstance(self._value, SyntaxTree)
        return self._value.evaluate()


@dataclasses.dataclass
class SyntaxTree:
    _node: str
    _children: List[Union[SyntaxNode, 'SyntaxTree']]

    def add_to(self, equation: Union[SyntaxNode, 'SyntaxTree']):
        self._children = [equation] + self._children
        return self

    def evaluate(self) -> int:
        if self._node == '+':
            return self._children[0].evaluate() + self._children[1].evaluate()
        return self._children[0].evaluate() * self._children[1].evaluate()


class SyntaxTree2(SyntaxTree):
    def add_to(self, equation: Union[SyntaxNode, SyntaxTree]):
        if isinstance(equation, SyntaxTree) and self._node == '+':
            self._children = [equation._children[1]] + self._children
            equation._children[1] = self
            return equation

        self._children = [equation] + self._children
        return self


def parse_equation(eq_str: str) -> Tuple[SyntaxTree, str]:
    equation, remaining_str = parse_next_operation(eq_str)

    while remaining_str:
        node, remaining_str = parse_next_operation(
            remaining_str
        )
        if node is None:
            return equation, remaining_str

        equation = node.add_to(equation)

    return equation, ""


def parse_next_operation(eq_str: str) -> Tuple[Optional[SyntaxTree], str]:
    remaining_str = eq_str
    child = None
    op = None

    while child is None:
        next_char, *remaining_str = remaining_str

        if next_char.isspace():
            continue

        if next_char == '(':
            child, remaining_str = parse_equation(remaining_str)
            child = SyntaxNode(child)
        elif next_char == ')':
            return None, remaining_str

        elif next_char.isdigit():
            child = SyntaxNode(int(next_char))
        elif next_char in ['+', '*']:
            op = next_char

    if op is None:
        return child, remaining_str

    return Tree(op, [child,]), remaining_str


if __name__ == "__main__":
    Tree = SyntaxTree
    equations = [
        parse_equation(equation)[0]
        for equation in utils.get_data(18).splitlines()
    ]
    assert sum(equation.evaluate() for equation in equations) == 75592527415659

    Tree = SyntaxTree2
    equations = [
        parse_equation(equation)[0]
        for equation in utils.get_data(18).splitlines()
    ]
    assert sum(equation.evaluate() for equation in equations) == 360029542265462