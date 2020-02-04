from curblr import CurbLRObject
from curblr.authority import Authority
from curblr.utils import from_camelcase

class Rule(CurbLRObject):

    activity = ['parking', 'no parking', 'standing',
                'no standing', 'loading', 'no loading']

    def __init__(self,
                 activity: str,
                 reason: str = None,
                 max_stay: int = None,
                 no_return: int = None,
                 payment: bool = False,
                 authority: Authority = None):

        if activity.to_lower() in Rule.activity:
            self.activity = activity.to_lower()
        else:
            Exception('"activity" value must be one of {}, got {}'.format(
                Rule.activity, activity))

        self.reason = reason
        self.max_stay = max_stay
        self.no_return = no_return
        self.payment = payment
        self.authority = authority

    def to_dict(self):
        d = {'activity': self.activity}

        if self.reason:
            d['reason'] = self.reason
        if self.max_stay:
            d['maxStay'] = self.max_stay
        if self.no_return:
            d['noReturn'] = self.no_return
        if self.payment: # should this be included by default?
            d['payment'] = self.payment
        if self.authority:
            d['authority'] = self.authority.to_dict()
        
        return d

    @staticmethod
    def from_dict(d):
        kwargs = {}
        if isinstance(d.get('authority'), dict):
            kwargs['authority'] = Authority.from_dict(d.get('authority'))
        else:
            kwargs['authority'] = d.get('authority')
        for arg in ['activity', 'reason', 'maxStay', 'noReturn', 'payment']:
            kwargs[from_camelcase(arg)] = d.get(arg)
        return Rule(**kwargs)
