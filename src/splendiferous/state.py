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

    def pretty(self):
        return '\n'.join(self._pretty(indent='  '))

    def _pretty(self, indent):
        yield f"{type(self).__name__}:"
        yield f"{indent}bank_gems: {self.bank_gems}"
        yield f"{indent}player_gems: {self.player_gems}"
        if self.player_cards:
            yield f"{indent}player_cards ({len(self.player_cards)}):"
            for card in sorted(self.player_cards):
                yield f"{indent}{indent}{card}"

    @property
    def score(self):
        return self._score(self.player_cards)

    @staticmethod
    @cache
    def _score(cards):
        return sum(card.points for card in cards)

    @property
    def discounts(self):
        return self._discounts(self.player_cards)

    @staticmethod
    @cache
    def _discounts(cards):
        return sum([card.discount for card in cards], gems.ZERO)

    @property
    def purchase_power(self):
        return self._purchase_power(self.player_gems, self.discounts)

    @staticmethod
    @cache
    def _purchase_power(gems, discounts):
        return gems + discounts

    def successors(self):
        yield from self.takes()
        yield from self.buys()

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
        discounts = self.discounts
        purchase_power = self.purchase_power
        for card in self.bank_cards:
            if purchase_power >= card.price:
                cost = card.price.less(discounts)
                yield type(self)(
                    bank_gems=self.bank_gems + cost,
                    bank_cards=self._sell(self.bank_cards, card),
                    player_gems=self.player_gems - cost,
                    player_cards=self._buy(self.player_cards, card),
                )

    @staticmethod
    @cache
    def _sell(bank_cards, card):
        return bank_cards - {card}

    @staticmethod
    @cache
    def _buy(player_cards, card):
        return player_cards | {card}
