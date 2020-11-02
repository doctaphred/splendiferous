from collections import namedtuple

from . import gems
from .utils import cache


class State(namedtuple('State', [
    'bank_gems',
    'bank_cards',
    'player_gems',
    'player_cards',
])):

    # def __init__(self, *args, **kwargs):
    #     assert all(v >= 0 for v in self.bank_gems)
    #     assert all(v >= 0 for v in self.player_gems)

    def __repr__(self):
        return self.pretty()

    def pretty(self, cards=False):
        return '\n'.join(self._pretty(indent='  ', cards=cards))

    def _pretty(self, indent, cards):
        yield f"{type(self).__name__}:"
        yield f"{indent}bank_gems: {self.bank_gems}"
        yield f"{indent}player_gems: {self.player_gems}"
        yield f"{indent}score: {self.player_cards.score}"
        yield f"{indent}discounts: {self.player_cards.discounts}"
        yield f"{indent}player_cards: {len(self.player_cards)}"
        if cards:
            for card in sorted(self.player_cards):
                yield f"{indent}{indent}{card}"

    @cache
    def successors(self):
        return tuple(self.takes()) + tuple(self.buys())

    def takes(self):
        for taken in gems.takes(self.bank_gems):
            player_gems = self.player_gems + taken
            if sum(player_gems) <= 10:  # TODO: Allow discarding down.
                bank_gems = self.bank_gems - taken
                new_state = type(self)(
                    bank_gems=bank_gems,
                    bank_cards=self.bank_cards,
                    player_gems=player_gems,
                    player_cards=self.player_cards,
                )
                yield new_state

    def buys(self):
        discounts = self.player_cards.discounts
        purchase_power = self.player_gems + discounts
        for card in self.bank_cards:
            if purchase_power >= card.price:
                cost = card.price.less(discounts)
                yield type(self)(
                    bank_gems=self.bank_gems + cost,
                    bank_cards=self.bank_cards.sell(card),
                    player_gems=self.player_gems - cost,
                    player_cards=self.player_cards.buy(card),
                )
