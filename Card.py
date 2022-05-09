import pygame

WHITE = (255, 255, 255)


class Card(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        super().__init__()

        self.name = filename.split('.')[0]

        self.original_image = pygame.image.load('images/aliens/' + filename)
        self.original_image = pygame.transform.scale(self.original_image, (64, 96))
        self.back_image = pygame.image.load('images/aliens/' + filename)
        self.back_image = pygame.transform.scale(self.back_image, (64, 96))

        pygame.draw.rect(self.back_image, WHITE, self.back_image.get_rect())

        self.image = self.back_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shown = False

    def update(self):
        self.image = self.original_image if self.shown else self.back_image

    def show(self):
        self.shown = True

    def hide(self):
        self.shown = False
