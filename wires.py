import time
import RPi.GPIO as GPIO
import sys
import subprocess 

class Thing(object):
    instances = []
    """Class that will handle a button,selector, switch, etc"""

    def __init__(self, activePort, validPort, *passivePorts):
        self.activePort = activePort
        self.validPort = validPort
        self.passivePorts = passivePorts
        Thing.instances.append(self)

        # input ports are the ones that could receive voltaje that is valid plus passive ports
        self.inputPorts = list(passivePorts)
        self.inputPorts.append(validPort)

        setGpio(inputPorts, "input")
        setGpio(activePort, "output")

    def checkCompleted(self):
        """if we activate the activeport and we receive in the validport, the Thing is solved"""
        """ We don't store the status in a class variables because the status of each Thing 
        must be checked each time you want to know 
        the overall status of the puzzle"""

        GPIO.output(self.activePort, True)
        # TODO: Change to interrupts
        if GPIO.input(self.validPort):        
            return True
        else:
            return False
        GPIO.output(self.activePort, False)
        

    def checkReset(self):
       """Test if the Thing is in its normal(reset) state""" 
        GPIO.output(self.activePort, True)
        for port in self.inputPorts:
            if GPIO.input(port):
                return False
            else:
                return True



class WiresPuzzle(Thing):
    """handle a wires puzzle composed for various Things"""
    """This puzzle could be something like a pairs of female-female connectors plus more 
    connectors dummies (connected as passive ports) and pairs of wires male-male"""
    ##TODO: Eliminate append instance
    def __init__(self, steps):
        """ steps is a tuple that contain n Things"""
        self.steps = steps

    def __len__(self):
        return len(self.steps)

    def checkCompleted(self):
        """all Things must be completed at the same time """
        for thing in self.steps:
            if thing.checkCompleted() == False:
                return False
            else:
                return True


class Game:
    """This class will handle the data of the game"""
    pass


def setGpio(gpiolist, io):
    """ set a gpio or list of them as input or output mode """
    if io == "input":
        GPIO.setup(gpiolist, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    elif io == "output":
        GPIO.setup(gpiolist, GPIO.OUT , initial=GPIO.LOW)


GPIO.setmode(GPIO.BOARD)
movie=("/data/precuelaGotham.mov")

def playEnd():
    subprocess.run(['killall', 'omxplayer.bin'])
    omxc =  subprocess.Popen(['omxplayer', '-b', movie])

def checkReset(gpiosUsed):
    for pin in gpiosUsed:
        checkcombinations=gpios
        
def main():
    playing = False
    test=Thing(40,38)
    while True:
        time.sleep(0.2)
        if (test.checkCompleted()) and  (playing==False):
            playEnd()
            playing=True

    # TODO:Only play once. Wait for a button pressed
    GPIO.cleanup()


if __name__ == "__main__":
    main()
