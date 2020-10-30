import heapq


class MinQueue:
    """Minimum-first priority queue implemented using a heap.

    This implementation ensures stability: items with the same value are
    returned in the order they were added, and the values of the items
    themselves are never compared.

        >>> q = MinQueue()
        >>> q.push('lmao', 0)
        >>> q.push('ayy', -1)
        >>> while q:
        ...     print(q.pop())
        ayy
        lmao

    The queue may be destructively iterated over:

        >>> q.push('ayy', None)
        >>> q.push('lmao', None)
        >>> len(q), list(q)
        (2, ['ayy', 'lmao'])
        >>> len(q), list(q)
        (0, [])

    """

    def __init__(self):
        from itertools import count
        self._heap = []
        self._ids = count()

    def _wrap(self, item, value):
        # Entries are stored as tuples, which heapq compares when they
        # are pushed or popped. The value and a unique ID are stored as
        # the first two elements to make sure the item itself is never
        # included in any comparison.
        #
        # The heapq module implements a min-heap, so the IDs should
        # monotonically increase to ensure stability.
        return (value, next(self._ids), item)

    def push(self, item, value):
        heapq.heappush(self._heap, self._wrap(item, value))

    def pop(self):
        return heapq.heappop(self._heap)[-1]

    def pushpop(self, item, value):
        return heapq.heappushpop(self._heap, self._wrap(item, value))[-1]

    def replace(self, item, value):
        return heapq.heapreplace(self._heap, self._wrap(item, value))[-1]

    def peek(self):
        """
        >>> q = MinQueue()
        >>> q.peek()
        Traceback (most recent call last):
          ...
        IndexError: list index out of range
        >>> q.push(None, None)
        >>> q.peek()
        """
        return self._heap[0][-1]

    def __bool__(self):
        """
        >>> q = MinQueue()
        >>> bool(q)
        False
        >>> q.push(None, None)
        >>> bool(q)
        True
        >>> q.pop()
        >>> bool(q)
        False
        """
        return bool(self._heap)

    def __len__(self):
        """
        >>> q = MinQueue()
        >>> len(q)
        0
        >>> q.push(None, None)
        >>> len(q)
        1
        >>> q.pop()
        >>> len(q)
        0
        """
        return len(self._heap)

    def __contains__(self, item):
        """
        >>> q = MinQueue()
        >>> 'ayy' in q
        False
        >>> q.push('ayy', None)
        >>> 'ayy' in q
        True
        >>> 'ayy' in q
        True
        >>> q.pop()
        'ayy'
        >>> 'ayy' in q
        False
        """
        return any(entry[-1] == item for entry in self._heap)

    def __next__(self):
        try:
            return self.pop()
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return self
