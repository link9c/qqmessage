# sql返回字典类型
import datetime
import re
import hashlib

from tornado.web import authenticated

from api.base import BaseHandler
from . import logic


class LoginHandler(BaseHandler):

    def get(self):
        self.render('index.html')

    async def post(self):
        data = {'code': None, 'msg': None}
        secretNum = self.get_argument('secretNum')
        res = await logic.auth_check(secretNum)
        if res:
            self.set_secure_cookie('user', secretNum)
            data['code'] = 0
            data['msg'] = 'charts/heat'
            self.write(data)


class HeatHandler(BaseHandler):
    @authenticated
    async def get(self):
        group_id = self.group_id

        week_year = self.week_year

        new_data = []
        for data in week_year:
            if data not in new_data:
                new_data.append(data)

        years = list(set([y[1] for y in new_data]))

        start_week = week_year[0][0]

        text_weeks = [(datetime.datetime.strptime('%s-%s-0' % (w[1], w[0]), '%Y-%U-%w'),
                       datetime.datetime.strptime('%s-%s-6' % (w[1], w[0]), '%Y-%U-%w')) for w in new_data]
        text_weeks = [f"第{i + start_week}周-{w[0].month}月{w[0].day}号~{w[1].month}月{w[1].day}号" for i, w in
                      enumerate(text_weeks)]
        print(text_weeks)
        if group_id:
            await self.render('charts/heat.html', group_id=group_id, years=years, weeks=text_weeks)
        else:
            self.write_error(404)

    async def post(self):
        _year, _week, _day = datetime.datetime.now().isocalendar()
        startpoint = datetime.datetime.now() - datetime.timedelta(_day + 6)
        endpoint = datetime.datetime.now() - datetime.timedelta(_day - 1)
        stamp_st = datetime.datetime(startpoint.year, startpoint.month, startpoint.day)
        stamp_end = datetime.datetime(endpoint.year, endpoint.month, endpoint.day)

        group_id = self.get_argument('group_id', '187861757')
        year = self.get_argument('year', "")
        week = self.get_argument('week', "")
        print(year, week)
        if week != "选择周数" and year != "选择年份" and week != "" and year != "":
            nums = re.findall('\d+', week)
            stamp_st = datetime.datetime(int(year), int(nums[1]), int(nums[2]))
            stamp_end = datetime.datetime(int(year), int(nums[3]), int(nums[4]))

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
        group_id = self.group_id
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
        group_id = self.group_id
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
        group_id = self.group_id
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

        resp = """        """
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
