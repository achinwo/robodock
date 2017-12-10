from motor import Motor
from lib.gpio import Signal, inPi


def diagnostics():
    print('diagnostics starting...')

    thenWait = 2 if inPi else 1

    with Signal.default().prepared():
        fwdBackMotor = Motor(Motor.MOVE)
        turnMotor = Motor(Motor.TURN)

        fwdBackMotor.moveForward(thenWait=thenWait)
        fwdBackMotor.moveBack(thenWait=thenWait)

        turnMotor.turnRight(thenWait=thenWait)
        turnMotor.turnLeft(thenWait=thenWait)

        fwdBackMotor.stop()

if __name__ == '__main__':
    diagnostics()