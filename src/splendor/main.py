from collections import namedtuple


colors = tuple('wbgrk')


class Gemset(namedtuple('Gemset', colors)):
    __slots__ = ()

    def __new__(cls, w=0, b=0, g=0, r=0, k=0):
        return super().__new__(cls, w, b, g, r, k)

    def __init__(self, *args, **kwargs):
        assert all(isinstance(c, int) for c in self)

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
        return sum(self * self) ** 0.5

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
