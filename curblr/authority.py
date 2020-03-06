from curblr import CurbLRObject


class Authority(CurbLRObject):

    fields = ['name', 'url', 'phone']

    def __init__(self, name=None, url=None, phone=None):
        self.name = name
        self.url = url
        self.phone = phone

    def to_dict(self):
        return super().to_dict(Authority)
