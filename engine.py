import pygame
import numpy as np
from kelvin_table import kelvin_table

BACKGROUND = BLACK = (0, 0, 100)
DAMPING = 0.50
SCREEN = WIDTH, HEIGHT = 800, 600
HALF_HEIGHT = HEIGHT // 2

class AirParticle(pygame.sprite.Sprite):
    def __init__(self, x, y, nozzle, velocity=(20, 1)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("particle.png")
        self.image = pygame.transform.scale(self.image, (5, 5))
        self.rect = self.image.get_rect()
        self.image.fill(BACKGROUND)
        self.pos = np.array([x, y], dtype=np.float64)
        self.vel = np.array(velocity, dtype=np.float64)
        self.size = np.array(self.image.get_size(), dtype=np.float64)

        self.nozzle_rect = nozzle.get_rect()

        self.temperature = 6000 # Kelvin
        self.opacity = 255
        self.image.fill(kelvin_table[self.temperature])

    def update(self):
        collisions = pygame.sprite.spritecollide(self, self.groups()[0], False)
        if self.rect.colliderect(self.nozzle_rect):
            #self.vel *= -1 * DAMPING
            pass
        for collision in collisions:
            if collision is not self:
                self.vel += collision.vel * DAMPING
                collision.vel = -self.vel

        self.vel += np.random.randint(-1, 2, 2)
        self.pos += self.vel

        if self.pos[0] < 0 or self.pos[0] > WIDTH:
            self.vel[0] *= -1 * DAMPING
        if self.pos[1] < 0 or self.pos[1] > HEIGHT:
            self.vel[1] *= -1 * DAMPING

        self.temperature -= 100

        screen.fill(BACKGROUND)
        try:
            self.image.fill(kelvin_table[self.temperature])
        except KeyError:
            self.temperature = 900
            self.opacity -= 5
            self.image.set_alpha(self.opacity)
            if self.opacity <= 0:
                self.kill()
        self.size = abs(self.size - 0.1)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect.center = self.pos

class Engine(pygame.sprite.Sprite):
    def __init__(self):
        self.nozzle = pygame.image.load("engine_nozzle.png").convert_alpha()
        self.nozzle = pygame.transform.scale(self.nozzle, (750, 500))
        self.particles = pygame.sprite.Group()

    def update(self):
        self.particles.add(AirParticle(50, np.random.randint(HALF_HEIGHT-20, HALF_HEIGHT+20), self.nozzle))
        self.particles.update()
        self.particles.draw(screen)
        screen.blit(engine.nozzle, (-100, 0))

class FPS(pygame.sprite.Sprite):
    def __init__(self):
        self.font = pygame.font.SysFont("monospace", 15)
        self.fps = 0
        self.last = 0

    def update(self):
        self.fps = int(clock.get_fps())
        self.last += 1
        if self.last == 60:
            self.last = 0
            print(self.fps)
        
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SCREEN)
    pygame.display.set_caption("Engine")
    pygame.display.set_icon(pygame.image.load("icon.png"))

    clock = pygame.time.Clock()
    engine = Engine()
    fps = FPS()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        engine.update()
        fps.update()
        pygame.display.flip()
        clock.tick(60)