
from ccd.constants import dtd
from ccd.utils import (get_permit_zone, metering_to_paid, time_to_hm,
                       validate_dow)


class ParkingTime(object):
    def __init__(self, hour, minute=0):
        self.hour = hour
        self.minute = minute

        self.invalid = False
        if None in [self.hour, self.minute]:
            self.invalid = True

    def to_dt_dict(self, next_day=False):
        if self.invalid:
            return None
        else:
            day = 1
            hour = self.hour
            if next_day:
                day += 1
            if hour == 24:
                hour = 0
                day += 1
            return {
                'year': 2019,
                'month': 6,
                'day': day,
                'hour': hour,
                'minute': self.minute
            }


class AllTime(ParkingTime):
    def __init__(self):
        super().__init__(None)
