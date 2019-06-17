import os
import unittest

from ccd.constants import dtd
from ccd.utils import day_range


class TestDayRange(unittest.TestCase):
    def test_day_range(self):
        self.assertEqual(day_range('tu', 'wed'), ['tu', 'we'])
        self.assertEqual(day_range('tu', 'tu'), ['tu'])
        self.assertEqual(day_range('2', '3'), ['tu', 'we'])
        self.assertEqual(day_range('1', 'Wednesday'), ['mo', 'tu', 'we'])
        self.assertIsNone(day_range('N/A', 'n/a'))
        self.assertEqual(day_range('999', '7'), ['su'])
        self.assertEqual(day_range('5', 'monday'), ['fr', 'sa', 'su', 'mo'])


if __name__ == '__main__':
    unittest.main()
