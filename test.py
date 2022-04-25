import pygame
from healthBar import  HealthBar
from player import Player
from enemy import Enemy

pygame.init()
clock = pygame.time.Clock()
fps = 60

clicked = False

messages = []
currMsg = 0
messages.append('Currently testing')

screenWidth = 400
screenHeight = 700

screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption('Cards & Crypts')

# define game variaables
current_turn = 0 # 0: your turn , 1 : enemy's turn
action_waitTime = 90
action_cooldown = 0

# define font
font = pygame.font.SysFont('Jokerman',25)
#define colors
red = (255, 0, 0)
green = (0, 255, 0)
white = (255,255,255)

rpg_background = pygame.image.load('img/backgrounds/rpg_back.png')
rpg_background = pygame.transform.scale(rpg_background,(400,225))

rpg_panel = pygame.image.load('img/backgrounds/panel.png')
rpg_panel = pygame.transform.scale(rpg_panel,(400,75))
def draw_bg():
    screen.blit(rpg_background,(0,0))
def draw_panel():
    #draw panel rectangle
    screen.blit(rpg_panel,(0,225))
    # draw text
    draw_text(messages[currMsg],font,white,90,230)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    rect = img.get_rect(center=(screenWidth/2, 260))
    screen.blit(img,rect)

plaey = Player()
demon = Enemy('demon',1)
playerHealthBar = HealthBar(50,50,plaey.curr_health,plaey.max_health)
demonHealthBar = HealthBar(270,30,demon.curr_health,demon.max_health)
run = True
while run:
    clock.tick(fps)
    draw_bg()
    draw_panel()
    playerHealthBar.draw(plaey.curr_health/plaey.max_health,screen)
    demonHealthBar.draw(demon.curr_health/demon.max_health, screen)
    plaey.update()
    demon.update()
    demon.draw(screen)
    plaey.draw(screen)


    #control player action






    # player action

    # enemy action:
    if demon.alive:
        if current_turn ==1:
            action_cooldown+=1
            if action_cooldown>= action_waitTime:
                dmg,effect = demon.attack()
                plaey.recieveDamage(dmg,effect)
                current_turn = 0
                action_cooldown = 0



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print('aa')
                if plaey.alive:
                    if current_turn == 0:
                        action_cooldown += 1
                        if action_cooldown <= action_waitTime:
                            dmg, effect = plaey.offensive('basicAttack')
                            demon.recieveDamage(dmg, effect)
                            current_turn = 1
                            action_cooldown = 0
        else:
            clicked = False
    pygame.display.update()
pygame.quit()