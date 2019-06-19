import unittest

from ccd.parking_time import AllTime, ParkingTime


class TestParkingTime(unittest.TestCase):
    def setUp(self):
        self.pt1 = ParkingTime(0)
        self.pt2 = ParkingTime(2, 30)
        self.pt3 = ParkingTime(25)
        self.pt4 = ParkingTime(22, 60)
        self.pt5 = ParkingTime(24, 60)
        self.pt6 = ParkingTime(24)

    def test_constructor(self):
        # pt1
        self.assertIsInstance(self.pt1, ParkingTime)
        self.assertEqual(self.pt1.hour, 0)
        self.assertEqual(self.pt1.minute, 0)
        self.assertFalse(self.pt1.invalid)
        # pt2
        self.assertIsInstance(self.pt2, ParkingTime)
        self.assertEqual(self.pt2.hour, 2)
        self.assertEqual(self.pt2.minute, 30)
        self.assertFalse(self.pt2.invalid)
        # pt3
        self.assertTrue(self.pt3.invalid)
        self.assertIsNone(self.pt3.hour)
        self.assertIsNone(self.pt3.minute)
        # pt4
        self.assertEqual(self.pt4.hour, 23)
        self.assertEqual(self.pt4.minute, 0)
        # pt5
        self.assertTrue(self.pt5.invalid)
        # pt6
        self.assertFalse(self.pt6.invalid)
        self.assertEqual(self.pt6.hour, 24)

    def test_to_dt_dict(self):
        def get_dict(hour, minute=0, day=1):
            return {
                'year': 2019,
                'month': 6,
                'day': day,
                'hour': hour,
                'minute': minute
            }
            
        self.assertEqual(self.pt1.to_dt_dict(), get_dict(0))
        self.assertEqual(self.pt2.to_dt_dict(), get_dict(2, 30))
        self.assertIsNone(self.pt3.to_dt_dict())
        self.assertEqual(self.pt4.to_dt_dict(), get_dict(23))
        self.assertIsNone(self.pt5.to_dt_dict())
        self.assertEqual(self.pt6.to_dt_dict(), get_dict(0, 0, 2))


class TestAllTime(unittest.TestCase):
    def setUp(self):
        self.at = AllTime()

    def test_constructor(self):
        self.assertIsInstance(self.at, AllTime)
        self.assertIsInstance(self.at, ParkingTime)
        self.assertTrue(self.at.invalid)
        self.assertIsNone(self.at.hour)
        self.assertIsNone(self.at.minute)

    def test_to_dt_dict(self):
        self.assertIsNone(self.at.to_dt_dict())


if __name__ == '__main__':
    unittest.main()
