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

        if self.direction in (Car.DIRECTION_LFT, Car.DIRECTION_RGT, Car.TURN_STOP):
            self._direction = (newVal, self._direction[1])
        else:
            self._direction = (self._direction[0], newVal)

CAR = RoboCar()

class MainHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.car = CAR

    def toggleMove(self, fwd=True):
        if self.car.direction[1] in (Car.DIRECTION_FWD, Car.DIRECTION_BCK):
            self.car.direction = Car.MOVE_STOP
        else:
            self.car.direction = Car.DIRECTION_FWD if fwd else Car.DIRECTION_BCK

        return self.car.moving

    def toggleTurn(self, right=True):
        if self.car.direction[0] in (Car.DIRECTION_RGT, Car.DIRECTION_LFT):
            self.car.direction = Car.TURN_STOP
        else:
            self.car.direction = Car.DIRECTION_RGT if right else Car.DIRECTION_LFT

        return self.car.moving

    def get(self):

        cmd = self.request.path[1:]
        logger.info('path: %s', self.request.path)

        fn = {
            'forward':self.toggleMove,
            'forward_stop':self.toggleMove,
            'back': lambda : self.toggleMove(False),
            'back_stop': lambda : self.toggleMove(False),

            'right':self.toggleTurn,
            'right_stop':self.toggleTurn,
            'left': lambda : self.toggleTurn(False),
            'left_stop': lambda : self.toggleTurn(False),
              }.get(cmd.lower())

        if not fn:
            res = 'unknown command: %s' % cmd
        else:
            directionX, directionY = self.car.direction

            fn()

            newDirectionX, newDirectionY = self.car.direction
            res = '%s: %s -> %s<br\>%s: %s -> %s' % ('Move', directionY, newDirectionY, 'Turn', directionX, newDirectionX)

        self.add_header('Content-Type', 'text/html')
        self.write(str(res))

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
        logger.info('stared server on %s...', port)
        tornado.ioloop.IOLoop.current().start()

    except Exception as ex:
        logger.error('server error: %s', ex)
    finally:
        Signal.default().cleanup()