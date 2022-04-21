# main.py
import sys
import traceback

import supply
from control import *
from music import *
from view import *

# 载入游戏背景
bg = Background()
bg.init_game()

# 载入游戏音乐
music = Music()
music.init_music()


def main():
    music.start_music()
    # 生成敌人控制器实例
    enemies_control = EnemyControl(bg.bg_size)

    # 生成子弹控制器实例
    bullet_control = BulletControl(common_bullet_num=4, super_bullet_num=8, delay=100)

    # 生成补给控制实例
    supply_control = SupplyControl(bg.bg_size)

    # 生成我方飞机
    my_plane_control = MyPlaneControl(bg.bg_size)

    # 初始化敌机
    enemies_control.init_enemies()

    # 初始化子弹
    bullet_control.init_bullet(my_plane_control.my_plane.rect.midtop,
                               (my_plane_control.my_plane.rect.centerx - 33, my_plane_control.my_plane.rect.centery),
                               (my_plane_control.my_plane.rect.centerx + 30, my_plane_control.my_plane.rect.centery))

    # 创建时钟对象
    clock = pygame.time.Clock()

    # 生成分数面板控制实例
    score_control = ScoreControl()

    # 标志是否暂停游戏
    paused = False

    # 设置难度级别
    level = 1

    # 每30秒发放一个补给包
    bullet_supply = supply.BulletSupply(bg.bg_size)
    bomb_supply = supply.BombSupply(bg.bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)

    # 超级子弹定时器
    DOUBLE_BULLET_TIME = USEREVENT + 1

    # 我方无敌状态定时器
    INVINCIBLE_TIME = USEREVENT + 2

    # 标记游戏进行
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
                    if supply_control.bomb_num:
                        supply_control.bomb_num -= 1
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
                bullet_control.is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            elif event.type == INVINCIBLE_TIME:
                my_plane_control.my_plane.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

        # 根据用户的得分增加难度
        if level == 1 and score_control.score > 50000:
            level = 2
            music.upgrade_sound.play()
            # 增加3架小型敌机、2架中型敌机和1架大型敌机
            enemies_control.add_small_enemies(3)
            enemies_control.add_mid_enemies(2)
            enemies_control.add_big_enemies(1)
            # 提升小型敌机的速度
            enemies_control.inc_speed(enemies_control.small_enemies, 1)
        elif level == 2 and score_control.score > 300000:
            level = 3
            music.upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            enemies_control.add_small_enemies(5)
            enemies_control.add_mid_enemies(3)
            enemies_control.add_big_enemies(2)
            # 提升小型敌机的速度
            enemies_control.inc_speed(enemies_control.small_enemies, 1)
            enemies_control.inc_speed(enemies_control.mid_enemies, 1)
        elif level == 3 and score_control.score > 600000:
            level = 4
            music.upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            enemies_control.add_small_enemies(5)
            enemies_control.add_mid_enemies(3)
            enemies_control.add_big_enemies(2)
            # 提升小型敌机的速度
            enemies_control.inc_speed(enemies_control.small_enemies, 1)
            enemies_control.inc_speed(enemies_control.mid_enemies, 1)
        elif level == 4 and score_control.score > 1000000:
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

        if my_plane_control.life_num and not paused:
            # 检测用户的键盘操作
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                my_plane_control.my_plane.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                my_plane_control.my_plane.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                my_plane_control.my_plane.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                my_plane_control.my_plane.moveRight()

            # 绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                bg.screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, my_plane_control.my_plane):
                    music.get_bomb_sound.play()
                    if supply_control.bomb_num < 3:
                        supply_control.bomb_num += 1
                    bomb_supply.active = False

            # 绘制超级子弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move()
                bg.screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, my_plane_control.my_plane):
                    music.get_bullet_sound.play()
                    supply_control.is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bullet_supply.active = False

            if not (bullet_control.delay % 10):
                # 播放发射子弹的音乐
                music.bullet_sound.play()
                # 发射子弹
                bullet_control.shoot_bullet(my_plane_control.my_plane)

            # 检测子弹是否击中敌机
            bullet_control.is_bullet_to_enemies(bg, enemies_control)

            # 绘制大型敌机
            enemies_control.show_big_enemies(bg, music, score_control, bullet_control)

            # 绘制中型敌机：
            enemies_control.show_mid_enemies(bg, music, score_control, bullet_control)

            # 绘制小型敌机：
            enemies_control.show_small_enemies(bg, music, score_control, bullet_control)

            # 检测我方飞机是否被撞
            my_plane_control.attacked_by_enemies(enemies_control, supply_control)

            # 绘制我方飞机
            my_plane_control.show_my_plane(bg, music, supply_control, bullet_control)

            # 绘制全屏炸弹数量
            bg.show_bomb(supply_control)

            # 绘制剩余生命数量
            bg.show_life(my_plane_control)

            # 绘制得分
            bg.draw_record_panel(score=score_control.score)

        # 绘制游戏结束画面
        elif my_plane_control.life_num == 0:
            # 背景音乐停止
            pygame.mixer.music.stop()

            # 停止全部音效
            pygame.mixer.stop()

            # 停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)

            # 对分数进行存档
            score_control.write_record_score()

            # 绘制结束画面
            bg.show_end_scene(record_score=score_control.record_score, score=score_control.score)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击“重新开始”
                if bg.again_rect.left < pos[0] < bg.again_rect.right and \
                        bg.again_rect.top < pos[1] < bg.again_rect.bottom:
                    # 调用main函数，重新开始游戏
                    main()
                # 如果用户点击“结束游戏”
                elif bg.gameover_rect.left < pos[0] < bg.gameover_rect.right and \
                        bg.gameover_rect.top < pos[1] < bg.gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()

        # 绘制暂停按钮
        bg.show_pause_button()

        # 切换飞机图片
        my_plane_control.switch_plane_image(bullet_control)

        # 刷新游戏画面
        pygame.display.flip()

        # 游戏帧数
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
