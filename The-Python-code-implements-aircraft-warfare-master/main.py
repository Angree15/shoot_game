# main.py
import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply

from pygame.locals import *
from random import *
from music import *
from view import *
from control import *

# 载入游戏背景
bg = Background()
bg.init_background()

# 载入游戏音乐
music = Music()
music.init_music()


def main():
    music.start_music()
    # 生成敌人控制器实例
    enemies_control = EnemyControl(bg.size)

    # 生成子弹控制器实例
    bullet_control = BulletControl(common_bullet_num=4, super_bullet_num=8)

    # 生成我方飞机
    my_plane = myplane.MyPlane(bg.size)

    # 初始化敌机
    enemies_control.init_enemies()

    # 初始化子弹
    bullet_control.init_bullet(my_plane.rect.midtop,
                               (my_plane.rect.centerx - 33, my_plane.rect.centery),
                               (my_plane.rect.centerx + 30, my_plane.rect.centery))

    # 创建时钟对象
    clock = pygame.time.Clock()
    
    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0
    
    # 统计得分
    score = 0
    score_font = pygame.font.Font("font/font.ttf", 36)
    
    # 标志是否暂停游戏
    paused = False
    pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = bg.width - paused_rect.width - 10, 10
    paused_image = pause_nor_image
    
    # 设置难度级别
    level = 1
    
    # 全屏炸弹
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 48)
    bomb_num = 3
    
    # 每30秒发放一个补给包
    bullet_supply = supply.BulletSupply(bg.size)
    bomb_supply = supply.BombSupply(bg.size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
    
    # 超级子弹定时器
    DOUBLE_BULLET_TIME = USEREVENT + 1
    
    # 我方无敌状态定时器
    INVINCIBLE_TIME = USEREVENT + 2
    
    # 生命数量
    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3
    
    # 用于阻止重复打开记录文件
    recorded = False
    
    # 游戏结束画面
    gameover_font = pygame.font.Font("font/font.TTF", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()
    
    # 用于切换图片
    switch_image = True
    
    # 用于延迟
    delay = 100
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
            
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        music.bomb_sound.play()
                        for each in enemies_control.enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            
            elif event.type == SUPPLY_TIME:
                music.supply_sound.play()
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            
            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)
            
            elif event.type == INVINCIBLE_TIME:
                my_plane.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)
        
        # 根据用户的得分增加难度
        if level == 1 and score > 50000:
            level = 2
            music.upgrade_sound.play()
            # 增加3架小型敌机、2架中型敌机和1架大型敌机
            enemies_control.add_small_enemies(3)
            enemies_control.add_mid_enemies(2)
            enemies_control.add_big_enemies(1)
            # 提升小型敌机的速度
            enemies_control.inc_speed(enemies_control.small_enemies, 1)
        elif level == 2 and score > 300000:
            level = 3
            music.upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            enemies_control.add_small_enemies(5)
            enemies_control.add_mid_enemies(3)
            enemies_control.add_big_enemies(2)
            # 提升小型敌机的速度
            enemies_control.inc_speed(enemies_control.small_enemies, 1)
            enemies_control.inc_speed(enemies_control.mid_enemies, 1)
        elif level == 3 and score > 600000:
            level = 4
            music.upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            enemies_control.add_small_enemies(5)
            enemies_control.add_mid_enemies(3)
            enemies_control.add_big_enemies(2)
            # 提升小型敌机的速度
            enemies_control.inc_speed(enemies_control.small_enemies, 1)
            enemies_control.inc_speed(enemies_control.mid_enemies, 1)
        elif level == 4 and score > 1000000:
            level = 5
            music.upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            enemies_control.add_small_enemies(5)
            enemies_control.add_mid_enemies(3)
            enemies_control.add_big_enemies(2)
            # 提升小型敌机的速度
            enemies_control.inc_speed(enemies_control.small_enemies, 1)
            enemies_control.inc_speed(enemies_control.mid_enemies, 1)
        
        bg.screen.blit(bg.image, (0, 0))
        
        if life_num and not paused:
            # 检测用户的键盘操作
            key_pressed = pygame.key.get_pressed()
            
            if key_pressed[K_w] or key_pressed[K_UP]:
                my_plane.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                my_plane.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                my_plane.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                my_plane.moveRight()
            
            # 绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                bg.screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, my_plane):
                    music.get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False
            
            # 绘制超级子弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move()
                bg.screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, my_plane):
                    music.get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bullet_supply.active = False

            if not (delay % 10):
                # 播放发射子弹的音乐
                music.bullet_sound.play()
                # 发射子弹
                bullet_control.shoot_bullet(my_plane)
            
            # 检测子弹是否击中敌机
            for b in bullet_control.bullets:
                if b.active:
                    b.move()
                    bg.screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies_control.enemies, False, pygame.sprite.collide_mask)
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
            
            # 绘制大型敌机
            for each in enemies_control.big_enemies:
                if each.active:
                    each.move()
                    bg.screen.blit(each.image, each.rect)
                    
                    # 绘制血槽
                    pygame.draw.line(bg.screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)
                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.BigEnemy.energy
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
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            music.enemy3_destroy_sound.play()
                        bg.screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 4
                        if e3_destroy_index == 0:
                            music.enemy3_fly_sound.stop()
                            score += 10000
                            each.reset()
            
            # 绘制中型敌机：
            for each in enemies_control.mid_enemies:
                if each.active:
                    each.move()
                    bg.screen.blit(each.image, each.rect)
                    
                    # 绘制血槽
                    pygame.draw.line(bg.screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)
                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
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
                    if not (delay % 3):
                        if e2_destroy_index == 0:
                            music.enemy2_destroy_sound.play()
                        bg.screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            each.reset()
            
            # 绘制小型敌机：
            for each in enemies_control.small_enemies:
                if each.active:
                    each.move()
                    bg.screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    if not (delay % 3):
                        if e1_destroy_index == 0:
                            music.enemy1_destroy_sound.play()
                        bg.screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()
            
            # 检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(my_plane, enemies_control.enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not my_plane.invincible:
                my_plane.active = False
                for e in enemies_down:
                    e.active = False
            
            # 绘制我方飞机
            if my_plane.active:
                if switch_image:
                    bg.screen.blit(my_plane.image1, my_plane.rect)
                else:
                    bg.screen.blit(my_plane.image2, my_plane.rect)
            else:
                # 毁灭
                if not (delay % 3):
                    if me_destroy_index == 0:
                        music.me_destroy_sound.play()
                    bg.screen.blit(my_plane.destroy_images[me_destroy_index], my_plane.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        my_plane.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)
            
            # 绘制全屏炸弹数量
            bomb_text = bomb_font.render("× %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            bg.screen.blit(bomb_image, (10, bg.height - 10 - bomb_rect.height))
            bg.screen.blit(bomb_text, (20 + bomb_rect.width, bg.height - 5 - text_rect.height))
            
            # 绘制剩余生命数量
            if life_num:
                for i in range(life_num):
                    bg.screen.blit(life_image,
                                (bg.width - 10 - (i + 1) * life_rect.width,
                                 bg.height - 10 - life_rect.height))
            
            # 绘制得分
            score_text = score_font.render("Score : %s" % str(score), True, WHITE)
            bg.screen.blit(score_text, (10, 5))
        
        # 绘制游戏结束画面
        elif life_num == 0:
            # 背景音乐停止
            pygame.mixer.music.stop()
            
            # 停止全部音效
            pygame.mixer.stop()
            
            # 停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)
            
            if not recorded:
                recorded = True
                # 读取历史最高得分
                with open("record.txt", "r") as f:
                    record_score = int(f.read())
                
                # 如果玩家得分高于历史最高得分，则存档
                if score > record_score:
                    with open("record.txt", "w") as f:
                        f.write(str(score))
            
            # 绘制结束画面
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            bg.screen.blit(record_score_text, (50, 50))
            
            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                (bg.width - gameover_text1_rect.width) // 2, bg.height // 3
            bg.screen.blit(gameover_text1, gameover_text1_rect)
            
            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                (bg.width - gameover_text2_rect.width) // 2, \
                gameover_text1_rect.bottom + 10
            bg.screen.blit(gameover_text2, gameover_text2_rect)
            
            again_rect.left, again_rect.top = \
                (bg.width - again_rect.width) // 2, \
                gameover_text2_rect.bottom + 50
            bg.screen.blit(again_image, again_rect)
            
            gameover_rect.left, gameover_rect.top = \
                (bg.width - again_rect.width) // 2, \
                again_rect.bottom + 10
            bg.screen.blit(gameover_image, gameover_rect)
            
            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击“重新开始”
                if again_rect.left < pos[0] < again_rect.right and \
                        again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数，重新开始游戏
                    main()
                # 如果用户点击“结束游戏”
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                        gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()
                    
                    # 绘制暂停按钮
        bg.screen.blit(paused_image, paused_rect)
        
        # 切换图片
        if not (delay % 5):
            switch_image = not switch_image
        
        delay -= 1
        if not delay:
            delay = 100
        
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
