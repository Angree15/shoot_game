import pygame
from myplane import MyPlane
from bullet import CommonBullet, SuperBullet
from pygame.locals import *
from enemy import SmallEnemy, MidEnemy, BigEnemy
from bullet import CommonBullet, SuperBullet
from color import *
from supply import *


class MyPlaneControl:
    def __init__(self, bg_size):
        # 生命数量
        self.life_image = pygame.image.load("images/life.png").convert_alpha()
        self.life_rect = self.life_image.get_rect()
        self.life_num = 3
        self.key_pressed = pygame.key.get_pressed()
        self.my_plane = MyPlane(bg_size)
        self.me_destroy_index = 0
        # 用于切换图片
        self.switch_image = True

    # 检测我方飞机是否被撞
    def attacked_by_enemies(self, enemies_control, supply_control):
        enemies_down = pygame.sprite.spritecollide(self.my_plane, enemies_control.enemies, False,
                                                   pygame.sprite.collide_mask)
        if enemies_down and not supply_control.is_buff:
            self.my_plane.active = False
            for e in enemies_down:
                e.active = False
        elif enemies_down and supply_control.is_buff:
            for e in enemies_down:
                e.active = False

    def attacked_by_planets(self, bg_control, supply_control):
        planets_down = pygame.sprite.spritecollide(self.my_plane, bg_control.planets, False,
                                                   pygame.sprite.collide_mask)
        if planets_down and not supply_control.is_buff:
            self.my_plane.active = False
            for e in planets_down:
                e.active = False
        elif planets_down and supply_control.is_buff:
            for e in planets_down:
                e.active = False

    #  毁灭飞机
    def destroy_my_plane(self, bg, music, supply_control):
        if self.me_destroy_index == 0:
            music.me_destroy_sound.play()
        bg.screen.blit(self.my_plane.destroy_images[self.me_destroy_index], self.my_plane.rect)
        self.my_plane.me_destroy_index = (self.me_destroy_index + 1) % 3
        if self.me_destroy_index == 0:
            self.life_num -= 1
            self.my_plane.reset()
            pygame.time.set_timer(supply_control.buff_time, 3 * 1000)

    # 绘制我方飞机
    def show_my_plane(self, bg, music, supply_control, bullet_control):
        if self.my_plane.active:
            if self.switch_image:
                bg.screen.blit(self.my_plane.image1, self.my_plane.rect)
            else:
                bg.screen.blit(self.my_plane.image2, self.my_plane.rect)
        else:
            if not (bullet_control.delay % 3):
                self.destroy_my_plane(bg, music, supply_control)  # 毁灭飞机

    def move(self, supply_control):
        self.key_pressed = pygame.key.get_pressed()
        if not supply_control.is_confuse:
            if self.key_pressed[K_w] or self.key_pressed[K_UP]:
                self.my_plane.moveUp()
            if self.key_pressed[K_s] or self.key_pressed[K_DOWN]:
                self.my_plane.moveDown()
            if self.key_pressed[K_a] or self.key_pressed[K_LEFT]:
                self.my_plane.moveLeft()
            if self.key_pressed[K_d] or self.key_pressed[K_RIGHT]:
                self.my_plane.moveRight()
        else:
            if self.key_pressed[K_w] or self.key_pressed[K_UP]:
                self.my_plane.moveDown()
            if self.key_pressed[K_s] or self.key_pressed[K_DOWN]:
                self.my_plane.moveUp()
            if self.key_pressed[K_a] or self.key_pressed[K_LEFT]:
                self.my_plane.moveRight()
            if self.key_pressed[K_d] or self.key_pressed[K_RIGHT]:
                self.my_plane.moveLeft()

    # 切换图片
    def switch_plane_image(self, bullet_control):
        if not (bullet_control.delay % 5):
            self.switch_image = not self.switch_image
        bullet_control.delay -= 1
        if not bullet_control.delay:
            bullet_control.delay = 100


