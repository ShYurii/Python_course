import random
import pygame

class Explosion:
    def __init__(self, x: float, y: float, size: int = 5, color=(255,0,0), particles_count: int = 20):
        self.particles = []
        for _ in range(particles_count):
            dx = random.uniform(-3, 3)
            dy = random.uniform(-3, 3)
            self.particles.append([x, y, dx, dy, size, color])
        self.alive = True

    def update(self):
        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]
            p[4] *= 0.95
        self.particles = [p for p in self.particles if p[4] > 1]
        if not self.particles:
            self.alive = False

    def draw(self, surface):
        for p in self.particles:
            pygame.draw.circle(surface, p[5], (int(p[0]), int(p[1])), int(p[4]))
