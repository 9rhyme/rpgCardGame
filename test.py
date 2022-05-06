import pygame

import rng
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
action_cooldown = 50
fps = 60
enemyAlive = False
deathPlayed = False
enemyDeathPlayed = False
wantNextEnemy= True
effectsManaged = False
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
font3 = pygame.font.SysFont('Calibri',15)

#define colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0,0,255)
yellow = (255, 255, 0)
white = (255,255,255)
eff_col = red

# load necessary images
rpg_background = pygame.image.load('img/backgrounds/rpg_back_2.png')
rpg_background = pygame.transform.scale(rpg_background,(400,225))
heart_img = pygame.image.load('img/icons/heart.png')
heart_img = pygame.transform.scale(heart_img,(15,15))
gameOverScreen = pygame.image.load('img/backgrounds/game_over_1.png')
rpg_panel = pygame.image.load('img/backgrounds/panel.png')
rpg_panel = pygame.transform.scale(rpg_panel,(400,75))
bleeding_icon = pygame.image.load('img/icons/bleeding.png')
bleeding_icon = pygame.transform.scale(bleeding_icon,(25,25))
burning_icon = pygame.image.load('img/icons/burning.png')
burning_icon = pygame.transform.scale(burning_icon,(25,25))
zapped_icon = pygame.image.load('img/icons/zapped.png')
zapped_icon = pygame.transform.scale(zapped_icon,(25,25))
incAttack_icon = pygame.image.load('img/icons/incAttack.png')
incAttack_icon = pygame.transform.scale(incAttack_icon,(25,25))
incDefence_icon = pygame.image.load('img/icons/incDefence.png')
incDefence_icon = pygame.transform.scale(incDefence_icon,(25,25))

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
# draw status effects active on both the player and the enemy, sides: 0 player, 1 enemy
def draw_statusIcons(effectsDict,side):
    sides = (5,370)
    for effect in list(effectsDict):
        if effect == 'bleeding':
            screen.blit(bleeding_icon, (sides[side], 10))
        if effect == 'burning':
            screen.blit(burning_icon, (sides[side], 40))
        if effect == 'zapped':
            screen.blit(zapped_icon, (sides[side], 70))
        if effect == 'incAttack':
            screen.blit(incAttack_icon, (sides[side], 100))
        if effect == 'incDefence':
            screen.blit(incDefence_icon, (sides[side], 130))





def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    rect = img.get_rect(center=(screenWidth/2, 260))
    screen.blit(img,rect)

# create a player
knight = Player()
playerHealthBar = HealthBar(65, 100, knight.curr_health, knight.max_health)
#we don't want to see same enemy twice in a row
previousEnemy = ''
previousEnemyLvl = 0

