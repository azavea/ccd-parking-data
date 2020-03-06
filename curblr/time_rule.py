from abc import ABC, abstractmethod

from curblr.utils import (from_camelcase, parse_date, parse_day_of_month,
                          parse_day_of_week, parse_occurrence, parse_time)


class TimeRule(ABC):
    pass


class DaysOfWeek(TimeRule):
    def __init__(self, days, occurences_in_month=None):
        if isinstance(days, str):
            days = [days]
        self.days = [parse_day_of_week(day) for day in days]
        self.occurences_in_month = None
        if occurences_in_month:
            self.occurences_in_month = [
                parse_occurrence(o) for o in occurences_in_month]

    @staticmethod
    def from_dict(d):
        return DaysOfWeek(d['days'])

    def to_dict(self):
        return {'days': self.days}


class DaysOfMonth(TimeRule):
    def __init__(self, days):
        if isinstance(days, 'str'):
            days = [days]
        self.days = [parse_day_of_month(day) for day in days]

    @staticmethod
    def from_dict(d):
        return DaysOfMonth(d['days'])

    def to_dict(self):
        return {'days': self.days}


class DesignatedPeriod(TimeRule):
    def __init__(self, name, apply):
        self.name = name
        apply = apply.lower()
        self.apply = None
        if apply in ('except during', 'only during'):
            self.apply = apply

    @staticmethod
    def from_dict(d):
        return DesignatedPeriod(d['name'], d['apply'])

    def to_dict(self):
        d = {'name': self.name}
        if self.apply:
            d['apply'] = self.apply

        return d


class EffectiveDates(TimeRule):
    def __init__(self, date_from, date_to):
        self.date_from = parse_date(date_from)
        self.date_to = parse_date(date_to)
        self.year = False
        if len(date_from.split('-')) > 2 and len(date_to.split('-')) > 2:
            self.year = True

    @staticmethod
    def from_dict(d):
        return EffectiveDates(d['from'], d['to'])

    def to_dict(self):
        d = {
            'from': '{}-{}'.format(self.date_from.month, self.date_from.day),
            'to': '{}-{}'.format(self.date_to.month, self.date_to.day)
        }

        if self.year:
            d['from'] = '{}-'.format(self.date_from.year) + d['from']
            d['to'] = '{}-'.format(self.date_to.year) + d['to']

        return d


class TimeOfDay(TimeRule):
    def __init__(self, time_from, time_to):
        self.time_from = parse_time(time_from)
        self.time_to = parse_time(time_to)

    def is_equal(self, time_of_day):
        return self.to_dict() == time_of_day.to_dict()

    @staticmethod
    def from_dict(d):
        return TimeOfDay(d['from'], d['to'])

    def to_dict(self):
        st_h = str(self.time_from.hour).zfill(2)
        st_m = str(self.time_from.minute).zfill(2)
        en_h = str(self.time_to.hour).zfill(2)
        en_m = str(self.time_to.minute).zfill(2)
        return {'from': '{}:{}'.format(st_h, st_m), 'to': '{}:{}'.format(en_h, en_m)}
