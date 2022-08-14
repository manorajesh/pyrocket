import pygame
import random
import numpy as np

BACKGROUND = BLACK = (0, 0, 0)
SCREEN = WIDTH, HEIGHT = 800, 600

class AirParticles(pygame.sprite.Sprite):
    def __init__(self, x, y, vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2, 2))
        self.rect = self.image.get_rect()
        self.image.fill(BACKGROUND)
        pygame.draw.circle(self.image, (255, 255, 255), (1, 1), 1)
        self.pos = np.array([x, y], dtype=np.float64)
        self.vel = np.array(vel, dtype=np.float64)

        self.speed = 1
        self.temperature = 0

    def update(self):
        self.pos += self.vel
        x, y = self.pos
        
        if x < 0 or x > WIDTH:
            self.vel[0] *= -1
        if y < 0 or y > HEIGHT:
            self.vel[1] *= -1

        self.rect.x = x
        self.rect.y = y

class Engine:
    def __init__(self, screen):
        self.screen = screen
        self.air_particles = pygame.sprite.Group()
        self.air_particles.add(AirParticles(30, HEIGHT//2))

    def update(self):
        self.air_particles.update()

    def draw(self):
        self.air_particles.draw(self.screen)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SCREEN)
    engine = Engine(screen)
    clock = pygame.time.Clock()
    while True:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        engine.update()
        engine.draw()
        pygame.display.flip()