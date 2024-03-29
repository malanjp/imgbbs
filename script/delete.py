# -*- coding: utf-8 -*-
import os, sys
import socket
from datetime import datetime, timedelta
import pymysql
import pymysql.cursors

from celery import Celery
from celery.task import periodic_task


celery = Celery('tasks', broker='amqp://guest@localhost//')


def session():
    if socket.gethostname() == 'mshibata-vm-ubuntu':
        return pymysql.connect(db='imgbbs', host='192.168.72.100', user='imgbbs', passwd='_WioT.A', charset='utf8')
    else:
        return pymysql.connect(db='imgbbs', host='localhost', user='imgbbs', passwd='_WioT.A', charset='utf8')


# 親に連なるエントリ削除
@periodic_task(run_every=timedelta(minutes=1))
def delete():

    current_path = os.path.abspath(os.path.dirname(__file__))

    con = session()
    db = con.cursor(pymysql.cursors.DictCursor)
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
            db.execute("update upimage, reply set upimage.reply_count = (select count(*) from reply where upimage.id = reply.parent_id)")
            con.commit()

        # 親エントリ削除
        query = "delete from upimage where id = %s " % row.get('id')
        db.execute(query)
        con.commit()
   
    
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
            db.execute("update upimage, reply set upimage.reply_count = (select count(*) from reply where upimage.id = reply.parent_id)")
            con.commit()

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
        db.execute("update upimage, reply set upimage.reply_count = (select count(*) from reply where upimage.id = reply.parent_id)")
        con.commit()

    db.close()
    con.close()