while run:
    if not enemyAlive and wantNextEnemy:# if there is not an alive enemy create one
        wantNextEnemy = False
        # no repeating enemies
        nextEnemy = random.choice(list(Enemy.enemyTypes))
        while nextEnemy == previousEnemy:
            nextEnemy = random.choice(list(Enemy.enemyTypes))
        opponent = Enemy(nextEnemy, previousEnemyLvl+1)
        previousEnemy = opponent.type
        previousEnemyLvl +=1
        opponentHealthBar = HealthBar(270, opponent.height, opponent.curr_health, opponent.max_health,opponent.level)
        enemyAlive = True
    # limit fps
    clock.tick(fps)
    # draw recurring elements
    draw_bg()
    draw_panel()
    draw_statusIcons(knight.activeEffects,0)
    draw_statusIcons(opponent.activeEffects,1)
    playerHealthBar.draw(knight.curr_health / knight.max_health, screen,heart_img)

    if opponent.alive:
        lvl = opponentHealthBar.draw(opponent.curr_health / opponent.max_health, screen, heart_img, font3)
        hovering_texts_group.add(lvl)
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

                opponent.manageStatusEffects()


                if opponent.isFrozen:
                    print('frozen turn lost')
                    current_turn = 0

                    action_cooldown = 0
                    opponent.isFrozen = False
                else:
                    en_dmg,en_effect = opponent.attack()
                    current_turn = 0

                    action_cooldown = 0
                effectsManaged = False
    else: # wait until animation finishes
        if enemyDeathPlayed:
            enemyAlive = False
    # check if enemy dealt damage and if so make the player recieve it
    # sideNote: i also check if the enemy action is back to zero
    #           this way things progress after the attack animation is finished
    if en_dmg != 0 and opponent.action == 0:
        # handle hovering text over player
        if knight.alive:
            damage_text = HoveringText(95, 68, str(rng.round(en_dmg * (1 - knight.defence))), red, font2)
            hovering_texts_group.add(damage_text)
            if en_effect is not None:
                if en_effect == 'frozen':
                    eff_col = blue
                elif en_effect == 'zapped':
                    eff_col = yellow
                else:
                    eff_col = red
                effect_text = HoveringText(95, 85, str(en_effect), eff_col, font2)
                hovering_texts_group.add(effect_text)


        #make the player recieve damage
        if knight.curr_health>=1:
            knight.recieveDamage(en_dmg, en_effect)

        en_dmg = 0
        en_effect = None

    # manage the status effects of the player
    if current_turn == 0 and not effectsManaged:
        knight.manageStatusEffects()
        effectsManaged = True
    # handle player action
    movePermit = False
    if knight.alive:
        if current_turn == 0:
            action_cooldown += 1
            if action_cooldown >= action_waitTime:

                if knight.isFrozen:
                    print('frozen turn lost')
                    current_turn = 1
                    action_cooldown = 0
                    knight.isFrozen = False
                else:
                    movePermit = True
    else: # handle death animation
        if not deathPlayed:
            knight.action = 11
            knight.frame_index = 0
            deathPlayed = True
    if not knight.alive:
        current_turn = 2 # stop enemies from attacking after player is dead
        draw_gameOver()
    # handle key inputs ( will be replaced with card minigame)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_a and movePermit:

                pl_dmg, pl_effect = knight.offensive('basicAttack')
                current_turn = 1
                action_cooldown = 0
                movePermit = False
            if event.key == pygame.K_s and movePermit:
                pl_dmg, pl_effect = knight.offensive('spinAttack')
                current_turn = 1
                action_cooldown = 0
                movePermit = False
            if event.key == pygame.K_d and movePermit:
                knight.defensive('heal')
                temp = HoveringText(95,80,'heal',green,font2)
                hovering_texts_group.add(temp)
                current_turn = 1
                action_cooldown = 0
                movePermit = False
            if event.key == pygame.K_w and movePermit:
                pl_dmg, pl_effect = knight.offensive('iceShard')
                current_turn = 1
                action_cooldown = 0
                movePermit = False
            if event.key == pygame.K_q and movePermit:
                pl_dmg, pl_effect = knight.offensive('lightningBolt')
                current_turn = 1
                action_cooldown = 0
                movePermit = False
            if event.key == pygame.K_SPACE:
                wantNextEnemy = True


    # same logic as the last time but for the opposite side
    if pl_dmg != 0 and knight.action == 0:
        #handle the hovering text above enemy
        damage_text = HoveringText(295, 68, str(rng.round(pl_dmg)), red, font2)
        hovering_texts_group.add(damage_text)
        if pl_effect is not None:
            effect_text = HoveringText(295, 85, str(pl_effect), red, font2)
            hovering_texts_group.add(effect_text)
        opponent.recieveDamage(pl_dmg, pl_effect)

        pl_dmg = 0
        pl_effect = None
        # check if enemy is dead and the animation is finished
    if opponent.curr_health == 0 and opponent.deathPlayed:
        enemyDeathPlayed = True




    pygame.display.update()
pygame.quit()

