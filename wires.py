import time
import Rpi.GPIO as GPIO
import sys
import os from subprocess 
import Popen

combinations = [[1, 2], [3, 4], [5, 6]]
gpiosUsed = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
wires = len(combinations)
movie=("/data/movie")

correctCombinations = 0
GPIO.setmode(GPIO.BOARD)


def setInputGpios(gpiolist):
    GPIO.setup(gpiolist, GPIO.IN)


def checkPairStatus(pair):
    # One wire has one source and one destination. 
    # The source will be used to send high signal and dst will read 
    srcPin = pair.pop()
    dstPin = pair.pop()
    GPIO.setup(srcPin, GPIO.OUT , initial=GPIO.HIGH)
    dstInputStatus=GPIO.input(dstPin)


    if dstInputStatus == 1:
        correctCombinations += 1

    SetInputGpios([scrPint,dstPin])


def playEnd():
    os.system('killall omxplayer.bin')
    omxc = Popen(['omxplayer', '-b', movie])

def checkReset(gpiosUsed):
    for pin in gpiosUsed:
        checkcombinations=gpios
        


def main():
    setInputGpios(gpiosUsed)

    while correctCombinations < wires:
        correctCombinations = 0
        setInputGpios()
        for pair in combinations:
            checkPairStatus(pair)

    time.sleep(0.2)
    playEnd()
    # TODO:Only play once. Wait for a button pressed
    GPIO.cleanup()


if __name__ == "__main__":
    main()
