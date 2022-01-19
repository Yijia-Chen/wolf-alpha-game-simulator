import threading


# Meta
SECONDS_IN_DAY = 24 * 60 * 60
LOCK = threading.Lock()
TRUE_INPUTS = ['t', 'T', 'true', 'True', 'y', 'Y', 'yes', 'Yes']

# Game settings
PACK_COUNT: int = 14
MAX_PLAYER_COUNT_BY_LEVEL: 'dict[int, int]' = {
    0: 12067,
    5: 891,
    6: 529,
    7: 308,
    8: PACK_COUNT
}

# Pack returns
TOTAL_WINNING_POOL = 500000000
FRACTION_WINNING_POOL_BY_PLACE = [
    0.2,
    0.1575,
    0.12,
    0.0975,
    0.0775,
    0.0625,
    0.0525,
    0.045,
    0.0375,
    0.035,
    0.0325,
    0.03,
    0.0275,
    0.025
]
REWARD_BY_PLACE = TOTAL_WINNING_POOL * FRACTION_WINNING_POOL_BY_PLACE

# Individual returns
FRACTION_WOOL_FOR_ALPHA = 0.05
MIN_WOOL_WIN = 10000
POINTS_EARNED_DAILY_BY_LEVEL = {
    0: 50,        # sheep
    5: 50**2,    # omega wolf
    6: 60**2,    # delta wolf
    7: 70**2,    # beta wolf
    8: 0         # alpha wolf
}

# Actions
FRACTION_POINTS_REDUCED_BY_ATTACK = 0.03
