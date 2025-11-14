import pygame
from essential.projects.air_shooter.core_of_game import resources
from essential.projects.air_shooter import settings


class Player:
    def __init__(self):
        self.width = settings.PLANE_WIDTH
        self.height = settings.PLANE_HEIGHT
        self.x = settings.PLANE_X
        self.y = settings.HEIGHT // 2
        self.speed_y = 0
        self.img = resources.load_image("plane.png", self.width, self.height)

        self.shoot_sound = None
        self.flap_sound = None

    def set_sounds(self, shoot_sound, flap_sound):
        self.shoot_sound = shoot_sound
        self.flap_sound = flap_sound

    def handle_input(self, keys):

        shot = False
        if keys[pygame.K_UP]:
            self.speed_y += settings.LIFT
            if self.flap_sound:
                self.flap_sound.play()
        else:
            self.speed_y += settings.GRAVITY

        self.speed_y = max(min(self.speed_y, settings.MAX_FALL_SPEED), settings.MAX_RISE_SPEED)
        self.y += self.speed_y
        return shot

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        if self.img:
            surface.blit(self.img, (self.x, self.y))
        else:
            pygame.draw.rect(surface, settings.RED, (self.x, self.y, self.width, self.height))

    def shoot(self):
        bx = self.x + self.width
        by = self.y + self.height // 2 - settings.BULLET_HEIGHT // 2
        if self.shoot_sound:
            self.shoot_sound.play()
        return pygame.Rect(bx, by, settings.BULLET_WIDTH, settings.BULLET_HEIGHT)
