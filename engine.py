import pygame
import numpy as np
from kelvin_table import kelvin_table

BACKGROUND = BLACK = (0, 0, 0)
DAMPING = 0.50
SCREEN = WIDTH, HEIGHT = 800, 600
HALF_HEIGHT = HEIGHT // 2

class AirParticle(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity=(20, 1)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("particle.png")
        self.rect = self.image.get_rect()
        self.image.fill(BACKGROUND)
        self.pos = np.array([x, y], dtype=np.float64)
        self.vel = np.array(velocity, dtype=np.float64)

        self.temperature = 3400 # Kelvin
        self.opacity = 255
        self.image.fill(kelvin_table[self.temperature])

    def update(self):
        collisions = pygame.sprite.spritecollide(self, self.groups()[0], False)
        for collision in collisions:
            if collision is not self:
                self.vel += collision.vel * DAMPING
                collision.vel = -self.vel

        self.vel[1] -= 0.01
        self.vel += np.random.randint(-1, 2, 2)
        self.pos += self.vel

        if self.pos[0] < 0 or self.pos[0] > WIDTH:
            self.vel[0] *= -1 * 0.90
        if self.pos[1] < 0 or self.pos[1] > HEIGHT:
            self.vel[1] *= -1 * 0.90

        self.temperature -= 100

        screen.fill(BACKGROUND)
        #screen.blit(nozzle, (100, HALF_HEIGHT-250))
        try:
            self.image.fill(kelvin_table[self.temperature])
        except KeyError:
            self.temperature = 900
            self.opacity -= 50
            self.image.set_alpha(self.opacity)
            if self.opacity <= 0:
                self.kill()
        self.rect.center = self.pos

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    nozzle = pygame.image.load("nozzle.png").convert_alpha()
    nozzle = pygame.transform.scale(nozzle, (100, 500))
    particles = pygame.sprite.Group()
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        particles.add(AirParticle(0, np.random.randint(HALF_HEIGHT-30, HALF_HEIGHT+30)))
        particles.add(AirParticle(0, np.random.randint(HALF_HEIGHT-30, HALF_HEIGHT+30)))
        particles.add(AirParticle(0, np.random.randint(HALF_HEIGHT-30, HALF_HEIGHT+30)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        particles.update()
        particles.draw(screen)
        pygame.display.flip()