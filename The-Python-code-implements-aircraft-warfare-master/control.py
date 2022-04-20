import pygame
from enemy import SmallEnemy, MidEnemy, BigEnemy
from bullet import commonBullet, superBullet
from color import *


class EnemyControl:
    def __init__(self, bg_size):
        self.bg_size = bg_size
        self.switch_image = True  # 用于切换图片
        self.enemies = pygame.sprite.Group()
        self.small_enemies = pygame.sprite.Group()
        self.mid_enemies = pygame.sprite.Group()
        self.big_enemies = pygame.sprite.Group()
        self.init_enemies()

    def add_small_enemies(self, num):
        for i in range(num):
            e1 = SmallEnemy(self.bg_size)
            self.small_enemies.add(e1)
            self.enemies.add(e1)

    def add_mid_enemies(self, num):
        for i in range(num):
            e2 = MidEnemy(self.bg_size)
            self.mid_enemies.add(e2)
            self.enemies.add(e2)

    def add_big_enemies(self, num):
        for i in range(num):
            e3 = BigEnemy(self.bg_size)
            self.big_enemies.add(e3)
            self.enemies.add(e3)

    @staticmethod
    def inc_speed(target, inc):
        for each in target:
            each.speed += inc

    # 绘制小型敌机
    def show_small_enemies(self, space_scene, score_panel_control, myPlane_control):
        for each in self.small_enemies:
            if each.active:
                each.move()
                space_scene.screen.blit(each.image, each.rect)
            else:
                # 毁灭
                if not (myPlane_control.bullet_control.delay % 3):
                    if myPlane_control.my_plane.e1_destroy_index == 0:
                        space_scene.enemy1_destroy_sound.play()
                    space_scene.screen.blit(each.destroy_images[myPlane_control.my_plane.e1_destroy_index], each.rect)
                    myPlane_control.my_plane.e1_destroy_index = (myPlane_control.my_plane.e1_destroy_index + 1) % 4
                    if myPlane_control.my_plane.e1_destroy_index == 0:
                        score_panel_control.score += 1000
                        each.reset()

    def show_mid_enemies(self, space_scene, score_panel_control, myPlane_control):
        # 绘制中型敌机
        for each in self.mid_enemies:
            if each.active:
                each.move()
                space_scene.screen.blit(each.image, each.rect)

                # 绘制血槽
                pygame.draw.line(space_scene.screen, BLACK,
                                 (each.rect.left, each.rect.top - 5),
                                 (each.rect.right, each.rect.top - 5),
                                 2)
                # 当生命大于20%显示绿色，否则显示红色
                energy_remain = each.energy / MidEnemy.energy
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(space_scene.screen, energy_color,
                                 (each.rect.left, each.rect.top - 5),
                                 (each.rect.left + each.rect.width * energy_remain,
                                  each.rect.top - 5), 2)
            else:
                # 毁灭
                if not (myPlane_control.bullet_control.delay % 3):
                    if myPlane_control.my_plane.e2_destroy_index == 0:
                        space_scene.enemy2_destroy_sound.play()
                    space_scene.screen.blit(each.destroy_images[myPlane_control.my_plane.e2_destroy_index], each.rect)
                    myPlane_control.my_plane.e2_destroy_index = (myPlane_control.my_plane.e2_destroy_index + 1) % 4
                    if myPlane_control.my_plane.e2_destroy_index == 0:
                        score_panel_control.score += 2000
                        each.reset()

    def show_big_enemies(self, space_scene, score_panel_control, myPlane_control):
        # 绘制大型敌机
        for each in self.big_enemies:
            if each.active:
                each.move()
                space_scene.screen.blit(each.image, each.rect)

                # 绘制血槽
                pygame.draw.line(space_scene.screen, BLACK,
                                 (each.rect.left, each.rect.top - 5),
                                 (each.rect.right, each.rect.top - 5),
                                 2)
                # 当生命大于20%显示绿色，否则显示红色
                energy_remain = each.energy / BigEnemy.energy
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(space_scene.screen, energy_color,
                                 (each.rect.left, each.rect.top - 5),
                                 (each.rect.left + each.rect.width * energy_remain,
                                  each.rect.top - 5), 2)

                # 即将出现在画面中，播放音效
                if each.rect.bottom == -50:
                    space_scene.enemy3_fly_sound.play(-1)
            else:
                # 毁灭
                if not (myPlane_control.bullet_control.delay % 3):
                    if myPlane_control.my_plane.e3_destroy_index == 0:
                        space_scene.enemy3_destroy_sound.play()
                    space_scene.screen.blit(each.destroy_images[myPlane_control.my_plane.e3_destroy_index], each.rect)
                    myPlane_control.my_plane.e3_destroy_index = (myPlane_control.my_plane.e3_destroy_index + 1) % 4
                    if myPlane_control.my_plane.e3_destroy_index == 0:
                        space_scene.enemy3_fly_sound.stop()
                        score_panel_control.score += 5000
                        each.reset()

    def show_enemies(self, space_scene, score_panel_control, myPlane_control):
        self.show_big_enemies(space_scene, score_panel_control, myPlane_control)  # 绘制大型敌机
        self.show_mid_enemies(space_scene, score_panel_control, myPlane_control)  # 绘制中型敌机
        self.show_small_enemies(space_scene, score_panel_control, myPlane_control)  # 绘制小型敌机

    def init_enemies(self):
        self.add_small_enemies(15)  # 生成敌方小型敌机
        self.add_mid_enemies(4)  # 生成敌方中型敌机
        self.add_big_enemies(2)  # 生成敌方大型敌机


