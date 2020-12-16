import dataclasses
import numpy
import re
from typing import Dict, List, Set, Tuple

import utils


@dataclasses.dataclass(frozen=True)
class TicketField:
    name: str
    range: Set[int]


@dataclasses.dataclass
class Ticket:
    fields: List[int]


def parse_ticket_fields(ticket_field_strs: List[str]) -> List[TicketField]:
    ticket_fields = []
    for field_str in ticket_field_strs:
        match = re.match(
            r"([a-z ]*): ([0-9]*)-([0-9]*) or ([0-9]*)-([0-9]*)", field_str
        )
        assert match is not None

        ticket_fields.append(
            TicketField(
                match.group(1),
                set(range(int(match.group(2)), int(match.group(3)) + 1))
                | set(range(int(match.group(4)), int(match.group(5)) + 1))
            )
        )

    return ticket_fields


def parse_ticket(ticket_str: str) -> Ticket:
    return Ticket([int(field) for field in ticket_str.split(',')])


def parse_input() -> Tuple[List[TicketField], Ticket, List[Ticket]]:
    ticket_field_strs, your_ticket_str, nearby_ticket_strs = utils.get_data(
        16
    ).split("\n\n")

    return (
        parse_ticket_fields(ticket_field_strs.splitlines()),
        parse_ticket(your_ticket_str.splitlines()[1]),
        [
            parse_ticket(ticket_str)
            for ticket_str in nearby_ticket_strs.splitlines()[1:]
        ]
    )


def find_one_to_one_mapping(mapping: Dict[str, Set[int]]) -> Dict[str, int]:
    all_in = set.intersection(*[values for values in mapping.values()])
    all_values = set.union(*[values for values in mapping.values()])
    remaining_values = all_values
    remaining_keys = set(mapping.keys())

    new_mapping = {}

    while remaining_values:
        for key in remaining_keys:
            potential_mappings = mapping[key] & remaining_values
            if len(potential_mappings) == 1:
                new_mapping[key] = potential_mappings.pop()

        remaining_keys = set(mapping.keys()) - set(new_mapping.keys())
        remaining_values = all_values - set(new_mapping.values())

    return new_mapping


def find_fields(
    fields: List[TicketField],
    tickets: List[Ticket]
) -> Dict[TicketField, int]:
    field_name_map = {
        field.name: field for field in fields
    }
    max_index = range(len(tickets[0].fields))
    field_to_index = {
        field.name: set(max_index) for field in fields
    }

    for ticket in tickets:
        field_to_index = {
            field_name: {
                index
                for index in value_indices
                if ticket.fields[index] in field_name_map[field_name].range
            }
            for field_name, value_indices in field_to_index.items()
        }

    return find_one_to_one_mapping(field_to_index)


def remove_invalid_tickets(
    ticket_fields: List[TicketField],
    tickets: List[Ticket]
) -> Tuple[List[Ticket], int]:
    valid_tickets = []
    error_rate = 0
    valid_values = set.union(*[field.range for field in ticket_fields])

    for ticket in tickets:
        if (invalid_values := set(ticket.fields) - valid_values):
            error_rate += sum(invalid_values)
        else:
            valid_tickets.append(ticket)

    return valid_tickets, error_rate


if __name__ == "__main__":
    ticket_fields, your_ticket, nearby_tickets = parse_input()

    nearby_tickets, error_rate = remove_invalid_tickets(
        ticket_fields, nearby_tickets
    )
    assert error_rate == 25788
    field_map = find_fields(ticket_fields, nearby_tickets)
    assert (
        numpy.prod(
            list(
                your_ticket.fields[index]
                for field, index in field_map.items()
                if field.startswith("departure")
            )
        )
    ) == 3902565915559