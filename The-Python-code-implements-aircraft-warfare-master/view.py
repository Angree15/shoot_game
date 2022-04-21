import pygame
from color import *


class Background:
    def __init__(self):
        # 生成pygame类
        self.init_game()
        # 游戏背景
        self.bg_size = self.width, self.height = 500, 700
        self.screen = pygame.display.set_mode(self.bg_size)
        self.image = pygame.image.load("images/background.png").convert()
        # 游戏分数面板
        self.panel_size = 36
        self.score_font = pygame.font.Font("font/font.ttf", self.panel_size)
        # 游戏结束画面
        self.gameover_font = pygame.font.Font("font/font.TTF", 48)
        self.again_image = pygame.image.load("images/again.png").convert_alpha()
        self.again_rect = self.again_image.get_rect()
        self.gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
        self.gameover_rect = self.gameover_image.get_rect()
        # 暂停游戏图标
        self.pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
        self.pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
        self.resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
        self.resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
        self.paused_rect = self.pause_nor_image.get_rect()
        self.paused_rect.left, self.paused_rect.top = self.width - self.paused_rect.width - 10, 10
        self.paused_image = self.pause_nor_image
        # 剩余生命数量
        self.life_image = pygame.image.load("images/life.png").convert_alpha()
        self.life_rect = self.life_image.get_rect()
        # 全屏炸弹数量
        self.bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
        self.bomb_rect = self.bomb_image.get_rect()
        self.bomb_font = pygame.font.Font("font/font.ttf", 48)

    # 绘制得分面板
    def draw_record_panel(self, score):
        score_text = self.score_font.render("Score : %s" % str(score), True, WHITE)
        self.screen.blit(score_text, (10, 5))

    # 绘制结束画面
    def show_end_scene(self, record_score, score):
        record_score_text = self.score_font.render("Best : %d" % record_score, True, WHITE)
        self.screen.blit(record_score_text, (50, 50))
        gameover_text1 = self.gameover_font.render("Your Score", True, WHITE)
        gameover_text1_rect = gameover_text1.get_rect()
        gameover_text1_rect.left, gameover_text1_rect.top = (
                                                                    self.width - gameover_text1_rect.width) // 2, self.height // 3
        self.screen.blit(gameover_text1, gameover_text1_rect)

        gameover_text2 = self.gameover_font.render(str(score), True, WHITE)
        gameover_text2_rect = gameover_text2.get_rect()
        gameover_text2_rect.left, gameover_text2_rect.top = (
                                                                    self.width - gameover_text2_rect.width) // 2, gameover_text1_rect.bottom + 10
        self.screen.blit(gameover_text2, gameover_text2_rect)

        self.again_rect.left, self.again_rect.top = (
                                                            self.width - self.again_rect.width) // 2, gameover_text2_rect.bottom + 50
        self.screen.blit(self.again_image, self.again_rect)

        self.gameover_rect.left, self.gameover_rect.top = (
                                                                  self.width - self.again_rect.width) // 2, self.again_rect.bottom + 10
        self.screen.blit(self.gameover_image, self.gameover_rect)

    @staticmethod
    def init_game():
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("shoot game")

    # 绘制剩余生命数量
    def show_life(self, my_plane_control):
        if my_plane_control.life_num:
            for i in range(my_plane_control.life_num):
                self.screen.blit(self.life_image,
                                 (self.width - 10 - (i + 1) * self.life_rect.width,
                                  self.height - 10 - self.life_rect.height))

    # 绘制全屏炸弹数量
    def show_bomb(self, supply_control):
        bomb_text = self.bomb_font.render("× %d" % supply_control.bomb_num, True, WHITE)
        text_rect = bomb_text.get_rect()
        self.screen.blit(self.bomb_image, (10, self.height - 10 - self.bomb_rect.height))
        self.screen.blit(bomb_text, (20 + self.bomb_rect.width, self.height - 5 - text_rect.height))

    # 绘制暂停按钮
    def show_pause_button(self):
        self.screen.blit(self.paused_image, self.paused_rect)
