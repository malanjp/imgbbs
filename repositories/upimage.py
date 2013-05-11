from hashlib import sha1 as sha
from models.upimage import UpImage
from config import secretkey
from config import SELECT_LIMIT

class Repository(object):

    def __init__(self, db):
        self.db = db

    def list_upimages(self, page=1):
        offset = 1
        if int(page) > 1:
            offset = (int(page) - 1) * SELECT_LIMIT + 1

        cursor = self.db.execute("""
                SELECT id, created_on, author, title, message, img, thumb
                FROM upimage
                ORDER BY id DESC
                LIMIT ?
                OFFSET ?
        """, (SELECT_LIMIT, offset))
        return [UpImage(
                id=row[0],
                created_on=row[1],
                author=row[2],
                title=row[3],
                message=row[4],
                img=row[5],
                thumb=row[6]
               ) for row in cursor.fetchall()]

    def add_upimage(self, upimage):
        print(upimage.delkey)
        upimage.delkey = self.generate_password(upimage.delkey)
        self.db.execute("""
                INSERT INTO upimage (created_on, author, title, message, img, thumb, delkey)
                VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (upimage.created_on, upimage.author, upimage.title, upimage.message, upimage.img, upimage.thumb, upimage.delkey))
        return True

    def get_count(self):
        cursor = self.db.execute("""
                SELECT count(*)
                FROM upimage
        """)
        row = cursor.fetchone()
        count = row[0]
        return count

    def get_upimages(self, filename):
        cursor = self.db.execute("""
                SELECT id, created_on, author, title, message, img, thumb
                FROM upimage
                WHERE img = ?
        """, (filename,))
        row = cursor.fetchone()
        return UpImage(
                id=row[0],
                created_on=row[1],
                author=row[2],
                title=row[3],
                message=row[4],
                img=row[5],
                thumb=row[6]
              )

    def delete_upimages(self, upimage):
        passwd = self.generate_password(upimage.delkey)
        cursor = self.db.execute("""
                SELECT count(*)
                FROM upimage
                WHERE id = ? and delkey = ?
        """, (upimage.id, passwd))
        row = cursor.fetchone()
        count = row[0]
        res = False
        if count > 0:
            res = self.db.execute("""
                    DELETE
                    FROM upimage
                    WHERE id = ?
            """, (upimage.id,))
        return res

    def generate_password(self, key):
        return sha(key.encode('utf-8') + secretkey.encode('utf-8')).hexdigest()



