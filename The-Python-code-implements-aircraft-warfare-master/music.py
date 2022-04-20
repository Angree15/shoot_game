import pygame


# 载入游戏音乐
class Music:
    def __init__(self):
        self.bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
        self.bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
        self.supply_sound = pygame.mixer.Sound("sound/supply.wav")
        self.get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
        self.get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
        self.enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
        self.upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
        self.enemy1_destroy_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
        self.enemy2_destroy_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
        self.enemy3_destroy_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
        self.me_destroy_sound = pygame.mixer.Sound("sound/me_down.wav")

    def init_music(self):
        pygame.mixer.music.load("sound/game_music.ogg")
        pygame.mixer.music.set_volume(0.2)
        self.bullet_sound.set_volume(0.2)
        self.bomb_sound.set_volume(0.2)
        self.supply_sound.set_volume(0.2)
        self.get_bomb_sound.set_volume(0.2)
        self.get_bullet_sound.set_volume(0.2)
        self.upgrade_sound.set_volume(0.2)
        self.enemy3_fly_sound.set_volume(0.2)
        self.enemy1_destroy_sound.set_volume(0.2)
        self.enemy2_destroy_sound.set_volume(0.2)
        self.enemy3_destroy_sound.set_volume(0.5)
        self.me_destroy_sound.set_volume(0.2)

    @staticmethod
    def start_music():
        pygame.mixer.music.play(-1)
