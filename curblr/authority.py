from curblr import CurbLRObject

class Authority(CurbLRObject):
    def __init__(self, name=None, url=None, phone=None):
        self.name = name
        self.url = url
        self.phone = phone
    
    def to_dict(self):
        d = {}
        if self.name:
            d['name'] = self.name
        if self.url:
            d['url'] = self.url
        if self.phone:
            d['phone'] = self.phone
        
        return d
    
    @staticmethod
    def from_dict(d):
        return Authority(d.get('name'), d.get('url'), d.get('phone'))
