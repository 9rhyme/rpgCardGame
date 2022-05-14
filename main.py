import random

import pygame

import rng
from Game import Game
from button import Button
from enemy import Enemy
from gui import HealthBar
from gui import HoveringText
from player import Player

pygame.init()

# define game variables
FPS = 60
clock = pygame.time.Clock()
current_turn = 0  # 0: your turn , 1 : enemy's turn
action_waitTime = 70
action_cooldown = 0

en_attackMissed = False
pl_attackMissed = False
initiateGame = False
gameState = 0  # 0: main menu, 1 game , -1 : game over, 2 : how to play, 4 : pause
pl_dmg = 0
pl_effect = None
en_dmg = 0
en_effect = None
musicPlaying = False

# variables for handling message panel ui element
msgCounter = 0
msgCooldown = 70

# hovering texts group
hovering_texts_group = pygame.sprite.Group()

# screen variables
screenWidth = 400
screenHeight = 730
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Cards & Crypts')

# defined fonts
font1 = pygame.font.Font('fonts/Forte.ttf', 25)
font2 = pygame.font.Font('fonts/Jokerman.ttf', 15)
font3 = pygame.font.Font('fonts/Calibri.ttf', 15)

# define colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (34, 34, 168)
yellow = (255, 255, 0)
white = (255, 255, 255)
eff_col = red

# load necessary images
# ui images and Button objects
mainMenuImg = pygame.image.load('img/ui/mainMenu.png')
startButtonImg = pygame.image.load('img/ui/startButton.png')
startButton = Button(screen, 110, 500, startButtonImg, 187, 70)
nextButtonImg = pygame.image.load('img/ui/nextButton.png')
nextButton = Button(screen,130, 90,nextButtonImg,187,70)
menuButtonImg = pygame.image.load('img/ui/menuButton.png')
menuButton = Button(screen, 150, 600, menuButtonImg, 187, 70)
gameOverScreen = pygame.image.load('img/ui/game_over_1.png')
gameOverScreen = pygame.transform.scale(gameOverScreen, (400, 120))
pauseImg = pygame.image.load('img/ui/pause.png')
rpg_panel = pygame.image.load('img/ui/panel.png')
rpg_panel = pygame.transform.scale(rpg_panel, (400, 75))
# backgrounds
rpg_background = pygame.image.load('img/backgrounds/rpg_back_4.png')
rpg_background = pygame.transform.scale(rpg_background, (400, 225))
# Hud elements
heart_img = pygame.image.load('img/icons/heart.png')
heart_img = pygame.transform.scale(heart_img, (15, 15))
bleeding_icon = pygame.image.load('img/icons/bleeding.png')
bleeding_icon = pygame.transform.scale(bleeding_icon, (30, 30))
burning_icon = pygame.image.load('img/icons/burning.png')
burning_icon = pygame.transform.scale(burning_icon, (30, 30))
zapped_icon = pygame.image.load('img/icons/zapped.png')
zapped_icon = pygame.transform.scale(zapped_icon, (30, 30))
incAttack_icon = pygame.image.load('img/icons/incAttack.png')
incAttack_icon = pygame.transform.scale(incAttack_icon, (30, 30))
incDefence_icon = pygame.image.load('img/icons/incDefence.png')
incDefence_icon = pygame.transform.scale(incDefence_icon, (30, 30))


# drawing methods for ui elements
def draw_gameOver():
    global gameState
    screen.blit(gameOverScreen, (0, 50))
    if musicPlaying:
        pygame.mixer.music.stop()
    if menuButton.draw():
        gameState = 0


def mainMenu():
    global musicPlaying
    if not musicPlaying:
        pygame.mixer.music.load('music/title.wav')
        pygame.mixer.music.play(-1)
        musicPlaying = True
    global gameState
    global initiateGame
    screen.blit(mainMenuImg, (0, 13))
    if startButton.draw():
        gameState = 1
        musicPlaying = False
        initiateGame = True
        screen.fill(pygame.color.Color(0, 0, 0))


def pause():
    screen.blit(pauseImg, (50, 50))


def draw_bg():
    screen.blit(rpg_background, (0, 0))


def draw_panel():
    # draw panel rectangle
    screen.blit(rpg_panel, (0, 225))
    # draw text
    # draw_text(messages[currMsg], font1, white, 90, 230)


# draw status effects active on both the player and the enemy, sides: 0 player, 1 enemy
def draw_statusIcons(effectsDict, side):
    sides = (5, 370)
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



# initiate card game
game = Game(screen)

