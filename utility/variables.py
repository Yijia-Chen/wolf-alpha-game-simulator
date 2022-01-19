from utility.constants import *


wool_price_usd_initial: float = 0.26
wool_price_usd = wool_price_usd_initial
timespan_in_days: float = 10.0
fraction_playing_players_initial: float = 0.1
player_count_by_level = {
    0: MAX_PLAYER_COUNT_BY_LEVEL[0] * fraction_playing_players_initial,
    5: MAX_PLAYER_COUNT_BY_LEVEL[5] * fraction_playing_players_initial,
    6: MAX_PLAYER_COUNT_BY_LEVEL[6] * fraction_playing_players_initial,
    7: MAX_PLAYER_COUNT_BY_LEVEL[7] * fraction_playing_players_initial,
    8: PACK_COUNT
}
wool_supply_total: float = 76610840.0
fraction_wool_active: float = 0.1
wool_staked_per_player: float = wool_supply_total * \
    fraction_wool_active / sum(player_count_by_level.values())
