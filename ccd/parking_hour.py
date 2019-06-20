from datetime import datetime

import numpy as np
import pandas as pd

from ccd.constants import (CONTRACTOR_PLACARD_DEFAULT, REG_IS_DEFAULT,
                           REG_IS_NOT_DEFAULT, REGULATIONS, TIME_LIMIT_DEFAULT,
                           NON_REGS, PAID_DEFAULT)
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
            'reg_is': REG_IS_DEFAULT,
            'reg_is_not': REG_IS_NOT_DEFAULT,
            'time_limit': TIME_LIMIT_DEFAULT,
            'paid': PAID_DEFAULT,
            'tow_zone': chars['TowZone'],
            'contractor_placard': CONTRACTOR_PLACARD_DEFAULT,
            'permit_zone': get_permit_zone(chars),
            'check_flag': ''
        }

        self.chars = chars
        self.ptr = HourParkingTimeRange(self.start, self.end, self.dow)

    @property
    def df(self):
        return pd.DataFrame([self.data])

    def add_regulation(self, reg):
        reg_type = REGULATIONS[reg.regulation]['type']
        if reg.regulation not in NON_REGS:
            if reg_type == 'reg_is':
                if self.data['reg_is'] == REG_IS_DEFAULT:
                    self.data['reg_is'] = ''
                if self.data['reg_is'] != '':
                    self.data['reg_is'] += '|'
                self.data['reg_is'] += reg.regulation
            elif reg_type == 'reg_is_not':
                if self.data['reg_is_not'] == REG_IS_NOT_DEFAULT:
                    self.data['reg_is_not'] = ''
                if self.data['reg_is_not'] != '':
                    self.data['reg_is_not'] += '|'
                self.data['reg_is_not'] += reg.regulation
            else:
                raise Exception(
                    'reg_type must be one of "reg_is" or "reg_is_not", got "{}"'.format(reg_type))
        
        if not np.isnan(reg.time_limit):
            if self.data['time_limit'] == TIME_LIMIT_DEFAULT:
                self.data['time_limit'] = ''
            if self.data['time_limit'] != '':
                self.data['time_limit'] += '|'
            self.data['time_limit'] += str(reg.time_limit)
        
        if reg.regulation == 'Time Limited Auto Parking':
            self.data['paid'] = metering_to_paid(self.chars['Metering'])

        if reg.regulation == 'Contractor Placard Not Valid':
            self.data['contractor_placard'] = 'Not Valid'


    def check_regulations(self, rules):
        """
        Given the information derived from the shape, and the 
        rules for this specific segment, update attributes of 
        this parking hour
        """
        for _, row in rules.iterrows():
            row = row.to_dict()
            reg = Rule(row)
            ovlp_vals = set(['within', 'overlap_right'])

            for r in reg.ptr_primary:
                ovlp1 = self.ptr.check_overlap(r)
                if ovlp1 in ovlp_vals:
                    self.add_regulation(reg)

            for r in reg.ptr_secondary:
                ovlp2 = self.ptr.check_overlap(r, secondary=True)
                if ovlp2 in ovlp_vals:
                    self.add_regulation(reg)
        
        if '|' in self.data['reg_is']:
            self.data['check_flag'] = 'check'
