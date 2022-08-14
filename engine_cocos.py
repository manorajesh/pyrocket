import cocos
from cocos.director import director
import cocos.euclid as eu
import numpy as np
from kelvin_table import kelvin_table

BACKGROUND = BLACK = (0, 0, 0)
DAMPING = 0.50
SCREEN = WIDTH, HEIGHT = 800, 600
HALF_HEIGHT = HEIGHT // 2

class AirParticle(cocos.sprite.Sprite):
    def __init__(self, x, y, velocity=(20, 1)):
        super().__init__("particle.png")
        self.pos = np.array([x, y], dtype=np.float64)
        self.vel = np.array(velocity, dtype=np.float64)

        self.temperature = 3400 # Kelvin
        self.position = self.pos

class MainLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.particles = []
        
        for i in range(100):  
            self.particle = AirParticle(0, np.random.randint(HALF_HEIGHT-30, HALF_HEIGHT+30))
            self.add(self.particle, i)

if __name__ == "__main__":
    director.init(width=WIDTH, height=HEIGHT, caption="Air Simulation")
    main_scene = cocos.scene.Scene()
    sim_layer = MainLayer()
    main_scene.add(sim_layer)
    director.run(main_scene)