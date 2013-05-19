import os, sys
from datetime import datetime
import pymysql
import pymysql.cursors

current_path = os.path.abspath(os.path.dirname(__file__))

def session():
    return pymysql.connect(db='imgbbs', user='imgbbs', passwd='_WioT.A', charset='utf8')


con = session()
db = con.cursor(pymysql.cursors.DictCursor)

# 親に連なるエントリ削除
db.execute("select * from upimage where deltime <= now()")
for row in db.fetchall():
    if row.get('img'):
        try:
            os.remove(os.path.join(current_path, '../', 'contents/static/upload/', row.get('img')))
            os.remove(os.path.join(current_path, '../', 'contents/static/upload/', row.get('thumb')))
        except FileNotFoundError as e:
            print(e)

    # 子画像削除
    query = "select * from reply where parent_id = %s" % row.get('id')
    db.execute(query)
    for child_row in db.fetchall():
        if child_row.get('img'):
            try:
                os.remove(os.path.join(current_path, '../', 'contents/static/upload/', child_row.get('img')))
                os.remove(os.path.join(current_path, '../', 'contents/static/upload/', child_row.get('thumb')))
            except FileNotFoundError as e:
                print(e)

        # 子エントリ削除
        query = "delete from reply where id = %s " % child_row.get('id')
        db.execute(query)

    # 親エントリ削除
    query = "delete from upimage where id = %s " % row.get('id')
    db.execute(query)

    con.commit()


# 子エントリのみ削除
db.execute("select * from reply where deltime <= now()")
for row in db.fetchall():
    if row.get('img'):
        try:
            os.remove(os.path.join(current_path, '../', 'contents/static/upload/', row.get('img')))
            os.remove(os.path.join(current_path, '../', 'contents/static/upload/', row.get('thumb')))
        except FileNotFoundError as e:
            print(e)

    # エントリ削除
    query = "delete from reply where id = %s " % row.get('id')
    db.execute(query)
    con.commit()




