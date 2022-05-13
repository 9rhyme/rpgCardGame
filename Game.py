import os
import random

import pygame

from Card import Card

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FPS = 60


class Game:
    def __init__(self, screen):
        self.WINDOW_WIDTH = 400
        self.WINDOW_HEIGHT = 300
        self.level_complete = False
        self.screen = screen
        # aliens
        # self.all_aliens = [f for f in os.listdir('images/aliens') if os.path.join('images/aliens', f)]
        self.all_cards = [f for f in os.listdir('img/cards/frontface/') if os.path.join('img/cards/frontface/', f)]

        self.img_width, self.img_height = (64, 96)
        self.padding = 10
        self.margin_top = 310
        self.cols = 5
        self.rows = 4

        self.cards_group = pygame.sprite.Group()

        # flipping & timing
        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        # generate first level
        self.generate_level()

        """
        # initialize music
        self.is_music_playing = True
        self.sound_on = pygame.image.load('images/speaker.png').convert_alpha()
        self.sound_off = pygame.image.load('images/mute.png').convert_alpha()
        self.music_toggle = self.sound_on
        self.music_toggle_rect = self.music_toggle.get_rect(topright=(self.WINDOW_WIDTH - 10, self.WINDOW_HEIGHT - 10))

        # load music
        pygame.mixer.music.load('sounds/bg-music.mp3')
        pygame.mixer.music.set_volume(.2)
        pygame.mixer.music.play()
        """

    def update(self, event_list):
        self.user_input(event_list)
        self.draw()
        return self.check_level_complete(event_list)

    def check_level_complete(self, event_list):
        return_value = None
        if not self.block_game:
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for card in self.cards_group:
                        if card.rect.collidepoint(event.pos) and card.shown is not True:
                            self.flipped.append(card.name)
                            card.show()
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                else:
                                    return_value = card.name
                                    self.flipped = []
                                    for card_check in self.cards_group:
                                        if card_check.shown:
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
        return return_value

    def generate_level(self):
        self.cards = self.select_random_cards()
        self.level_complete = False
        self.generate_cardset()

    def generate_cardset(self):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows
        CARDS_WIDTH = (self.img_width * self.cols + self.padding * 3)
        LEFT_MARGIN = (self.WINDOW_WIDTH - CARDS_WIDTH) // 2
        self.cards_group.empty()

        for i in range(len(self.cards)):
            x = LEFT_MARGIN + ((self.img_width + self.padding) * (i % self.cols))
            y = self.margin_top + (i // self.rows * (self.img_height + self.padding))
            card = Card(self.cards[i], x, y)
            self.cards_group.add(card)

    def select_random_cards(self):
        cards = random.sample(self.all_cards, 5)
        cards_copy = cards.copy()
        cards.extend(cards_copy)
        random.shuffle(cards)
        return cards

    def user_input(self, event_list):
        for event in event_list:
            """
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
            """
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.generate_level()

    def draw(self):
        self.screen.fill(BLACK)

        # fonts
        content_font = pygame.font.Font('fonts/Little Alien.ttf', 24)
        next_text = content_font.render('Level complete. Press Space for next level', True, WHITE)
        next_rect = next_text.get_rect(midbottom=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT - 40))

        # pygame.draw.rect(self.screen, WHITE, (self.WINDOW_WIDTH - 90, 0, 100, 50))
        # self.screen.blit(self.music_toggle, self.music_toggle_rect)

        # draw cardset
        self.cards_group.draw(self.screen)
        self.cards_group.update()

        if self.level_complete:
            self.screen.blit(next_text, next_rect)
