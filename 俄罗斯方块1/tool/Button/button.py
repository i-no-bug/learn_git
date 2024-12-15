import pygame
from pygame.color import Color

# 按钮类
class Button:

    # 初始化
    def __init__(self, text, x, y, width, height):

        # 按钮文本
        self.text = text
        # 按钮区域9
        self.rect = pygame.Rect(x, y, width, height)

    # 绘制按钮
    def draw(self, screen):
    #先绘制按钮-悬停时的颜色
        white = (255, 255, 255)
        default_color = (181, 181, 181)  # 默认颜色
        hover_color = (191, 239, 255)  # 悬停颜色
        border_color = (0, 0, 0)  # 边框颜色
        if self.is_hovered():
            color = hover_color
        else:
            color = default_color
        #绘制
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        #绘制阴影
        shadow_rect = self.rect.move(3, 3)
        pygame.draw.rect(screen, color, shadow_rect,width=2, border_radius=10)
        #绘制边框
        pygame.draw.rect(screen, border_color, self.rect, width=2, border_radius=10)
        #创建并显示文字
        font = pygame.font.Font("C:\\Windows\\Fonts\\msyh.ttc", 36)
        text_surface = font.render(self.text, True, white)
        text_rect = text_surface.get_rect(center=self.rect.center)  # 文字矩形居中
        screen.blit(text_surface, text_rect)  # 显示文字



    #绘制对话框
    def draw_dialog(self, title, message, buttons):
        # 对话框的宽度和高度
        dialog_width = 400
        dialog_height = 300
        dialog_x = (self.screen.get_width() - dialog_width) // 2
        dialog_y = (self.screen.get_height() - dialog_height) // 2

        # 绘制对话框背景
        pygame.draw.rect(self.screen, (255, 255, 255), (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (dialog_x, dialog_y, dialog_width, dialog_height), 2)

        # 绘制对话框标题
        font = pygame.font.Font('C:\\Windows\\Fonts\\msyhbd.ttc', 24)
        title_surface = font.render(title, True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 30))
        self.screen.blit(title_surface, title_rect)

        # 绘制对话框信息
        font = pygame.font.Font('C:\\Windows\\Fonts\\msyhbd.ttc', 20)
        message_surface = font.render(message, True, (0, 0, 0))
        message_rect = message_surface.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 100))
        self.screen.blit(message_surface, message_rect)

        # 绘制按钮
        button_width = 100
        button_height = 40
        button_x = dialog_x + (dialog_width - button_width) // 2
        button_y = dialog_y + dialog_height - 70

        for button in buttons:
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(self.screen, button['color'], button_rect)
            button_text = font.render(button['text'], True, (255, 255, 255))
            button_text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, button_text_rect)
            button_y += 50  # 下一按钮位置

        pygame.display.flip()


    # 检查鼠标是否悬停在按钮上
    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)





