from hashlib import sha1 as sha
from datetime import datetime
from models.upimage import UpImage, Reply
from config import secretkey
from config import SELECT_LIMIT

class Repository(object):

    def __init__(self, con):
        self.db = con.cursor()
        self.con = con

    def list_upimages(self, page=1):
        offset = 0
        if int(page) > 1:
            offset = (int(page) - 1) * SELECT_LIMIT

        self.db.execute("""
                SELECT id, created_on, author, title, message, img, thumb
                FROM upimage
                ORDER BY id DESC
                LIMIT %s
                OFFSET %s
        """, (SELECT_LIMIT, offset))
        return [UpImage(
                id=row[0],
                created_on=row[1],
                author=row[2],
                title=row[3],
                message=row[4],
                img=row[5],
                thumb=row[6]
               ) for row in self.db.fetchall()]

    def add_upimage(self, upimage):
        upimage.delkey = self.generate_password(upimage.delkey)
        if upimage.deltime == '':
            upimage.deltime = None
        #if upimage.deltime:
        #  upimage.deltime = datetime.strptime(upimage.deltime, "%Y-%m-%dT%H%M")
        print('repo deltime=', upimage.deltime)
        self.db.execute("""
                INSERT INTO upimage (created_on, author, title, message, img, thumb, delkey, deltime)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (upimage.created_on, upimage.author, upimage.title, upimage.message, upimage.img, upimage.thumb, upimage.delkey, upimage.deltime))
        return True

    def get_count(self):
        self.db.execute("""
                SELECT count(*)
                FROM upimage
        """)
        row = self.db.fetchone()
        count = row[0]
        return count

    def get_upimage(self, id):
        self.db.execute("""
                SELECT id, created_on, author, title, message, img, thumb, deltime
                FROM upimage
                WHERE id = %s
        """, (id,))
        row = self.db.fetchone()
        if not row:
            return None
        return UpImage(
                id=row[0],
                created_on=row[1],
                author=row[2],
                title=row[3],
                message=row[4],
                img=row[5],
                thumb=row[6],
                deltime=row[7]
              )

    def add_reply(self, reply):
        reply.delkey = self.generate_password(reply.delkey)
        if reply.deltime == '':
            reply.deltime = None
        #if reply.deltime:
        #  reply.deltime = datetime.strptime(reply.deltime, "%Y-%m-%dT%H%M")
        self.db.execute("""
                INSERT INTO reply (created_on, parent_id, author, message, img, thumb, delkey, deltime)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (reply.created_on, reply.parent_id, reply.author, reply.message, reply.img, reply.thumb, reply.delkey, reply.deltime))
        return True

    def get_replies(self, parent_id):
        self.db.execute("""
                SELECT id, parent_id, created_on, author, message, img, thumb, deltime
                FROM reply
                WHERE parent_id = %s
        """, (parent_id,))
        return [Reply(
                id=row[0],
                parent_id=[1],
                created_on=row[2],
                author=row[3],
                message=row[4],
                img=row[5],
                thumb=row[6],
                deltime=row[7]
              ) for row in self.db.fetchall()]

    def get_reply(self, id):
        self.db.execute("""
                SELECT id, parent_id, created_on, author, message, img, thumb, deltime
                FROM reply
                WHERE id = %s
        """, (id,))
        row = self.db.fetchone()
        if not row:
            return None
        return Reply(
                id=row[0],
                parent_id=[1],
                created_on=row[2],
                author=row[3],
                message=row[4],
                img=row[5],
                thumb=row[6],
                deltime=row[7] 
              )

    def delete_reply(self, reply):
        passwd = self.generate_password(reply.delkey)
        self.db.execute("""
                SELECT count(*)
                FROM reply
                WHERE id = %s and delkey = %s
        """, (reply.id, passwd))
        row = self.db.fetchone()
        count = row[0]
        res = False
        if count > 0:
            res = self.db.execute("""
                    DELETE
                    FROM reply
                    WHERE id = %s
            """, (reply.id,))
        self.con.commit()
        return res

    def delete_upimage(self, upimage):
        passwd = self.generate_password(upimage.delkey)
        self.db.execute("""
                SELECT count(*)
                FROM upimage
                WHERE id = %s and delkey = %s
        """, (upimage.id, passwd))
        row = self.db.fetchone()
        count = row[0]
        res = False
        if count > 0:
            res = self.db.execute("""
                    DELETE
                    FROM upimage
                    WHERE id = %s
            """, (upimage.id,))
        self.con.commit()
        return res

    def generate_password(self, key):
        if not key:
          key = ''
        return sha(key.encode('utf-8') + secretkey.encode('utf-8')).hexdigest()



