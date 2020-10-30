from functools import lru_cache


caches = {}


def cache(func):
    assert func not in caches
    cached = lru_cache(maxsize=None)(func)
    # cached = lru_cache(maxsize=0)(func)
    caches[func] = cached
    return cached


def print_cache_info(caches=caches):
    infos = sorted(CacheInfo.get(func) for func in caches.values())
    total_hits = total_misses = 0
    print('Cache results:')
    for info in infos:
        total_hits += info.hits
        total_misses += info.misses
        print(info)
    print("\nTotal:")
    print("{:>11,}: {:>11,} ✘, {:>11,} ✔ ({:6.4%})".format(
        total_hits + total_misses,
        total_misses,
        total_hits,
        total_hits / (total_hits + total_misses) if total_hits else 0
    ))


class CacheInfo:

    def __init__(self, func, hits, misses):
        self.func = func
        self.hits = hits
        self.misses = misses

        self.name = f"{self.func.__module__}::{self.func.__qualname__}"
        self.total = self.hits + self.misses
        self.fraction = self.hits / self.total if self.hits else 0

        self._value = self.hits, -self.misses, self.name

    def __lt__(self, other):
        return self._value < other._value

    @classmethod
    def get(cls, func):
        info = func.cache_info()
        return cls(func, info.hits, info.misses)

    def __repr__(self):
        return "{:>11,}: {:>11,} ✘, {:>11,} ✔ ({:6.2%}): {}".format(
            self.total,
            self.misses,
            self.hits,
            self.fraction,
            self.name,
        )
