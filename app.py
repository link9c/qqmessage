import platform

if platform.system() == "Windows":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import tornado.ioloop
import tornado.web
from tornado.web import url

from api.base import BaseHandler
from api.handler import HeatHandler
from api.handler import LoginHandler
from api.handler import BarHandler
from api.handler import LineHandler
from api.handler import WordCloudHandler
from api.handler import WeChatCheck

from settings import APP_CONFIG

print('now restart')
import asyncio

loop = asyncio.get_event_loop()


def make_app():
    return tornado.web.Application([

        url(r"/", LoginHandler, name='login'),
        url(r"/wechat", WeChatCheck),

        url(r"/charts/wordcloud", WordCloudHandler, name='wordcloud'),
        url(r"/charts/heat", HeatHandler, name='heat'),
        url(r"/charts/bar", BarHandler, name='bar'),
        url(r"/charts/line", LineHandler, name='line'),
        (r".*", BaseHandler),
        # (
        #     r"/(.*)", StaticFileHandler,
        #     {"path": os.path.join(Base_Dir, "static/html"), "default_filename": "hotmap.html"})
    ],
        # mysql=tornado.ioloop.IOLoop.current().run_sync(connect_aiomysql),
        # mysql=loop.run_until_complete(connect_aiomysql()),
        **APP_CONFIG

    )


# asyncio.new_event_loop().run_until_complete()

if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
