import cocos
import numpy as np
from kelvin_table import kelvin_table

class AirParticle():
    def __init__(self, x, y, velocity=(20, 1)):
        self.pos = np.array([x, y], dtype=np.float64)
        self.vel = np.array(velocity, dtype=np.float64)

        self.temperature = 3400 # Kelvin
        self.particle = cocos.draw.Circle(x, y, 1, color=kelvin_table[self.temperature])

    def update(self):
        pass