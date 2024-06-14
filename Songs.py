import time
from Buzzer import *

class Song:
    """
    class for playing game related songs / jingles using a passive buzzer
    """
    def __init__(self):
        # init song class with buzzer attribute
        self.buzzer = PassiveBuzzer(16)

    def play_jingle(self, notes, durations):
        # plays sequence of notes w/ specified durations
        if len(notes) != len(durations):
            raise ValueError("Number of notes must match number of durations")

        for note, duration in zip(notes, durations):
            self.buzzer.play(tone=note)
            time.sleep(duration)
        self.buzzer.stop()

    def gamestart(self):
        # plays a simple song indicating the start of the game
        gsnotes = [DO, MI, SO]
        gsdurations = [0.25, 0.25, 0.25]  
        self.play_jingle(gsnotes, gsdurations)

    def gameover(self):
        # sad song for game over 
        gonotes = [LA, FA, DO]
        godurations = [0.25, 0.25, 0.25]  
        self.play_jingle(gonotes, godurations)

    def pointwon(self):
        # upbeat song for point won
        pwnotes = [MI, RE, DO]
        pwdurations = [0.1, 0.1, 0.1]  
        self.play_jingle(pwnotes, pwdurations)
