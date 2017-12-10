from motor import Motor
from lib.gpio import Signal, inPi
import lib.logging as logger

class Diagnostics():

    def __init__(self):
        self.fwdBackMotor = Motor(Motor.MOVE)
        self.turnMotor = Motor(Motor.TURN)

    def moveFwdThenBack(self, stop=True):
        thenWait = 2 if inPi else 0.5
        self.fwdBackMotor.moveForward(thenWait=thenWait)
        self.fwdBackMotor.moveBack(thenWait=thenWait)

        if stop:
            self.fwdBackMotor.stop()

    def turnRightThenLeft(self, stop=True):
        thenWaitTurn = 1 if inPi else 0.5
        self.turnMotor.turnRight(thenWait=thenWaitTurn)
        self.turnMotor.turnLeft(thenWait=thenWaitTurn)
        self.turnMotor.turnRight(thenWait=thenWaitTurn)
        self.turnMotor.turnLeft(thenWait=thenWaitTurn)
        self.turnMotor.turnRight(thenWait=thenWaitTurn)

        if stop:
            self.turnMotor.stop()

    def start(self):
        logger.debug('[Diagnostics] diagnostics starting...')

        with Signal.default().prepared():
            logger.debug('[Diagnostics] #### Performing sequencial run ####')
            self.moveFwdThenBack(stop=True)
            self.turnRightThenLeft()

            logger.debug('[Diagnostics] #### Performing parallel run ####')
            self.moveFwdThenBack(stop=False)
            self.turnRightThenLeft()

            self.turnMotor.stop()

        logger.debug('[Diagnostics] diagnostics complete!')


if __name__ == '__main__':
    Diagnostics().start()