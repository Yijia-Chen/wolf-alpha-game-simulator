from utils import *
from simpy import Environment
import uuid


def initialize_game():
    for _ in range(pack_count):
        alpha_wolf_id = str(uuid.uuid1())
        alpha_wolf = Player(
            id=alpha_wolf_id,
            is_wolf=True,
            level=8,
            initial_wood_staked=2000)  # FIXME initial wool
        all_players[alpha_wolf_id] = alpha_wolf
        pack_id = str(uuid.uuid1())
        all_packs[pack_id] = Pack(
            id=pack_id,
            leader_id=alpha_wolf_id,
            leader_wool=alpha_wolf.wool_staked
        )

    for _ in range(player_count):
        # TODO correct distribution of player types
        id = str(uuid.uuid1())
        all_players[id] = Player(
            id=id,
            is_wolf=False,
            level=0,
            initial_wood_staked=50
        )


def start_simulation():
    env = Environment()

    initialize_game()
