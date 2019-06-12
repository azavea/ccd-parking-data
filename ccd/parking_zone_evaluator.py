from parking_hour import ParkingHour

class ParkingZoneEvaluator(object):
    def __init__(self, shapes, rules, images):
        self.shapes = shapes
        self.rules = rules
        self.images = images
    
    def generate_base_shape_json(self, uuid):
        shape_chars = self.shapes[self.shapes['GlobalID'] == uuid].iloc[0].to_dict()
#         rules = self.rules[self.rules['GUID'] == uuid].to_dict()
#         images = self.images[self.images['REL_GLOBALID'] == uuid].to_dict()
        
        parking_hours = []
        dow = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        for d in dow:
            for h in range(24):
                parking_hours.append(ParkingHour(shape_chars, d, h))
        
        return parking_hours