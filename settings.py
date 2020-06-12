import os

import aiomysql
import pymysql
import redis

from secret import *

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
        host=HOST,
        # host="127.0.0.1",
        port=3306,
        user=USER,
        password=MYSQLPASS,
        db="coolq"
    )


async def connect_aiomysql():
    return await aiomysql.connect(
        host=HOST,
        # host="127.0.0.1",
        port=3306,
        user=USER,
        password=MYSQLPASS,
        db="coolq"
    )


def connect_redis():
    return redis.StrictRedis(
        host=HOST,
        port=6379,
        db=0,
        password=REDISPASS)


if __name__ == '__main__':
    # connect_redis()
    pass
