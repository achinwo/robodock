from motor import Motor
from lib.gpio import Signal


def diagnostics():
    print('diagnostics starting...')

    with Signal.default().prepared():
        fwdBackMotor = Motor(Motor.MOVE)

        fwdBackMotor.moveForward(thenWait=2)
        fwdBackMotor.stop()

if __name__ == '__main__':
    diagnostics()