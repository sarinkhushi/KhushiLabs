import time
import random
from StateModel import *
from Button import *
from Counters import *
from Log import *
from AlienBase import *
from Player import *
from Buzzer import *
from LightStrip import *
from Displays import LCDDisplay 
from Songs import *


class GameController:

    def __init__(self):

        self._button1 = Button(10, "white", buttonhandler=None)
        self._button2 = Button(11, "red", buttonhandler=None)
        self._button3 = Button(12, "yellow", buttonhandler=None)
        self._button4 = Button(13, "blue", buttonhandler=None)

        self._lightstrip = LightStrip(pin = 2, numleds = 16)

        self._display = LCDDisplay(sda = 0, scl = 1, i2cid = 0)

        self._buzzer = PassiveBuzzer(16)

        self._song = Song()

        self._timer = SoftwareTimer(handler = self)

        self._alienbase = AlienBase()

        self._player = Player()

        self._player.score = 0
        
        self._allbases = [None]*3

        for x in range(0, 3):
            self._allbases[x] = AlienBase()

        self._model = StateModel(7, self, debug=True)
        
        # BUTTONS
        self._model.addButton(self._button1)
        self._model.addButton(self._button2)
        self._model.addButton(self._button3)
        self._model.addButton(self._button4)

        self._model.addTimer(self._timer)
        
        # TRANSITIONS
        self._model.addTransition(0, [BTN1_PRESS], 1)

        self._model.addTransition(1, [BTN1_PRESS], 2)
        self._model.addTransition(2, [TIMEOUT], 1)

        self._model.addTransition(1, [BTN2_PRESS], 3)
        self._model.addTransition(3, [TIMEOUT], 1)

        self._model.addTransition(1, [BTN3_PRESS], 4)
        self._model.addTransition(4, [TIMEOUT], 1)

        self._model.addTransition(1, [BTN4_PRESS], 5)
        self._model.addTransition(5, [TIMEOUT], 1)

        self._model.addTransition(6, [TIMEOUT], 0)


    def shoot(self, color):
        # defines how a shot happens and what happens when a shot = last base
        if len(self._allbases) > 0:
            lastbase = self._allbases[len(self._allbases) - 1]
            if lastbase.getColor() == color:
                for x in range(0, 16 - len(self._allbases) + 1):
                    self._lightstrip.setPixel(x, color)
                    time.sleep(0.01)
                    self._lightstrip.setPixel(x, BLACK)
                self._song.pointwon()
                self._allbases.pop()
                self._player.score = self._player.score + 1
                self._display.showText(f'Your score is {self._player.score}')
                Log.d(f'Shot an alien base!')
            else:
                for x in range(0, 16 - len(self._allbases)):
                    self._lightstrip.setPixel(x, color)
                    time.sleep(0.01)
                    self._lightstrip.setPixel(x, BLACK)
                self._buzzer.beep(tone=RE)
                Log.d(f'Shot missed!')

    
    def restart(self):
        # restarts the game from the beginning
        for x in range(0, len(self._allbases)):
            totalbases = self._allbases[x]
            if totalbases != None:
                self._lightstrip.setPixel(15-x, BLACK, show=False)
        self._lightstrip.show()
        self._allbases = [None]*3
        for x in range(0, 3):
            self._allbases[x] = AlienBase()
        self._player.score = 0
        Log.d(f'Restarting game...')
    
    def addBases(self):
        self._allbases.append((AlienBase()))

    def showBases(self):
        for x in range(0, len(self._allbases)):
            allbases = self._allbases[x]
            if allbases != None:
                self._lightstrip.setPixel(15-x, allbases.getColor(), show=False)
            self._lightstrip.show()

    def run(self):
        self._model.run()

    """
    stateDo - the method that handles the do/actions for each state
    """
    def stateDo(self, state):
        # Now if you want to do different things for each state you can do it:
        if state == 0:
            # State 0 do/actions
            pass 
        elif state == 1:
            time.sleep(1)
            self.addBases()
            self.showBases()
            self._buzzer.beep()
            if len(self._allbases) == 16:
                self._model.gotoState(6)
            Log.d(f'Adding bases')

    def stateEntered(self, state, event):
        # Again if statements to do whatever entry/actions you need
        Log.d(f'State {state} entered')
        if state == 0:
            self.restart()
            self._display.reset()
            self._display.showText('Alien Invaders!\nWhite to Start!')
            self._song.gamestart()
        
        elif state == 1:
            self.addBases()
            self.showBases()
            if len(self._allbases) == 16:
                self._model.gotoState(6)

        elif state == 2:
            Log.d(f'Shot white')
            self.shoot(WHITE)
            self._timer.start(1)
        
        elif state == 3:
            Log.d(f'Shot red')
            self.shoot(RED)
            self._timer.start(1)
        
        elif state == 4:
            Log.d(f'Shot yellow')
            self.shoot(YELLOW)
            self._timer.start(1)
        
        elif state == 5:
            Log.d(f'Shot blue')
            self.shoot(BLUE)
            self._timer.start(1)

        elif state == 6:
            self._display.reset()
            self._song.gameover()
            self._display.showText(f'GAME OVER \nFINAL SCORE: {self._player.score}')
            Log.d(f'Thanks for playing!')
            self._timer.start(5)
            

    def stateLeft(self, state, event):
        Log.d(f'State {state} exited')
        if state == 0:
            self._display.reset()
        elif state in (1,2,4,5,6):
            self._timer.cancel()
    

if __name__ == '__main__':
    GameController().run()