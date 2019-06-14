from ccd.parking_time import ParkingTimeRange, rule_parking_time
from ccd.utils import time_to_hm, validate_dow


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

        # Get parking time ranges
        self.row_to_ptrs(row)

    def row_to_ptrs(self, row):
        def _a(row, ft, i):
            d_key = 'Day_{}_{}'.format(ft, i)
            t_key = 'Time_{}_{}'.format(ft, 1)
            return rule_parking_time(row[d_key], row[t_key])

        rpts = {}
        for ft in ('From', 'To'):
            for i in (1, 2):
                rpts['{}_{}'.format(ft, i)] = _a(row, ft, i)

        self.ptr_1 = ParkingTimeRange(rpts['From_1'], rpts['To_1'])
        self.ptr_2 = ParkingTimeRange(rpts['From_2'], rpts['To_2'])
