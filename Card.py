import pygame

WHITE = (255, 255, 255)


class Card(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        super().__init__()

        self.name = filename.split('.')[0]

        self.original_image = pygame.image.load('img/cards/frontface/' + filename)
        self.original_image = pygame.transform.scale(self.original_image, (70, 96))
        self.back_image = pygame.image.load('img/cards/frontface/' + filename)
        self.back_image = pygame.transform.scale(self.back_image, (70, 96))
        self.background_image = pygame.image.load('img/cards/background.png')
        self.background_image = pygame.transform.scale(self.background_image, (70, 96))

        pygame.draw.rect(self.back_image, WHITE, self.back_image.get_rect())

        self.image = self.background_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shown = False

    def update(self):
        self.image = self.original_image if self.shown else self.background_image

    def show(self):
        self.shown = True

    def hide(self):
        self.shown = False
