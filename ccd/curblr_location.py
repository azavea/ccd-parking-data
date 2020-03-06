from curblr.location import Location

class CCDLocation(Location):
    @staticmethod
    def from_lr_feature(feature):
        return Location.from_lr_feature(feature, objectId='pp_globalid', marker='sign', streetName='pp_street')
