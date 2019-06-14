from datetime import datetime

import pandas as pd

from ccd.constants import dtd, regulations, non_regs
from ccd.parking_time import ParkingTime, ParkingTimeRange
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
    
    @property
    def df(self):
        return pd.DataFrame([self.data])

    def add_regulation(self, reg):
        reg_type = regulations[reg.regulation]['type']
        if reg.regulation not in non_regs:
            if reg_type == 'reg_is':
                if self.data.reg_is != '':
                    self.data.reg_is += '|'
                self.data.reg_is += reg.regulation
            elif reg_type == 'reg_is_not':
                if self.data.reg_is_not != '':
                    self.data.reg_is_not += '|'
                self.data.reg_is_not += reg.regulation
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
            # ovlp1 = self.ptr.check_overlap(reg.ptr_1)
            # ovlp2 = self.ptr.check_overlap(reg.ptr_2)

            # ovlp_vals = set(['within', 'overlap_right', 'overlap_left'])
            # chk_ovlp = set([ovlp1, ovlp2])
            # if len(ovlp_vals.intersection(chk_ovlp)) > 0:
            #     self.add_regulation(reg)

    # @staticmethod
    # def get_parking_hour_times(hour):
    #     start = ParkingTime(hour)
    #     end_hour = hour + 1
    #     dows = list(dtd.keys())
    #     if end_hour == 24:
    #         end_hour = 0
    #         dow_index = dows.index(end_day.lower())
    #         if dow_index == len(dows) - 1:
    #             end_day = dows[0]
    #         else:
    #             end_day = dows[dow_index + 1]
    #     end = ParkingTime(end_day, end_hour)

    #     return start, end

        # self.ptr = ParkingTimeRange(start, end, [self.day])


