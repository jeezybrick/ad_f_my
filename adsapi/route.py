import settings
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options
from db import ConnectionHandler
from app import *

db = ConnectionHandler().db_connect()
define("port", default=8050, help="run server on given port", type=int)

class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")

application = tornado.web.Application([
        (r'/getContent/?', AdContentHandler),
        (r'/saveRedeemed/', SaveUserTokenHandler),
        (r'/saveDollar/', SaveCouponDollarHandler),
        (r'/notifyMe/', NotifyHandler),
        (r'/socalShare/', SocialShareHandler),
        (r'/static/(.*)', NoCacheStaticFileHandler, {
            'path': settings.STATIC_PATH
        }),
    ], db=db
)
http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(options.port, address='23.239.11.140')
tornado.ioloop.IOLoop.instance().start()


