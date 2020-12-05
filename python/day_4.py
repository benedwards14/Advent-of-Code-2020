from typing import List
import re

import utils


class Passport:
    REQUIRED = {
        "byr": r"(19[2-9][0-9]|200[0-2])$",
        "iyr": r"(201[0-9]|2020)$",
        "eyr": r"(202[0-9]|2030)$",
        "hgt": r"((1([5-8][0-9]|9[0-3]))cm|(59|6[0-9]|7[0-6])in)$",
        "hcl": r"#[0-9a-f]{6}$",
        "ecl": r"(amb|blu|brn|gry|grn|hzl|oth)$",
        "pid": r"[0-9]{9}$",
    }
    def __init__(self, passport_str: str):
        self._entries = dict(
            entry.split(':')
            for entry in passport_str.split()
        )

    def validate_1(self) -> bool:
        return set(self._entries.keys()) >= set(self.REQUIRED.keys())

    def validate_2(self) -> bool:
        return all(
            re.match(regex, self._entries[key]) is not None
            if key in self._entries else False
            for key, regex in self.REQUIRED.items()
        )


if __name__ == "__main__":
    passports = [
        Passport(passport_str)
        for passport_str in utils.get_data(4).split("\n\n")
    ]

    assert sum(passport.validate_1() for passport in passports) == 239
    assert sum(passport.validate_2() for passport in passports) == 188