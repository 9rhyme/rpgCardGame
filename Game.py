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
        self.all_cards = [f for f in os.listdir('img/cards/frontface/') if os.path.join('img/cards/frontface/', f)]
        self.img_width, self.img_height = (70, 96)
        self.padding = 10
        self.margin_top = 310
        self.cols = 5
        self.rows = 5
        self.cards_group = pygame.sprite.Group()

        # flipping & timing
        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        # generate first level
        self.generate_level()

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
                            if card.name == "stumble":
                                self.block_game = True
                                return_value = card.name
                                self.flipped = []
                                for card_check in self.cards_group:
                                    if card_check.shown:
                                        self.level_complete = True
                                    else:
                                        self.level_complete = False
                                        break
                                return return_value
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                    return_value = "wrong"
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
        CARDS_WIDTH = (self.img_width * self.cols + self.padding * 3)
        LEFT_MARGIN = (self.WINDOW_WIDTH - CARDS_WIDTH) // 2 - 5
        self.cards_group.empty()

        for i in range(len(self.cards)):
            x = LEFT_MARGIN + ((self.img_width + self.padding) * (i % self.cols))
            y = self.margin_top + (i // self.rows * (self.img_height + self.padding))
            card = Card(self.cards[i], x, y)
            self.cards_group.add(card)
        self.show_cards()

    def select_random_cards(self):
        cards = random.sample(self.all_cards, 10)
        cards_copy = cards.copy()
        cards.extend(cards_copy)
        random.shuffle(cards)
        return cards

    def user_input(self, event_list):
        for event in event_list:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.generate_level()

    def draw(self):
        # fonts
        content_font = pygame.font.Font('fonts/font_4.ttf', 24)
        next_text = content_font.render('Press Space for New Deck', True, BLACK)
        next_rect = next_text.get_rect(midbottom=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT - 250))

        # draw cardset
        self.cards_group.draw(self.screen)
        self.cards_group.update()

        if self.level_complete:
            self.screen.blit(next_text, next_rect)

    def show_cards(self):
        delay = 5
        for card in self.cards_group:
            card.show()
        self.cards_group.update()
        self.cards_group.draw(self.screen)
        pygame.display.flip()
        pygame.event.pump()
        pygame.time.delay(1000 * delay)
        for card in self.cards_group:
            card.hide()
