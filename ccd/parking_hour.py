from utils import get_permit_zone, metering_to_paid


class ParkingHour(object):
    def __init__(self, chars, day, hour):
        self.id = chars['GlobalID']
        self.length = chars['Length']
        self.block = chars['Block']
        self.street = chars['Street']
        self.day = day
        self.hour = hour
        self.reg_is = None
        self.reg_is_not = None
        self.time_limit = None
        self.paid = metering_to_paid(chars['Metering'])
        self.tow_zone = chars['TowZone']
        self.placard = None
        self.permit_zone = get_permit_zone(chars)
        
    def check_regulations(self, rules):
        """
        Given the information derived from the shape, and the rules for this specific 
        segment, update attributes of this parking hour
        """
        pass