run = True
while run:
    clock.tick(FPS)
    # handle key inputs
    eventlist = pygame.event.get()
    for event in eventlist:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if gameState == 1:
                    gameState = 4
                elif gameState == 4:
                    gameState = 1

    # rpg part
    if gameState == 0:
        mainMenu()
        if initiateGame:
            # create a player
            knight = Player()
            playerHealthBar = HealthBar(65, 100, knight.curr_health, knight.max_health)
            # we don't want to see same enemy twice in a row

            # from here we restart all essential game variables for the new game loop
            previousEnemy = ''
            previousEnemyLvl = 0
            currentStage = 1
            messages = []
            currMsg = 0
            enemyAlive = False
            deathPlayed = False
            enemyDeathPlayed = False
            wantNextEnemy = True
            effectsManaged = False
            current_turn = 0
            initiateGame = False

    elif gameState == 1:
        if not musicPlaying:
            pygame.mixer.music.load('music/battle.wav')
            pygame.mixer.music.play(-1)
            musicPlaying = True
        if not enemyAlive and wantNextEnemy:  # if there is not an alive enemy create one
            wantNextEnemy = False
            # no repeating enemies
            nextEnemy = random.choice(list(Enemy.enemyTypes))
            while nextEnemy == previousEnemy:
                nextEnemy = random.choice(list(Enemy.enemyTypes))
            opponent = Enemy(nextEnemy, previousEnemyLvl + 1)
            previousEnemy = opponent.type
            previousEnemyLvl += 1
            opponentHealthBar = HealthBar(270, opponent.height, opponent.curr_health, opponent.max_health,
                                          opponent.level)
            enemyAlive = True


        # draw recurring elements
        draw_bg()
        draw_panel()
        draw_statusIcons(knight.activeEffects, 0)
        draw_statusIcons(opponent.activeEffects, 1)
        playerHealthBar.draw(knight.curr_health / knight.max_health, screen, heart_img)

        if opponent.alive:
            lvl = opponentHealthBar.draw(opponent.curr_health / opponent.max_health, screen, heart_img, font3)
            hovering_texts_group.add(lvl)
        # animate the knight if he's alive
        if knight.alive:
            knight.update()
        else:
            if knight.frame_index < len(knight.animation_list[11]):
                knight.update()
        knight.draw(screen)
        # animate the enemy
        if opponent.alive:
            opponent.update()
        else:
            if opponent.frame_index < len(opponent.animation_list[2]):
                opponent.update()

        opponent.draw(screen)

        # draw hovering text
        hovering_texts_group.update()
        hovering_texts_group.draw(screen)

        # handle panel prompts
        msgCounter += 1
        if msgCounter >= msgCooldown:
            if currMsg <= len(messages) - 1:
                hovering_texts_group.add(messages[currMsg])
                currMsg += 1
            msgCounter = 0

        # enemy action:
        if opponent.alive:
            if current_turn == 1:
                action_cooldown += 1  # if sufficient time passes do the move
                if action_cooldown >= action_waitTime:
                    opponent.manageStatusEffects()
                    if opponent.isFrozen:
                        print('frozen turn lost')
                        current_turn = 0
                        action_cooldown = 0
                        opponent.isFrozen = False
                    else:
                        en_dmg, en_effect = opponent.attack()
                        if en_dmg == 0:
                            en_attackMissed = True
                        current_turn = 0

                        action_cooldown = 0
                    effectsManaged = False
        else:  # wait until animation finishes
            if enemyDeathPlayed:
                current_turn = 0
                enemyAlive = False
        if not enemyAlive:
            if nextButton.draw():
                knight.curr_health = knight.max_health
                wantNextEnemy = True
                game.level_complete = True
                current_turn = 0
        # check if enemy dealt damage and if so make the player receive it
        # sideNote: i also check if the enemy action is back to zero
        #           this way things progress after the attack animation is finished
        if en_attackMissed and opponent.action == 0:
            prompt = HoveringText(screenWidth / 2, 260, 'Enemy Missed', white, font1, True)
            messages.append(prompt)
            en_attackMissed = False
        if en_dmg != 0 and opponent.action == 0:
            # handle hovering text over player

            if knight.alive:
                damage_text = HoveringText(95, 68, str(rng.round(en_dmg * (1 - knight.defence))), red, font2)
                prompt = HoveringText(screenWidth / 2, 260,
                                      'You took ' + str(rng.round(en_dmg * (1 - knight.defence))) + ' damage.', white,
                                      font1, True)
                messages.append(prompt)

                hovering_texts_group.add(damage_text)
                if en_effect is not None:
                    if en_effect == 'frozen':
                        eff_col = blue
                    elif en_effect == 'zapped':
                        eff_col = yellow
                    else:
                        eff_col = red
                    effect_text = HoveringText(95, 85, str(en_effect), eff_col, font2)
                    prompt = HoveringText(screenWidth / 2, 260, 'You are  ' + en_effect, eff_col, font1, True)
                    messages.append(prompt)
                    hovering_texts_group.add(effect_text)

            # make the player receive damage
            if knight.curr_health >= 1:
                knight.receiveDamage(en_dmg, en_effect)

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
        else:  # handle death animation
            if not deathPlayed:
                knight.action = 11
                knight.frame_index = 0
                deathPlayed = True
        if not knight.alive:
            current_turn = 2  # stop enemies from attacking after player is dead
            draw_gameOver()

        if pl_attackMissed and knight.action == 0:
            prompt = HoveringText(screenWidth / 2, 260, 'You Missed', white, font1, True)
            messages.append(prompt)
            pl_attackMissed = False
        # same logic as the last time but for the opposite side
        if pl_dmg != 0 and knight.action == 0:
            # handle the hovering text above enemy
            damage_text = HoveringText(295, 68, str(rng.round(pl_dmg)), red, font2)
            prompt = HoveringText(screenWidth / 2, 260,
                                  'Enemy took ' + str(rng.round(pl_dmg * (1 - opponent.defence))) + ' damage.', white,
                                  font1, True)
            messages.append(prompt)
            hovering_texts_group.add(damage_text)
            if pl_effect is not None:
                if pl_effect == 'frozen':
                    eff_col = blue
                elif pl_effect == 'zapped':
                    eff_col = yellow
                else:
                    eff_col = red
                effect_text = HoveringText(295, 85, str(pl_effect), eff_col, font2)
                prompt = HoveringText(screenWidth / 2, 260, 'Enemy is ' + pl_effect, eff_col, font1, True)
                messages.append(prompt)
                hovering_texts_group.add(effect_text)
            opponent.receiveDamage(pl_dmg, pl_effect)
            # enemy slain prompt
            if not opponent.alive:
                prompt = HoveringText(screenWidth / 2, 260, 'Enemy Slain', red, font1, True)
                messages.append(prompt)

            pl_dmg = 0
            pl_effect = None
            # check if enemy is dead and the animation is finished
        if opponent.curr_health == 0 and opponent.deathPlayed:
            enemyDeathPlayed = True

        # cards part
        picked_card = game.update(eventlist)
        if picked_card is not None:
            if picked_card == 'basicAttack' and movePermit:
                pl_dmg, pl_effect = knight.offensive('basicAttack')
                if pl_dmg == 0:
                    pl_attackMissed = True

            elif picked_card == 'spinAttack' and movePermit:
                pl_dmg, pl_effect = knight.offensive('spinAttack')
                if pl_dmg == 0:
                    pl_attackMissed = True

            elif picked_card == 'ultAttack' and movePermit:
                pl_dmg, pl_effect = knight.offensive('ultAttack')
                if pl_dmg == 0:
                    pl_attackMissed = True

            elif picked_card == 'heal' and movePermit:
                knight.defensive('heal')
                temp = HoveringText(95, 80, 'heal', green, font2)
                prompt = HoveringText(screenWidth / 2, 260, 'You Healed', green, font1, True)
                messages.append(prompt)
                hovering_texts_group.add(temp)

            elif picked_card == 'incAttack' and movePermit:
                knight.defensive('incAttack')
                temp = HoveringText(95, 80, 'incAttack', green, font2)
                prompt = HoveringText(screenWidth / 2, 260, 'Your Attack Power Increased', green, font1, True)
                messages.append(prompt)
                hovering_texts_group.add(temp)

            elif picked_card == 'incDefence' and movePermit:
                knight.defensive('incDefence')
                temp = HoveringText(95, 80, 'incDefence', green, font2)
                prompt = HoveringText(screenWidth / 2, 260, 'Your Defence Increased', green, font1, True)
                messages.append(prompt)
                hovering_texts_group.add(temp)

            elif picked_card == 'fireBall' and movePermit:
                pl_dmg, pl_effect = knight.offensive('fireBall')
                if pl_dmg == 0:
                    pl_attackMissed = True

            elif picked_card == 'lightningBolt' and movePermit:
                pl_dmg, pl_effect = knight.offensive('lightningBolt')
                if pl_dmg == 0:
                    pl_attackMissed = True

            elif picked_card == 'iceShard' and movePermit:
                pl_dmg, pl_effect = knight.offensive('iceShard')
                if pl_dmg == 0:
                    pl_attackMissed = True

            elif picked_card == 'stumble' and movePermit:
                print('you stumbled and lost your turn')
                prompt = HoveringText(screenWidth / 2, 260, 'You stumbled', red, font1, True)
                messages.append(prompt)

            current_turn = 1
            action_cooldown = 0
            movePermit = False
            print(picked_card)

    elif gameState == 4:  # pause
        pause()



    # draw card game part


    pygame.display.update()


pygame.quit()
