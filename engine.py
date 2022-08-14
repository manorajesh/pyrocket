import pygame
import numpy as np

BACKGROUND = (50, 50, 50)
BLACK = (0, 0, 0)
DAMPING = 0.50
SCREEN = WIDTH, HEIGHT = 800, 600
HALF_HEIGHT = HEIGHT // 2

class AirParticle(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity=(4.4, 1)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2, 2))
        self.rect = self.image.get_rect()
        self.image.fill(BACKGROUND)
        self.pos = np.array([x, y], dtype=np.float64)
        self.vel = np.array(velocity, dtype=np.float64)
        pygame.draw.circle(self.image, (255, 255, 255), (1, 1), 1)

        self.temperature = 3400 # Kelvin

    def update(self):
        if pygame.sprite.spritecollide(nozzle_rect, self.groups()[0], False):
            self.vel[0] *= -1
        self.pos += self.vel

        if self.pos[0] < 0 or self.pos[0] > WIDTH:
            self.vel[0] *= -1
        if self.pos[1] < 0 or self.pos[1] > HEIGHT:
            self.vel[1] *= -1

        screen.fill(BACKGROUND)
        screen.blit(nozzle, (0, HALF_HEIGHT-250))
        self.rect.center = self.pos

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    nozzle = pygame.image.load("nozzle.png")
    nozzle = pygame.transform.scale(nozzle, (100, 500))
    nozzle.set_colorkey(BLACK)
    nozzle_rect = nozzle.get_rect()
    particles = pygame.sprite.Group()
    clock = pygame.time.Clock()
    while True:
        clock.tick(10)
        particles.add(AirParticle(0, np.random.randint(HALF_HEIGHT-30, HALF_HEIGHT+30)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        particles.update()
        particles.draw(screen)
        pygame.display.flip()