class BulletControl:
    def __init__(self, common_bullet_num, super_bullet_num):
        """
        common_bullet_num:画面上显示发射的普通子弹数量
        super_bullet_num:画面上显示发射的超级子弹数量
        """
        self.bullets = []
        self.common_bullet = []
        self.common_bullet_index = 0
        self.common_bullet_num = common_bullet_num
        self.super_bullet = []
        self.super_bullet_index = 0
        self.super_bullet_num = super_bullet_num
        # 标志是否使用超级子弹
        self.is_double_bullet = False

    # 生成普通子弹
    def add_common_bullet(self, midTop_position):
        """
        midTop_position:飞机弹孔的中心位置-->元组
        """
        for i in range(self.common_bullet_num):
            self.common_bullet.append(commonBullet(midTop_position))

    # 生成超级子弹
    def add_super_bullet(self, leftTop, rightTop):
        """
        leftTop:飞机左边弹孔的位置-->元组
        rightTop:飞机右边弹孔的位置-->元组
        """
        for i in range(self.super_bullet_num // 2):
            self.super_bullet.append(superBullet(leftTop))
            self.super_bullet.append(superBullet(rightTop))

    # 初始化子弹
    def init_bullet(self, midTop, leftTop, rightTop):
        """
        midTop:飞机中间弹孔的位置-->元组
        leftTop:飞机左边弹孔的位置-->元组
        rightTop:飞机右边弹孔的位置-->元组
        """
        self.add_common_bullet(midTop)
        self.add_super_bullet(leftTop, rightTop)

    # 发射超级子弹
    def shoot_super_bullet(self, my_plane):
        """
        my_plane:飞机类-->MyPlane
        """
        self.bullets = self.super_bullet
        self.bullets[self.super_bullet_index].reset((my_plane.rect.centerx - 33, my_plane.rect.centery))
        self.bullets[self.super_bullet_index + 1].reset((my_plane.rect.centerx + 30, my_plane.rect.centery))
        self.super_bullet_index = (self.super_bullet_index + 2) % self.super_bullet_num

    # 发射普通子弹
    def shoot_common_bullet(self, my_plane):
        """
        my_plane:飞机类-->MyPlane
        """
        self.bullets = self.common_bullet
        self.bullets[self.common_bullet_index].reset(my_plane.rect.midtop)
        self.common_bullet_index = (self.common_bullet_index + 1) % self.common_bullet_num

    # 发射子弹
    def shoot_bullet(self, my_plane):
        """
        my_plane:飞机类-->MyPlane
        """
        if self.is_double_bullet:
            # 发射超级子弹
            self.shoot_super_bullet(my_plane)
        else:
            # 发射普通子弹
            self.shoot_common_bullet(my_plane)
