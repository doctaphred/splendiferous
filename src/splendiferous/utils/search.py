from .priorityqueue import MinQueue


class AStar:

    def __init__(self, starts):
        self.precursors = {}
        self.costs = {}
        self.frontier = MinQueue()

        for state, cost in starts:
            self.enqueue(None, state, cost)
        self.state = self.frontier.pop()

    def enqueue(self, state, new_state, new_cost):
        self.precursors[new_state] = state
        self.costs[new_state] = new_cost
        estimated_cost = new_cost + self.heuristic(new_state)
        self.frontier.push(new_state, estimated_cost)

    def heuristic(self, state):
        return 0

    def transitions(self, state):
        for new_state in self.successors(state):
            yield 1, new_state

    def successors(self, state):
        raise NotImplementedError

    def __repr__(self):
        return "<{}: {} appraised, {} in frontier>".format(
            type(self).__name__,
            len(self.precursors),
            len(self.frontier),
        )

    def __iter__(self):
        return self

    def __next__(self):
        self.explore(self.state, self.costs[self.state])
        try:
            self.state = self.frontier.pop()
        except IndexError:
            raise StopIteration
        return self.state

    def explore(self, state, cost):
        for marginal_cost, new_state in self.transitions(state):
            new_cost = cost + marginal_cost
            if new_state not in self.costs or new_cost < self.costs[new_state]:
                self.enqueue(state, new_state, new_cost)

    class NotFound(LookupError):
        pass

    def search_until(self, stop):
        for state in self:
            if stop(state):
                return
        raise self.NotFound(stop)

    def search_for(self, goal):
        if goal not in self.precursors:
            self.search_until(goal.__eq__)

    def find_path(self, state):
        self.search_for(state)
        return self._path(state)

    def _path(self, state):
        path = list(self._trace(state))
        path.reverse()
        return path

    def _trace(self, state):
        while state is not None:
            yield state
            state = self.precursors[state]
