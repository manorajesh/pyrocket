import pyglet
from kelvin_table import kelvin_table
import numpy as np

SCREEN = WIDTH, HEIGHT = 800, 600
HALF_HEIGHT = HEIGHT // 2

class AirParticle():
    def __init__(self, x, y, velocity=(20, 1)):
        self.pos = np.array([x, y], dtype=np.float64)
        self.vel = np.array(velocity, dtype=np.float64)

        self.temperature = 3400 # Kelvin
        self.particle = pyglet.shapes.Circle(x, y, 1, color=kelvin_table[self.temperature])

    def update(self):
        if self.vel[0] < 0 or self.vel[0] > WIDTH:
            self.vel[0] *= -1 * 0.90
        if self.vel[1] < 0 or self.vel[1] > HEIGHT:
            self.vel[1] *= -1 * 0.90

        self.pos += self.vel

        self.particle.x = self.pos[0]
        self.particle.y = self.pos[1]

if __name__ == "__main__":
    window = pyglet.window.Window(width=WIDTH, height=HEIGHT)
    particles = []
    @window.event
    def on_draw():
        window.clear()
        for particle in particles:
            particle.particle.draw()
    def update(dt):
        particles.append(AirParticle(0, np.random.randint(HALF_HEIGHT-30, HALF_HEIGHT+30)))
        for particle in particles:
            particle.update()
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()