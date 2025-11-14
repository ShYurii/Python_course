import sys
import pygame

import settings


from core_of_game.player import Player
from core_of_game.enemy import Enemy
from core_of_game.bonus import Bonus
from core_of_game.explosion import Explosion
from core_of_game import resources
import utils

def main():
    pygame.init()
    resources.init_audio()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption(settings.CAPTION)
    clock = pygame.time.Clock()

    font_big = pygame.font.Font(None, 80)
    font_small = pygame.font.Font(None, 50)

    shoot_sound = resources.load_sound("shoot.wav")
    flap_sound = resources.load_sound("flap.wav")
    crash_sound = resources.load_sound("crash.wav")
    score_sound = resources.load_sound("score.wav")

    bg_img = resources.load_image("BG.png", settings.WIDTH, settings.HEIGHT)
    bullet_img = resources.load_image("bullet.png", settings.BULLET_WIDTH, settings.BULLET_HEIGHT)
    enemy_bullet_img = resources.load_image("enemy_bullet.png", settings.ENEMY_BULLET_WIDTH, settings.ENEMY_BULLET_HEIGHT)
    bonus_img = resources.load_image("bonus.png", settings.BONUS_WIDTH, settings.BONUS_HEIGHT)

    player = Player()
    player.set_sounds(shoot_sound, flap_sound)

    plane_y, plane_speed_y, score, bullets, enemy_bullets, enemies, bonuses, explosions = utils.reset_game_state()
    player.y = plane_y
    player.speed_y = plane_speed_y

    game_over = False
    shoot_cooldown = 0
    enemy_timer = 0
    bonus_timer = 0
    enemy_shoot_timer = 0

    utils.show_instructions(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                plane_y, plane_speed_y, score, bullets, enemy_bullets, enemies, bonuses, explosions = utils.reset_game_state()
                player.y = plane_y
                player.speed_y = plane_speed_y
                game_over = False

        keys = pygame.key.get_pressed()

        if not game_over:
            if keys[pygame.K_UP]:
                player.speed_y += settings.LIFT
                if flap_sound:
                    flap_sound.play()
            else:
                player.speed_y += settings.GRAVITY
            player.speed_y = max(min(player.speed_y, settings.MAX_FALL_SPEED), settings.MAX_RISE_SPEED)
            player.y += player.speed_y

            if keys[pygame.K_SPACE] and shoot_cooldown == 0:
                bullets.append(player.shoot())
                shoot_cooldown = 10
            if shoot_cooldown > 0:
                shoot_cooldown -= 1

            plane_rect = player.rect()

            for b in bullets:
                b.x += settings.BULLET_SPEED
            bullets = [b for b in bullets if b.x < settings.WIDTH]

            for b in enemy_bullets:
                b.x -= settings.ENEMY_BULLET_SPEED
            enemy_bullets = [b for b in enemy_bullets if b.x > 0]

            enemy_timer += 1
            if enemy_timer > 90:
                enemies.append(Enemy())
                enemy_timer = 0

            enemy_shoot_timer += 1
            if enemy_shoot_timer > 120:
                for e in enemies:
                    enemy_bullets.append(e.shoot())
                enemy_shoot_timer = 0

            for e in enemies[:]:
                e.move()
                if plane_rect.colliderect(e.rect()):
                    explosions.append(Explosion(player.x + player.width // 2, player.y + player.height // 2, size=8, color=settings.RED, particles_count=50))
                    game_over = True
                    if crash_sound:
                        crash_sound.play()
                for b in bullets[:]:
                    if b.colliderect(e.rect()):
                        try:
                            bullets.remove(b)
                        except ValueError:
                            pass
                        try:
                            enemies.remove(e)
                        except ValueError:
                            pass
                        explosions.append(Explosion(e.x + e.width // 2, e.y + e.height // 2, size=6, color=settings.YELLOW))
                        score += 1
                        if score_sound:
                            score_sound.play()
                if e.x + e.width < 0:
                    try:
                        enemies.remove(e)
                    except ValueError:
                        pass

            bonus_timer += 1
            if bonus_timer > 300:
                bonuses.append(Bonus())
                bonus_timer = 0

            for bonus in bonuses[:]:
                bonus.move()
                if plane_rect.colliderect(bonus.rect()):
                    try:
                        bonuses.remove(bonus)
                    except ValueError:
                        pass
                    score += 5
                    if score_sound:
                        score_sound.play()
                elif bonus.x + bonus.width < 0:
                    try:
                        bonuses.remove(bonus)
                    except ValueError:
                        pass

            for b in enemy_bullets[:]:
                if plane_rect.colliderect(b):
                    try:
                        enemy_bullets.remove(b)
                    except ValueError:
                        pass
                    explosions.append(Explosion(player.x + player.width // 2, player.y + player.height // 2, size=8, color=settings.RED, particles_count=50))
                    game_over = True
                    if crash_sound:
                        crash_sound.play()

            if player.y < 0:
                player.y = 0
                player.speed_y = 0
            if player.y + player.height > settings.HEIGHT:
                player.y = settings.HEIGHT - player.height
                player.speed_y = 0

        if bg_img:
            screen.blit(bg_img, (0, 0))
        else:
            screen.fill(settings.SKY)

        player.draw(screen)

        for b in bullets:
            if bullet_img:
                screen.blit(bullet_img, (b.x, b.y))
            else:
                pygame.draw.rect(screen, settings.YELLOW, b)

        for b in enemy_bullets:
            if enemy_bullet_img:
                screen.blit(enemy_bullet_img, (b.x, b.y))
            else:
                pygame.draw.rect(screen, settings.RED, b)

        for e in enemies:
            e.draw(screen)
        for bonus in bonuses:
            bonus.draw(screen)

        for exp in explosions[:]:
            exp.update()
            exp.draw(screen)
            if not exp.alive:
                try:
                    explosions.remove(exp)
                except ValueError:
                    pass

        score_text = font_small.render(str(score), True, settings.WHITE)
        screen.blit(score_text, (settings.WIDTH // 2 - score_text.get_width() // 2, 20))

        if game_over:
            text1 = font_big.render("GAME OVER", True, settings.BLACK)
            text2 = font_small.render("Press R to Restart", True, settings.WHITE)
            screen.blit(text1, (settings.WIDTH // 2 - text1.get_width() // 2, settings.HEIGHT // 2 - 80))
            screen.blit(text2, (settings.WIDTH // 2 - text2.get_width() // 2, settings.HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(settings.FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
