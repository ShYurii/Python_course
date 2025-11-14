import pygame
from essential.projects.air_shooter import settings


def reset_game_state():
    plane_y = settings.HEIGHT // 2
    plane_speed_y = 0
    score = 0
    bullets = []
    enemy_bullets = []
    enemies = []
    bonuses = []
    explosions = []
    return plane_y, plane_speed_y, score, bullets, enemy_bullets, enemies, bonuses, explosions

def show_instructions(screen):
    screen.fill((0,0,0))
    font_title = pygame.font.Font(None, 60)
    font_text = pygame.font.Font(None, 40)

    lines = [
        "Air Shooter",
        "",
        "Arrow UP — Move the plane up",
        "SPACE — Shoot bullets",
        "",
        "Press any key to start"
    ]

    y = 100
    for line in lines:
        if line == "Air Shooter":
            text = font_title.render(line, True, settings.WHITE)
        else:
            text = font_text.render(line, True, settings.WHITE)
        screen.blit(text, (settings.WIDTH // 2 - text.get_width() // 2, y))
        y += 60

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                waiting = False
