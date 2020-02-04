from curblr import CurbLRObject
from curblr.rule import Rule
from curblr.userclass import UserClass

class Regulation(CurbLRObject):
    def __init__(self,
                 rule: Rule,
                 userclasses: [UserClass],
                 timespans,
                 priority,
                 payment=None):
        self.rule = rule
        self.userclasses = userclasses
        self.timespans = timespans
        self.priority = priority
        self.payment = payment

    def to_dict(self):
        pass

    @staticmethod
    def from_dict(regulation_dict):
        pass
