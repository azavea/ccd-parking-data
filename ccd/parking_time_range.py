from datetime import datetime

from ccd.constants import DTD
from ccd.parking_time import AllTime, ParkingTime
from ccd.utils import shift_days


class ParkingTimeRange(object):
    """ 
    A day-agnostic time range
    """

    def __init__(self, start: ParkingTime, end: ParkingTime):
        self.invalid = False
        self.all_time = False

        if isinstance(start, AllTime) or isinstance(end, AllTime):
            self.all_time = True
            self.start = None
            self.end = None

        elif start.invalid or end.invalid:
            self.invalid = True
            self.start = None
            self.end = None

        else:
            next_day = False
            if end.hour < start.hour:
                next_day = True
            self.start = datetime(**start.to_dt_dict())
            self.end = datetime(**end.to_dt_dict(next_day=next_day))


class RuleParkingTimeRange(ParkingTimeRange):
    """
    A parking time range that repeats over several days
    """

    def __init__(self, start: ParkingTime, end: ParkingTime, days: list):
        super().__init__(start, end)
        self.days = days
        if not self.days:
            self.days = list(DTD.keys())


class HourParkingTimeRange(ParkingTimeRange):
    """
    A parking time rang that only applies to one day 
    """

    def __init__(self, start: ParkingTime, end: ParkingTime, day: str):
        super().__init__(start, end)
        self.day = day

    def check_overlap(self, rule_tr: RuleParkingTimeRange, secondary=False):
        """
        Check the relationship of this time range to another
        """

        if secondary:
            if rule_tr.all_time:
                return None

        if self.invalid or rule_tr.invalid:
            return None
        if self.all_time and rule_tr.all_time:
            return 'within'
        if self.all_time:
            return 'encompass'
        if rule_tr.all_time:
            return 'within'
        if self.day.lower() not in rule_tr.days:
            return 'outside'

        starts_after_start = self.start >= rule_tr.start
        ends_before_end = self.end <= rule_tr.end
        ends_before_start = self.end <= rule_tr.start
        starts_after_end = self.start >= rule_tr.end

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


def get_rpts(start: ParkingTime, end: ParkingTime, days: list):
    if start.hour is None or end.hour is None:
        return [RuleParkingTimeRange(start, end, days)]
    if start.hour <= end.hour:
        return [RuleParkingTimeRange(start, end, days)]
    if start.hour > end.hour:
        rpt1 = RuleParkingTimeRange(ParkingTime(
            start.hour), ParkingTime(24), days)
        rpt2 = RuleParkingTimeRange(ParkingTime(
            0), ParkingTime(end.hour), shift_days(days))

        return [rpt1, rpt2]
