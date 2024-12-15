from msilib.schema import SelfReg
from time import sleep
import pygame
import requests
from gongju.Button import button as b
from mian.shezhi import settings as s
from mysql import add_friends as hy
class LoginScreen:
    # 初始化+
    def __init__(self):
        self.y_move = 100  # 修正为 self.y_move，避免局部变量名错误
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("登录")

        # 配色方案
        self.input_box_color = (255, 255, 255)  # 输入框颜色
        self.border_color = (200, 200, 200)  # 边框颜色
        self.button_color = (0, 122, 255)  # 按钮颜色
        self.text_color = (0, 0, 0)  # 文本颜色
        self.cursor_color = (0, 0, 0)  # 光标颜色

        # 字体
        self.font = pygame.font.Font('C:\\Windows\\Fonts\\msyhbd.ttc', 20)

        # 好友列表
        self.friends = []

        # 账号输入框
        self.username_box = pygame.Rect(250, 10, 300, 40)
        self.quit_button = b.Button("退出", 0, 0, 100, 50)
        self.look_button = b.Button("搜索", 550, 10 / 5, 100, 50)

        # 用户输入
        # 记录输入账号
        self.username = ""
        self.username_len = 0
        self.active_box = None  # 当前活动输入框

        # 光标闪烁控制
        self.cursor_visible = False
        self.cursor_timer = 0
        self.cursor_flash_rate = 500  # 光标闪烁间隔（毫秒）

        # 提示信息
        self.message = ""
        self.message_color = (255, 0, 0)  # 错误提示默认颜色为红色

        # 创建 MySQL 实例
        self.mysql = hy.MySQL()

    # 绘制界面
    def draw(self):
        # 绘制背景
        s.Settings.set_draw(self)

        # 绘制退出按钮
        self.quit_button.draw(self.screen)

        # 绘制登录按钮
        self.look_button.draw(self.screen)

        # 绘制用户名输入框
        pygame.draw.rect(self.screen, self.input_box_color, self.username_box)
        pygame.draw.rect(self.screen, self.border_color, self.username_box, width=2)
        if not self.username and self.active_box != "username":
            username_hint = self.font.render("请输入账号", True, (150, 150, 150))
            self.screen.blit(username_hint, (self.username_box.x + 5, self.username_box.y + 8))
        else:
            username_surface = self.font.render(self.username, True, self.text_color)
            self.screen.blit(username_surface, (self.username_box.x + 5, self.username_box.y + 8))

        # 绘制光标
        if self.cursor_visible:
            if self.active_box == "username":
                cursor_x = self.username_box.x + 5 + self.font.size(self.username)[0]
                pygame.draw.line(self.screen, self.cursor_color, (cursor_x, self.username_box.y + 8),
                                 (cursor_x, self.username_box.y + 32), width=2)

        # 绘制提示信息
        if self.message:
            message_surface = self.font.render(self.message, True, self.message_color)
            self.screen.blit(message_surface, (250, 50))

        # 绘制好友列表及删除按钮
        if self.friends:
            y_offset = 100  # 从 (10, 100) 开始绘制好友列表
            for index, friend in enumerate(self.friends):
                friend_surface = self.font.render(friend, True, self.border_color)
                pygame.draw.rect(self.screen, self.border_color, pygame.Rect(10, y_offset, 200, 40), 2)
                self.screen.blit(friend_surface, (10, y_offset + 8))

                # 绘制删除按钮
                delete_button = b.Button("删除", 220, y_offset, 100, 40)
                delete_button.draw(self.screen)
                if delete_button.is_hovered():
                    # 如果鼠标悬停，显示提示信息
                    delete_hover_text = self.font.render("点击删除", True, self.text_color)
                    self.screen.blit(delete_hover_text, (220, y_offset + 50))

                # 如果点击了删除按钮
                if delete_button.is_hovered() and pygame.mouse.get_pressed()[0]:
                    self.remove_friend(index)

                y_offset += 50  # 每个好友占50像素高度

    # 输入
    def handle_input(self, event):
        # 用户名输入处理
        if self.active_box == "username":
            if event.key == pygame.K_BACKSPACE:
                # 删除字符并更新长度
                self.username = self.username[:-1]
            elif len(self.username) < 10:
                # 添加字符，但限制长度
                self.username += event.unicode

    # 连接数据库-验证账号
    def check_login(self):
        a = self.mysql.look_user(self.username)  # 调用 MySQL 实例的 look_user 方法
        if a:
            self.message = f"找到{self.username},正在自动添加好友"
            self.friends.append(self.username)
        else:
            self.message = f'没有找到{self.username}'

    # 删除好友
    def remove_friend(self, index):
        if 0 <= index < len(self.friends):
            del self.friends[index]
            self.message = "好友已删除"

    # 事件处理
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.quit_button.is_hovered():
                    sleep(0.5)
                    return False
                # 按了活动窗口
                elif self.username_box.collidepoint(event.pos):
                    # 当前活动窗为 username
                    self.active_box = "username"
                # 按了搜索
                elif self.look_button.is_hovered():
                    if self.username in self.friends:
                        self.message = "你已经添加了此好友，无法在添加"
                    elif len(self.friends) < 7:
                        # 连接数据库，进行比对
                        self.check_login()
                    else:
                        self.message = "好友已满，无法添加"
                else:
                    self.active_box = None
            elif event.type == pygame.KEYDOWN and self.active_box:
                self.handle_input(event)
        return True

    # 主程序
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(60)
            self.draw()

            running = self.handle_events()

            # 控制光标闪烁
            self.cursor_timer += clock.get_time()
            if self.cursor_timer >= self.cursor_flash_rate:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
            pygame.display.flip()


def main():
    sleep(0.5)
    app = LoginScreen()
    app.run()


if __name__ == "__main__":
    main()
