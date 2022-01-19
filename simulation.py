from utility import *
from simpy import Environment
import uuid
import random
from strategy import *


def daily_update_user_count() -> int:
    """
    A daily condition whether to join game or not.

    Based purely on $WOOL price.

    Current formula: 2x price increase -> 1.5x player increase
    """
    update_wool_price()
    price_ratio = wool_price_usd / wool_price_usd_initial
    # TODO Implement logistic function w.r.t. price


def add_new_players(new_player_count: int) -> None:
    pass  # TODO


def initialize_game():
    # initialize alpha wolves and packs
    for _ in range(PACK_COUNT):
        alpha_wolf_id = str(uuid.uuid1())
        alpha_wolf = Player(
            id=alpha_wolf_id,
            is_wolf=True,
            level=8,
            initial_wood_staked=wool_staked_per_player)  # FIXME initial wool
        all_players[alpha_wolf_id] = alpha_wolf
        pack_id = str(uuid.uuid1())
        all_packs[pack_id] = Pack(
            id=pack_id,
            leader_id=alpha_wolf_id,
            leader_wool=alpha_wolf.wool_staked
        )

    # initialize other players
    for level, count in player_count_by_level.items():
        for _ in range(count):
            id = str(uuid.uuid1())
            all_players[id] = Player(
                id=id,
                is_wolf=(level > 0),
                level=level,
                initial_wood_staked=wool_staked_per_player
            )
            pack_id = random.choice(all_packs.keys)
            all_players[id].join(pack_id)  # FIXME better join mechanism


def start_simulation():
    env = Environment()

    initialize_game()
