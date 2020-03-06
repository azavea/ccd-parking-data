from curblr import CurbLRObject
from curblr.utils import from_camelcase, to_camelcase


class Payment(CurbLRObject):

    fields = ['rates', 'methods', 'forms', 'operator', 'phone', 'device_ids']

    def __init__(self, rates=None, methods=None, forms=None, operator=None, phone=None, device_ids=None):
        self.rates = []
        self.methods = []
        self.forms = []
        self.device_ids = []

        self.add_list('rates', rates)
        self.add_list('methods', methods)
        self.add_list('forms', forms)
        self.add_list('device_ids', device_ids)

        self.operator = operator
        self.phone = phone

    def to_dict(self):
        return super().to_dict(Payment)


class Rate(CurbLRObject):

    fields = ['fees', 'durations', 'time_spans']

    def __init__(self, fees=None, durations=None, time_spans=None):
        self.fees = []
        self.durations = []
        self.time_spans = []

        self.add_list('fees', fees)
        self.add_list('durations', durations)
        self.add_list('time_spans', time_spans)

    def to_dict(self):
        return super().to_dict(Rate)
