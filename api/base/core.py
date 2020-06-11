import datetime
import json
import time

import tornado.web

from settings import connect_pymysql
from settings import connect_redis


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        # self.aiomysql = self.settings['mysql']
        self.pymysql = connect_pymysql()
        try:
            self.redis = connect_redis()
        except Exception as e:
            print(e)


    def get_current_user(self):
        user_cookie = self.get_secure_cookie("user")
        if user_cookie:
            return json.loads(user_cookie)
        return None

    def prepare(self):
        try:
            db = self.redis
            ip = self.request.remote_ip
            print(f"{datetime.datetime.now()}:{ip}")
            # 判断是否存在ip
            if not db.exists(ip):
                db.rpush(ip, time.time())
            else:
                db.rpush(ip, time.time())
                l = db.llen(ip)
                end = float(db.lindex(ip, l - 1).decode("utf-8"))
                start = float(db.lindex(ip, 0).decode("utf-8"))
                if l > 60 and (end - start) < 60:
                    self.write_error(404)
                    db.lpop(ip)
                else:
                    if l > 60 and end - start >= 60:
                        db.ltrim(ip, l - 2, l - 1)
        except Exception as e:
            print(e)

    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('404.html')
        elif status_code == 500:
            self.write('500')
        else:
            self.write('error:' + str(status_code))

    def get_group_id(self):
        conn = self.pymysql
        cursor = conn.cursor()
        sql = """select distinct group_id from qqmessage"""
        try:
            cursor.execute(sql)
            conn.close()
            res = cursor.fetchall()
            group_id = [r[0] for r in res]
            return group_id
        except Exception as e:
            print(e)
            return None
