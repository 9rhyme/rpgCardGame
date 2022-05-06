import pygame
class HealthBar: #class for handling healt bar ui element
    def __init__(self, x, y, hp, max_hp,level = 0):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        self.level = level
    # draw the bar
    def draw(self, ratio, screen,heart_img,font=None):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 75, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 75 * ratio, 5))
        screen.blit(heart_img,(self.x-13,self.y-5))
        if self.level > 0:
            lvl = HoveringText(self.x+17,self.y-7,'lvl '+str(self.level),(255, 255, 255),font,True)
            return lvl



# a class for displaying hovering text
class HoveringText(pygame.sprite.Sprite):

    def __init__(self, x, y, text, color, font, stationary=False):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        self.stationary = stationary

    def update(self):
        if not self.stationary:
            # move up
            self.rect.y -= 1
            # delete after few seconds
        self.counter += 1
        if self.counter > 50:
            self.kill()




