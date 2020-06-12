import os

import aiomysql
import pymysql
import redis

Base_Dir = os.path.dirname(__file__)
APP_CONFIG = dict(
    static_path=os.path.join(Base_Dir, 'static'),
    template_path=os.path.join(Base_Dir, 'template'),
    login_url='/',
    # static_url_prefix='/',
    cookie_secret='aaavvv',
    debug=False,

)


def connect_pymysql():
    return pymysql.connect(
        host="118.xxx.209",
        # host="127.0.0.1",
        port=3306,
        user="link",
        password="xxx",
        db="coolq"
    )


async def test_aiomysql(sql):
    conn = await aiomysql.connect(host="118.xxx.209",
                                  # host="127.0.0.1",
                                  port=3306,
                                  user="link",
                                  password="xxx",
                                  db="coolq")

    async with conn.cursor() as cur:
        await cur.execute(sql)
        print(cur.description)
        r = await cur.fetchall()
    conn.close()
    return r


async def connect_aiomysql():
    return await aiomysql.connect(
        host="118.xxx.209",
        # host="127.0.0.1",
        port=3306,
        user="link",
        password="xxx",
        db="coolq"
    )


def connect_redis():
    return redis.StrictRedis(
        host='118.xxx.209',
        port=6379,
        db=0,
        password=xxx)


if __name__ == '__main__':
    # connect_redis()
    pass