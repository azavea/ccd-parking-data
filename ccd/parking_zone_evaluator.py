from ccd.parking_hour import ParkingHour


class ParkingZoneEvaluator(object):
    def __init__(self, shapes, rules, images):
        self.shapes = shapes
        self.rules = rules
        self.images = images

    def generate_base_shape_json(self, uuid):
        chars = self.shapes[self.shapes['GlobalID'] == uuid].iloc[0].to_dict()
        rules = self.rules[self.rules['GUID'] == uuid]

        parking_hours = []
        dow = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        for d in dow:
            for h in range(24):
                ph = ParkingHour(d, h, chars)
                ph.check_regulations(rules)
                parking_hours.append(ph.df)

        return parking_hours
