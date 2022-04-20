import pygame
from random import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 0
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("images/destroy_1.png").convert_alpha(),
            pygame.image.load("images/destroy_2.png").convert_alpha(),
            pygame.image.load("images/destroy_3.png").convert_alpha(),
            pygame.image.load("images/destroy_4.png").convert_alpha()
        ])

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        pass


class SmallEnemy(Enemy):
    def __init__(self, bg_size):
        Enemy.__init__(self, bg_size)
        self.image = pygame.image.load("images/enemy1.png").convert_alpha()
        self.active = True
        self.rect = self.image.get_rect()
        self.speed = 2
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-5 * self.height, 0)
        self.mask = pygame.mask.from_surface(self.image)

    def reset(self):
        self.active = True
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-5 * self.height, 0)


class MidEnemy(Enemy):
    energy = 8

    def __init__(self, bg_size):
        Enemy.__init__(self, bg_size)

        self.image = pygame.image.load("images/enemy2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-15 * self.height, -self.height)
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = 8

    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, (self.height - self.rect.height) // 2
        self.rect.top = randint(-10 * self.height, -self.height)


class BigEnemy(Enemy):
    energy = 30

    def __init__(self, bg_size):
        Enemy.__init__(self, bg_size)

        self.image = pygame.image.load("images/enemy3.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-10 * self.height, -self.height)
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = MidEnemy.energy

    def reset(self):
        self.active = True
        self.energy = BigEnemy.energy
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-10 * self.height, -5 * self.height)

