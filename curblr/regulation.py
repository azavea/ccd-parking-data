from curblr import CurbLRObject
from curblr.payment import Payment
from curblr.rule import Rule
from curblr.timespan import TimeSpan
from curblr.userclass import UserClass


class Regulation(CurbLRObject):

    fields = ['rule', 'user_classes', 'time_spans', 'priority', 'payment']

    def __init__(self,
                 rule,
                 user_classes=None,
                 time_spans=None,
                 priority=None,
                 payment=None):
        self.rule = rule
        self.user_classes = None if user_classes == [{}] else user_classes
        self.time_spans = None if time_spans == [] else time_spans
        self.priority = priority
        self.payment = payment

    def to_dict(self):
        return super().to_dict(Regulation)

    @staticmethod
    def from_dict(d):
        rule = Rule.from_dict(d.get('rule'))
        user_classes = d.get('user_classes')
        if user_classes:
            user_classes = [UserClass.from_dict(
                x) for x in d.get('user_classes')]
        time_spans = d.get('time_spans')
        if time_spans:
            time_spans = [TimeSpan.from_dict(x) for x in d.get('time_spans')]

        priority = d.get('priority')
        payment = d.get('payment')
        if payment:
            payment = Payment.from_dict(d.get('payment'))

        return Regulation(rule, user_classes, time_spans, priority, payment)
