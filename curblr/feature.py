from datetime import time

from shapely.geometry import LineString, shape

from curblr import CurbLRObject, Location
from curblr.constants import DAYS
from curblr.parking_time import ParkingTime
from curblr.parking_time_range import (HourParkingTimeRange, ParkingTimeRange,
                                       RuleParkingTimeRange)
from curblr.regulation import Regulation
from curblr.time_rule import DaysOfWeek, TimeOfDay
from curblr.timespan import TimeSpan


class Feature(CurbLRObject):

    fields = ['geometry', 'location', 'regulations', 'images']

    def __init__(self, geometry, location=None, regulations=None, images=None):
        self.type = 'Feature'
        if isinstance(geometry, dict):
            geometry = LineString(shape(geometry))
        self.geometry = geometry
        self.location = location
        self.regulations = regulations
        self.images = images

    def add_regulation(self, reg):
        if not self.regulations:
            self.regulations = []
        self.regulations.append(reg)

    def add_image(self, image):
        if not self.images:
            self.images = []
        self.images.append(image)

    def to_dict(self, keep_shapely=False):
        ld = None
        if self.location:
            ld = self.location.to_dict()

        d = {
            'type': self.type,
            'geometry': self.geometry,
            'properties': {
                'location': ld,
                'regulations': [r.to_dict() for r in self.regulations]
            }
        }

        if self.images:
            d['properties']['images'] = self.images

        if not keep_shapely:
            d['geometry'] = d['geometry'].__geo_interface__

        return d

    def add_location(self, location):
        self.location = Location

    def fill_unregulated_time(self, default_parking_rule):
        z = time(0, 0)
        m = time(23, 59)

        restricted = {d: [] for d in DAYS}
        available = {d: [] for d in DAYS}

        for r in self.regulations:
            if r.rule.activity.startswith('no') and r.user_classes and len(r.user_classes) > 0:
                continue
            
            if not r.time_spans:
                return
            else:
                for t in r.time_spans:
                    days = t.days_of_week.days if t.days_of_week else DAYS
                    if not t.times_of_day:
                        rpts = [RuleParkingTimeRange(ParkingTime.from_datetime(
                            z), ParkingTime.from_datetime(m), days)]
                    else:
                        rpts = RuleParkingTimeRange.from_time_span(t)

                    for rpt in rpts:
                        for day in days:
                            hpt = HourParkingTimeRange(ParkingTime.from_datetime(rpt.start),
                                                       ParkingTime.from_datetime(
                                                           rpt.end),
                                                       day)
                            restricted[day].append(hpt)

        if all([len(x) == 0 for x in restricted.values()]):
            timespans = None
        else:
            for k, v in restricted.items():
                if v == []:
                    available[k].append((z, m))
                else:
                    restricted_ranges = sorted(v, key=lambda x: x.start)

                    ranges = []
                    st = None
                    en = None

                    for rr in restricted_ranges:
                        s = rr.start.time()
                        e = rr.end.time()

                        if not st:
                            st = s
                        if not en:
                            en = e
                        if s > en:
                            ranges.append((st, en))
                            st = s
                            en = e
                            continue
                        if (s == st and e > en) or s == en:
                            en = e

                    st = st if st else z
                    en = en if en else m
                    ranges.append((st, en))

                    if ranges[0][0] != z:
                        available[k].append((z, ranges[0][0]))
                    if len(ranges) > 1:
                        available[k] += [(ranges[i-1][1], ranges[i][0])
                                        for i in range(1, len(ranges))]
                    if ranges[-1][1] != m:
                        available[k].append((ranges[-1][1], m))

            trs = {}
            for k, v in available.items():
                if v != []:
                    if str(v) in trs.keys():
                        trs[str(v)]['days'].append(k)
                    else:
                        trs[str(v)] = {'days': [k], 'time': v}

            timespans = []
            for _, v in trs.items():
                times = v['time']
                dow = DaysOfWeek(v['days']) if len(v['days']) < 7 else None
                if times == [(z, m)]:
                    tods = None
                else:
                    tods = [TimeOfDay(s, e) for s, e in times]
                timespans.append(TimeSpan(days_of_week=dow, times_of_day=tods))
        
        if timespans != []:
            self.regulations.append(Regulation(
                default_parking_rule, time_spans=timespans))

    @staticmethod
    def from_dict(d):
        location = Location.from_dict(d['properties']['location'])
        regulations = [Regulation.from_dict(r)
                       for r in d['properties']['regulations']]
        geometry = d['geometry']
        images = d.get('images')
        if isinstance(images, str):
            images = [images]
        return Feature(geometry, location, regulations, images)

    @staticmethod
    def from_lr_feature(feature, **kwargs):
        return Feature(feature['geometry'], Location.from_lr_feature(feature, **kwargs))
