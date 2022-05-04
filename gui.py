import pygame
class HealthBar: #class for handling healt bar ui element
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
    # draw the bar
    def draw(self, ratio, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 75, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 75 * ratio, 5))

# a class for displaying hovering text
class HoveringText(pygame.sprite.Sprite):

    def __init__(self, x, y, text, color, font):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self,stationary=False):
        if not stationary:
            # move up
            self.rect.y -= 1
            # delete after few seconds
            self.counter += 1
            if self.counter > 50:
                self.kill()




