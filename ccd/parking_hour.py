from datetime import datetime

import numpy as np
import pandas as pd

from ccd.constants import (CHECK_FLAG_DEFAULT, CONTRACTOR_PLACARD_DEFAULT,
                           PAID_DEFAULT, REG_IS_DEFAULT, REG_IS_NOT_DEFAULT,
                           REGULATION_HIERARCHY, REGULATIONS,
                           SNOW_EMERGENCY_DEFAULT, TIME_LIMIT_DEFAULT)
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
            'snow_emergency_zone': SNOW_EMERGENCY_DEFAULT,
            'check': CHECK_FLAG_DEFAULT
        }

        self.chars = chars
        self.ptr = HourParkingTimeRange(self.start, self.end, self.dow)

    @property
    def df(self):
        return pd.DataFrame([self.data])

    def add_regulation(self, reg):
        reg_type = REGULATIONS[reg.regulation]['type']
        if reg_type == 'reg_is':
            # get the time limit
            time_limit = reg.time_limit
            if np.isnan(reg.time_limit):
                time_limit = TIME_LIMIT_DEFAULT
            # if there is no regulation yet, add one
            if self.data['reg_is'] == REG_IS_DEFAULT:
                self.data['reg_is'] = reg.regulation
                self.data['time_limit'] = time_limit
            # otherwise check the hierarchy
            else:
                for r in (self.data['reg_is'], reg.regulation):
                    if r not in REGULATION_HIERARCHY:
                        raise Exception('{} is not in regulation hierarchy'.format(r))
                if REGULATION_HIERARCHY.index(reg.regulation) < REGULATION_HIERARCHY.index(self.data['reg_is']):
                    self.data['reg_is'] = reg.regulation
                    self.data['time_limit'] = time_limit
                self.data['check'] = 'Yes'
        elif reg_type == 'reg_is_not':
            if self.data['reg_is_not'] == REG_IS_NOT_DEFAULT:
                self.data['reg_is_not'] = ''
            if self.data['reg_is_not'] != '':
                self.data['reg_is_not'] += '|'
            self.data['reg_is_not'] += reg.regulation
        elif reg_type == 'contractor_placard':
            self.data['contractor_placard'] = 'Not Valid'
        elif reg_type == 'snow_reg':
            self.data['snow_emergency_zone'] = 'Yes'
        else:
            raise Exception('Unfamiliar reg type: "{}"'.format(reg_type))    

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