import dataclasses
import re
from typing import Callable, ClassVar, List, Pattern

import utils


@dataclasses.dataclass
class Password:
    value: str
    restricted_char: str
    first_num: str
    second_num: str

    LINE_PATTERN: ClassVar[Pattern] = (
        r"(?P<first_num>\d+)-(?P<second_num>\d+) "
        "(?P<restricted_char>[a-z]): (?P<value>[a-z]*)"
    )

    @classmethod
    def from_string(cls, pwd_str: str) -> 'Password':
        return cls(
            **re.match(Password.LINE_PATTERN, pwd_str).groupdict()
        )

    def __post_init__(self):
        self.first_num = int(self.first_num)
        self.second_num = int(self.second_num)

    def __str__(self) -> str:
        return self.value

    def __getitem__(self, index: int) -> str:
        return self.value[index - 1]


def validate_pwd_1(password: Password) -> bool:
    occurences = str(password).count(password.restricted_char)
    return (
        occurences >= password.first_num
        and occurences <= password.second_num
    )


def validate_pwd_2(password: Password) -> bool:
    first_matches = password[password.first_num] == password.restricted_char
    second_matches = password[password.second_num] == password.restricted_char

    return first_matches != second_matches


def count_valid_pwds(
    passwords: List[str], validate: Callable[[str], bool]
) -> int:
    return sum(validate(password) for password in passwords)


if __name__ == "__main__":
    passwords = [
        Password.from_string(password)
        for password in utils.get_data(2).split('\n')
    ]

    assert count_valid_pwds(passwords, validate_pwd_1) == 515
    assert count_valid_pwds(passwords, validate_pwd_2) == 711