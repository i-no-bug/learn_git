import webbrowser
from sys import flags

import pygame,sys
from gongju.Button import button as b
from mian.friends import Friends as h
from mian.shezhi import settings as s
from mian.Game import game as g
from mian.login import login as f
from mysql import login_mysql as m
from gongju.tupian import globals



class Login:

    # 初始化
    def __init__(self):
        # 初始化 Pygame
        pygame.init()


        # 设置窗口
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("俄罗斯方块-游戏菜单")
        # 字体
        self.font = pygame.font.Font('C:\\Windows\\Fonts\\msyhbd.ttc', 20)
        # 好友界面-提示框
        self.haoyou = False
        self.haoyuo_color = (255, 0, 0)  # 错误提示默认颜色为红色


        # 创建按钮
        self.start_button = b.Button("开始", 350, 200, 100, 50)
        self.map_button = b.Button("好友", 350, 300, 100, 50)
        self.settings_button = b.Button("设置", 350, 400, 100, 50)
        self.lioatian = b.Button('客服',0,0,100,50)
        self.lioatian1 = b.Button('登录',100,0,100,50)

        # 页面状态
        self.current_page = "login"  # 当前页面


    #按键判断-处理事件
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # 退出游戏循环
            # 检测鼠标点击事件
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左键点击
                if self.current_page == "login":
                    if self.start_button.is_hovered():
                        self.haoyou = False
                        g.main()  # 跳转到游戏界面
                    elif self.map_button.is_hovered():
                        if globals.logged_in_user:
                            self.haoyou = False
                            h.main()  # 跳转到好友界面
                        else:
                            self.haoyou = True
                    elif self.settings_button.is_hovered():
                        s.main()  # 跳转设置界面
                    elif self.lioatian.is_hovered():
                        self.haoyou = False
                        webbrowser.open_new_tab("http://127.0.0.1:5000/")

                        #进入客服
                    elif self.lioatian1.is_hovered():
                        #进入登录
                        f.main()
                        self.haoyou = False

        return True

    #绘制界面
    def draw(self):
        # 绘制背景
        s.Settings.set_draw(self)

        # 绘制按钮
        self.start_button.draw(self.screen)
        self.map_button.draw(self.screen)
        self.settings_button.draw(self.screen)
        self.lioatian.draw(self.screen)
        self.lioatian1.draw(self.screen)

        # 绘制提示信息
        if self.haoyou:
            message_surface = self.font.render('请登录', True, self.haoyuo_color)
            self.screen.blit(message_surface, (250, 325))

        # 更新显示
        pygame.display.flip()

    #游戏循环
    def run(self):
        running = True
        while running:
            # 绘制界面
            self.draw()
            # 处理事件
            running = self.handle_events()

        #循环结束-退出游戏
        pygame.quit()
        #终止程序运行
        sys.exit()


if __name__ == "__main__":
    login_screen = Login()
    login_screen.run()
    a = Login()


def main():
    a = Login()
    a.run()