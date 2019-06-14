from datetime import datetime

from ccd.constants import dtd
from ccd.utils import (get_permit_zone, metering_to_paid, time_to_hm,
                       validate_dow)


class ParkingTime(object):
    def __init__(self, dow, hour, minute=0):
        self.dow = dow
        if dow:
            self.day = dtd[dow.lower()]
        else:
            self.day = None
        self.hour = hour
        self.minute = minute

        self.invalid = False
        if None in [self.day, self.hour, self.minute]:
            self.invalid = True

    def to_dt_dict(self):
        if self.invalid:
            return None
        else:
            return {
                'year': 2019,
                'month': 6,
                'day': self.day,
                'hour': self.hour,
                'minute': self.minute
            }

class AllTime(ParkingTime):
    def __init__(self):
        super().__init__(None, None, None)

def rule_parking_time(day, time):
    if time == 9911:
        return AllTime()
    else:
        dow = validate_dow(day)
        h, m = time_to_hm(time)
        return ParkingTime(dow, h, m)

class ParkingTimeRange(object):
    def __init__(self, start: ParkingTime, end: ParkingTime, days: list):
        self.invalid = False
        self.all_time = False

        if start.day and not end.day:
            end.day = start.day

        if isinstance(start, AllTime) or isinstance(end, AllTime):
            self.all_time = True
            self.start = None
            self.end = None

        elif start.invalid or end.invalid:
            self.invalid = True
            self.start = None
            self.end = None
        else:
            if start.day > end.day:
                end.day += 7
            self.start = datetime(**start.to_dt_dict())
            self.end = datetime(**end.to_dt_dict())

    def check_overlap(self, ref_tr):
        """
        Check the relationship of this time range to another
        """
        if self.invalid or ref_tr.invalid:
            return None
        if self.all_time and ref_tr.all_time:
            return 'within'
        if self.all_time:
            return 'encompass'
        if ref_tr.all_time:
            return 'within'

        starts_after_start = self.start >= ref_tr.start
        ends_before_end = self.end <= ref_tr.end
        ends_before_start = self.end <= ref_tr.start
        starts_after_end = self.start >= ref_tr.end

        if starts_after_start and ends_before_end:
            return 'within'

        if ends_before_start or starts_after_end:
            return 'outside'

        if not starts_after_start and not ends_before_end:
            return 'encompass'

        if not starts_after_start and ends_before_end:
            return 'overlap_left'

        if starts_after_start and not ends_before_end:
            return 'overlap_right'

        raise Exception('None of the time relationships met.')

