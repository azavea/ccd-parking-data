from ccd.parking_time import AllTime, ParkingTime, SchoolTime
from ccd.parking_time_range import RuleParkingTimeRange, get_rpts
from ccd.utils import day_range, time_to_hm, validate_dow


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
        self.ptr_primary = self._get_time_ranges(row, 1)
        self.ptr_secondary = self._get_time_ranges(row, 2)

    def _get_time_ranges(self, row, i):
        timestart = self.rule_parking_time(row['Time_From_{}'.format(i)])
        timeend = self.rule_parking_time(row['Time_To_{}'.format(i)])
        days = day_range(row['Day_From_{}'.format(i)],
                         row['Day_To_{}'.format(i)])
        return get_rpts(timestart, timeend, days)

    @staticmethod
    def rule_parking_time(time):
        if time == 9911:
            return AllTime()
        if time == 9910:
            return SchoolTime()
        else:
            h, m = time_to_hm(time)
            return ParkingTime(h, m)
