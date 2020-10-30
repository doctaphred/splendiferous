from collections import Counter
from itertools import combinations

from .utils import cache


class Gemset(tuple):
    __slots__ = ()

    @cache
    def __add__(self, other):
        return type(self)(map(int.__add__, self, other))

    @cache
    def __sub__(self, other):
        return type(self)(map(int.__sub__, self, other))

    @cache
    def __mul__(self, other):
        assert isinstance(other, int)
        return type(self)(map(other.__mul__, self))

    @cache
    def __le__(self, other):
        return all(map(int.__le__, self, other))

    @cache
    def __ge__(self, other):
        return all(map(int.__ge__, self, other))

    @cache
    def __lt__(self, other):
        return self <= other and self != other

    @cache
    def __gt__(self, other):
        return self >= other and self != other

    @cache
    def __and__(self, other):
        return type(self)(map(min, self, other))

    @cache
    def less(self, other):
        return type(self)((max(0, v) for v in self - other))

    @cache
    def __bool__(self):
        return any(self)

    @classmethod
    def read(cls, colors):
        c = Counter(colors)
        return cls(c[color] for color in 'wbgrk')

    @classmethod
    def unit(cls, i):
        return cls(int(i == j) for j in range(5))


UNITS = tuple(Gemset.unit(i) for i in range(5))
ZERO = Gemset((0, 0, 0, 0, 0))
ALL = Gemset((7, 7, 7, 7, 7))
# ALL = sum(UNITS, ZERO) * 7


@cache
def takes(gemset):
    return double_takes(gemset) + single_takes(gemset)


# @cache
def double_takes(gemset):
    return tuple(_double_takes(gemset))


def _double_takes(gemset):
    for unit in UNITS:
        double = unit + unit
        if gemset & (double + double):
            yield double


# @cache
def singles(gemset):
    return tuple(filter(gemset.__and__, UNITS))


# @cache
def single_takes(gemset):
    return _single_takes(singles(gemset))


@cache
def _single_takes(singles):
    return tuple(__single_takes(singles))


def __single_takes(singles):
    for combo in combinations(singles, 3):
        yield sum(combo, ZERO)
    for combo in combinations(singles, 2):
        yield sum(combo, ZERO)
    for component in singles:
        yield component
