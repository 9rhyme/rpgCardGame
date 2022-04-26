import pygame
import os
import random
import cv2
from Card import Card

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FPS = 60


class Game:
    def __init__(self, screen):
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 860
        self.level = 1
        self.level_complete = False
        self.screen = screen
        # aliens
        self.all_aliens = [f for f in os.listdir('images/aliens') if os.path.join('images/aliens', f)]

        self.img_width, self.img_height = (128, 128)
        self.padding = 20
        self.margin_top = 160
        self.cols = 4
        self.rows = 2
        self.width = 1280

        self.cards_group = pygame.sprite.Group()

        # flipping & timing
        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        # generate first level
        self.generate_level()

        # initialize video
        self.is_video_playing = True
        self.play = pygame.image.load('images/play.png').convert_alpha()
        self.stop = pygame.image.load('images/stop.png').convert_alpha()
        self.video_toggle = self.play
        self.video_toggle_rect = self.video_toggle.get_rect(topright=(self.WINDOW_WIDTH - 50, 10))
        self.get_video()

        # initialize music
        self.is_music_playing = True
        self.sound_on = pygame.image.load('images/speaker.png').convert_alpha()
        self.sound_off = pygame.image.load('images/mute.png').convert_alpha()
        self.music_toggle = self.sound_on
        self.music_toggle_rect = self.music_toggle.get_rect(topright=(self.WINDOW_WIDTH - 10, 10))

        # load music
        pygame.mixer.music.load('sounds/bg-music.mp3')
        pygame.mixer.music.set_volume(.3)
        pygame.mixer.music.play()

    def update(self, event_list):
        if self.is_video_playing:
            self.success, self.img = self.cap.read()

        self.user_input(event_list)
        self.draw()
        self.check_level_complete(event_list)

    def check_level_complete(self, event_list):
        if not self.block_game:
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for card in self.cards_group:
                        if card.rect.collidepoint(event.pos):
                            self.flipped.append(card.name)
                            card.show()
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                else:
                                    self.flipped = []
                                    for tile in self.cards_group:
                                        if tile.shown:
                                            self.level_complete = True
                                        else:
                                            self.level_complete = False
                                            break
        else:
            self.frame_count += 1
            if self.frame_count == FPS:
                self.frame_count = 0
                self.block_game = False

                for card in self.cards_group:
                    if card.name in self.flipped:
                        card.hide()
                self.flipped = []

    def generate_level(self):
        self.aliens = self.select_random_aliens()
        self.level_complete = False
        self.rows = self.level + 1
        self.cols = 4
        self.generate_cardset(self.aliens)

    def generate_cardset(self, aliens):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows

        CARDS_WIDTH = (self.img_width * self.cols + self.padding * 3)
        LEFT_MARGIN = (self.width - CARDS_WIDTH) // 2
        # cards = []
        self.cards_group.empty()

        for i in range(len(aliens)):
            x = LEFT_MARGIN + ((self.img_width + self.padding) * (i % self.cols))
            y = self.margin_top + (i // self.rows * (self.img_height + self.padding))
            card = Card(aliens[i], x, y)
            self.cards_group.add(card)

    def select_random_aliens(self):
        aliens = random.sample(self.all_aliens, (self.level + self.level + 2))
        aliens_copy = aliens.copy()
        aliens.extend(aliens_copy)
        random.shuffle(aliens)
        return aliens

    def user_input(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.music_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.is_music_playing:
                        self.is_music_playing = False
                        self.music_toggle = self.sound_off
                        pygame.mixer.music.pause()
                    else:
                        self.is_music_playing = True
                        self.music_toggle = self.sound_on
                        pygame.mixer.music.unpause()
                if self.video_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.is_video_playing:
                        self.is_video_playing = False
                        self.video_toggle = self.stop
                    else:
                        self.is_video_playing = True
                        self.video_toggle = self.play

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.level += 1
                    if self.level >= 6:
                        self.level = 1
                    self.generate_level()

    def draw(self):
        self.screen.fill(BLACK)

        # fonts
        title_font = pygame.font.Font('fonts/Little Alien.ttf', 44)
        content_font = pygame.font.Font('fonts/Little Alien.ttf', 24)

        # text
        title_text = title_font.render('Memory Game', True, WHITE)
        title_rect = title_text.get_rect(midtop=(self.WINDOW_WIDTH // 2, 10))

        level_text = content_font.render('Level ' + str(self.level), True, WHITE)
        level_rect = level_text.get_rect(midtop=(self.WINDOW_WIDTH // 2, 80))

        info_text = content_font.render('Find 2 of each', True, WHITE)
        info_rect = info_text.get_rect(midtop=(self.WINDOW_WIDTH // 2, 120))

        if self.is_video_playing:
            if self.success:
                self.screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 120))
            else:
                self.get_video()
        else:
            self.screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 120))

        if not self.level == 5:
            next_text = content_font.render('Level complete. Press Space for next level', True, WHITE)
        else:
            next_text = content_font.render('Congrats. You Won. Press Space to play again', True, WHITE)
        next_rect = next_text.get_rect(midbottom=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT - 40))

        self.screen.blit(title_text, title_rect)
        self.screen.blit(level_text, level_rect)
        self.screen.blit(info_text, info_rect)
        pygame.draw.rect(self.screen, WHITE, (self.WINDOW_WIDTH - 90, 0, 100, 50))
        self.screen.blit(self.video_toggle, self.video_toggle_rect)
        self.screen.blit(self.music_toggle, self.music_toggle_rect)

        # draw cardset
        self.cards_group.draw(self.screen)
        self.cards_group.update()

        if self.level_complete:
            self.screen.blit(next_text, next_rect)

    def get_video(self):
        self.cap = cv2.VideoCapture('video/earth.mp4')
        self.success, self.img = self.cap.read()
        self.shape = self.img.shape[1::-1]
