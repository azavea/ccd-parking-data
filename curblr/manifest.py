from datetime import datetime

from curblr import CurbLRObject
from curblr.authority import Authority


class Manifest(CurbLRObject):

    fields = ['time_zone', 'currency', 'authority', 'create_date', 'last_update_date',
              'unit_height_length', 'unit_weight']

    def __init__(self,
                 time_zone,
                 currency,
                 authority,
                 create_date=None,
                 last_update_date=None,
                 unit_height_length=None,
                 unit_weight=None):
        self.time_zone = time_zone
        self.currency = currency
        self.authority = authority
        if isinstance(authority, dict):
            self.authority = Authority.from_dict(authority)
        self.create_date = create_date
        if not self.create_date:
            self.create_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self.last_update_date = last_update_date
        self.unit_height_length = unit_height_length
        self.unit_weight = unit_weight

    def to_dict(self):
        return super().to_dict(Manifest)
