#!/usr/bin/python3 

import json
import time
import RPi.GPIO as GPIO
import sys
import subprocess 

class Relay():
    def __init__(self, pin):
        self.pin = pin
        setGpio(self.pin, 'input')

    def activate(self):
        setGpio(self.pin, 'output')

    def deactivate(self):
        setGpio(self.pin, 'input')

class Thing():
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
        return self.name
        #return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def checkCompleted(self):
        """if we activate the activeport and we receive in the validport, the Thing is solved
        We don't store the status in a class variables because the status of each Thing 
        must be checked each time you want to know the overall status of the puzzle"""

        GPIO.output(self.activePort, True) if self.activePort else None
        # TODO: Change to interrupts
        if GPIO.input(self.validPort):        
            time.sleep(0.8)
            if GPIO.input(self.validPort):
                """ Double check due to false positives"""
                self.completed = True
                print ("Paso completado : ", self.name)
                return True
        else:
            self.completed = False
            print ("Paso completado : ", self.name)
            return False
        GPIO.output(self.activePort, False) if self.activePort else None
        

    def checkReset(self):
        """ Test if the Thing is in its normal(reset) state """ 
        GPIO.output(self.activePort, True)  if self.activePort else None
        for port in self.inputPorts:
            if GPIO.input(port):
                print(self.name, ' NO Reseteado', ' port: ', port)
                return False
            else:
                print(self.name, ' Reseteado')
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
            # print('Puzzle Wires Completed')
            return True


    def checkReset(self):
        """ All Thing.checkReset() must be true """
        self.reset = []
        for step in self.steps:
            self.reset.append(step.checkReset())
        if False in self.reset:
            return False
            print ("Paso NO completado : ", self.name)
        else:
            print ("Paso completado : ", self.name)
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
        print(game.secuence)
        for step in ( step for step in game.secuence if game.secuence.index(step) < game.currentStep ):
            print(step.name)
            """ iterate for each game step until the current one """
            while currentCheck == False: 
                if step.checkCompleted():
                    currentCheck = True
                else:
                    currentCheck = False
                time.sleep(0.2)
            currentCheck = False
            game.currentStep +=1	

        
        relay.activate() 
        playEnd()
        for step in game.secuence:
            while not step.checkReset():
                time.sleep(0.5)

            for step in game.secuence:
                step.completed = False

            relay.deactivate()


    # TODO:Only play once. Wait for a button pressed



if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    movie=("/data/precuelaGotham.mp4")

    relay = Relay(38)

    wire1 = Thing(37, 7, name = 'paso 4.a')
    wire2 = Thing(21, 5, name = 'paso 4.b')
    wiresPuzzle1 = WiresPuzzle(wire1, wire2, name = 'Conexiones1')
    
    selector1 = Thing(None, 10, 12 ,name = 'on/off')

    wire3 = Thing(3, 33, name = 'paso 6.a')
    wire4 = Thing(19, 15, name = 'paso 6.b')
    wiresPuzzle2 = WiresPuzzle(wire1, wire2, name = 'Conexiones2')

    switch1 = Thing(None, 16, name = 'on/off')

    gameSecuence = [ wiresPuzzle1, selector1, wiresPuzzle2, switch1 ]
    game = Game(gameSecuence)

    main()

    GPIO.cleanup()
