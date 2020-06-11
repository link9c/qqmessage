# sql返回字典类型
import datetime
import hashlib

from tornado.web import authenticated

from api.base import BaseHandler
from . import logic


class LoginHandler(BaseHandler):

    def get(self):
        self.render('index.html')

    def post(self):
        data = {'code': None, 'msg': None}
        secretNum = self.get_argument('secretNum')
        if secretNum == '10086':
            self.set_secure_cookie('user', secretNum)
            data['code'] = 0
            data['msg'] = 'charts/heat'
            self.write(data)


class HeatHandler(BaseHandler):
    @authenticated
    def get(self):
        group_id = self.get_group_id()
        if group_id:
            self.render('charts/heat.html', group_id=group_id)
        else:
            self.write_error(404)

    async def post(self):
        group_id = self.get_argument('group_id') or '187861757'
        year, week, day = datetime.datetime.now().isocalendar()
        startpoint = datetime.datetime.now() - datetime.timedelta(day + 6)
        endpoint = datetime.datetime.now() - datetime.timedelta(day - 1)
        stamp_st = datetime.datetime(startpoint.year, startpoint.month, startpoint.day)
        stamp_end = datetime.datetime(endpoint.year, endpoint.month, endpoint.day)
        title = f'一周发言热力图{stamp_st}～{stamp_end}'
        data, content_list = await logic.heat_chart_handle(group_id, stamp_st, stamp_end)
        resp = {
            'resp': {"data": data,
                     "title": title},
            "code": 0
        }

        self.write(resp)


class BarHandler(BaseHandler):
    @authenticated
    def get(self):
        group_id = self.get_group_id()
        if group_id:
            self.render('charts/bar.html', group_id=group_id)
        else:
            self.write_error(404)

    async def post(self):
        group_id = self.get_argument('group_id') or '187861757'
        date = self.get_argument('date')
        print(group_id, date)
        startpoint = datetime.datetime.strptime(date, '%Y-%m-%d')
        endpoint = startpoint + datetime.timedelta(1)
        users, data, msg_num = await logic.bar_chart_handle(group_id, startpoint, endpoint)
        print('users %s msg num %s' % (users, msg_num))
        resp = {
            "resp": {
                "nums": data,
                "users": users,
                "msg_num": msg_num[::-1]
            },
            "code": 0,
        }
        self.write(resp)


class LineHandler(BaseHandler):
    @authenticated
    def get(self):
        group_id = self.get_group_id()
        if group_id:
            self.render('charts/line.html', group_id=group_id)
        else:
            self.write_error(404)

    async def post(self):
        group_id = self.get_argument('group_id') or '187861757'
        date_list, msg = await logic.line_chart_handle(group_id)
        resp = {
            "resp": {
                "date": date_list,
                "msg_num": msg
            },
            "code": 0,
        }
        self.write(resp)


class WordCloudHandler(BaseHandler):
    @authenticated
    def get(self):
        group_id = self.get_group_id()
        if group_id:
            self.render('charts/wordcloud.html', group_id=group_id)
        else:
            self.write_error(404)


class WeChatCheck(BaseHandler):
    def get(self):
        signature = self.get_argument("signature")
        timestamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")
        echostr = self.get_argument("echostr")
        print(signature, timestamp, nonce, echostr)
        token = '123qwe'
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        print(hashcode, signature)
        # if hashcode == signature:
        self.write(echostr)

    def post(self):
        print(self.request.headers.get("Content-Type"))
        json_data = self.request.body
        print(json_data)

        resp = """
        <xml>
  <ToUserName><![CDATA[oy5vOwp8LdIVwrFKImdkWnCDu3v8]]></ToUserName>
  <FromUserName><![CDATA[gh_1dc5dc067a98]]></FromUserName>
  <CreateTime>1584543275</CreateTime>
  <MsgType><![CDATA[text]]></MsgType>
  <Content><![CDATA[你好]]></Content>
</xml>
        """
        self.write(resp)


class DemoHandler(BaseHandler):
    pass
    # async def post(self):
    #     async with self.aiomysql.cursor(DictCursor) as cursor:
    #         sql = """
    #         select * from qqmessage where group_id = '876153248' and user_id = '470349106' limit 8000
    #         """
    #         try:
    #             await cursor.execute(sql)
    #
    #             res = cursor.fetchall().result()
    #         except Exception as e:
    #             print(e)
    #             self.write({'code': 0})
    #     raw_content = [r['content'] for r in res]
    #     count, content, _ = logic.handle_command(raw_content)
    #
    #     face_count, cleaned_content, _ = logic.handle_face(content)
    #
    #     content = ','.join(cleaned_content).replace(' ', '')
    #     # print(content)
    #     # content = logic.word_cloud(content)
    #     # print(content)
    #     resp = {
    #         'code': 0,
    #         'content': content
    #     }
    #
    #     self.write(resp)
