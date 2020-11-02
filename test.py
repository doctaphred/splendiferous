from tqdm import tqdm

from splendiferous import cards
from splendiferous import gems
from splendiferous.state import State
from splendiferous.utils import print_cache_info
from splendiferous.utils.search import AStar


class Search(AStar):

    def successors(self, state):
        yield from state.successors()

    def heuristic(self, state):
        return 0
        return 1 - (state.player_cards.score / max_score)
        return (
            len(state.bank_cards)
            - (sum(state.player_cards.discounts) / combined_discounts)
            + 1
        )


start = State(
    bank_gems=gems.ALL,
    bank_cards=cards.ALL,
    player_gems=gems.ZERO,
    player_cards=cards.NONE,
)

discounts = [card.discount for card in start.bank_cards]
total_discounts = sum(discounts, start=gems.ZERO)
combined_discounts = sum(total_discounts)
max_score = sum(card.points for card in cards.ALL)

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
            # if len(state.bank_cards) == 0:
            if i == 100_000:
                break

    except KeyboardInterrupt:
        pass
    finally:
        info()


if __name__ == '__main__':
    main()
