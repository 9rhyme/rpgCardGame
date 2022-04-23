import rng
class Player:
    def __init__(self, type, level):
        self.max_health = 100.0
        self.curr_health = self.max_health
        self.max_stamina = 100.0
        self.curr_stamina = self.max_stamina
        self.defence = 0.0
        self.attackPow = 1.0
        self.activeEffects = {}
        self.accuracy = 1.0
        self.allMoves = {'basicAttack' : 10, 'spinAttack' : 17, 'fireball' : 20 , 'heal' : 30, 'defence' : 0.3} # list of all moves
        self.combatDeck = {'basicAttack' : 10, 'fireball' : 20 } # list of available moves

    def recieveDamage(self, dmg, effect = None):
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
        dmg = 0
        effect = None
        if rng.RNG_Outcome(self.accuracy):
            dmg = rng.RNG_Shift(self.attackPow * self.combatDeck[attackType], 10)
            print(' you dealt',dmg, 'damage')

        if rng.RNG_Outcome(0.1):
            effect = self.getPassive(attackType)

        return dmg , effect
    def getPassive(self, attackType):
        passiveDict = {'basicAttack' : None, 'spinAttack' : 'bleeding', 'fireball' : 'burn'}
        return passiveDict[attackType]

    def defensive(self, moveType):
        if rng.RNG_Outcome(self.accuracy):
            if moveType == 'heal':
                healAmount = rng.RNG_Shift(self.allMoves['heal'],10)
                self.curr_healt += healAmount
                print('you healed',healAmount)
            if moveType == 'defence':



