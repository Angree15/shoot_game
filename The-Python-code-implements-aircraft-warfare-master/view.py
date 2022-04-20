import pygame


class Background:
    def __init__(self):
        self.size = self.width, self.height = 500, 700
        self.screen = pygame.display.set_mode(self.size)
        self.image = pygame.image.load("images/background.png").convert()

    def init_background(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("shoot game -- FishC Demo")
