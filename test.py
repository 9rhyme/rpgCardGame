import pygame


from gui import HealthBar
from gui import HoveringText
from player import Player
from enemy import Enemy
import random

pygame.init()
clock = pygame.time.Clock()

# define game variables
current_turn = 0 # 0: your turn , 1 : enemy's turn
action_waitTime = 90
action_cooldown = 0
fps = 60
enemyAlive = False
deathPlayed = False
enemyDeathPlayed = False
wantNextEnemy= True
run = True
pl_dmg = 0
pl_effect = None
en_dmg = 0
en_effect = None

# block for handling message panel ui element
messages = []
currMsg = 0
messages.append('Currently testing')

# hovering texts
hovering_texts_group = pygame.sprite.Group()

# screen variables
screenWidth = 400
screenHeight = 700
screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption('Cards & Crypts')

# define font
font1 = pygame.font.SysFont('Jokerman', 25)
font2 = pygame.font.SysFont('Jokerman', 15)

#define colors
red = (255, 0, 0)
green = (0, 255, 0)
white = (255,255,255)

# load necessary images
rpg_background = pygame.image.load('img/backgrounds/rpg_back.png')
rpg_background = pygame.transform.scale(rpg_background,(400,225))
gameOverScreen = pygame.image.load('img/backgrounds/game_over_1.png')
rpg_panel = pygame.image.load('img/backgrounds/panel.png')
rpg_panel = pygame.transform.scale(rpg_panel,(400,75))

# drawing methods for ui elements
def draw_gameOver():
    screen.blit(gameOverScreen,(30,50))
def draw_bg():
    screen.blit(rpg_background,(0,0))
def draw_panel():
    #draw panel rectangle
    screen.blit(rpg_panel,(0,225))
    # draw text
    draw_text(messages[currMsg], font1, white, 90, 230)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    rect = img.get_rect(center=(screenWidth/2, 260))
    screen.blit(img,rect)

# create a player
knight = Player()
playerHealthBar = HealthBar(65, 100, knight.curr_health, knight.max_health)
#we don't want to see same enemy twice in a row
previousEnemy = ''
while run:
    if not enemyAlive and wantNextEnemy:
        wantNextEnemy = False# if there is not an alive enemy create one
        # no repeating enemies
        nextEnemy = random.choice(list(Enemy.enemyTypes))
        while nextEnemy == previousEnemy:
            nextEnemy = random.choice(list(Enemy.enemyTypes))
        opponent = Enemy(nextEnemy, 1)
        previousEnemy = opponent.type
        opponentHealthBar = HealthBar(270, opponent.height, opponent.curr_health, opponent.max_health)
        enemyAlive = True
    # limit fps
    clock.tick(fps)
    # draw recurring elements
    draw_bg()
    draw_panel()
    playerHealthBar.draw(knight.curr_health / knight.max_health, screen)
    opponentHealthBar.draw(opponent.curr_health / opponent.max_health, screen)
    # animate the knight if he's alive
    if knight.alive:
        knight.update()
    else:
        if knight.frame_index<len(knight.animation_list[11]):
            knight.update()
    knight.draw(screen)
    # animate the enemy
    if opponent.alive:
        opponent.update()
    else:
        if opponent.frame_index<len(opponent.animation_list[2]):
            opponent.update()
    opponent.draw(screen)

    #draw hovering text
    hovering_texts_group.update()
    hovering_texts_group.draw(screen)

    # enemy action:
    if opponent.alive:
        if current_turn == 1:
            action_cooldown += 1 # if sufficient time passes do the move
            if action_cooldown >= action_waitTime:
                en_dmg,en_effect = opponent.attack()
                current_turn = 0
                action_cooldown = 0
    else: # wait until animation finishes
        if enemyDeathPlayed:
            enemyAlive = False
    # check if enemy dealt damage and if so make the player recieve it
    # sideNote: i also check if the enemy action is back to zero
    #           this way things progress after the attack animation is finished
    if en_dmg != 0 and opponent.action == 0:
        # handle hovering tet over player
        damage_text = HoveringText(95, 68, str(en_dmg), red, font2)
        hovering_texts_group.add(damage_text)
        if en_effect is not None:
            effect_text = HoveringText(95,85, str(en_effect), red, font2)
            hovering_texts_group.add(effect_text)


        #make the player recieve damage
        knight.recieveDamage(en_dmg, en_effect)
        en_dmg = 0
        en_effect = None

    # handle player action
    movePermit = False
    if knight.alive:
        if current_turn == 0:
            action_cooldown += 1
            if action_cooldown >= action_waitTime:
                if knight.isFrozen:
                    print('frozen turn lost')
                    current_turn = 1
                    knight.isFrozen = False
                else:
                    movePermit = True
    else: # handle death animation
        if not deathPlayed:
            knight.action = 11
            knight.frame_index = 0
            deathPlayed = True
    if not knight.alive:
        draw_gameOver()
    # handle key inputs ( will be replaced with card minigame)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_a and movePermit:
                pl_dmg, pl_effect = knight.offensive('basicAttack', 1)
                current_turn = 1
                action_cooldown = 0
                movePermit = False
            if event.key == pygame.K_s and movePermit:
                pl_dmg, pl_effect = knight.offensive('spinAttack', 2)
                current_turn = 1
                action_cooldown = 0
                movePermit = False
            if event.key == pygame.K_d and movePermit:
                knight.defensive('heal')
                temp = HoveringText(95,80,'heal',green,font2)
                hovering_texts_group.add(temp)
                print(knight.activeEffects)
                current_turn = 1
                action_cooldown = 0
                movePermit = False
            if event.key == pygame.K_SPACE:
                wantNextEnemy = True

    # same logic as the last time but for the opposite side
    if pl_dmg != 0 and knight.action == 0:
        #handle the hovering text above enemy
        damage_text = HoveringText(295, 68, str(pl_dmg), red, font2)
        hovering_texts_group.add(damage_text)
        if pl_effect is not None:
            effect_text = HoveringText(295, 85, str(pl_effect), red, font2)
            hovering_texts_group.add(effect_text)
        opponent.recieveDamage(pl_dmg, pl_effect)
        print(pl_effect)
        pl_dmg = 0
        pl_effect = None
        # check if enemy is dead and the animation is finished
    if opponent.curr_health == 0 and opponent.deathPlayed:
        enemyDeathPlayed = True




    pygame.display.update()
pygame.quit()

