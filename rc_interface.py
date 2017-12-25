import lib.logging as logger
import tornado

from motor import Motor
from lib.gpio import Signal, inPi

import tornado.ioloop
import tornado.web

# import signal, os

# def handler(signum, frame):
#     print 'Signal handler called with signal', signum
#     os.exit(0)
#
# # Set the signal handler and a 5-second alarm
# signal.signal(signal.SIGINT, handler)
# signal.signal(signal.SIGTERM, handler)


class Car(object):
    DIRECTION_FWD = 'forward'
    DIRECTION_BCK = 'back'
    DIRECTION_RGT = 'right'
    DIRECTION_LFT = 'left'

    MOVE_STOP = 'move_stop'
    TURN_STOP = 'turn_stop'

class RoboCar(Car):

    def __init__(self):
        self._direction = (None, None)
        self.F = Motor(Motor.MOVE)
        self.T = Motor(Motor.TURN)

    @property
    def moving(self):
        return self.direction[1] not in (None, self.MOVE_STOP)

    @property
    def turning(self):
        return self.direction[0] not in (None, self.TURN_STOP)

    @property
    def direction(self):
        return self._direction

    def stop(self):
        self.direction = None
        logger.info('car stopping: moving=%s, turning=%s', self.moving, self.turning)

    @direction.setter
    def direction(self, newVal):

        if newVal == Car.DIRECTION_FWD:
            self.F.moveForward()
        elif newVal == Car.DIRECTION_BCK:
            self.F.moveBack()
        elif newVal == Car.DIRECTION_LFT:
            self.T.turnLeft()
        elif newVal == Car.DIRECTION_RGT:
            self.T.turnRight()
        elif newVal == Car.TURN_STOP:
            self.T.stop()
        elif newVal == Car.MOVE_STOP:
            self.F.stop()
        else:
            self.T.stop()
            self.F.stop()

        if newVal in (Car.DIRECTION_LFT, Car.DIRECTION_RGT, Car.TURN_STOP):
            self._direction = (newVal, self._direction[1])
        elif newVal in (Car.DIRECTION_FWD, Car.DIRECTION_BCK, Car.MOVE_STOP):
            self._direction = (self._direction[0], newVal)
        else:
            self._direction = (None, None)

CAR = RoboCar()

class MainHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def initialize(self):
        self.car = CAR

    def move(self, fwd=True):
        self.car.direction = Car.DIRECTION_FWD if fwd else Car.DIRECTION_BCK
        return self.car.moving

    def moveStop(self):
        self.car.direction = Car.MOVE_STOP

    def turnStop(self):
        self.car.direction = Car.TURN_STOP

    def turn(self, right=True):
        self.car.direction = Car.DIRECTION_RGT if right else Car.DIRECTION_LFT
        return self.car.moving

    def get(self):

        cmd = self.request.path[1:]
        logger.info('path: %s', self.request.path)

        if self.request.path in ('/', 'index.html'):
            self.add_header('Content-Type', 'text/html')
            with open('./assets/index.html') as f:
                return self.write(f.read())

        fn = {
            'forward':self.move,
            'forward_stop':self.moveStop,
            'back': lambda : self.move(False),
            'back_stop': self.moveStop,

            'right':self.turn,
            'right_stop':self.turn,
            'left': lambda : self.turn(False),
            'left_stop': self.turnStop,
              }.get(cmd.lower(), lambda : self.car.stop())

        if not fn:
            res = 'unknown command: %s' % cmd
        else:
            directionX, directionY = self.car.direction

            fn()

            newDirectionX, newDirectionY = self.car.direction
            res = '%s: %s -> %s<br\>%s: %s -> %s' % ('Move', directionY, newDirectionY, 'Turn', directionX, newDirectionX)

        self.add_header('Content-Type', 'text/html')
        return self.write(str(res))

def make_app():
    return tornado.web.Application([
        (r"/.*", MainHandler),
    ])

if __name__ == "__main__":
    Signal.default().setup()
    try:
        app = make_app()
        port = 80 if inPi else 8080
        app.listen(port)
        logger.info('started server on %s...', port)
        tornado.ioloop.IOLoop.current().start()

    except Exception as ex:
        logger.error('server error: %s', ex)
    finally:
        Signal.default().cleanup()