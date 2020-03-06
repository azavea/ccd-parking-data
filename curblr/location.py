from uuid import uuid1

from curblr import CurbLRObject


class Location(CurbLRObject):

    fields = ['shst_ref_id', 'side_of_street', 'shst_location_start', 'shst_location_end',
              'derived_from', 'object_id', 'marker', 'bays_angle', 'bays_count', 'street_name']

    def __init__(self,
                 shst_ref_id,
                 side_of_street,
                 shst_location_start,
                 shst_location_end,
                 derived_from=None,
                 object_id=None,
                 marker=None,
                 bays_angle=None,
                 bays_count=None,
                 street_name=None):
        self.shst_ref_id = shst_ref_id
        self.side_of_street = side_of_street
        self.shst_location_start = shst_location_start
        self.shst_location_end = shst_location_end
        self.derived_from = derived_from
        self.object_id = object_id
        self.marker = marker
        self.bays_angle = bays_angle
        self.bays_count = bays_count
        self.street_name = street_name

    def to_dict(self):
        return super().to_dict(Location)

    @classmethod
    def from_lr_feature(cls,
                        feature,
                        object_id=None,
                        derived_from=None,
                        marker=None,
                        bays_angle=None,
                        bays_count=None,
                        street_name=None):
        if not feature:
            return None

        props = feature['properties']

        props['shstRefId'] = props['shstReferenceId']
        props['shstLocationStart'] = props['section'][0]
        props['shstLocationEnd'] = props['section'][1]

        if object_id:
            props['objectId'] = props[object_id]
        if derived_from:
            props['derivedFrom'] = props[derived_from]
        if marker:
            props['marker'] = props[marker]
        if bays_angle:
            props['baysAngle'] = props[bays_angle]
        if bays_count:
            props['baysCount'] = props[bays_count]
        if street_name:
            props['streetName'] = props[street_name]

        return cls.from_dict(props)
