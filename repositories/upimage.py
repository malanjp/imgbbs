from hashlib import sha1 as sha
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
        self.db.execute("""
                INSERT INTO upimage (created_on, author, title, message, img, thumb, delkey)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (upimage.created_on, upimage.author, upimage.title, upimage.message, upimage.img, upimage.thumb, upimage.delkey))
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
                SELECT id, created_on, author, title, message, img, thumb
                FROM upimage
                WHERE id = %s
        """, (id,))
        row = self.db.fetchone()
        return UpImage(
                id=row[0],
                created_on=row[1],
                author=row[2],
                title=row[3],
                message=row[4],
                img=row[5],
                thumb=row[6]
              )

    def add_reply(self, reply):
        reply.delkey = self.generate_password(reply.delkey)
        self.db.execute("""
                INSERT INTO reply (created_on, parent_id, author, title, message, img, thumb, delkey)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (reply.created_on, reply.parent_id, reply.author, reply.title, reply.message, reply.img, reply.thumb, reply.delkey))
        return True

    def get_reply(self, parent_id):
        self.db.execute("""
                SELECT id, parent_id, created_on, author, title, message, img, thumb
                FROM reply
                WHERE parent_id = %s
        """, (parent_id,))
        return [Reply(
                id=row[0],
                parent_id=[1],
                created_on=row[2],
                author=row[3],
                title=row[4],
                message=row[5],
                img=row[6],
                thumb=row[7]
              ) for row in self.db.fetchall()]

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
        return sha(key.encode('utf-8') + secretkey.encode('utf-8')).hexdigest()



