import rng
import pygame


class Player:
    def __init__(self):
        self.max_health = 100.0
        self.curr_health = self.max_health
        self.isFrozen = False
        self.defence = 0.0
        self.attackPow = 1.0
        self.activeEffects = {}
        self.accuracy = 1.0
        self.alive = True
        self.update_time = pygame.time.get_ticks()
        self.moveLengths = {'idle': 8, 'basicAttack': 11, }
        self.allMoves = {'idle': 0, 'basicAttack': 10, 'spinAttack': 17, 'fireball': 20, 'heal': 30,
                         'defence': 0.3}  # list of all moves
        self.combatDeck = {'basicAttack': 10, 'fireball': 20}  # list of available moves

        self.animation_list = []
        self.action = 0  # 0:idle, 1:basicAttack, ...
        self.frame_index = 0

        self.loadSprites()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)

    def loadSprites(self):
        for move in self.moveLengths.keys():
            temp_list = []
            for i in range(1, self.moveLengths[move] + 1):
                img = pygame.image.load(f'img/animations/player/{move}/_ ({i}).png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                temp_list.append(img)
            self.animation_list.append(temp_list)

    def update(self):
        animation_cooldown = 70
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed for animation
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index == len(self.animation_list[self.action]):
                self.frame_index = 0
                self.idle()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def recieveDamage(self, dmg, effect=None):
        if dmg == 0:
            print("Enemy missed.")
        else:
            print(" You recieved", dmg, 'damage')
            self.curr_health -= dmg * (1 - self.defence)
            if effect is not None:
                self.applyEffect(effect)

    def applyEffect(self, effect):
        if effect not in self.activeEffects.keys():
            self.activeEffects[effect] = 3

    def offensive(self, attackType):
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        dmg = 0
        effect = None
        if rng.RNG_Outcome(self.accuracy):
            dmg = rng.RNG_Shift(self.attackPow * self.combatDeck[attackType], 10)
            print(' you dealt', dmg, 'damage')

        if rng.RNG_Outcome(0.1):
            effect = self.getPassive(attackType)

        return dmg, effect

    def getPassive(self, attackType):
        passiveDict = {'basicAttack': None, 'spinAttack': 'bleeding', 'fireball': 'burning'}
        return passiveDict[attackType]

    def defensive(self, moveType):
        if rng.RNG_Outcome(self.accuracy):
            if moveType == 'heal':
                healAmount = rng.RNG_Shift(self.allMoves['heal'], 10)
                self.curr_health += healAmount
                print('you healed', healAmount)
            if moveType == 'defence':
                self.applyEffect('defence')
                print('you used a defence spell')

    def manageStatusEffects(self):
        for effect in self.activeEffects.keys():
            if self.activeEffects[effect] == 3:
                if effect == 'defence':
                    self.defence += 0.3
                if effect == 'zapped':
                    self.accuracy -= 0.2
                if effect == 'frozen':
                    self.isFrozen = True
                    self.activeEffects[effect] = 0
                if effect == 'burning':
                    self.defence -= 0.2
                if effect == 'bleeding':
                    self.curr_health -= self.max_health * 0.05
                self.activeEffects[effect] -= 1
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
                    self.isFrozen = False
                if effect == 'burning':
                    self.defence += 0.2
                self.activeEffects.pop(effect)
