from datetime import datetime


class UpImage(object):

    def __init__(self, id=0, created_on=None, author='', title='', message='',
                img=None, thumb=None, delkey='', deltime=None, reply_count=0, last_modified=''):
        self.id = id
        self.created_on = created_on or datetime.now()
        self.author = author
        self.title = title
        self.message = message
        self.img = img
        self.thumb = thumb
        self.delkey = delkey
        self.deltime = deltime
        self.last_modified = last_modified or datetime.now()
        self.reply_count = reply_count


class Reply(object):

    def __init__(self, id=0, parent_id=0, created_on=None, author='', title='', message='',
                img=None, thumb=None, delkey='', deltime=None):
        self.id = id
        self.parent_id = parent_id
        self.created_on = created_on or datetime.now()
        self.author = author
        self.message = message
        self.img = img
        self.thumb = thumb
        self.delkey = delkey
        self.deltime = deltime



