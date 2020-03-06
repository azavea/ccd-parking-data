from abc import ABC, abstractmethod

from curblr.time_rule import TimeRule
from curblr.utils import from_camelcase, to_camelcase


class CurbLRObject(ABC):

    fields = []

    @classmethod
    def from_dict(cls, d):
        kwargs = {}
        for a in cls.fields:
            kwargs[a] = d.get(to_camelcase(a))

        return cls(**kwargs)

    def to_dict(self, sub_class):
        d = {}

        for f in sub_class.fields:
            obj = self.__getattribute__(f)
            if obj is not None:
                ccf = to_camelcase(f)
                if isinstance(obj, list):
                    d[ccf] = []
                    for x in obj:
                        try:
                            d[ccf].append(x.to_dict())
                        except AttributeError:
                            d[ccf].append(x)
                else:
                    try:
                        d[ccf] = obj.to_dict()
                    except AttributeError:
                        d[ccf] = obj
        return d

    def add_list(self, name, list_attr):
        if list_attr:
            if isinstance(list_attr, (set, tuple)):
                list_attr = list(list_attr)
            if not isinstance(list_attr, list):
                list_attr = [list_attr]
        self.__setattr__(name, list_attr)
