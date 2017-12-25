import lib.logging as logger
from contextlib import contextmanager

class MockGPIO():
    BCM = 1

    OUT = 'OUT'

    @staticmethod
    def setup(*args):
        pass

    @staticmethod
    def cleanup(*args):
        pass

    @staticmethod
    def output(*args):
        pass

    @staticmethod
    def setmode(*args):
        pass

try:
    import RPi.GPIO as GPIO
    inPi = True
except ImportError as error:
    inPi = False
    GPIO = MockGPIO

class Pin():

    DEFAULT_FWD_AXIS_UP = 18 # forward
    DEFAULT_FWD_AXIS_DWN = 23 # back

    DEFAULT_SIDES_AXIS_UP = 16 # left
    DEFAULT_SIDES_AXIS_DWN = 21 # right

    @staticmethod
    def all():
        return {16:'DEFAULT_SIDES_AXIS_UP',
                21:'DEFAULT_SIDES_AXIS_DWN',
                18:'DEFAULT_FWD_AXIS_UP',
                23:'DEFAULT_FWD_AXIS_DWN'
                }

    @classmethod
    def toName(cls, value):
        return cls.all()[value]

class Signal():

    INSTANCE = None

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.pinStates = {}
        self.mode = GPIO.BCM

    @contextmanager
    def prepared(self):

        if self.verbose:
            logger.debug('[Signal] preparing GPIO dirver (inPi=%s)', inPi)

        self.setup()
        yield
        self.cleanup()

    def setup(self):
        GPIO.setmode(self.mode)

        for pin in Pin.all():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

        if self.verbose:
            logger.debug('[Signal#setup] GPIO setup complete')

    def cleanup(self):
        GPIO.cleanup()

        if self.verbose:
            logger.debug('[Signal#cleanup] GPIO cleanup complete')

    def _changePinValue(self, pin, value):
        GPIO.output(pin, value)

        oldValue = self.pinStates.get(pin, '<NO_VALUE>')
        self.pinStates[pin] = value

        if self.verbose:
            logger.debug('[Signal] Pin %s(%s) changed: %s -> %s', Pin.toName(pin), pin, oldValue, value)

    def off(self, pin):
        self._changePinValue(pin, False)

    def on(self, pin):
        self._changePinValue(pin, True)

    @classmethod
    def default(cls):
        instance = cls.INSTANCE

        if instance is None:
            instance = cls.INSTANCE = cls()

        return instance



