import tornado.ioloop
import tornado.websocket
import tornado.web
import rc_responder
import lib.logging as logger



class Reciever(object):

    def __init__(self, port=1661):
        self.hotReload = True
        self._app = None
        self.port = 1661

    def messages(self, msg):
        pass

    @property
    def tornadoApp(self):
        app = self._app

        if not app:
            app = tornado.web.Application([
                ('/', ReceiverHttpAdaptor),
                ('/connect', ReceiverWsAdaptor),
            ])
        return app

    @property
    def responder(self):
        if self.hotReload:
            reload(rc_responder)

        return rc_responder

    def start(self, **kwargs):
        self.tornadoApp.listen(self.port)
        logger.debug('[start] listening on %s', self.port)
        tornado.ioloop.IOLoop.current().start()

class ReceiverAdaptor(object):

    @classmethod
    def mountArgs(cls):
        return []

class ReceiverHttpAdaptor(tornado.web.RequestHandler, ReceiverAdaptor):

    def get(self):
        self.write("Hello, world")

class ReceiverWsAdaptor(tornado.websocket.WebSocketHandler, ReceiverAdaptor):

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")

if __name__ == "__main__":
    Reciever().start()
