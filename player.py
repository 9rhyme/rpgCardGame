import rng
import pygame



class Player:
    def __init__(self):
        self.max_health = 1000.0
        self.curr_health = self.max_health
        self.isFrozen = False
        self.defence = 0.0
        self.attackPow = 1.0
        self.activeEffects = {}
        self.accuracy = 1.0
        self.alive = True
        self.deathPlayed = False
        self.update_time = pygame.time.get_ticks()
        self.moveLengths = {'idle': 8, 'basicAttack': 11,'spinAttack': 19,'ultAttack':18,'fireBall':10, 'iceShard':10, 'lightningBolt': 10,'heal':19, 'incAttack':19,
                            'incDefence': 19, 'hurt' : 6, 'death':13 }
        self.allMoves = {'idle': 0, 'basicAttack': 10, 'spinAttack': 17,'ultAttack': 25, 'fireBall': 20,'iceShard' : 20, 'lightningBolt': 23, 'heal': 30,
                         'incDefence': 0.3, 'incAttack' : 0.3}  # list of all moves


        self.animation_list = []
        self.action = 0  # 0:idle, 1:basicAttack, 2 : spin ...
        self.frame_index = 0

        self.loadSprites()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (100, 110)

    # method for loading all sprites for various animations
    def loadSprites(self):
        for move in self.moveLengths.keys():
            temp_list = []
            for i in range(1, self.moveLengths[move] + 1):
                img = pygame.image.load(f'img/animations/player/{move}/_ ({i}).png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                temp_list.append(img)
            self.animation_list.append(temp_list)

    # update the image to get smooth animations, if death; stop refreshing frame index
    def update(self):
        # we check if alive here instead of recievedmg because we may die from bleeding too
        if self.curr_health < 1:
            self.alive = False
        animation_cooldown = 60
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed for animation
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            if not self.deathPlayed:
                self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 11:
                    self.deathPlayed = True
                else:
                    self.frame_index = 0
                    self.idle()


    # draw the current image to the screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # put player back to idle state after any move
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    # recieve damage, effects and play relevant animation
    def recieveDamage(self, dmg, effect=None):
        if dmg == 0:
            print("Enemy missed.")
        else:
            print(" You recieved", dmg, 'damage')
            self.action = 10
            self.frame_index = 0
            self.curr_health -= dmg * (1 - self.defence)
            if effect is not None:
                self.applyEffect(effect)

    # apply effects if not already present
    def applyEffect(self, effect):
        if effect == 'frozen':
            self.isFrozen = True
        else:
            if effect not in self.activeEffects.keys():
                self.activeEffects[effect] = 3

    # take offensive action
    def offensive(self, attackType):
        self.action = list(self.allMoves).index(attackType)
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        dmg = 0
        effect = None
        outcome = rng.RNG_Outcome(self.accuracy)
        if outcome:
            dmg = rng.RNG_Shift(self.attackPow * self.allMoves[attackType], 20)
            print(' you dealt', dmg, 'damage')

        if rng.RNG_Outcome(0.2):
            effect = self.getPassive(attackType)
        return dmg, effect

    # gets relative passive effect for attack types
    def getPassive(self, attackType):
        passiveDict = {'basicAttack': None, 'spinAttack': 'bleeding','ultAttack':'burning','fireBall':'burning', 'iceShard':'frozen', 'lightningBolt': 'zapped'}
        return passiveDict[attackType]

    # take defensive action
    def defensive(self, moveType):
        if rng.RNG_Outcome(self.accuracy):
            if moveType == 'heal':
                self.action = 7
                self.frame_index = 0
                healAmount = rng.RNG_Shift(self.allMoves['heal']*self.max_health/100.0, 10)
                self.curr_health += healAmount
                if self.curr_health>self.max_health:
                    self.curr_health = self.max_health
                print('you healed', healAmount)
            if moveType == 'incDefence':
                self.action = 8
                self.frame_index = 0
                self.applyEffect('incDefence')
                print('you used a defence spell')
            if moveType == 'incAttack':
                self.action = 9
                self.frame_index = 0
                self.applyEffect('incAttack')
                print('you used an attack power increasing spell')

    # one method to
    def manageStatusEffects(self):
        for effect in list(self.activeEffects):
            if self.activeEffects[effect] == 3:
                if effect == 'incDefence':
                    self.defence += self.allMoves['incDefence']
                if effect == 'incAttack':
                    self.attackPow += self.allMoves['incAttack']
                if effect == 'zapped':
                    self.accuracy -= 0.2
                if effect == 'burning':
                    self.defence -= 0.2
                if effect == 'bleeding':
                    self.curr_health -= self.max_health * 0.1
                    print('health lost due to bleeding-----------------------')
                self.activeEffects[effect] -= 1
            elif self.activeEffects[effect] == 2:
                if effect == 'bleeding':
                    self.curr_health -= self.max_health *  0.1
                    print('health lost due to bleeding-----------------------')
                self.activeEffects[effect] -= 1
            elif self.activeEffects[effect] == 1:
                if effect == 'bleeding':
                    self.curr_health -= self.max_health * 0.1
                    print('health lost due to bleeding-------------------')
                self.activeEffects[effect] -= 1
            else:
                if effect == 'incDefence':
                    self.defence -= 0.3
                elif effect == 'zapped':
                    self.accuracy += 0.2
                elif effect == 'incAttack':
                    self.attackPow -= 0.3
                elif effect == 'burning':
                    self.defence += 0.2
                self.activeEffects.pop(effect)
