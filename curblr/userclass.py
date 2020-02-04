from curblr import CurbLRObject
from curblr.utils import to_camelcase

class UserClass(CurbLRObject):
    
    attributes = ['classes', 'subclasses', 'max_height', 'min_height','max_length','min_length','max_weight', 'min_weight']
    
    def __init__(self,
                 classes: [str] = None,
                 subclasses: [str] = None,
                 max_height=None,
                 min_height=None,
                 max_length=None,
                 min_length=None,
                 max_weight=None,
                 min_weight=None):
        self.classes = classes
        self.subclasses = subclasses
        self.max_height = max_height
        self.min_height = min_height
        self.max_length = max_length
        self.min_length = min_length
        self.max_weight = max_weight
        self.min_weight = min_weight
    
    @staticmethod
    def from_dict(d):
        kwargs = {}
        for a in UserClass.attributes:
            arg = to_camelcase(a)
            kwargs[a] = d.get(arg)
        
        return UserClass(**kwargs)
    
    def to_dict(self):
        d = {}
        for a in UserClass.attributes:
            if self.__getattribute__(a):
                d[to_camelcase(a)] = self.__getattribute__(a)
        
        return d