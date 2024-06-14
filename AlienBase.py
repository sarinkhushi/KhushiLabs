import random 
from LightStrip import *


class AlienBase:
    def __init__(self, color=None):
        if color:
            self._color = color
        else:
            colors = [WHITE, RED, YELLOW, BLUE]
            self._color = random.choice(colors)
    def getColor(self):
        return self._color 