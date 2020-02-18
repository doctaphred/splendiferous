from collections import namedtuple


colors = tuple('wbgrk')


class Gemset(namedtuple('Gemset', colors)):
    __slots__ = ()

    def __new__(cls, w=0, b=0, g=0, r=0, k=0):
        return super().__new__(cls, w, b, g, r, k)

    def __init__(self, *args, **kwargs):
        assert all(isinstance(c, int) for c in self), self

    def __neg__(self):
        return type(self)(*map(int.__neg__, self))

    def __add__(self, other):
        return type(self)(*map(int.__add__, self, other))

    def __sub__(self, other):
        return type(self)(*map(int.__sub__, self, other))

    def __mul__(self, other):
        assert isinstance(other, int)
        return type(self)(*map(other.__mul__, self))

    def __le__(self, other):
        return all(map(int.__le__, self, other))

    def __ge__(self, other):
        return all(map(int.__ge__, self, other))

    def __lt__(self, other):
        return self <= other and self != other

    def __gt__(self, other):
        return self >= other and self != other

    def __abs__(self):
        return type(self)(*(max(0, v) for v in self))

    @classmethod
    def empty(cls):
        return cls(0, 0, 0, 0, 0)

    @classmethod
    def sum(cls, objs):
        return sum(objs, cls.empty())


class Card(namedtuple('Card', ['color', 'points', 'cost'])):
    __slots__ = ()

    def __new__(cls, color, points=0, cost=Gemset.empty()):
        return super().__new__(cls, color, points, cost)

    def __init__(self, *args, **kwargs):
        assert self.color in colors, self.color
        assert isinstance(self.points, int), self.points
        assert isinstance(self.cost, Gemset), self.cost

    def benefit(self):
        # TODO: This is gross.
        # Consider storing Card.benefit instead of Card.color.
        return Gemset(**{self.color: 1})


class Noble(namedtuple('Noble', ['points', 'criteria'])):
    __slots__ = ()

    def satisfied(self, cards):
        return self.criteria <= Gemset.sum(card.benefit() for card in cards)


class Player:

    def __init__(self, gems, cards, nobles):
        # TODO: Wildcards, hand.
        self.gems = gems
        self.cards = cards
        self.nobles = nobles

    def score(self):
        return (
            sum(card.points for card in self.cards)
            + sum(noble.points for noble in self.nobles)
        )

    def discounts(self):
        return Gemset.sum(card.benefit() for card in self.cards)

    def power(self):
        return self.discounts() + self.gems

    def cost(self, card):
        return abs(card.cost - self.discounts())

    def can_buy(self, card):
        return card.cost <= self.power()

    def buy(self, card):
        assert self.can_buy(card)
        cost = self.cost(card)
        assert cost <= card.cost
        self.cards.append(card)
        self.gems -= cost
