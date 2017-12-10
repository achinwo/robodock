import lib.logging as logger

from lib.gpio import Signal, Pin
import time

class Motor():

    TURN = 'LEFT_RIGTH'
    MOVE = 'FRONT_BACK'

    def __init__(self, axis, verbose=True):
        self.verbose = verbose

        assert axis in (self.TURN, self.MOVE), "valid axis are Motor.AXIS_X and Motor.AXIS_Y"
        self._axis = axis

    @property
    def signal(self):
        return Signal.default()

    def axis(self, directionUp, thenWait=0):

        if directionUp:
            if self.type == Motor.MOVE:
                self.signal.on(Pin.DEFAULT_FWD_AXIS_UP)
                self.signal.off(Pin.DEFAULT_FWD_AXIS_DWN)
            elif self.type == Motor.TURN:
                self.signal.on(Pin.DEFAULT_SIDES_AXIS_UP)
                self.signal.off(Pin.DEFAULT_SIDES_AXIS_DWN)
            else:
                RuntimeError("invalid motor definition: %s" % self.type)
        else:
            if self.type == Motor.MOVE:
                self.signal.on(Pin.DEFAULT_FWD_AXIS_DWN)
                self.signal.off(Pin.DEFAULT_FWD_AXIS_UP)
            elif self.type == Motor.TURN:
                self.signal.on(Pin.DEFAULT_SIDES_AXIS_DWN)
                self.signal.off(Pin.DEFAULT_SIDES_AXIS_UP)
            else:
                RuntimeError("invalid motor definition: %s" % self.type)

        if thenWait:

            if self.verbose:
                logger.debug('[Motor(%s)] waiting %s seconds', self.type, thenWait)

            time.sleep(thenWait)

    def moveForward(self, *args, **kwargs):
        if self.verbose:
            logger.debug('[Motor(%s)] move forward', self.type)

        self.axis(True, *args, **kwargs)

    def moveBack(self, *args, **kwargs):
        if self.verbose:
            logger.debug('[Motor(%s)] move backwards', self.type)

        self.axis(False, *args, **kwargs)

    def turnLeft(self, *args, **kwargs):
        if self.verbose:
            logger.debug('[Motor(%s)] turn left', self.type)

        self.axis(False, *args, **kwargs)

    def turnRight(self, *args, **kwargs):
        if self.verbose:
            logger.debug('[Motor(%s)] turn right', self.type)

        self.axis(True, *args, **kwargs)

    def stop(self):
        if self.verbose:
            logger.debug('[Motor(%s)] stopping...', self.type)

        if self.type == Motor.MOVE:
            self.signal.off(Pin.DEFAULT_FWD_AXIS_UP)
            self.signal.off(Pin.DEFAULT_FWD_AXIS_DWN)
        elif self.type == Motor.TURN:
            self.signal.off(Pin.DEFAULT_SIDES_AXIS_UP)
            self.signal.off(Pin.DEFAULT_SIDES_AXIS_DWN)
        else:
            RuntimeError("invalid motor definition: %s" % self.type)

        if self.verbose:
            logger.debug('[Motor(%s)] stopped', self.type)

    @property
    def type(self):
        return self._axis


if __name__ == '__main__':
    print(Signal.default)