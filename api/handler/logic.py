import datetime
import re

import jieba
import jieba.analyse

# from app import Base_Dir
from settings import connect_aiomysql


def get_all_text(resp: tuple):
    pass


def handle_command(words: list, user_id: int = None) -> tuple:
    """

    :param words: 所有用词
    :param user_id: 用户id
    :return: 调用命令次数，去除命令后的words，用户id
    """
    count = 0
    content = []
    for word in words:
        if '/' in word:
            count += 1
        else:
            content.append(word)
    # print(f'{user_id} command use {count} times')

    return count, content, user_id


def handle_face(words: list, user_id: int = None, only_face: bool = False) -> tuple:
    type_count = {}
    content = []
    pattern = r'\[CQ:.+?,\D+?=.+?\]'
    for word in words:
        # resp = re.search(pattern, word)
        if resp := re.findall(pattern, word):
            for r in resp:
                if type_count.get(r):
                    type_count[r] += 1
                else:
                    type_count.setdefault(r, 1)

                word = word.replace(r, '')
            if word:
                content.append(word)

        else:
            content.append(word)
    # print(f'{user_id} face count {type_count}')

    return type_count, content, user_id


def word_cloud(content):
    jieba.load_userdict('utils/dict.txt')
    seg_list = jieba.analyse.extract_tags(content, withWeight=True)

    return seg_list


async def heat_chart_handle(group_id: str, start, end) -> tuple:
    conn = await connect_aiomysql()
    async with conn.cursor() as cursor:
        # async with self.aiomysql.cursor() as cursor:
        sql = """
                select format_time,content from qqmessage where group_id = %s and format_time >= %s and format_time < %s order by time
                """
        await cursor.execute(sql, (group_id, start, end))
        res = await cursor.fetchall()
    temp_data = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}
    for r in res:
        # 2020-03-01 22:06:10
        format_time = datetime.datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S")
        # 返回周几
        day = format_time.isocalendar()[-1]

        hour = format_time.hour
        if temp_data[day - 1].get(hour):
            temp_data[day - 1][hour] += 1
        else:
            temp_data[day - 1].setdefault(hour, 1)
    data = []
    point = []
    for day, value in temp_data.items():
        if value.items():
            for hour, count in value.items():
                new_point = point.copy()
                new_point.extend([day, hour, count])
                data.append(new_point)
    content_list = [r[1] for r in res]
    return data, content_list


async def bar_chart_handle(group_id: str, start, end) -> tuple:
    """

    :param res: tuple sql response
    :return:
    users:发言数量前6的用户名,只计算发言条数
    data:发言中类别细分数据，一条发言可能有多个图片，表情等
    msg_num:发言数量

    """
    conn = await connect_aiomysql()
    async with conn.cursor() as cursor:
        # async with self.aiomysql.cursor() as cursor:
        sql = """
                select user_id,sender,content from qqmessage where group_id = %s and format_time >= %s and format_time < %s
                """
        await cursor.execute(sql, (group_id, start, end))
        res = await cursor.fetchall()

    print('find %s contents' % len(res))
    order_list = {}
    regx = lambda x: re.findall(r'nickname\': \'(.+?)\'', x)
    for r in res:
        user_id = r[0]
        user_name = regx(r[1])[0]
        pin = user_id + ' ' + user_name.strip()
        if order_list.get(pin):
            order_list[pin] += 1
        else:
            order_list.setdefault(pin, 1)
    order = sorted(order_list.items(), key=lambda x: x[1], reverse=True)

    order = order[:6] if len(order) >= 6 else order
    temp_data = {}
    for user in [r[0] for r in order]:
        user_id = user.split(' ')[0]
        user_name = user.replace(user_id, '').strip()
        content_list = [r[2] for r in res if r[0] == user_id]
        type_count, content, _ = handle_face(content_list)
        category = {'face': 0, 'at': 0, 'img': 0, 'record': 0, 'content': 0}
        for k, v in type_count.items():
            if 'image' in k:
                category['img'] += v
            if 'face' in k:
                category['face'] += v
            if 'record' in k:
                category['record'] += v
            if 'at' in k:
                category['at'] += v
        category['content'] = len(content)

        temp_data[user_name] = category

    users = [k for k in temp_data.keys()][::-1]
    data = []
    if len(temp_data.values()) > 0:
        for k in list(temp_data.values())[0].keys():
            data.append([v.get(k) for v in temp_data.values()][::-1])

    msg_num = [r[1] for r in order]

    return users, data, msg_num


async def line_chart_handle(group_id: str) -> tuple:
    conn = await connect_aiomysql()
    async with conn.cursor() as cursor:
        sql = f"""
        select date_format(format_time, '%y-%m-%d') dat, count(user_id) coun from qqmessage where group_id = '{group_id}'
        group by date_format(format_time, '%y-%m-%d') 
        """
        await cursor.execute(sql)
        res = await cursor.fetchall()

    date_list = []
    msg = []
    for i, r in enumerate(res):
        date_list.append(r[0])
        msg.append(r[1])
        if i < len(res) - 1:
            this_day = int(res[i][0].split('-')[-1])
            next_day = int(res[i + 1][0].split('-')[-1])
            step = next_day - this_day
            if step > 1:
                for k in range(step):
                    tmp_res = res[i][0].split('-')
                    insert_day = this_day + k
                    tmp_res[-1] = str(insert_day)
                    date_list.append("-".join(tmp_res))
                    msg.append(0)

    return date_list, msg


if __name__ == '__main__':
    print(handle_face([
        '[CQ:at,qq=3522292626] 一个家庭又有了新成员，我们要以礼相待，更要真诚相待。让刚到的新人，敢到温暖，没有陌生[CQ:image,file=6A4FC4C393D1212FDE8CB77AD0F2F97A.jpg]']))
