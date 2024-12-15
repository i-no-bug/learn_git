import pygame,random,sys
from time import sleep
from gongju.Button import button as b
from mian.friends import Friends as m
from mian.shezhi import settings as s
from mian.Game import game as g
from gongju.Button import difficulty as d
from mian.interface import Interface as l


class TetrisGame:
    # 初始化
    def __init__(self):
        pygame.init()

        # 设置窗口
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("俄罗斯方块游戏")
        # 字体
        font1 = pygame.font.Font("C:\\Windows\\Fonts\\msyh.ttc", 20)
        self.font2 = pygame.font.Font("C:\\Windows\\Fonts\\msyh.ttc", 36)

        # 游戏区域网格
        self.grid_width = 10  # 列数
        self.grid_height = 20  # 行数
        self.block_size = 30  # 每个方块大小-长和宽

        # 黑色游戏区域位置和尺寸
        # 起始点
        self.game_x = 220
        self.game_y = 0
        # 进行计算找出宽，高
        self.game_width = self.grid_width * self.block_size
        self.game_height = self.grid_height * self.block_size

        # 初始化网格和游戏属性，列表-grid = [[0] * 行数]
        self.grid = [[0] * self.grid_width for _ in range(self.grid_height)]
        # 分数
        self.score = 0
        #绘制按钮等
        self.quit_button = b.Button('退出', 650, 525, 100, 50)
        self.set_up = b.Button('设置',10,10,100,50)
        self.next_block_text = font1.render("下一个方块:", True, (255, 255, 255))
        self.k_left = font1.render('左移动：\u2190', True, (255, 255, 255))
        self.k_right = font1.render('旋转：   \u2191', True, (255, 255, 255))
        self.k_up = font1.render('右移动：\u2192', True, (255, 255, 255))
        self.k_down = font1.render('下移动：\u2193', True, (255, 255, 255))

        # 方块形状
        self.shapes = [
            [[1, 1, 1, 1]],  # I 形
            [[1, 1], [1, 1]],  # O 形
            [[0, 1, 0], [1, 1, 1]],  # T 形
            [[1, 1, 0], [0, 1, 1]],  # S 形
            [[0, 1, 1], [1, 1, 0]],  # Z 形
            [[1, 0, 0], [1, 1, 1]],  # L 形
            [[0, 0, 1], [1, 1, 1]]  # J 形
        ]

        # 当前方块
        self.current_shape = random.choice(self.shapes)
        # 下一个方块
        self.next_shape = random.choice(self.shapes)
        # 渲染颜色
        # self.current_color = (255 ,255, 240	)
        # 初始位置--没有在游戏方框设置，单独设置
        self.shape_x, self.shape_y = 3, 0  # 初始位置
        # 是否超出栈顶
        self.game_over = False
        # 中间 - 黑色游戏区域
        pygame.draw.rect(self.screen, (83, 134, 139), (self.game_x, self.game_y, self.game_width, self.game_height))

    #绘制方块-填充
    def draw_grid(self):
        # 遍历每一行（y方向）和每一列（x方向）的网格单元
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                # 绘制方块
                a = d.Difficulty.Blind_chess(self)
                if a:
                    # 绘制已填充的方块
                    if self.grid[y][x]:
                        pygame.draw.rect(self.screen, self.grid[y][x], pygame.Rect(
                            # 左上角坐标-网格起始位置 + 移动位置
                            self.game_x + x * self.block_size,
                            self.game_y + y * self.block_size,
                            self.block_size - 2, self.block_size - 2
                        )
                                         )
                # 绘制网格线
                pygame.draw.rect(self.screen, (250, 250, 210), pygame.Rect(
                    self.game_x + x * self.block_size,
                    self.game_y + y * self.block_size,
                    self.block_size, self.block_size
                ), width=1
                                 )

    # 绘制方块-出现
    def draw_shape(self):
        """在给定位置绘制指定形状的俄罗斯方块"""
        # y:整下标索引，整方块
        for y, row in enumerate(self.current_shape):
            # x:分方块索引，分方块
            for x, cell in enumerate(row):
                # 如果是1
                if cell:
                    # 绘制矩形-draw.rect(窗口，颜色，方块区域)
                    pygame.draw.rect(self.screen, (142, 229, 238), pygame.Rect(
                        # 黑色起始点 + (移动 + 方块索引)* 30
                        self.game_x + (self.shape_x + x) * self.block_size,
                        self.game_y + (self.shape_y + y) * self.block_size,
                        # 宽减2，高减2
                        self.block_size - 2, self.block_size - 2
                    )
                                     )

    # 方块的旋转
    def rotate_shape(self):
        # zip(*)行变列，列变行--转置矩阵
        rotated_shape = [list(row) for row in zip(*self.current_shape[::-1])]
        # 原来的矩阵进行备份
        old_shape = self.current_shape
        # 将新矩阵替换原来的
        self.current_shape = rotated_shape
        # 检查碰撞
        if self.check_collision(0, 0):
            self.current_shape = old_shape

    # 是否有下移动-检查是否有碰撞
    def drop_shape(self):
        # 如果没有碰撞，向下移动方块
        if not self.check_collision(0, 1):
            self.shape_y += 1
        else:
            # 如果发生碰撞，锁定方块
            self.lock_shape()

    # 碰撞停止
    def check_collision(self, dx, dy):
        # 需要找到方块1的位置
        for y, row in enumerate(self.current_shape):
            # x:方块形状的索引 cell：方块值
            for x, cell in enumerate(row):
                if cell:
                    # 计算当前方块单元格移动后的目标位置
                    new_x = self.shape_x + x + dx
                    new_y = self.shape_y + y + dy
                    # x方向是否超出范围两边已经y是否超出范围
                    if new_x < 0 or new_x >= self.grid_width or new_y >= self.grid_height:
                        return True
                    # 如果有方块
                    if self.grid[new_y][new_x]:
                        return True
        return False

    # 锁定方块
    def lock_shape(self):
        list1 = ['#e1930e', '#0eaae1', '#e4f16a']
        a = random.choice(list1)
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    # 锁定当前方块到网格
                    new_y = self.shape_y + y
                    new_x = self.shape_x + x
                    if new_y <= 0:  # 检查是否有方块在顶部之外
                        self.game_over = True
                        return  # 立即返回，结束游戏
                    self.grid[new_y][new_x] = a
        # 是否满行
        self.clear_lines()
        # 当前方块转换为下一个方块
        self.current_shape = self.next_shape
        # 下一个方块转换为下下一个方块
        self.next_shape = random.choice(self.shapes)
        # 当前方块初始位置
        self.shape_x, self.shape_y = 3, 0

    # 满行消除
    def clear_lines(self):
        lines_to_clear = []
        # 检查每一行中是否有满行
        for y in range(self.grid_height):
            # all-看查列表中是否有元素，且值大于1
            if all(self.grid[y]):
                # 记录行索引
                lines_to_clear.append(y)

        # 更新分数和消除行
        for y in lines_to_clear:
            # 每消除一行加分
            self.score += 100
            # 删除满的行,且会自动下移
            del self.grid[y]
            # 在顶部插入新行
            self.grid.insert(0, [0] * self.grid_width)
    # 行移动
    def move_shape(self, dx):
        if not self.check_collision(dx, 0):
            self.shape_x += dx

    # 显示下一个即将出现的方块
    def draw_next_shape(self):
        for y, row in enumerate(self.next_shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, (142, 229, 238), pygame.Rect(650 + x * 30, 100 + y * 30, 29, 29))

    # 结束界面
    def exit_out(self):
        if self.game_over:
            running = True  # 控制循环运行状态

            # 初始化字体，设置字体样式和大小
            self.font = pygame.font.Font("C:\\Windows\\Fonts\\msyh.ttc", 36)

            # 小屏幕矩形的区域定义
            popup_rect = pygame.Rect(200, 150, 400, 300)

            # 按钮尺寸和位置参数
            button_width, button_height = 150, 40  # 按钮宽度和高度
            button_gap = 20  # 按钮之间的水平间距

            # 重新开始按钮的位置计算
            restart_button_rect = pygame.Rect(
                popup_rect.centerx - button_width - button_gap // 2,  # 左侧按钮x坐标
                popup_rect.centery + 30,  # 按钮y坐标（中心稍偏下）
                button_width,
                button_height,
            )

            # 返回菜单按钮的位置计算
            menu_button_rect = pygame.Rect(
                popup_rect.centerx + button_gap // 2,  # 右侧按钮x坐标
                popup_rect.centery + 30,  # 按钮y坐标（中心稍偏下）
                button_width,
                button_height,
            )

            # 创建按钮对象
            self.restart_button = Button("重新开始", restart_button_rect.x, restart_button_rect.y, button_width,
                                         button_height)
            self.menu_button = Button("返回菜单", menu_button_rect.x, menu_button_rect.y, button_width, button_height)

            # 游戏结束界面循环
            while running:
                self.screen.fill((0, 0, 0))  # 绘制黑色背景

                # 绘制小屏幕矩形作为弹窗
                pygame.draw.rect(self.screen, (50, 50, 50), popup_rect)  # 灰色背景
                pygame.draw.rect(self.screen, (200, 200, 200), popup_rect, 5)  # 白色边框

                # 显示“游戏结束”文字
                game_over_text = self.font.render("游戏结束", True, (255, 0, 0))  # 渲染红色字体
                text_rect = game_over_text.get_rect(center=(popup_rect.centerx, popup_rect.top + 40))  # 文字位置顶部居中
                self.screen.blit(game_over_text, text_rect)  # 绘制文字

                # 绘制两个按钮
                self.restart_button.draw(self.screen)  # 绘制"重新开始"按钮
                self.menu_button.draw(self.screen)  # 绘制"返回菜单"按钮

                # 事件监听
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # 处理窗口关闭事件
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 处理鼠标左键点击事件
                        if self.restart_button.is_hovered():  # 检查是否点击了"重新开始"按钮
                            running = False  # 停止当前界面循环，返回游戏主逻辑
                        elif self.menu_button.is_hovered():  # 检查是否点击了"返回菜单"按钮
                            l.main()  # 调用主菜单函数，返回菜单界面

                # 刷新屏幕显示
                pygame.display.flip()

    #获取游戏难度
    def get1(self):
        chess = s.Settings.set_game(self)
        if chess == '简单':
            return 1000
        elif chess == '普通':
            return 500
        elif chess == '困难':
            return 100
        else:
            return 500

    # 界面
    def draw(self):

        # 绘制左边界面
        #pygame.draw.rect(self.screen, (122, 197, 205), (0, 0, 250, 600))
        s.Settings.set_draw(self)
        # 中间 - 黑色游戏区域
        pygame.draw.rect(self.screen, (83, 134, 139), (self.game_x, self.game_y, self.game_width, self.game_height))

        # 右边界面
        #pygame.draw.rect(self.screen, (121, 205, 205), (519, 0, 400, 600))


        # 左---绘画分数栏,时间栏
        score_text = self.font2.render(f"分数: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 100))

        # 中----绘制网格
        self.draw_grid()
        # 中---- 绘画方块
        self.draw_shape()

        # 右---绘制预测方块区
        self.screen.blit(self.k_left, (620,310))
        self.screen.blit(self.k_right, (620, 360))
        self.screen.blit(self.k_up, (620, 410))
        self.screen.blit(self.k_down, (620,460))
        self.screen.blit(self.next_block_text, (620, 50))

        # 显示下一个即将出现的方块
        self.draw_next_shape()

        # 绘制退出键按钮
        self.quit_button.draw(self.screen)
        #绘制设置
        self.set_up.draw(self.screen)

    # 主程序--游戏循环
    def run(self):
        # 帧率控制器
        clock = pygame.time.Clock()
        self.drop_timer = 0  # 方块下落计时器
        drop_interval = self.get1()  # 普通下落间隔
        fast_drop_interval = 50  # 快速下落间隔
        fast_drop_active = False  # 是否激活快速下落
        # 绘制界面
        self.draw()

        running = True
        while running:
            # 获取循环时间
            delta_time = clock.tick(30)  # 限制帧率为60帧
            self.drop_timer += delta_time

            # 绘制界面
            self.draw()
            self.exit_out()

            # 自动下落：根据当前状态选择下落间隔
            current_interval = fast_drop_interval if fast_drop_active else drop_interval
            if self.drop_timer >= current_interval:
                self.drop_shape()
                self.drop_timer = 0

            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_shape(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.move_shape(1)
                    #持续下落
                    elif event.key == pygame.K_DOWN:
                        fast_drop_active = True  # 启动快速下落
                    elif event.key == pygame.K_UP:
                        self.rotate_shape()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        fast_drop_active = False  # 停止快速下落
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.quit_button.is_hovered():
                        return
                    elif event.button == 1 and self.set_up.is_hovered():
                        s.main()

            # 刷新屏幕
            pygame.display.flip()


def main():
    sleep(0.5)
    game = TetrisGame()
    game.run()


if __name__ == '__main__':
    main()
