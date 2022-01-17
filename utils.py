from datetime import datetime
import logging
import random
import threading


#################### CONSTANTS ####################

# Meta
SECONDS_IN_DAY = 24 * 60 * 60
LOCK = threading.Lock()
TRUE_INPUTS = ['t', 'T', 'true', 'True', 'y', 'Y', 'yes', 'Yes']

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
    def __init__(self, id: int, leader_id: int, leader_wool: float) -> None:
        LOCK.acquire()

        # base info
        self.id = id
        self.leader_id = leader_id  # id of the alpha wolf
        self.player_ids: set[int] = {leader_id}

        # actions
        self.action_types: list[bool] = []   # True - attack, False - fortify
        self.target_ids: list[int] = []
        self.used_at: list[datetime] = []
        self.fortification: int = 0

        # points
        self.points: float = 0.0
        self.point_contributions: dict[int, float] = {}

        # wool and action progress
        self.wool: float = leader_wool
        self.next_action_progress: float = 0
        self.progress_updated_at: datetime = datetime.now()
        # self.wool_contributions: dict[int, float] = {}

        logging.info('pack %d: initialized' % self.id)
        LOCK.release()

    def gain_action(self, is_attack: bool) -> None:
        LOCK.acquire()

        if len(self.action_types) > len(self.target_ids):
            logging.warning('pack %d: cannot hoard action' % self.id)
        else:
            self.action_types.append(is_attack)
            logging.info('pack %d: gain action successful' % self.id)

        LOCK.release()

    def targeted(self) -> None:
        LOCK.acquire()

        percent_reduced = FRACTION_POINTS_REDUCED_BY_ATTACK * 100
        # check if need to lose points
        if self.fortification >= percent_reduced:
            self.fortification -= percent_reduced
            logging.info('pack %d: lost %d fortification' %
                         (self.id, percent_reduced))
            LOCK.release()
            return

        # need to lose points
        update_points(self.id)  # update all gains so far
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

        LOCK.release()

    def attack(self, targetId: int) -> None:
        LOCK.acquire()

        if not self.action_types.pop():
            logging.error('pack %d: wrong type of action' % self.id)

        self.target_ids.append(targetId)
        self.used_at.append(datetime.now())
        logging.info('pack %d: attacked pack %d' % (self.id, targetId))

        LOCK.release()

    def fortify(self) -> None:
        LOCK.acquire()

        if self.action_types.pop():
            logging.error('pack %d: wrong type of action' % self.id)

        self.fortification += 1
        logging.info('pack %d: fortified' % self.id)

        LOCK.release()

    def update_next_action_progress(self) -> None:
        # assume that wool is stable for period since last update
        LOCK.acquire()

        timespan_in_days = get_elapsed_days(self.progress_updated_at)
        self.next_action_progress += timespan_in_days / self.days_to_earn_action
        if self.next_action_progress >= 1:
            is_attack = input(
                'pack %d: would you like an attack or fortify action?')
            self.gain_action(is_attack=(is_attack in TRUE_INPUTS))
            self.next_action_progress -= 1
            logging.info('pack %d: gained an action' % self.id)

            if self.next_action_progress >= 1:
                logging.error('meta: action progress updated too infrequently')

        self.progress_updated_at = datetime.now()

        LOCK.release()

    @property
    def days_to_earn_action(self) -> float:
        return self.wool / (self.daily_point_rate * 250)

    @property
    def daily_point_rate(self) -> float:
        daily_point_rate: float = 0.0
        for p in self.player_ids:
            daily_point_rate += POINTS_EARNED_DAILY_BY_LEVEL[all_players[p].level]
        return daily_point_rate


class Player:
    def __init__(self, id: int, is_wolf: bool, level: int, initial_wood_staked: float) -> None:
        if level not in POINTS_EARNED_DAILY_BY_LEVEL:
            logging.error('player %d: incorrect level at initialization' % id)

        self.id = id
        self.is_wolf = is_wolf
        self.level = level
        self.pack_ids: list[int] = []
        self.joined_at: list[datetime] = []
        self.points: float = 0.0
        self.wool_staked = initial_wood_staked
        self.wool_changes: list[float] = []
        logging.info('player %d: initialized' % self.id)

    def stake(self, amount: float) -> None:
        LOCK.acquire()

        self.wool_staked += amount
        all_packs[self.pack_ids[-1]].wool += amount
        self.wool_changes.append(amount)
        logging.info('player %d: staked %d wool' % (self.id, amount))
        # TODO update action progress here

        LOCK.release()

    def unstake(self, amount: float) -> None:
        LOCK.acquire()

        if amount > self.wool_staked:
            logging.error(
                'player %d: cannot unstake more than staked' % self.id)

        self.wool_staked -= amount
        all_packs[self.pack_ids[-1]].wool -= amount
        self.wool_changes.append(-amount)
        logging.info('player %d: unstaked %d wool' % (self.id, amount))
        # TODO update action progress here

        LOCK.release()

    def join(self, pack_id: int) -> None:
        LOCK.acquire()

        if self.pack_ids and self.pack_ids[-1] == pack_id:
            return

        update_points()
        self.points = 0  # clear points as cost for joining a new pack

        # update players for current and new pack
        if self.pack_ids:
            curr_pack_id = self.pack_ids[-1]
            all_packs[curr_pack_id].player_ids.remove(self.id)
        all_packs[pack_id].player_ids.add(self.id)

        self.pack_ids.append(pack_id)
        self.joined_at.append(datetime.now())
        logging.info('player %d: joined pack %d' % (self.id, pack_id))

        LOCK.release()


#################### VARIABLES ####################
# In-game
all_players: 'dict[int, Player]' = {
    # id -> player
}
all_packs: 'dict[int, Pack]' = {
    # id -> pack
}

# Meta
wool_price_usd: float = 0.26
timespan_in_days: float = 10.0
pack_count: int = 25
player_count: int = 2000  # FIXME


#################### FUNCTIONS ####################
def get_elapsed_days(timestamp: datetime) -> float:
    return (datetime.now() - timestamp).total_seconds() / SECONDS_IN_DAY


def attack(attackerId, targetId) -> None:
    all_packs[attackerId].attack(targetId)
    all_packs[targetId].targeted()


def update_points() -> None:
    """
    Update points for all players since they last rejoined.
    """
    for playerId, player in all_players.items():
        pack = all_packs[player.pack_ids[-1]]
        timespan_in_days = get_elapsed_days(player.joined_at[-1])
        points_earned = POINTS_EARNED_DAILY_BY_LEVEL[player.level] * \
            timespan_in_days
        player.points += points_earned
        pack.points += points_earned
        if playerId not in pack.point_contributions:
            pack.point_contributions[playerId] = points_earned
        else:
            pack.point_contributions[playerId] += points_earned
    logging.info('meta: points updated')


def update_all() -> None:
    update_points()
    for _, pack in all_packs.items():
        pack.update_next_action_progress()
