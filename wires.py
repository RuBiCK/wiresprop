import time
import RPi.GPIO as GPIO
import sys
import subprocess 

class Thing(object):
    instances = []
    """Class that will handle a button,selector,etc"""

    def __init__(self, activePort, validPort, *passivePorts):
        self.activePort = activePort
        self.validPort = validPort
        self.passivePorts = passivePorts
        Thing.instances.append(self)
        inputPorts = list(passivePorts)
        inputPorts.append(validPort)

        setInputGpios(inputPorts)
        #TODO: Set output gpios
        #TODO: change setInputGpios for input/output function

    def CheckCompleted(self):
        pass


    def CheckReset(self):
        pass



class WiresArray(Thing):
    """handle a wires puzzle composed for various Things"""
    ##TODO: Eliminate append instance
    pass

class Game:
    """This class will handle the data of the game"""
    pass


def setInputGpios(gpiolist):
    GPIO.setup(gpiolist, GPIO.IN)

GPIO.setmode(GPIO.BOARD)

combinations = [[1, 2], [3, 4], [5, 6]]
gpiosUsed = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
wires = len(combinations)
movie=("/data/movie")





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
    subprocess.run('killall omxplayer.bin')
    omxc =  subprocess.Popen(['omxplayer', '-b', movie])

def checkReset(gpiosUsed):
    for pin in gpiosUsed:
        checkcombinations=gpios
        
def main():

    while correctCombinations < wires:
        correctCombinations = 0
        setInputGpios()
        for pair in combinations:
            checkPairStatus(pair)

    time.sleep(0.2)
    playEnd()
    # TODO:Only play once. Wait for a button pressed
    GPIO.cleanup()


#if __name__ == "__main__":
#    main()
