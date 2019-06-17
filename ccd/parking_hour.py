from datetime import datetime

import pandas as pd

from ccd.constants import dtd, non_regs, regulations, time_limit_notes
from ccd.parking_time import ParkingTime
from ccd.parking_time_range import HourParkingTimeRange
from ccd.rule import Rule
from ccd.utils import (get_permit_zone, metering_to_paid, time_to_hm,
                       validate_dow)


class ParkingHour(object):
    def __init__(self, dow, hour, chars):
        self.start = ParkingTime(hour)
        self.end = ParkingTime(hour + 1)
        self.dow = dow
        self.hour = hour
        self.data = {
            'id': chars['GlobalID'],
            'length': chars['Length'],
            'block': chars['Block'],
            'street': chars['Street'],
            'day': self.dow,
            'hour': self.hour,
            'reg_is': '',
            'reg_is_not': '',
            'time_limit': None,
            'paid': metering_to_paid(chars['Metering']),
            'tow_zone': chars['TowZone'],
            'contractor_placard': '',
            'permit_zone': get_permit_zone(chars)
        }

        self.ptr = HourParkingTimeRange(self.start, self.end, self.dow)

    @property
    def df(self):
        return pd.DataFrame([self.data])

    def add_regulation(self, reg):
        reg_type = regulations[reg.regulation]['type']
        if reg.regulation not in non_regs:
            if reg_type == 'reg_is':
                if self.data['reg_is'] != '':
                    self.data['reg_is'] += '|'
                self.data['reg_is'] += reg.regulation
            elif reg_type == 'reg_is_not':
                if self.data['reg_is_not'] != '':
                    self.data['reg_is_not'] += '|'
                self.data['reg_is_not'] += reg.regulation
            else:
                raise Exception(
                    'reg_type must be one of "reg_is" or "reg_is_not", got "{}"'.format(reg_type))

        if reg.regulation == 'Contractor Placard Not Valid':
            self.data['contractor_placard'] = 'Not Valid'

        if reg.notes in time_limit_notes.keys():
            self.data['time_limit'] = time_limit_notes[reg.notes]

    def check_regulations(self, rules):
        """
        Given the information derived from the shape, and the 
        rules for this specific segment, update attributes of 
        this parking hour
        """
        for _, row in rules.iterrows():
            row = row.to_dict()
            reg = Rule(row)
            ovlp_vals = set(['within', 'overlap_right', 'overlap_left'])

            for r in reg.ptr_primary:
                ovlp1 = self.ptr.check_overlap(r)
                if ovlp1 in ovlp_vals:
                    self.add_regulation(reg)

            for r in reg.ptr_secondary:
                ovlp2 = self.ptr.check_overlap(r, secondary=True)
                if ovlp2 in ovlp_vals:
                    self.add_regulation(reg)
