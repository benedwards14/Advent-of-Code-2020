import itertools
import numpy
from typing import List

import utils

if __name__ == "__main__":
    expenses = [int(expense) for expense in utils.get_data(1).split()]

    def products(combination_of: int) -> List[str]:
        return [
            str(numpy.prod(expense_combination))
            for expense_combination in itertools.combinations(
                expenses, combination_of
            )
            if sum(expense_combination) == 2020
        ]

    assert products(2) == ["988771"]
    assert products(3) == ["171933104"]
