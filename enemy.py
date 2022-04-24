import rng
import pygame
class Enemy:
    enemyTypes = {'demon':'burn', 'B':None, 'C':'Bleeding', 'Boss': 'burn'}
    def __init__(self, type, level):
        self.level = level
        self.alive = True
        self.isFrozen = False
        self.max_health = 100.0 + (self.level-1) * 50
        self.curr_health = self.max_health
        self.type = type
        self.defence = 0.0
        self.attackPow = 10.0
        self.activeEffects = {}
        self.accuracy = 1.0
        self.passive = self.enemyTypes[type]
        self.update_time = pygame.time.get_ticks()


        self.animation_list = []
        self.frame_index = 0
        for i in range(1, 7):
            img = pygame.image.load(f'img/animations/enemies/{self.type}/idle/idle_{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (270, 50)

    def update(self):
        animation_cooldown = 150
        # handle animation
        # update image
        self.image = self.animation_list[self.frame_index]
        # check if enough time has passed for animation
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index == 6:
                self.frame_index = 0

    def draw(self, screen):
        screen.blit(self.image,self.rect)

    def recieveDamage(self, dmg, effect = None):
        self.curr_health -= dmg * (1-self.defence)
        if effect is not None:
            self.applyEffect(effect)

    def applyEffect(self, effect):
        if effect not in self.activeEffects.keys():
            self.activeEffects[effect] = 3

    def attack(self):
        dmg = 0
        effect = None
        if rng.RNG_Outcome(self.accuracy):
            dmg = rng.RNG_Shift(self.attackPow, 10)
            if rng.RNG_Outcome(0.1):
                effect = self.passive
        return dmg , effect

    def manageStatusEffects(self):
        for effect in self.activeEffects.keys():
            if self.activeEffects[effect] == 3:
                if effect == 'zapped':
                    self.accuracy -= 0.2
                if effect == 'frozen':
                    self.isFrozen == True
                    self.activeEffects[effect] = 0
                if effect == 'burning':
                    self.defence -= 0.2
                if effect == 'bleeding':
                    self.curr_health -= self.max_health*0.05
                self.activeEffects[effect] -=1
            elif self.activeEffects[effect] == 2:
                if effect == 'bleeding':
                    self.curr_health -= self.max_health * 0.05
                self.activeEffects[effect] -= 1
            elif self.activeEffects[effect] == 1:
                if effect == 'bleeding':
                    self.curr_health -= self.max_health * 0.05
                self.activeEffects[effect] -= 1
            else:
                if effect == 'defence':
                    self.defence -= 0.3
                if effect == 'zapped':
                    self.accuracy += 0.2
                if effect == 'frozen':
                    self.isFrozen == False
                if effect == 'burning':
                    self.defence += 0.2
                self.activeEffects.pop(effect)



