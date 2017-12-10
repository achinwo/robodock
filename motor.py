import logging as logger
from lib.gpio import Signal

class Motor():

    AXIS_X = "LEFT_RIGTH"
    AXIS_Y = "FRONT_BACK"

    def __init__(self, axis):
        assert axis in (self.AXIS_X, self.AXIS_Y), "valid axis are Motor.AXIS_X and Motor.AXIS_Y"
        self._axis = axis

    def axisUp(self):
        print(Signal.default)

    def axisDown(self):
        pass

    def moveForward(self):
        self.axisUp()

    def moveBack(self):
        self.axisDown()

    def turnLeft(self):
        self.axisUp()

    def turnRight(self):
        self.axisDown()

    @property
    def type(self):
        return self._axis