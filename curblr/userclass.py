from curblr import CurbLRObject
from curblr.utils import to_camelcase


class UserClass(CurbLRObject):

    fields = ['classes', 'subclasses', 'max_height', 'min_height',
              'max_length', 'min_length', 'max_weight', 'min_weight']

    def __init__(self,
                 classes,
                 subclasses=None,
                 max_height=None,
                 min_height=None,
                 max_length=None,
                 min_length=None,
                 max_weight=None,
                 min_weight=None):
        self.classes = [c for c in classes if c]
        self.subclasses = subclasses
        self.max_height = max_height
        self.min_height = min_height
        self.max_length = max_length
        self.min_length = min_length
        self.max_weight = max_weight
        self.min_weight = min_weight

    def to_dict(self):
        return super().to_dict(UserClass)
