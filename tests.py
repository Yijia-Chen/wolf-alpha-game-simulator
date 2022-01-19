import unittest
from utility import *
import time
# from simpy import Environment


class TestEntities(unittest.TestCase):
    def test_time(self):
        elapsed_days_expected = 5 / SECONDS_IN_DAY

        timestamp = datetime.now()
        time.sleep(5)
        elapsed_days_actual = get_elapsed_days(timestamp)

        self.assertAlmostEqual(elapsed_days_expected, elapsed_days_actual)


unittest.main()
