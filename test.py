import pygame
from player import Player
from enemy import Enemy

pygame.init()
clock = pygame.time.Clock()
fps = 60


screenWidth = 400
screenHeight = 700

screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption('Cards & Crypts')

rpg_background = pygame.image.load('img/backgrounds/rpg_back.png')
rpg_background = pygame.transform.scale(rpg_background,(400,225))

rpg_panel = pygame.image.load('img/backgrounds/panel.png')
rpg_panel = pygame.transform.scale(rpg_panel,(400,75))
def draw_bg():
    screen.blit(rpg_background,(0,0))
def draw_panel():
    screen.blit(rpg_panel,(0,225))

plaey = Player()
demon = Enemy('demon',1)
run = True
while run:
    clock.tick(fps)
    draw_bg()
    draw_panel()
    plaey.update()
    demon.update()
    demon.draw(screen)
    plaey.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()