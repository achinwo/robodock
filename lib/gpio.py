import logging as logger

class GPIO(): #TODO { anthony } - add dependency to project
    pass

class Pin():

    DEFAULT_FWD_AXIS_UP = 18 # forward
    DEFAULT_FWD_AXIS_DWN = 23 # back

    DEFAULT_SIDES_AXIS_UP = 16 # left
    DEFAULT_SIDE_AXIS_DWN = 21 # right

    @property
    @staticmethod
    def all():
        return {16:'DEFAULT_SIDES_AXIS_UP',
                21:'DEFAULT_SIDE_AXIS_DWN',
                18:'DEFAULT_FWD_AXIS_UP',
                23:'DEFAULT_FWD_AXIS_DWN'
                }

    @classmethod
    def toName(cls, value:int):
        return cls.all[value]

class Signal():

    INSTANCE = None

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.pinStates = {}


    def _changePinValue(self, pin:int, value:bool):
        GPIO.output(pin, value)
        self.pinStates[pin] = value

        if self.verbose:
            oldValue = self.pinStates.get(pin)
            logger.debug('Pin changed: %s -> %s', pin, value)

    def off(self, pin:int):
        self._changePinValue(False)

    def on(self, pin:int):
        self._changePinValue(True)

    @property
    @classmethod
    def default(cls):
        instance = cls.INSTANCE

        if instance is None:
            instance = cls.INSTANCE = cls()

        return instance



