"""
A basic template file for using the Model class in PicoLibrary
This will allow you to implement simple Statemodels with some basic
event-based transitions.

Currently supports only 4 buttons (hardcoded to BTN1 through BTN4)
and a TIMEOUT event for internal tranisitions.

For processing your own events such as sensors, you can implement
those in your run method for transitions based on sensor events.
"""

# Import whatever Library classes you need - Model is obviously needed
import time
import random
from StateModel import *
from Button import *
from Counters import *
from Log import *
from Buzzer import *
from Instruments import *
from LightStrip import *
from Displays import *
"""
This is the template Model Runner - you should rename this class to something
that is supported by your class diagram. This should associate with your other
classes, and any PicoLibrary classes. If you are using Buttons, you will implement
buttonPressed and buttonReleased.

To implement the model, you will need to implement 3 methods to support entry actions,
exit actions, and state actions.

This template currently implements a very simple state model that uses a button to
transition from state 0 to state 1 then a 5 second timer to go back to state 0.
"""

class MusicController:

    def __init__(self):
        
        # Instantiate whatever classes from your own model that you need to control
        # Handlers can now be set to None - we will add them to the model and it will
        # do the handling
        self._button1 = Button(10, "white", buttonhandler=None)
        self._button2 = Button(11, "red", buttonhandler=None)
        self._button3 = Button(12, "yellow", buttonhandler=None)
        self._button4 = Button(13, "blue", buttonhandler=None)
        self._button5 = Button(14, "black", buttonhandler=None)

        self._lightstrip = LightStrip(pin = 2, numleds = 16)

        self._display = LCDDisplay(sda = 0, scl = 1, i2cid = 0)

        self._buzzer = PassiveBuzzer(16)
        self._instrument = Organ()
        self._instrumentno = 0


        # self._timer = SoftwareTimer(None)
        
        # Instantiate a Model. Needs to have the number of states, self as the handler
        # You can also say debug=True to see some of the transitions on the screen
        # Here is a sample for a model with 4 states
        self._model = StateModel(10, self, debug=True)
        
        # Up to 5 buttons and a timer can be added to the model for use in transitions
        # Buttons must be added in the sequence you want them used. The first button
        # added will respond to BTN1_PRESS and BTN1_RELEASE, for example
        self._model.addButton(self._button1)
        self._model.addButton(self._button2)
        self._model.addButton(self._button3)
        self._model.addButton(self._button4)
        self._model.addButton(self._button5)

        # add other buttons (up to 3 more) if needed
        
        # Add any timer you have.
        # self._model.addTimer(self._timer)
        
        # Now add all the transitions that are supported by my Model
        # obvously you only have BTN1_PRESS through BTN4_PRESS
        # BTN1_RELEASE through BTN4_RELEASE
        # and TIMEOUT
        
        # some examples:

        # state 1
        self._model.addTransition(0, [BTN1_PRESS], 1)
        self._model.addTransition(1, [BTN1_RELEASE], 0)

        # state 2
        self._model.addTransition(0, [BTN2_PRESS], 2)
        self._model.addTransition(2, [BTN2_RELEASE], 0)

        # state 3
        self._model.addTransition(0, [BTN3_PRESS], 3)
        self._model.addTransition(3, [BTN3_RELEASE], 0)

        # state 4
        self._model.addTransition(0, [BTN4_PRESS], 4)
        self._model.addTransition(4, [BTN4_RELEASE], 0)

        # state 5        
        self._model.addTransition(1, [BTN2_PRESS], 5)
        self._model.addTransition(5, [BTN2_RELEASE], 1)

        self._model.addTransition(2, [BTN1_PRESS], 5)
        self._model.addTransition(5, [BTN1_RELEASE], 2)

        # state 6
        self._model.addTransition(2, [BTN3_PRESS], 6)
        self._model.addTransition(6, [BTN3_RELEASE], 2)

        self._model.addTransition(3, [BTN2_PRESS], 6)
        self._model.addTransition(6, [BTN2_RELEASE], 3)

        #state 7
        self._model.addTransition(3, [BTN4_PRESS], 7)
        self._model.addTransition(7, [BTN4_RELEASE], 3)

        self._model.addTransition(4, [BTN3_PRESS], 7)
        self._model.addTransition(7, [BTN3_RELEASE], 4)

        # state 8
        self._model.addTransition(1, [BTN4_PRESS], 8)
        self._model.addTransition(8, [BTN4_RELEASE], 1)

        self._model.addTransition(4, [BTN1_PRESS], 8)
        self._model.addTransition(8, [BTN1_RELEASE], 4)
        
        # state 9
        self._model.addTransition(0, [BTN5_PRESS], 9)
        self._model.addTransition(9, [NO_EVENT], 0)
        
        # self._model.addTransition(1, [TIMEOUT], 0)
        # etc.
    
    def changeInstrument(self):
        if self._instrumentno == 0:
            self._instrumentno = 1
            self._instrument = Violin()
            print('Instrument changed to Violin')
            
        elif self._instrumentno == 1:
            self._instrumentno = 2
            self._instrument = Bass()
            print('Instrument changed to Bass')

        elif self._instrumentno == 2:
            self._instrumentno = 3
            self._instrument = Piano()
            print('Instrument changed to Piano')
        
        elif self._instrumentno == 3:
            self._instrumentno = 0
            self._instrument = Organ()
            print('Instrument changed to Organ')

    """
    Create a run() method - you can call it anything you want really, but
    this is what you will need to call from main.py or someplace to start
    the state model.
    """

    def run(self):
        # The run method should simply do any initializations (if needed)
        # and then call the model's run method.
        # You can send a delay as a parameter if you want something other
        # than the default 0.1s. e.g.,  self._model.run(0.25)
        self._model.run()

    """
    stateDo - the method that handles the do/actions for each state
    """
    def stateDo(self, state):
        pass 

    """
    stateEntered - is the handler for performing entry/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    """
    def stateEntered(self, state, event):
        # Again if statements to do whatever entry/actions you need
        Log.d(f'State {state} entered')
        if state == 0:
            # entry actions for state 0
            pass
        
        elif state == 1:
            self._buzzer.play(self._instrument.getNote(0))
            self._lightstrip.setPixel(pixelno = 0, color = RED)

        elif state == 2:
            self._buzzer.play(self._instrument.getNote(1))
            self._lightstrip.setPixel(pixelno = 1, color = RED)

        elif state == 3:
            self._buzzer.play(self._instrument.getNote(2))
            self._lightstrip.setPixel(pixelno = 2, color = RED)

        elif state == 4:
            self._buzzer.play(self._instrument.getNote(3))
            self._lightstrip.setPixel(pixelno = 3, color = RED)
        
        elif state == 5:
            self._buzzer.play(self._instrument.getNote(4))
            self._lightstrip.setPixel(pixelno = 4, color = RED)
        
        elif state == 6:
            self._buzzer.play(self._instrument.getNote(5))
            self._lightstrip.setPixel(pixelno = 5, color = RED)

        elif state == 7:
            self._buzzer.play(self._instrument.getNote(6))
            self._lightstrip.setPixel(pixelno = 6, color = RED)
        
        elif state == 8:
            self._buzzer.play(self._instrument.getNote(7))
            self._lightstrip.setPixel(pixelno = 7, color = RED)
        
        elif state == 9:
            self.changeInstrument()
            self._lightstrip.on()
            if self._instrumentno == 0:
                self._display.reset()
                self._display.showText('Organ')
            if self._instrumentno == 1:
                self._display.reset()
                self._display.showText('Violin')
            if self._instrumentno == 2:
                self._display.reset()
                self._display.showText('Bass')
            if self._instrumentno == 3:
                self._display.reset()
                self._display.showText('Piano')
            
    """
    stateLeft - is the handler for performing exit/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    
    This is just like stateEntered, perform only exit/actions here
    """

    def stateLeft(self, state, event):
        Log.d(f'State {state} exited')
        if state in range(1,9):
            # exit actions for state 0
            self._buzzer.stop()
            self._lightstrip.off()
        if state == 9:
            self._lightstrip.off()
        # etc.
    