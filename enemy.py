import rng
class Enemy:
    def __init__(self, type, level):
        self.health = 100
        self.level = level
        self.type = type
        self.defense = 0
        self.attackPow = 10
        self.activeEffects = []
        self.accuracy = 1
        self.passive = "Poison"

    def recieveDamage(self, dmg, effect = None):
        self.health -= dmg * (1-self.defense)
        if effect is not None:
            self.applyEffect(effect)

    def applyEffect(self, effect):
        if self.activeEffects.count(effect) != 0 :
            self.activeEffects.append(effect)

    def attack(self):
        dmg = 0
        effect = None
        if rng.RNG_Outcome(self.accuracy):
            dmg = rng.RNG_Shift(self.attackPow, 10)

        if rng.RNG_Outcome(0.1):
            effect = self.passive
        return dmg , effect



