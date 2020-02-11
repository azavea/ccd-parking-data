from uuid import uuid1

from curblr import CurbLRObject


class Location(CurbLRObject):
    required_fields = ['shstRefId', 'sideOfStreet',
                       'shstLocationStart', 'shstLocationEnd']
    optional_fields = ['derivedFrom', 'objectId',
                       'marker', 'baysAngle', 'baysCount', 'streetName']
    fields = required_fields + optional_fields

    def __init__(self,
                 shstRefId,
                 sideOfStreet,
                 shstLocationStart,
                 shstLocationEnd,
                 derivedFrom=[],
                 objectId=None,
                 marker=None,
                 baysAngle=None,
                 baysCount=None,
                 streetName=None):
        self.shstRefId = shstRefId
        self.sideOfStreet = sideOfStreet
        self.shstLocationStart = shstLocationStart
        self.shstLocationEnd = shstLocationEnd
        self.derivedFrom = derivedFrom
        self.objectId = objectId
        self.marker = marker
        self.baysAngle = baysAngle
        self.baysCount = baysCount
        self.streetName = streetName

    def to_dict(self):
        return {f: getattr(self, f) for f in Location.fields if getattr(self, f)}

    @staticmethod
    def from_dict(location_dict):
        # can handle a dict (e.g. the output of linear referencing tool), that has
        # extra fields.
        kwargs = {f: location_dict[f]
                  for f in Location.fields if f in location_dict}
        return Location(**kwargs)

    @staticmethod
    def from_lr_feature(feature, derivedFrom=None, objectId=None, marker=None, baysAngle=None, baysCount=None, streetName=None):
        if not feature:
            return None

        props = feature['properties']

        kwargs = {}
        kwargs['shstRefId'] = props['shstReferenceId']
        kwargs['sideOfStreet'] = props['sideOfStreet']
        kwargs['shstLocationStart'] = props['section'][0]
        kwargs['shstLocationEnd'] = props['section'][1]

        for key, arg in list(zip(Location.optional_fields, [derivedFrom, objectId, marker, baysAngle, baysCount, streetName])):
            if arg:
                kwargs[key] = props[arg]

        return Location(**kwargs)
