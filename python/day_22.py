from collections import deque
import copy
from typing import List, Tuple

import utils


class Player:
    def __init__(self, player_id: int, cards: List[int]):
        self.player_id = player_id
        self.cards = deque(cards)

    @property
    def next_card(self) -> int:
        return self.cards.popleft()

    @property
    def score(self) -> int:
        return sum(
            (index+1) * card
            for index, card in enumerate(list(self.cards)[::-1])
        )

    def wins(self, *cards):
        self.cards.extend(cards)

    def __bool__(self) -> bool:
        return bool(self.cards)

    def __str__(self) -> str:
        return f"Player_{self.player_id}:{','.join(str(card) for card in self.cards)}"


def parse_player(player_id: int, player_cards: List[str]) -> Player:
    cards = [int(card) for card in player_cards]

    return Player(player_id, cards)


def parse_players() -> Tuple[Player, Player]:
    player_1_str, player_2_str = utils.get_data(22).split("\n\n")

    return (
        parse_player(1, player_1_str.splitlines()[1:]),
        parse_player(2, player_2_str.splitlines()[1:])
    )


def play_once(player_1: Player, player_2: Player) -> int:
    while player_1 and player_2:
        card_1 = player_1.next_card
        card_2 = player_2.next_card

        if card_1 > card_2:
            player_1.wins(card_1, card_2)
        else:
            player_2.wins(card_2, card_1)

    if player_1:
        return player_1.score
    return player_2.score


def play_recursive(player_1: Player, player_2: Player) -> Player:
    combinations = set()

    while player_1 and player_2:
        combo = str(player_1) + str(player_2)
        if combo in combinations:
            return player_1
        else:
            combinations.add(combo)

        card_1 = player_1.next_card
        card_2 = player_2.next_card

        if card_1 <= len(player_1.cards) and card_2 <= len(player_2.cards):
            winner = play_recursive(
                Player(1, list(player_1.cards)[:card_1]),
                Player(2, list(player_2.cards)[:card_2])
            )
        elif card_1 > card_2:
            winner = player_1
        else:
            assert card_2 > card_1
            winner = player_2

        if winner.player_id == 1:
            player_1.wins(card_1, card_2)
        else:
            player_2.wins(card_2, card_1)

    if player_1:
        return player_1
    return player_2


if __name__ == "__main__":
    player_1, player_2 = parse_players()
    assert play_once(player_1, player_2) == 33434

    player_1, player_2 = parse_players()
    assert play_recursive(player_1, player_2).score == 31657