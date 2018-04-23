import json

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.httpclient import AsyncHTTPClient

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", RootHandler),
        ]
        settings = dict()
        tornado.web.Application.__init__(self, handlers, **settings)


class RootHandler(tornado.web.RequestHandler):
    def post(self):

        data = self.get_argument('urls', 'No data received')
        self.write(data)
        data_urls = json.loads(data)

        http_client = AsyncHTTPClient()
        for url in data_urls:
            http_client.fetch(url, self._handle_response)

    def get(self):
        self.write('You can send POST queries with urls in json format {"urls": ["http://ya.ru/", ...]}')

    def _handle_response(self, response):
        if response.error:
            print("{} - error:{}".format(response.request.url, response.error))
        else:
            url = response.request.url
            code = response.code
            data = response.body
            print('{}: status {} - {} bytes'.format(url, code, len(data), ))


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


main()
