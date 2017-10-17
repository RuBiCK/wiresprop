import json
import time
import RPi.GPIO as GPIO
import sys
import subprocess 

class Thing(object):
    instances = []
    """Class that will handle a button,selector, switch, etc"""

    def __init__(self, activePort, validPort, *passivePorts, **kwargs):
        """ setup pin modes of the Thing
        'None' active port, means that there is no active port because it takes +5v directly and has no 
        possibity to mix with other things like connecting wires"""
        self.activePort = activePort if activePort else None 
        self.validPort = validPort
        self.passivePorts = passivePorts

        for k,v in kwargs.items():
            setattr(self,k,v)
        Thing.instances.append(self)

        # input ports are the ones that could receive voltaje that is valid plus passive ports
        self.inputPorts = list(passivePorts)
        self.inputPorts.append(validPort)

        setGpio(self.inputPorts, "input")
        setGpio(self.activePort, "output") if self.activePort else None


    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def checkCompleted(self):
        """if we activate the activeport and we receive in the validport, the Thing is solved
        We don't store the status in a class variables because the status of each Thing 
        must be checked each time you want to know 
        the overall status of the puzzle"""

        GPIO.output(self.activePort, True) if self.activePort else None
        # TODO: Change to interrupts
        if GPIO.input(self.validPort):        
            self.completed = True
            return True
        else:
            self.completed = False
            return False
        GPIO.output(self.activePort, False) if self.activePort else None
        

    def checkReset(self):
        """ Test if the Thing is in its normal(reset) state """ 
        GPIO.output(self.activePort, True)  if self.activePort else None
        for port in self.inputPorts:
            if GPIO.input(port):
                print('Reset no realizado en ', self.name)
                return False
            else:
                return True



class WiresPuzzle():
    """handle a wires puzzle composed for various Things"""
    """This puzzle could be something like a pairs of female-female connectors plus more 
    connectors dummies (connected as passive ports) and pairs of wires male-male"""
    ##TODO: Eliminate append instance
    def __init__(self, *steps, **kwargs):
        """ steps is a tuple that contain Things"""
        self.steps = steps
        self.completed = False
        for k,v in kwargs.items():
            setattr(self,k,v)

    def __len__(self):
        return len(self.steps)

    def checkCompleted(self):
        """all Things must be completed at the same time """
        self.status = []

        for step in self.steps:
            self.status.append(step.checkCompleted())

        """ If there is at least one False, the puzzle is considered not compelted """
        if False in self.status:
            return False
        else:
            self.completed = True
            print('Puzzle Wires Completed')
            return True


    def checkReset(self):
        """ All Thing.checkReset() must be true """
        self.reset = []
        for step in self.steps:
            self.reset.append(step.checkReset())
        if False in self.reset:
            return False
        else:
            print(self.name,' completed')
            return True



class Game:
    """This class will handle the data of the game"""

    def __init__(self,gameSecuence):
        self.secuence = gameSecuence
        self.currentStep = 1
        self.startTimestamp = time.strftime("%d/%m/%Y") + time.strftime("%H:%M:%S")  


    def __len__(self):
        return len(self.secuence)


def setGpio(gpiolist, io):
    """ set a gpio or list of them as input or output mode """
    if io == "input":
        GPIO.setup(gpiolist, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    elif io == "output":
        GPIO.setup(gpiolist, GPIO.OUT , initial=GPIO.LOW)


def playEnd():
    subprocess.run(['killall', 'omxplayer.bin'])
    omxc =  subprocess.run(['omxplayer', '-b', movie])

def main():
    playingMovie = False
    while True:
        currentCheck = False
        print('\n')
        for step in ( step for step in game.secuence if game.secuence.index(step) < game.currentStep ):
            """ iterate for each game step until the current one """
            while currentCheck == False: 
                if step.checkCompleted():
                    currentCheck = True
                else:
                    currentCheck = False
                print("Current Puzzle: " , step.name,'\nRealizado: ', step.completed, '\nsecuenceindex:',game.secuence.index(step),'\nchecknow:',step.checkCompleted())
                time.sleep(0.8)
            currentCheck = False
            print('pre +1step',game.currentStep)
            game.currentStep +=1	

        
        
        playEnd()
        for step in game.secuence:
            print(step.name)
            while not step.checkReset():
                print('no reseteado')
                time.sleep(0.8)
            print('reseteado')

    # TODO:Only play once. Wait for a button pressed



if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    movie=("/data/precuelaGotham.mov")

    #seleccionador = Thing(38, 40, 36, 32, name = 'seleccionador')
    wire1 = Thing(35, 37, name = 'paso1.1')
    wire2 = Thing(31, 33, name = 'paso1.2')
    wiresPuzzle1 = WiresPuzzle(wire1, wire2, name = 'Conexiones1')

    wire3 = Thing(38, 40, name = 'paso2.1')
    wire4 = Thing(32, 36, name = 'paso2.2')
    wiresPuzzle2 = WiresPuzzle(wire3, wire4, name = 'Conexiones2')
    
    switch1 = Thing(None, 23, name = 'switch')
    #interruptor = Thing(None,40, name = 'encendido')
    gameSecuence = [ wiresPuzzle1, switch1, wiresPuzzle2 ]
    game = Game(gameSecuence)

    main()

    GPIO.cleanup()
