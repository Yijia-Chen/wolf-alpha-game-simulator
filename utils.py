from datetime import datetime
import logging


#################### CONSTANTS ####################

# Meta
SECONDS_IN_DAY = 24 * 60 * 60

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


#################### TEMPLATES ####################
class Pack:
    def __init__(self, id: int) -> None:
        self.id = id
        self.action_types: list[bool] = []   # True - attack; False - fortify
        self.target_ids: list[int] = []
        self.used_at: list[datetime] = []
        self.fortification: int = 0
        self.points: float = 0.0
        logging.info('pack %d: initialized' % self.id)

    def gain_action(self, actionId) -> None:
        if len(self.actionIds) > len(self.target_ids):
            logging.warning('pack %d: cannot hoard action' % self.id)
            return
        self.actionIds.append(actionId)
        logging.info('pack %d: gain action successful' % self.id)

    def targeted(self) -> None:
        percent_reduced = FRACTION_POINTS_REDUCED_BY_ATTACK * 100
        # check if need to lose points
        if self.fortification >= percent_reduced:
            self.fortification -= percent_reduced
            logging.info('pack %d: lost %d fortification' %
                         (self.id, percent_reduced))
            return

        # need to lose points
        update_points(self.id)
        if self.fortification:
            temp = self.fortification
            percent_reduced -= temp
            self.fortification = 0
            self.points *= (1 - percent_reduced / 100)
            logging.info('pack %d: lost %d fortification and %d\% points' %
                         (self.id, temp, percent_reduced))
        else:
            self.points *= (1 - percent_reduced / 100)
            logging.info('pack %d: lost %d\% points' %
                         (self.id, percent_reduced))

    def attack(self, targetId: int) -> None:
        if not self.action_types.pop():
            logging.error('pack %d: wrong type of action' % self.id)
            return
        self.target_ids.append(targetId)
        self.used_at.append(datetime.now())
        logging.info('pack %d: attacked pack %d' % (self.id, targetId))

    def fortify(self) -> None:
        if self.action_types.pop():
            logging.error('pack %d: wrong type of action' % self.id)
            return
        self.fortification += 1
        logging.info('pack %d: fortified' % self.id)


class Player:
    def __init__(self, id: int, is_wolf: bool, level: int) -> None:
        if level not in POINTS_EARNED_DAILY_BY_LEVEL:
            logging.error('player %d: incorrect level at initialization' % id)

        self.id = id
        self.is_wolf = is_wolf
        self.level = level
        self.pack_ids: list[int] = []
        self.joined_at: list[datetime] = []
        self.points: float = 0.0
        logging.info('player %d: initialized' % self.id)

    def join(self, packId) -> None:
        if self.pack_ids[-1] == packId:
            return

        update_points()
        self.points = 0  # clear points as cost for joining a new pack
        self.pack_ids.append(packId)
        self.joined_at.append(datetime.now())
        logging.info('player %d: joined pack %d' % (self.id, packId))


#################### VARIABLES ####################
wool_price_usd = 0.26
timespan_in_days = 10
all_players: 'dict[int, Player]' = {
    # index -> player, such as the following
    -1: Player(id=-1, is_wolf=True, level=5)
}
all_packs: 'dict[int, Pack]' = {
    # index -> pack, such as the following
    -1: Pack(-1)
}


#################### FUNCTIONS ####################
def get_days_to_earn_action(wool_staked: float, pack_daily_points_rate: float) -> float:
    return wool_staked / (pack_daily_points_rate * 250)


def get_elapsed_days(timestamp: datetime) -> float:
    return (datetime.now() - timestamp).total_seconds() / SECONDS_IN_DAY


def attack(attackerId, targetId) -> None:
    all_packs[attackerId].attack(targetId)
    all_packs[targetId].targeted()


def update_points() -> None:
    """
    Update points for all players since they last rejoined.
    """
    for _, player in all_players.items():
        pack = all_packs[player.pack_ids[-1]]
        timespan_in_days = get_elapsed_days(player.joined_at[-1])
        points_earned = POINTS_EARNED_DAILY_BY_LEVEL[player.level] * \
            timespan_in_days
        player.points += points_earned
        pack.points += points_earned
