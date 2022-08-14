import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

WIDTH = 100
HEIGHT = 100

def lerp(a, b, k):
    return a + k * (b - a)

class Air():
    def __init__(self):
        self.density = np.zeros((WIDTH, HEIGHT))
        self.velocity = np.zeros((WIDTH, HEIGHT))
        self.time = 0

    def diffusion(self, x, y):
        k = 1 # amount of diffusion
        s = (self.density[x-1, y] + self.density[x+1, y] + self.density[x, y-1] + self.density[x, y+1])/4
        self.density[x, y] = self.density[x, y] + k * (s - self.density[x, y])

    def advection(self, x, y):
        origin_density = [x, y] - self.velocity[x, y]
        j, i = np.modf(origin_density)
        i = np.asarray(i, dtype=int)
        j = np.asarray(j*100, dtype=int)
        z1 = lerp(self.density[i[0], i[1]], self.density[i[0]+1, i[1]], j[0])
        z2 = lerp(self.density[i[0], i[1]+1], self.density[i[0]+1, i[1]+1], j[0])
        self.density[x, y] = lerp(z1, z2, j[1])

    def clearing_divergence(self, x, y):
        self.velocity[x, y] = (self.velocity[x-1, y] + self.velocity[x+1, y] + self.velocity[x, y-1] + self.velocity[x, y+1]) / 4

    def update(self):
        for x in range(1, WIDTH-1):
            for y in range(1, HEIGHT-1):
                self.diffusion(x, y)
                self.advection(x, y)
                #self.clearing_divergence(x, y)
        self.time += 1

if __name__ == "__main__":
    air = Air()
    for i in range(100):
        air.density[i, i] = 1
        air.velocity[i, i] = 1
    fig, ax = plt.subplots()
    im = ax.imshow(air.density, cmap='hot', interpolation='nearest')
    def update(frame):
        air.update()
        im.set_array(air.density)
        return [im]
    ani = FuncAnimation(fig, update, blit=True)
    plt.show()