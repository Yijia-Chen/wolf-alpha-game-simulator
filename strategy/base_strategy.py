"""
This file defines, for a given player, what its strategies may look like. Choosing a strategy is a function of 
- Number of other players: affects player count (word of mouth)
- WOOL price: affects stake/unstake
- Wolf/sheep price: affects player count
- Relative strength changes between pools: affects actions and join
- ... and other variables

There are two types of strategies, one for leaders (alpha wolves) and one for followers.

To make simulation simpler, we assume that everyone makes rational decisions.
"""


class Strategy:
    """
    The most general abstraction for a strategy.
    """

    def __init__(self) -> None:
        pass
