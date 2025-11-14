import os
import pygame
from typing import Optional
from essential.projects.air_shooter import settings


def init_audio():
    try:
        pygame.mixer.quit()
    except Exception:
        pass
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=64)
    except Exception:
        print("Audio init failed; sounds disabled.")

def load_image(name: str, width: int, height: int) -> Optional[pygame.Surface]:
    path = os.path.join(settings.IMAGES_DIR, name)
    try:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (width, height))
        return img
    except Exception:
        print(f"Image not found: {path}")
        return None

def load_sound(name: str) -> Optional[pygame.mixer.Sound]:
    path = os.path.join(settings.SOUNDS_DIR, name)
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        print(f"Sound not found: {path}")
        return None
