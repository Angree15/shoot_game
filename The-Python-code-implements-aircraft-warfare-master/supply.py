import pygame
from random import *


class Supply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 5
        self.active = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100


class BulletSupply(Supply):
    def __init__(self, bg_size):
        Supply.__init__(self, bg_size)
        self.image = pygame.image.load("images/bullet_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100
        self.mask = pygame.mask.from_surface(self.image)


class BombSupply(Supply):
    def __init__(self, bg_size):
        Supply.__init__(self, bg_size)
        self.image = pygame.image.load("images/bomb_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100
        self.mask = pygame.mask.from_surface(self.image)


class LifeSupply(Supply):
    def __init__(self, bg_size):
        Supply.__init__(self, bg_size)
        self.image = pygame.image.load("images/life_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100
        self.mask = pygame.mask.from_surface(self.image)


class BuffSupply(Supply):
    def __init__(self, bg_size):
        Supply.__init__(self, bg_size)
        self.image = pygame.image.load("images/buff_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100
        self.mask = pygame.mask.from_surface(self.image)


class SmallSupply(Supply):
    def __init__(self, bg_size):
        Supply.__init__(self, bg_size)
        self.image = pygame.image.load("images/small_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100
        self.mask = pygame.mask.from_surface(self.image)


class ConfuseSupply(Supply):
    def __init__(self, bg_size):
        Supply.__init__(self, bg_size)
        self.image = pygame.image.load("images/confuse_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100
        self.mask = pygame.mask.from_surface(self.image)


