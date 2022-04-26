import pygame


class HealthBar:
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, ratio, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 75, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 75 * ratio, 10))
