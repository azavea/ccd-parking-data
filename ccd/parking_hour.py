from datetime import datetime

import pandas as pd

from ccd.constants import dtd, regulations, non_regs
from ccd.parking_time import ParkingTime, ParkingTimeRange
from ccd.rule import Rule
from ccd.utils import (get_permit_zone, metering_to_paid, time_to_hm,
                       validate_dow)


class ParkingHour(object):
    def __init__(self, chars, day, hour):
        self.id = chars['GlobalID']
        self.length = chars['Length']
        self.block = chars['Block']
        self.street = chars['Street']
        self.day = day
        self.hour = hour
        self.reg_is = ''
        self.reg_is_not = ''
        self.time_limit = None
        self.paid = metering_to_paid(chars['Metering'])
        self.tow_zone = chars['TowZone']
        self.contractor_placard = ''
        self.permit_zone = get_permit_zone(chars)
        self.get_parking_time_range()

    def add_regulation(self, reg):
        reg_type = regulations[reg.regulation]['type']
        if reg.regulation not in non_regs:
            if reg_type == 'reg_is':
                if self.reg_is != '':
                    self.reg_is += '|'
                self.reg_is += reg.regulation
            elif reg_type == 'reg_is_not':
                if self.reg_is_not != '':
                    self.reg_is_not += '|'
                self.reg_is_not += reg.regulation
            else:
                raise Exception(
                    'reg_type must be one of "reg_is" or "reg_is_not", got "{}"'.format(reg_type))
            
        if reg.regulation == 'Contractor Placard Not Valid':
            self.contractor_placard = 'Not Valid'

    def check_regulations(self, rules):
        """
        Given the information derived from the shape, and the 
        rules for this specific segment, update attributes of 
        this parking hour
        """
        for _, row in rules.iterrows():
            row = row.to_dict()
            reg = Rule(row)
            ovlp1 = self.ptr.check_overlap(reg.ptr_1)
            ovlp2 = self.ptr.check_overlap(reg.ptr_2)

            ovlp_vals = set(['within', 'overlap_right', 'overlap_left'])
            chk_ovlp = set([ovlp1, ovlp2])
            if len(ovlp_vals.intersection(chk_ovlp)) > 0:
                self.add_regulation(reg)

    def get_parking_time_range(self):
        start = ParkingTime(self.day, self.hour)
        end_day = self.day
        end_hour = self.hour + 1
        dows = list(dtd.keys())
        if end_hour == 24:
            end_hour = 0
            dow_index = dows.index(end_day.lower())
            if dow_index == len(dows) - 1:
                end_day = dows[0]
            else:
                end_day = dows[dow_index + 1]
        end = ParkingTime(end_day, end_hour)

        self.ptr = ParkingTimeRange(start, end, [self.day])

    @property
    def df(self):
        d = {
            'id': self.id,
            'length': self.length,
            'block': self.block,
            'street': self.street,
            'day': self.day,
            'hour': self.hour,
            'reg_is': self.reg_is,
            'reg_is_not': self.reg_is_not,
            'time_limit': self.time_limit,
            'paid': self.paid,
            'tow_zone': self.tow_zone,
            'contractor_placard': self.contractor_placard,
            'permit_zone': self.permit_zone
        }

        return pd.DataFrame([d])
