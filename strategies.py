from utils import *

"""
This file defines, for a given player, what its strategies may look like. Choosing a strategy is a function of 
- Number of other players: affects player count (word of mouth)
- WOOL price: affects stake/unstake
- Wolf/sheep price: affects player count
- Relative strength changes between pools: affects actions and join

There are two types of strategies, one for leaders (alpha wolves) and one for followers.
"""


class Strategy:
    """
    The most general abstraction for a strategy.
    """

    def __init__(self) -> None:
        pass


class LeaderStrategy(Strategy):
    """
    Strategy for a leader (alpha wolf) of a pack.
    """

    def __init__(self) -> None:
        super().__init__()

    def select_action_type_and_target(
        ranked_packs: 'list[Pack]',
        expected_days_left: float
    ) -> tuple(bool, int):
        """
        Based on a list of inputs, namely
        - ranked_packs
        - expected_days_left
        """

        return True


# TODO expected points of pack at endgame
class PlayerStrategy(Strategy):
    """
    Strategy for any player who is not an alpha wolf.

    Involves:
    - Whether to stake/unstake at any given time. (requires ownership distribution)
    - Whether to join another pack at any given time.
    - Whether to join game. (for new players)
    """

    def __init__(self) -> None:
        super().__init__()


class GreedyStrategy(PlayerStrategy):
    def __init__(self) -> None:
        super().__init__()
