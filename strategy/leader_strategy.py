from utility import *
from base_strategy import Strategy


class LeaderStrategy(Strategy):
    """
    Strategy for a leader (alpha wolf) of a pack.
    """

    def __init__(self, pack_id: int) -> None:
        super().__init__()
        self.pack = all_packs[pack_id]

    def select_action_type_and_target(
        self,
        ranked_pack_ids: 'list[int]',
    ) -> tuple(bool, int):
        """
        At the time of getting an action, decide whether to get an attack or fortify 
        action, and if attack, which pack to target, based on the following inputs:
        - ranked_packs
        - expected_days_left

        Some things that matter:
        - Rank of pack
        - Reward per staked wool of pack (not worth if too many players in 1st place)

        Attack only makes sense for bumping oneself up.
        Fortify makes sense for protecting one's place.
        - Very small packs (far from top 14) first fortify, then attack.
        - Medium packs (close but not top 14) first fortify, then attack.
        - Large packs (top 14 but not top) balance fortify and attack based on ranks.
        - King packs (top) only fortify, but also attack to solidify place.

        Some scenarios:
        1. There are 20 packs, and we're at 5th place. We still don't know when the 
           game's gonna end.
        2. There are 50 packs, and we're at 1st place. We probably fortify, unless 
           second place is not fortified and close to our score.

        Returns a boolean indicating whether action is attack, and if so, the pack_id
        to target. Second variable returns -1 for fortify.
        """

        return False, -1


# TODO expected points of pack at endgame


class DefensiveStrategy(LeaderStrategy):
    """
    Only fortifies. Never attacks.
    """

    def __init__(self, pack_id: int) -> None:
        super().__init__(pack_id)

    def select_action_type_and_target(ranked_pack_ids: 'list[int]') -> tuple(bool, int):
        return super().select_action_type_and_target(ranked_pack_ids)


class MildStrategy(LeaderStrategy):
    """
    Only attacks a pack if it bumps us ahead of our upper neighbor.
    """

    def __init__(self, pack_id: int) -> None:
        super().__init__(pack_id)

    def select_action_type_and_target(self, ranked_pack_ids: 'list[int]') -> tuple(bool, int):
        idx_current_pack = ranked_pack_ids.index(self.pack.id)

        # if first place, do not attack
        if idx_current_pack == 0:
            return False, -1

        id_pack_above = ranked_pack_ids[idx_current_pack-1]
        points_pack_above = all_packs[id_pack_above].points
        if points_pack_above / self.pack.points <= 1.03:
            return True, id_pack_above

        return super().select_action_type_and_target(ranked_pack_ids)


class AggressiveStrategy(LeaderStrategy):
    """
    Attacks the pack with the highest point efficiency.
    """

    def __init__(self, pack_id: int) -> None:
        super().__init__(pack_id)

    def select_action_type_and_target(self, ranked_pack_ids: 'list[int]') -> tuple(bool, int):
        # calculate efficiency for all packs
        max_efficiency, id_max_efficiency = -1, 0
        for rank, pack_id in enumerate(ranked_pack_ids):
            efficiency = (REWARD_BY_PLACE[rank] /
                          all_packs[pack_id].daily_point_rate)
            if efficiency > max_efficiency:
                max_efficiency = efficiency
                id_max_efficiency = pack_id

        if id_max_efficiency != self.pack.id:
            return True, id_max_efficiency

        return super().select_action_type_and_target(ranked_pack_ids)
