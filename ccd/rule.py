from ccd.parking_time import (AllTime, ParkingTime, ParkingTimeRange,
                              rule_parking_time)
from ccd.utils import time_to_hm, validate_dow, day_range


class Rule(object):
    def __init__(self, row: dict):
        """
        Intantiate using a row of the regulations dataframe
        as a dict
        """
        self.id = row['GUID']
        self.regulation = row['Regulation']
        self.regcat = row['RegCat']
        self.notes = row['Notes']
        self.time_limit = row['Time_Limit']

    def _get_time_range(self, row, i):
        timestart = self.rule_parking_time(row['Time_From_{}'.format(i)])
        timeend = self.rule_parking_time(row['Time_To_{}'.format(i)])
        if isinstance(timestart, AllTime) or isinstance(timeend, AllTime):
            # figure out what to return here
            pass
        
        days = day_range(row['Day_From_{}'.format(i)], row['Day_From_{}'.format(i)])
        


    @staticmethod
    def rule_parking_time(time):
        if time == 9911:
            return AllTime()
        else:
            h, m = time_to_hm(time)
            return ParkingTime(h, m)

        # Get parking time ranges
    #     self.row_to_ptrs(row)

    # def row_to_ptrs(self, row):
    #     def _a(row, ft, i):
    #         d_key = 'Day_{}_{}'.format(ft, i)
    #         t_key = 'Time_{}_{}'.format(ft, 1)
    #         return rule_parking_time(row[d_key], row[t_key])

    #     rpts = {}
    #     for ft in ('From', 'To'):
    #         for i in (1, 2):
    #             rpts['{}_{}'.format(ft, i)] = _a(row, ft, i)

    #     self.ptr_1 = ParkingTimeRange(rpts['From_1'], rpts['To_1'])
    #     self.ptr_2 = ParkingTimeRange(rpts['From_2'], rpts['To_2'])
