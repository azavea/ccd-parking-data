from curblr.utils import time_to_hm


class ParkingTime(object):
    def __init__(self, hour, minute=0):
        self.hour = hour
        self.minute = minute
        self.invalid = False
        self._check_invalid()

    @staticmethod
    def from_datetime(date_time):
        return ParkingTime(date_time.hour, date_time.minute)

    def set_time(self, hour, minute=0):
        self.hour = hour
        self.minute = minute
        self._check_invalid()

    def _check_invalid(self):
        if None in [self.hour, self.minute]:
            self.invalid = True

        if self.invalid:
            self.hour = None
            self.minute = None
        else:
            if self.minute > 60:
                self.minute = None
                self.hour = None

            if self.minute == 60:
                self.minute = 0
                self.hour += 1

            if self.hour > 24:
                self.hour = None
                self.minute = None
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


class SchoolTime(ParkingTime):
    def __init__(self):
        super().__init__(None)


def rule_parking_time(time):
    if time == 9911:
        return AllTime()
    if time == 9910:
        return SchoolTime()
    else:
        h, m = time_to_hm(time)
        return ParkingTime(h, m)
