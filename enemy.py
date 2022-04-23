import rng
class Enemy:
    enemyTypes = {'A':'burn', 'B':None, 'C':'Bleeding', 'Boss': 'burn'}
    def __init__(self, type, level):
        self.max_health = 100.0
        self.curr_health = self.max_health
        self.level = level
        self.type = type
        self.defense = 0.0
        self.attackPow = 10.0
        self.activeEffects = {}
        self.accuracy = 1.0
        self.passive = self.enemyTypes[type]

    def recieveDamage(self, dmg, effect = None):
        self.health -= dmg * (1-self.defense)
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



