import random
import pygame
from essential.projects.air_shooter.core_of_game import resources
from essential.projects.air_shooter import settings


class Enemy:
    def __init__(self):
        self.width = settings.ENEMY_WIDTH
        self.height = settings.ENEMY_HEIGHT
        self.x = settings.WIDTH
        self.y = random.randint(50, settings.HEIGHT - self.height - 50)
        self.speed = random.randint(3, 6)
        self.img = resources.load_image("enemy.png", self.width, self.height)

    def move(self):
        self.x -= self.speed

    def draw(self, surface):
        if self.img:
            surface.blit(self.img, (self.x, self.y))
        else:
            pygame.draw.rect(surface, settings.RED, (self.x, self.y, self.width, self.height))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def shoot(self):
        bx = self.x
        by = self.y + self.height // 2 - settings.ENEMY_BULLET_HEIGHT // 2
        return pygame.Rect(bx, by, settings.ENEMY_BULLET_WIDTH, settings.ENEMY_BULLET_HEIGHT)
