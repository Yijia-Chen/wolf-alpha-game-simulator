from utility import *
from base_strategy import Strategy
import random


class PlayerStrategy(Strategy):
    """
    Strategy for any player who is not an alpha wolf.

    Involves:
    - Whether to stake/unstake at any given time. (requires ownership distribution, ngmi for now)
    - Whether to join another pack at any given time.
    """

    def __init__(self, level: int, pack_id: int) -> None:
        super().__init__()
        self.level = level
        self.pack_id = pack_id

    def daily_whether_to_join_and_which(self, ranked_pack_ids: 'list[int]') -> int:
        """
        Whether to join another pack, and if so which pack.

        FIXME Whether this is a daily or more frequent decision is TBD. For now, it's daily.

        Returns id of pack to join, or -1 if staying in current pack.
        """

        # low probability of switching for no reason, partly to test equilibrilizing effect
        switch_for_no_reason = random.choices([1, 0], [0.01, 0.99])
        if switch_for_no_reason:
            new_pack_id = random.choice(ranked_pack_ids)
            return new_pack_id if new_pack_id != self.pack_id else -1

        # examine cost of leaving current pack
        rank_current_pack = ranked_pack_ids.index(self.pack_id)
        individual_expected_reward = REWARD_BY_PLACE[rank_current_pack] * (
            POINTS_EARNED_DAILY_BY_LEVEL[self.level] /
            all_packs[self.pack_id].daily_point_rate
        ) / 2  # div by 2 because reward depends 50-50 on WOOL and points
        # probability_join_another = ?
        if individual_expected_reward > TOTAL_WINNING_POOL / get_total_active_players() / 10:
            return -1

        # calculate per player efficiency of every pack and join pack with highest worth
        max_efficiency, id_max_efficiency = -1, 0
        for rank, pack_id in enumerate(ranked_pack_ids):
            if pack_id == self.pack_id:
                continue

            efficiency = REWARD_BY_PLACE[rank] / \
                all_packs[pack_id].daily_point_rate
            if efficiency > max_efficiency:
                max_efficiency = efficiency
                id_max_efficiency = pack_id

        return id_max_efficiency
