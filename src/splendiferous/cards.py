from collections import namedtuple

from .gems import Gemset
from . import data


class Card(namedtuple('Card', ['level', 'points', 'discount', 'price'])):

    @classmethod
    def read(cls, line):
        level, points, color, price = line.strip().split()
        return cls(
            level=int(level),
            points=int(points),
            discount=Gemset.read(color),
            price=Gemset(*map(int, price)),
        )


CARDS = [Card.read(line) for line in data.cards.splitlines() if line]


if __name__ == '__main__':
    for card in CARDS:
        print(card)
