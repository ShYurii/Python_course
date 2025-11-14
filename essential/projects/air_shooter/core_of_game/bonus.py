import random
import pygame

from essential.projects.air_shooter import settings
from essential.projects.air_shooter.core_of_game import resources



class Bonus:
    def __init__(self):
        self.width = settings.BONUS_WIDTH
        self.height = settings.BONUS_HEIGHT
        self.x = settings.WIDTH
        self.y = random.randint(50, settings.HEIGHT - self.height - 50)
        self.speed = 3
        self.img = resources.load_image("bonus.png", self.width, self.height)
        self.font = pygame.font.Font(None, 24)
        self.text = self.font.render("5 $", True, (0,0,0))

    def move(self):
        self.x -= self.speed

    def draw(self, surface):
        if self.img:
            surface.blit(self.img, (self.x, self.y))
        else:
            pygame.draw.rect(surface, settings.YELLOW, (self.x, self.y, self.width, self.height))
        text_rect = self.text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        surface.blit(self.text, text_rect)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
