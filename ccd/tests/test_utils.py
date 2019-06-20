import os
import unittest

import numpy as np

from ccd.utils import (day_range, get_permit_zone, metering_to_paid,
                       shift_days, time_to_hm, validate_dow)


class TestDayRange(unittest.TestCase):
    def test_day_range(self):
        self.assertEqual(day_range('tu', 'wed'), ['tu', 'we'])
        self.assertEqual(day_range('tu', 'tu'), ['tu'])
        self.assertEqual(day_range('2', '3'), ['tu', 'we'])
        self.assertEqual(day_range('1', 'Wednesday'), ['mo', 'tu', 'we'])
        self.assertIsNone(day_range('N/A', 'n/a'))
        self.assertEqual(day_range('999', '7'), ['su'])
        self.assertEqual(day_range('5', 'monday'), ['fr', 'sa', 'su', 'mo'])


class TestGetPermitZone(unittest.TestCase):
    def test_get_permit_zone(self):
        chars = {'PermitZone1': np.nan, 'PermitZone2': np.nan}
        self.assertEqual(get_permit_zone(chars), '')
        chars['PermitZone1'] = 1
        self.assertEqual(get_permit_zone(chars), 1)
        chars['PermitZone2'] = 2
        self.assertEqual(get_permit_zone(chars), 1)
        chars['PermitZone1'] = np.nan
        self.assertEqual(get_permit_zone(chars), 2)
        chars['PermitZone1'] = None
        with self.assertRaises(TypeError):
            get_permit_zone(chars)
        chars = {'PermitZone1': 'a', 'PermitZone2': 'b'}
        with self.assertRaises(TypeError):
            get_permit_zone(chars)
        chars = {'PermitZone1': None, 'PermitZone2': 2}
        with self.assertRaises(TypeError):
            get_permit_zone(chars)
        chars = {'PermitZone1': 1, 'PermitZone2': 'b'}
        self.assertEqual(get_permit_zone(chars), 1)
        chars['PermitZone1'] = 1.5
        self.assertEqual(get_permit_zone(chars), 1.5)


class TestMeteringToPaid(unittest.TestCase):
    def test_metering_to_paid(self):
        vals = {'No Meters': 'No', 'Kiosk': 'Yes', 'Meters': 'Yes'}
        for k, v in vals.items():
            self.assertEqual(metering_to_paid(k), v)
            self.assertEqual(metering_to_paid(k.lower()), v)
        self.assertIsNone(metering_to_paid('Another value'))
        self.assertIsNone(metering_to_paid(None))


class TestShiftDays(unittest.TestCase):
    def test_shift_days(self):
        self.assertIsNone(shift_days(None))
        self.assertEqual(shift_days(['mo']), ['tu'])
        all_days = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']
        self.assertEqual(shift_days(all_days), all_days)
        self.assertEqual(shift_days(['su', 'sa']), all_days)
        self.assertEqual(shift_days(['sa', 'su', 'mo']), ['su', 'mo', 'tu'])
        self.assertEqual(shift_days(['mo', 'mo']), ['tu'])
        with self.assertRaises(Exception):
            shift_days([x.upper() for x in all_days])
            shift_days(['thursday'])
            shift_days(['mo', 'tue'])
            shift_days(['mo', None])
        with self.assertRaises(IndexError):
            shift_days([])


class TestTimeToHm(unittest.TestCase):
    def test_time_to_hm(self):
        self.assertEqual(time_to_hm(9911), 'all')
        self.assertEqual(time_to_hm(30), (0, 30))
        self.assertEqual(time_to_hm(1200), (12, 0))
        self.assertEqual(time_to_hm(0), (0, 0))
        self.assertEqual(time_to_hm(2400), (24, 0))
        self.assertEqual(time_to_hm(9910), (None, None))
        self.assertEqual(time_to_hm(2500), (None, None))
        self.assertEqual(time_to_hm(102), (1, 2))


class TestValidateDow(unittest.TestCase):
    def test_validate_dow(self):
        self.assertEqual(validate_dow('tu'), 'Tu')
        self.assertEqual(validate_dow('Tu'), 'Tu')
        self.assertEqual(validate_dow('2'), 'Tu')
        self.assertEqual(validate_dow(2), 'Tu')
        self.assertEqual(validate_dow('tuesday'), 'Tu')
        self.assertEqual(validate_dow('Tuesday'), 'Tu')
        self.assertIsNone(validate_dow('christmas'))
        self.assertIsNone(validate_dow(999))
        self.assertIsNone(validate_dow('999'))
        self.assertIsNone(validate_dow('N/A'))


if __name__ == '__main__':
    unittest.main()
