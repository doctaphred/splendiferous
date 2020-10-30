from tqdm import tqdm

from splendiferous.utils.search import AStar
from splendiferous.utils import print_cache_info
from splendiferous.cards import CARDS
from splendiferous.state import State
from splendiferous import gems


class Search(AStar):

    def successors(self, state):
        yield from state.successors()

    def heuristic(self, state):
        return 0
        return 1 - (state.score / max_score)
        return (
            len(state.bank_cards)
            - (sum(state.discounts) / combined_discounts)
            + 1
        )


start = State(
    bank_gems=gems.ALL,
    bank_cards=frozenset(CARDS),
    player_gems=gems.ZERO,
    player_cards=frozenset(),
)

discounts = [card.discount for card in start.bank_cards]
total_discounts = sum(discounts, start=gems.ZERO)
combined_discounts = sum(total_discounts)
max_score = sum(card.points for card in CARDS)

num_cards = len(start.bank_cards)


def main():

    def info():
        print()
        print('---')
        print(state.pretty(cards=False))
        print()
        print_cache_info()
        print()
        print(search)
        print(f"{i:,} states searched")
        print("path length", len(search.find_path(state)))

    try:
        search = Search([(start, 0)])
        best = 0
        for i, state in enumerate(tqdm(search)):
            current = len(state.player_cards)
            if current > best or not i % 1000:
                if current > best:
                    best = current
                info()
            if len(state.bank_cards) == 0:
                break

    except KeyboardInterrupt:
        pass
    finally:
        info()


if __name__ == '__main__':
    for _ in range(2):
        main()
