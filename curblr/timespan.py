from curblr import CurbLRObject


class TimeSpan(CurbLRObject):

    fields = ['effective_dates', 'days_of_week',
              'days_of_month', 'times_of_day', 'designated_periods']

    def __init__(self,
                 effective_dates=None,
                 days_of_week=None,
                 days_of_month=None,
                 times_of_day=None,
                 designated_periods=None):
        self.effective_dates = effective_dates
        self.days_of_week = days_of_week
        self.days_of_month = days_of_month
        self.times_of_day = times_of_day
        self.designated_periods = designated_periods

    def add_time_of_day(self, time_of_day):
        if not self.times_of_day:
            self.times_of_day = []
        for tod in self.times_of_day:
            if tod.is_equal(time_of_day):
                return
        self.times_of_day.append(time_of_day)

    def to_dict(self):
        d = super().to_dict(TimeSpan)
        if d == {}:
            return None
        return d

    def is_empty(self):
        if not self.to_dict():
            return True
        return False
