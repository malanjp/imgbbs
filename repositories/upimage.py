from hashlib import sha1 as sha
from models.upimage import UpImage
from config import secretkey

class Repository(object):

    def __init__(self, db):
        self.db = db

    def list_upimages(self):
        cursor = self.db.execute("""
                SELECT id, created_on, author, title, message, img, thumb
                FROM upimage
                ORDER BY id DESC
                LIMIT 20
        """)
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
        upimage.delkey = self.generate_password(upimage.delkey)
        self.db.execute("""
                INSERT INTO upimage (created_on, author, title, message, img, thumb, delkey)
                VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (upimage.created_on, upimage.author, upimage.title, upimage.message, upimage.img, upimage.thumb, upimage.delkey))
        return True

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

    def generate_password(self, key):
        return sha(key.encode('utf-8') + secretkey.encode('utf-8')).hexdigest()



