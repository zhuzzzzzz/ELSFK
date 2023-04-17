import sys
import pygame

from settings import Settings
from game_container import *


class GameCtrolor:
    def __init__(self):
        # 程序参数
        self.setting = Settings()
        self.fall_time_temp = self.setting.fall_time
        self.run_flag = 1
        self.game_flag = True

        # 初始化GameContainer类对象
        self.game_ctaner = GameContainer(self.setting.row_num, self.setting.column_num)

        self.game_ctaner.new_falling_rect()

        # pygame初始化
        pygame.init()
        self.screen = pygame.display.set_mode((self.setting.width, self.setting.height))
        pygame.display.set_caption('俄罗斯方块')
        self.screen.fill((255, 255, 255))  # 设置背景白色，可以防止出现黑色的方块间隔
        self.REFRESH_TIMER = pygame.USEREVENT  # 定义pygame用户事件，此处为定时器，即屏幕每隔100ms刷新一次
        self.FALL_TIMER = pygame.USEREVENT + 1  # 定义pygame用户事件，此处为定时器，即元素每隔500ms下落一格
        pygame.time.set_timer(self.REFRESH_TIMER, self.setting.refresh_time)  # 设置事件定时触发
        pygame.time.set_timer(self.FALL_TIMER, self.fall_time_temp)

        self.font = pygame.font.SysFont(None, 42)

        while True:
            # 循环获取事件，监听事件状态
            for event in pygame.event.get():
                # 判断用户是否点了"X"关闭按钮,并执行if代码段
                if event.type == pygame.KEYDOWN:  # 暂停监测
                    if event.key == pygame.K_ESCAPE:
                        self.run_flag = (self.run_flag + 1) % 2
                if event.type == pygame.QUIT:
                    # 卸载所有模块
                    pygame.quit()
                    # 终止程序，确保退出程序
                    sys.exit()
                if self.game_flag and self.run_flag == 1:  # 游戏运行部分
                    if event.type == self.REFRESH_TIMER:
                        self.refresh_process()
                    if event.type == self.FALL_TIMER:
                        self.falling_process()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.keyboard_answering('clockwise')
                        if event.key == pygame.K_DOWN:
                            self.keyboard_answering('anti-clockwise')
                        if event.key == pygame.K_LEFT:
                            self.keyboard_answering('move_left')
                        if event.key == pygame.K_RIGHT:
                            self.keyboard_answering('move_right')
                        if event.key == pygame.K_SPACE:
                            self.keyboard_answering('accelerate_fall')

    def keyboard_answering(self, command):
        if command == 'clockwise':
            self.game_ctaner.ctrl_rotating('clockwise')
        elif command == 'anti-clockwise':
            self.game_ctaner.ctrl_rotating('anti-clockwise')
        elif command == 'move_left':
            self.game_ctaner.ctrl_moving('left')
        elif command == 'move_right':
            self.game_ctaner.ctrl_moving('right')
        elif command == 'accelerate_fall':
            pygame.time.set_timer(self.FALL_TIMER, int(self.setting.refresh_time * 2))
            pass
        # self.refresh_process()  # 每次按键都立刻刷新屏幕

    def refresh_process(self):  # 屏幕刷新的处理程序
        ans = self.game_ctaner.display_rect()
        self.plot(ans)
        pygame.display.flip()  # 更新屏幕内容
        if ans[1] is None:
            self.new_falling()

    def falling_process(self):
        self.game_ctaner.ctrl_falling()
        self.refresh_process()  # 每次下落后都刷新屏幕
        if self.game_ctaner.post_fall():  # 如果有需要消除的方块，需等待一段时间
            pygame.time.wait(int(self.fall_time_temp / 2))
        if not self.game_ctaner.run_flag:  # 每次下落后若game_ctaner.run_flag为False，则游戏失败
            self.game_flag = False

    def new_falling(self):
        # 刷新一个下落元素，将下落时间调为self.fall_time_temp
        self.speed_ctrl()
        pygame.time.set_timer(self.FALL_TIMER, self.fall_time_temp)
        self.game_ctaner.new_falling_rect()

    def plot(self, res):
        game_rect = res[0]
        color_rect = res[1]

        # 游戏方块显示
        for i in range(self.setting.row_num):
            for j in range(self.setting.column_num):
                if game_rect[i][j] == 1:
                    temp = pygame.Surface((self.setting.unit_length - 1, self.setting.unit_length - 1),
                                          flags=pygame.HWSURFACE)
                    temp.fill(self.setting.rect_color)
                    self.screen.blit(temp, (j * self.setting.unit_length, i * self.setting.unit_length))
                elif game_rect[i][j] == 0:
                    temp = pygame.Surface((self.setting.unit_length, self.setting.unit_length), flags=pygame.HWSURFACE)
                    temp.fill(self.setting.background_color)
                    self.screen.blit(temp, (j * self.setting.unit_length, i * self.setting.unit_length))
                else:
                    temp = pygame.Surface((self.setting.unit_length - 1, self.setting.unit_length - 1),
                                          flags=pygame.HWSURFACE)
                    temp.fill(self.setting.bad_colar)
                    self.screen.blit(temp, (j * self.setting.unit_length, i * self.setting.unit_length))
                if color_rect:
                    if color_rect[i][j] == 1:
                        temp = pygame.Surface((self.setting.unit_length - 1, self.setting.unit_length - 1),
                                              flags=pygame.HWSURFACE)
                        temp.fill(self.setting.falling_rect_color)
                        self.screen.blit(temp, (j * self.setting.unit_length, i * self.setting.unit_length))

        # 计分板方块显示
        if game_rect[1][self.game_ctaner.width - 2] == 1:
            text = self.font.render(f"{self.game_ctaner.score}", True, (0, 0, 0), self.setting.rect_color)
        else:
            text = self.font.render(f"{self.game_ctaner.score}", True, (0, 0, 0), self.setting.background_color)
        if color_rect:
            if color_rect[1][self.game_ctaner.width - 2] == 1:
                text = self.font.render(f"{self.game_ctaner.score}", True, (0, 0, 0), self.setting.falling_rect_color)
        self.screen.blit(text, ((self.game_ctaner.width - 2) * self.setting.unit_length, 1 * self.setting.unit_length))

    def speed_ctrl(self):
        if 100 <= self.game_ctaner.score < 200:
            self.fall_time_temp = self.setting.fall_time - 100
        if 200 <= self.game_ctaner.score < 400:
            self.fall_time_temp = self.setting.fall_time - 200
        if self.game_ctaner.score > 400:
            self.fall_time_temp = self.setting.fall_time - 300


if __name__ == '__main__':
    pass
    g = GameCtrolor()
