from abc import ABC, abstractmethod


class CurbLRObject(ABC):

    @staticmethod
    @abstractmethod
    def from_dict(d):
        pass

    @abstractmethod
    def to_dict(self):
        pass
