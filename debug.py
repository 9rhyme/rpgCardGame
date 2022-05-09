import rng
from player import Player
pal = Player()
pal.accuracy = 0
for i in range(20):
    print(pal.offensive('basicAttack'))
    print(rng.RNG_Outcome(0))