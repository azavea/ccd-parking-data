from curblr import Regulation, Location, CurbLRObject


class Segment(CurbLRObject):
    def __init__(self, geometry, location: Location=None):
        self.type = 'Feature'
        self.geometry = geometry
        self.location = location
        self.regulations = []
        self.images = []

    def add_regulation(self, reg: Regulation, image=None):
        self.regulations.append(reg)
        self.images.append(image)

    def to_dict(self):
        return {
            'type': self.type,
            'geometry': self.geometry,
            'properties': {
                'location': self.location.to_dict(),
                'regulations': [r.to_dict() for r in self.regulations],
                'images': self.images
            }
        }

    def add_location(self, location: Location):
        self.location = Location

    @staticmethod
    def from_lr_feature(feature, **kwargs):
        clrs = Segment(feature['geometry'])
        location = Location.from_lr_feature(feature, **kwargs)
        clrs.add_location(location)
        return clrs

    @staticmethod
    def from_dict(segment_dict):
        pass
