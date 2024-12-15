from time import sleep
from gongju.Button import button as b
from mian.friends import Friends as m
from mian.shezhi import settings as s
from mian.Game import game as g
import pygame, sys
#显示当前设置
class GameSettings:
    difficulty = "普通"
    background = "背景1"
    #声音
    sound_volume = 50

#主要界面
class Settings:
    #初始化
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("设置")


        # 定义颜色
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (200, 200, 200)
        self.light_blue = self.black
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)

        # 字体
        self.title_font = pygame.font.Font("C:\\Windows\\Fonts\\msyhbd.ttc", 50)  # 标题字体
        self.option_font = pygame.font.Font("C:\\Windows\\Fonts\\msyh.ttc", 30)  # 选项字体
        self.small_font = pygame.font.Font("C:\\Windows\\Fonts\\msyh.ttc", 24)  # 辅助字体

        # 设置选项
        self.difficulties = ["简单", "普通", "困难"]
        self.backgrounds = ["背景1", "背景2"]
        #初始难度
        self.current_difficulty = 1
        #初始背景
        self.current_background = 0


        #声音位置初始化
        self.sound_volume = GameSettings.sound_volume

        # 创建按钮
        self.difficulty_buttons = [
            b.Button("简单", 50, 100, 100, 50),
            b.Button("普通", 170, 100, 100, 50),
            b.Button("困难", 290, 100, 100, 50)
        ]
        self.background_buttons = [
            b.Button("背景1", 50, 220, 100, 50),
            b.Button("背景2", 170, 220, 100, 50)
        ]
        self.quit_button = b.Button("退出", 650, 525, 120, 60)

        # 音量滑块
        self.slider_rect = pygame.Rect(50, 350, 300, 8)  # 滑块轨道
        self.slider_knob_rect = pygame.Rect(50 + self.sound_volume * 3 - 10, 346, 16, 16)  # 滑块按钮
        self.adjusting_volume = False  # 是否正在调整音量

    #绘制界面
    def draw(self):
        # 背景
        self.set_draw()
        # 绘制标题
        title = self.title_font.render("游戏设置", True, self.white)
        self.screen.blit(title, (300, 20))

        # 绘制难度选项
        difficulty_label = self.option_font.render("游戏难度:", True, self.white)
        self.screen.blit(difficulty_label, (50, 60))
        #循环-绘制三个难度选项
        for i, button in enumerate(self.difficulty_buttons):
            button.draw(self.screen)

        # 绘制背景选项
        background_label = self.option_font.render("背景设置:", True, self.white)
        self.screen.blit(background_label, (50, 180))
        for i, button in enumerate(self.background_buttons):
            button.draw(self.screen)

        # 绘制音量滑块
        sound_label = self.option_font.render("声音大小:", True, self.white)
        self.screen.blit(sound_label, (50, 300))
        # 滑块轨道
        pygame.draw.rect(self.screen, self.gray, self.slider_rect, border_radius=10)
        # 滑块按钮(椭圆)-slider_knob_rect四元元组
        pygame.draw.ellipse(self.screen, self.light_blue, self.slider_knob_rect)
        #显示声音比例
        sound_value = self.small_font.render(f"{self.sound_volume}%", True, self.white)
        self.screen.blit(sound_value, (370, 340))

        # 绘制当前设置
        current_settings_label = self.option_font.render("当前设置:", True, self.white)
        self.screen.blit(current_settings_label, (50, 400))
        current_difficulty_text = self.small_font.render(f"难度: {GameSettings.difficulty}", True, self.white)
        self.screen.blit(current_difficulty_text, (50, 440))
        current_background_text = self.small_font.render(f"背景: {GameSettings.background}", True, self.white)
        self.screen.blit(current_background_text, (50, 480))

        # 绘制退出按钮
        self.quit_button.draw(self.screen)

        pygame.display.flip()

    #按钮判断
    def handle_events(self):
        # 捕捉鼠标
        for event in pygame.event.get():
            # 退出
            if event.type == pygame.QUIT:
                return False
            # 点击
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    mouse_pos = event.pos
                    # 退出键
                    if self.quit_button.is_hovered():
                        sleep(0.5)
                        return False
                    # 循环-难度列表-获取索引和值
                    for i, button in enumerate(self.difficulty_buttons):
                        # 难度键是否按
                        if button.is_hovered():
                            # 修改难度-索引赋值
                            self.current_difficulty = i
                            # 显示难度
                            GameSettings.difficulty = self.difficulties[i]

                    # 循环-背景列表
                    for i, button in enumerate(self.background_buttons):
                        if button.is_hovered():
                            self.current_background = i
                            GameSettings.background = self.backgrounds[i]
                    # 是否点击声音键
                    if self.slider_knob_rect.collidepoint(mouse_pos):
                        self.adjusting_volume = True
            # 鼠标按键被释放
            elif event.type == pygame.MOUSEBUTTONUP:
                self.adjusting_volume = False
            # 鼠标是否移动
            elif event.type == pygame.MOUSEMOTION:
                # 是否需需要滑动
                if self.adjusting_volume:
                    # 当前位置mouse_x-根据鼠标位置更改
                    mouse_x = max(self.slider_rect.x, min(event.pos[0], self.slider_rect.y))
                    # 长度为300 // 3为100
                    self.sound_volume = (mouse_x - self.slider_rect.x) // 3
                    GameSettings.sound_volume = self.sound_volume
                    # 按钮位置
                    self.slider_knob_rect.x = mouse_x - 8
        return True

    #获取当前难度
    def set_game(self):
        return GameSettings.difficulty

    #获取当前背景
    def set_draw(self):
            self.image = pygame.image.load('C:\\pycharm-data\\俄罗斯方块\\图片\\1.jpg')
            self.scaled_image = pygame.transform.scale(self.image, (800, 600))
            self.image1 = pygame.image.load('C:\\pycharm-data\\俄罗斯方块\\图片\\1.img')
            self.scaled_image1 = pygame.transform.scale(self.image1, (800, 600))

            if GameSettings.background == '背景1':
                return self.screen.blit(self.scaled_image1, (0, 0))
            else:
                return self.screen.blit(self.scaled_image, (0, 0))

    # 主程序
    def run(self):
        running = True
        while running:
            #绘制界面
            self.draw()
            #处理事件
            running = self.handle_events()





def main():
    sleep(0.5)
    a = Settings()
    a.run()


if __name__ == "__main__":
    main()



