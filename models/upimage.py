from datetime import datetime

class UpImage(object):

    def __init__(self, id=0, created_on=None, author='', title='', message='', img=None, thumb=None, delkey=''):
        self.id = id
        self.created_on = created_on or datetime.now()
        self.author = author
        self.title = title
        self.message = message
        self.img = img
        self.thumb = thumb
        self.delkey = delkey


class Reply(object):

    def __init__(self, id=0, parent_id=0, created_on=None, author='', title='', message='', img=None, thumb=None, delkey=''):
        self.id = id
        self.parent_id = parent_id
        self.created_on = created_on or datetime.now()
        self.author = author
        self.title = title
        self.message = message
        self.img = img
        self.thumb = thumb
        self.delkey = delkey

