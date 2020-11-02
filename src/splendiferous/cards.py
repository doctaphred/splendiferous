from collections import namedtuple

from . import data
from . import gems
from .gems import Gemset
from .utils import cache


class Card(namedtuple('Card', ['level', 'points', 'discount', 'price'])):

    @classmethod
    def read(cls, line):
        level, points, color, price = line.strip().split()
        return cls(
            level=int(level),
            points=int(points),
            discount=Gemset.read(color),
            price=Gemset(map(int, price)),
        )


CARDS = [Card.read(line) for line in data.cards.splitlines() if line]


class Cardset:
    _values = {}
    _keys = {}

    def __new__(cls, value):
        """"Turbocached" constructor.

        Ensures that only one instance of this class is ever created for
        a given value, enabling equality (including cache checks) to be
        based on object identity rather than value.
        """
        value = frozenset(value)
        try:
            return cls._keys[value]
        except KeyError:
            key = cls._keys[value] = super().__new__(cls)
            cls._values[key] = value
            return key

    def __call__(self):
        return self._values[self]

    def __iter__(self):
        return iter(self())

    @cache
    def __len__(self):
        return len(self())

    @cache
    def sell(self, card):
        assert card in self()
        return type(self)(self() - {card})

    @cache
    def buy(self, card):
        assert card not in self()
        return type(self)(self() | {card})

    @property
    @cache
    def discounts(self):
        return sum([card.discount for card in self()], gems.ZERO)

    @property
    @cache
    def score(self):
        return sum(card.points for card in self())


ALL = Cardset(CARDS)
NONE = Cardset([])


if __name__ == '__main__':
    for card in CARDS:
        print(card)