class BulletControl:
    def __init__(self, common_bullet_num, super_bullet_num, delay):
        """
        common_bullet_num:画面上显示发射的普通子弹数量
        super_bullet_num:画面上显示发射的超级子弹数量
        """
        self.bullets = []
        self.common_bullet = []
        self.common_bullet_index = 0
        self.common_bullet_num = common_bullet_num
        self.super_bullet = []
        self.delay = delay
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
            self.common_bullet.append(CommonBullet(midTop_position))

    # 生成超级子弹
    def add_super_bullet(self, leftTop, rightTop):
        """
        leftTop:飞机左边弹孔的位置-->元组
        rightTop:飞机右边弹孔的位置-->元组
        """
        for i in range(self.super_bullet_num // 2):
            self.super_bullet.append(SuperBullet(leftTop))
            self.super_bullet.append(SuperBullet(rightTop))

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



    # 检测子弹是否击中敌机
    def is_bullet_to_enemies(self, bg, enemies_control):
        for b in self.bullets:
            if b.active:
                b.move()
                bg.screen.blit(b.image, b.rect)
                enemy_hit = pygame.sprite.spritecollide(b, enemies_control.enemies, False,
                                                        pygame.sprite.collide_mask)
                if enemy_hit:
                    b.active = False
                    for e in enemy_hit:
                        if e in enemies_control.mid_enemies or e in enemies_control.big_enemies:
                            e.hit = True
                            e.energy -= 1
                            if e.energy == 0:
                                e.active = False
                        else:
                            e.active = False


class SupplyControl:
    def __init__(self, bg_size):
        self.bullet_supply = BulletSupply(bg_size)
        self.bomb_supply = BombSupply(bg_size)
        self.life_supply = LifeSupply(bg_size)
        self.buff_supply = BuffSupply(bg_size)
        self.small_supply = SmallSupply(bg_size)
        self.confuse_supply = ConfuseSupply(bg_size)
        self.bomb_num = 3
        # 每15秒发放一个补给包
        pygame.time.set_timer(USEREVENT, 5 * 1000)
        # 补给时间
        self.supply_time = USEREVENT
        # 解除我方超级子弹定时器
        self.double_bullet_time = USEREVENT + 1
        # 解除我方无敌状态定时器
        self.buff_time = USEREVENT + 2
        # 解除我方变小状态定时器
        self.small_time = USEREVENT + 3
        # 解除我方混乱状态定时器
        self.confuse_time = USEREVENT + 4
        # 标志是否使用超级子弹
        self.is_double_bullet = False
        # 标志是否进入无敌状态
        self.is_buff = False
        # 标志是否进入变小状态
        self.is_small = False
        # 标志是否进入混乱状态
        self.is_confuse = False
        # # 全屏炸弹
        # self.bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
        # self.confuse_image = pygame.image.load("images/confuse.png").convert_alpha()
        # self.buff_image = pygame.image.load("images/buff.png").convert_alpha()
        # self.small_image = pygame.image.load("images/small.png").convert_alpha()
        # self.black_hole_image = pygame.image.load("images/black_hole.png").convert_alpha()
        # self.super_bullet_image = pygame.image.load("images/super_bullet.png").convert_alpha()
        # self.bomb_rect = self.bomb_image.get_rect()
        # self.bomb_font = pygame.font.Font("font/font.ttf", 48)
        # self.bomb_num = 3
        # self.bomb_text = self.bomb_font.render("× %d" % self.bomb_num, True, WHITE)
        # self.text_rect = self.bomb_text.get_rect()

    # 获得全屏炸弹补给
    def get_bomb_supply(self, space_scene, myPlane_control):
        if self.bomb_supply.active:
            self.bomb_supply.move()
            space_scene.screen.blit(self.bomb_supply.image, self.bomb_supply.rect)
            if pygame.sprite.collide_mask(self.bomb_supply, myPlane_control.my_plane):
                space_scene.get_bomb_sound.play()
                self.bomb_num += 1
                self.bomb_supply.active = False

    # 获得超级子弹补给
    def get_super_bullet_supply(self, space_scene, myPlane_control):
        if self.bullet_supply.active:
            self.bullet_supply.move()
            space_scene.screen.blit(self.bullet_supply.image, self.bullet_supply.rect)
            if pygame.sprite.collide_mask(self.bullet_supply, myPlane_control.my_plane):
                space_scene.get_bullet_sound.play()
                self.is_double_bullet = True
                self.bullet_supply.active = False
                pygame.time.set_timer(self.double_bullet_time, 18 * 1000)

    # 获得生命补给
    def get_life_supply(self, space_scene, myPlane_control):
        if self.life_supply.active:
            self.life_supply.move()
            space_scene.screen.blit(self.life_supply.image, self.life_supply.rect)
            if pygame.sprite.collide_mask(self.life_supply, myPlane_control.my_plane):
                space_scene.get_bomb_sound.play()
                if myPlane_control.my_plane.life_num < 10:
                    myPlane_control.my_plane.add_life()
                self.life_supply.active = False

    # 获得无敌状态补给
    def get_buff_supply(self, space_scene, myPlane_control):
        if self.buff_supply.active:
            self.buff_supply.move()
            space_scene.screen.blit(self.buff_supply.image, self.buff_supply.rect)
            if pygame.sprite.collide_mask(self.buff_supply, myPlane_control.my_plane):
                space_scene.get_bomb_sound.play()
                self.is_buff = True
                myPlane_control.my_plane.image = pygame.image.load("images/buff_me.png").convert_alpha()
                self.buff_supply.active = False
                pygame.time.set_timer(self.buff_time, 18 * 1000)

    # 获得变小状态补给
    def get_small_supply(self, space_scene, myPlane_control):
        if self.small_supply.active:
            self.small_supply.move()
            space_scene.screen.blit(self.small_supply.image, self.small_supply.rect)
            if pygame.sprite.collide_mask(self.small_supply, myPlane_control.my_plane):
                space_scene.get_bomb_sound.play()
                self.is_small = True
                myPlane_control.my_plane.image = pygame.image.load("images/small_me.png").convert_alpha()
                myPlane_position = myPlane_control.my_plane.rect.left, myPlane_control.my_plane.rect.top
                myPlane_control.my_plane.rect = myPlane_control.my_plane.image.get_rect()
                myPlane_control.my_plane.rect.left, myPlane_control.my_plane.rect.top = myPlane_position
                self.small_supply.active = False
                pygame.time.set_timer(self.small_time, 18 * 1000)

    # 获得混乱状态补给
    def get_confuse_supply(self, space_scene, myPlane_control):
        if self.confuse_supply.active:
            self.confuse_supply.move()
            space_scene.screen.blit(self.confuse_supply.image, self.confuse_supply.rect)
            if pygame.sprite.collide_mask(self.confuse_supply, myPlane_control.my_plane):
                space_scene.get_bomb_sound.play()
                self.is_confuse = True
                self.confuse_supply.active = False
                pygame.time.set_timer(self.confuse_time, 18 * 1000)

    # 检测是否获得补给
    def get_supply(self, space_scene, myPlane_control):
        self.get_bomb_supply(space_scene, myPlane_control)  # 检测全屏炸弹补给是否获得
        self.get_super_bullet_supply(space_scene, myPlane_control)  # 检测超级子弹补给是否获得
        self.get_life_supply(space_scene, myPlane_control)  # 出现生命补给，并检测生命补给是否获得
        self.get_buff_supply(space_scene, myPlane_control)  # 检测无敌补给是否获得
        self.get_small_supply(space_scene, myPlane_control)  # 检测变小补给是否获得
        self.get_confuse_supply(space_scene, myPlane_control)  # 检测混乱补给是否获得

    # # 显示全屏炸弹数量
    # def show_bombSupply_num(self, space_scene):
    #     self.bomb_text = self.bomb_font.render("× %d" % self.bomb_num, True, WHITE)
    #     text_rect = self.bomb_text.get_rect()
    #     space_scene.screen.blit(self.bomb_image, (10, space_scene.height - 10 - self.bomb_rect.height))
    #     space_scene.screen.blit(self.bomb_text, (20 + self.bomb_rect.width, space_scene.height - 5 - text_rect.height))
    #
    # # 显示混乱状态
    # def show_confuse_supply(self, space_scene):
    #     space_scene.screen.blit(self.confuse_image,
    #                             (self.bomb_rect.width + self.text_rect.width + 120,
    #                              space_scene.height - 10 - self.bomb_rect.height))
    #
    # # 显示变小状态
    # def show_small_supply(self, space_scene):
    #     space_scene.screen.blit(self.small_image,
    #                             (self.bomb_rect.width + self.text_rect.width + 180,
    #                              space_scene.height - 10 - self.bomb_rect.height))
    #
    # # 显示无敌状态
    # def show_buff_supply(self, space_scene):
    #     space_scene.screen.blit(self.buff_image,
    #                             (self.bomb_rect.width + self.text_rect.width + 240,
    #                              space_scene.height - 10 - self.bomb_rect.height))
    #
    # # 显示出现黑洞状态
    # def show_black_hole_supply(self, space_scene):
    #     space_scene.screen.blit(self.black_hole_image,
    #                             (self.bomb_rect.width + self.text_rect.width + 300,
    #                              space_scene.height - 10 - self.bomb_rect.height))
    #
    # # 显示双倍子弹状态
    # def show_super_bullet_supply(self, space_scene):
    #     space_scene.screen.blit(self.super_bullet_image,
    #                             (self.bomb_rect.width + self.text_rect.width + 360,
    #                              space_scene.height - 10 - self.bomb_rect.height))


class EnemyControl:
    def __init__(self, bg_size):
        self.bg_size = bg_size
        self.enemies = pygame.sprite.Group()
        self.small_enemies = pygame.sprite.Group()
        self.mid_enemies = pygame.sprite.Group()
        self.big_enemies = pygame.sprite.Group()
        # 中弹图片索引
        self.e1_destroy_index = 0
        self.e2_destroy_index = 0
        self.e3_destroy_index = 0
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
    def show_small_enemies(self, bg, music, score_panel_control, bullet_control):
        for each in self.small_enemies:
            if each.active:
                each.move()
                bg.screen.blit(each.image, each.rect)
            else:
                # 毁灭
                if not (bullet_control.delay % 3):
                    if self.e1_destroy_index == 0:
                        music.enemy1_destroy_sound.play()
                    bg.screen.blit(each.destroy_images[self.e1_destroy_index], each.rect)
                    self.e1_destroy_index = (self.e1_destroy_index + 1) % 4
                    if self.e1_destroy_index == 0:
                        score_panel_control.score += 1000
                        each.reset()

    def show_mid_enemies(self, bg, music, score_panel_control, bullet_control):
        # 绘制中型敌机
        for each in self.mid_enemies:
            if each.active:
                each.move()
                bg.screen.blit(each.image, each.rect)

                # 绘制血槽
                pygame.draw.line(bg.screen, BLACK,
                                 (each.rect.left, each.rect.top - 5),
                                 (each.rect.right, each.rect.top - 5),
                                 2)
                # 当生命大于20%显示绿色，否则显示红色
                energy_remain = each.energy / MidEnemy.energy
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(bg.screen, energy_color,
                                 (each.rect.left, each.rect.top - 5),
                                 (each.rect.left + each.rect.width * energy_remain,
                                  each.rect.top - 5), 2)
            else:
                # 毁灭
                if not (bullet_control.delay % 3):
                    if self.e2_destroy_index == 0:
                        music.enemy2_destroy_sound.play()
                    bg.screen.blit(each.destroy_images[self.e2_destroy_index], each.rect)
                    self.e2_destroy_index = (self.e2_destroy_index + 1) % 4
                    if self.e2_destroy_index == 0:
                        score_panel_control.score += 2000
                        each.reset()

    def show_big_enemies(self, bg, music, score_panel_control, bullet_control):
        # 绘制大型敌机
        for each in self.big_enemies:
            if each.active:
                each.move()
                bg.screen.blit(each.image, each.rect)

                # 绘制血槽
                pygame.draw.line(bg.screen, BLACK,
                                 (each.rect.left, each.rect.top - 5),
                                 (each.rect.right, each.rect.top - 5),
                                 2)
                # 当生命大于20%显示绿色，否则显示红色
                energy_remain = each.energy / BigEnemy.energy
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(bg.screen, energy_color,
                                 (each.rect.left, each.rect.top - 5),
                                 (each.rect.left + each.rect.width * energy_remain,
                                  each.rect.top - 5), 2)

                # 即将出现在画面中，播放音效
                if each.rect.bottom == -50:
                    music.enemy3_fly_sound.play(-1)
            else:
                # 毁灭
                if not (bullet_control.delay % 3):
                    if self.e3_destroy_index == 0:
                        music.enemy3_destroy_sound.play()
                    bg.screen.blit(each.destroy_images[self.e3_destroy_index], each.rect)
                    self.e3_destroy_index = (self.e3_destroy_index + 1) % 4
                    if self.e3_destroy_index == 0:
                        music.enemy3_fly_sound.stop()
                        score_panel_control.score += 5000
                        each.reset()

    def show_enemies(self, bg, score_panel_control, myPlane_control, bullet_control):
        self.show_big_enemies(bg, score_panel_control, myPlane_control, bullet_control)  # 绘制大型敌机
        self.show_mid_enemies(bg, score_panel_control, myPlane_control, bullet_control)  # 绘制中型敌机
        self.show_small_enemies(bg, score_panel_control, myPlane_control, bullet_control)  # 绘制小型敌机

    def init_enemies(self):
        self.add_small_enemies(15)  # 生成敌方小型敌机
        self.add_mid_enemies(4)  # 生成敌方中型敌机
        self.add_big_enemies(2)  # 生成敌方大型敌机


class ScoreControl:
    def __init__(self):
        # 记录当前得分
        self.score = 0
        # 记录历史的分
        self.record_score = 0
        # 用于阻止重复打开记录文件
        self.recorded = False

    # 读取历史最高得分
    def read_record_score(self):
        with open("record.txt", "r") as f:
            self.record_score = int(f.read())

    # 如果玩家得分高于历史最高得分，则存档
    def write_record_score(self):
        if not self.recorded:
            self.recorded = True
            self.read_record_score()
            if self.score > self.record_score:
                with open("record.txt", "w") as f:
                    f.write(str(self.score))
