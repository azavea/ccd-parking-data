import re
from datetime import datetime, time

from curblr.constants import DAYS


def from_camelcase(s):
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', s).lower()


def parse_date(s):
    if len(s.split('-')) < 3:
        s = '{}-'.format(datetime.now().year) + s

    return datetime.strptime(s, '%Y-%m-%d')


def parse_day_of_month(s):
    days_of_month = [str(n) for n in list(range(1, 32))] + \
        ['last', 'odd', 'even']
    s = s.lower()
    if s in days_of_month:
        return s
    else:
        return None


def parse_day_of_week(day):
    day = day.lower()

    sd = {'m': 'mo', 't': 'tu', 'w': 'we',
          'r': 'th', 'f': 'fr', 's': 'sa', 'u': 'su'}
    if len(day) == 1:
        return sd.get(day)

    return day[0:2]


def parse_occurrence(ocurrence):
    d = {
        '1': '1st',
        '1st': '1st',
        'first': '1st',
        '2': '2nd',
        '2nd': '2nd',
        'second': '2nd',
        '3': '3rd',
        '3rd': '3rd',
        'third': '3rd',
        '4': '4th',
        '4th': '4th',
        'fourth': '4th',
        'last': 'last',
        'even': 'even',
        'odd': 'odd'
    }

    return d.get(str(ocurrence).lower())


def parse_time(s):
    if isinstance(s, time):
        return s

    if isinstance(s, datetime):
        return s.time()

    s = str(s)
    if s == '24':
        s = '23:59'
    if ':' not in s:
        if len(s) > 4:
            raise Exception(
                'Unknown time string format "{}" must be in format %H:%M'.format(s))
        elif len(s) == 4:
            s = s[0:2] + ':' + s[2:4]
        elif len(s) == 3:
            s = s[0:1] + ':' + s[1:3]
        else:
            s += ':00'

    return datetime.strptime(s, '%H:%M').time()


def shift_days(days):
    dows = DAYS

    if days is None:
        return days

    for d in days:
        if d not in dows:
            raise Exception('{} not a valid day of the week'.format(d))

    if len(days) == len(dows):
        return days
    si = dows.index(days[0].lower()) + 1
    ei = dows.index(days[-1].lower()) + 1

    if si == 7:
        si = 0
    if ei == 7:
        ei = 0

    if ei < si:
        return dows[si:] + dows[0:ei + 1]
    return dows[si:ei + 1]


def time_str():
    return datetime.now().strftime("%m-%d_%H-%M")


def time_to_hm(time):
    if time == 9911:
        return 'all'

    if time == 9910:
        return 'school'

    if time > 2400 or time < 0:
        return None, None

    if len(str(time)) < 3:
        return 0, time

    h = int(str(time)[:-2])
    m = int(str(time)[-2:])
    return h, m


def to_camelcase(s):
    if s == '':
        return s
    w = s.split('_')
    if len(w) == 1:
        return s.lower()
    return w[0].lower() + ''.join([x.capitalize() for x in w[1:]])
