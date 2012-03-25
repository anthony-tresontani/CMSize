import tornado.web
import tornado.ioloop
from cms_processor import add_cms_contents


class CMSProcessorHandler(tornado.web.RequestHandler):
    def post(self, user):
        dom = self.get_argument("dom")
        response = add_cms_contents(user, dom)
	self.write(response)


application = tornado.web.Application([
    (r"/cms/(\w+)/", CMSProcessorHandler),
])

def start_server(application):
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    start_server(application)
