import pygame
import time
import random
import pygame.freetype  # 使用freetype模块支持中文

# 初始化pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# 定义窗口大小
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 创建游戏窗口
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("贪吃蛇游戏")

# 定义时钟
clock = pygame.time.Clock()

# 定义蛇的初始大小和速度
SNAKE_BLOCK = 20
SNAKE_SPEED = 15

# 定义字体（使用freetype模块）
font_style = pygame.freetype.Font(None, 50)  # 使用系统默认字体
score_font = pygame.freetype.Font(None, 35)

# 显示分数
def display_score(score):
    value, rect = score_font.render("Score: " + str(score), BLUE)
    window.blit(value, (10, 10))

# 绘制蛇
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(window, BLACK, [x[0], x[1], snake_block, snake_block])

# 显示消息
def display_message(msg, color):
    mesg, rect = font_style.render(msg, color)
    window.blit(mesg, (WINDOW_WIDTH / 6, WINDOW_HEIGHT / 3))

# 自动追踪果实的AI逻辑
def auto_move(x1, y1, food_x, food_y):
    if x1 < food_x:
        return SNAKE_BLOCK, 0  # 向右移动
    elif x1 > food_x:
        return -SNAKE_BLOCK, 0  # 向左移动
    elif y1 < food_y:
        return 0, SNAKE_BLOCK  # 向下移动
    elif y1 > food_y:
        return 0, -SNAKE_BLOCK  # 向上移动
    return 0, 0  # 保持不动

# 游戏循环
def game_loop():
    game_over = False
    game_close = False

    # 蛇的初始位置
    x1 = WINDOW_WIDTH / 2
    y1 = WINDOW_HEIGHT / 2

    # 蛇的移动变化
    x1_change = SNAKE_BLOCK  # 初始设置为向右移动
    y1_change = 0

    # 蛇的身体
    snake_list = []
    snake_length = 1

    # 果实的位置
    food_x = round(random.randrange(0, WINDOW_WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
    food_y = round(random.randrange(0, WINDOW_HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0

    while not game_over:
        # 处理所有事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_over = True
                if event.key == pygame.K_c:
                    game_loop()

        # 自动追踪果实
        x1_change, y1_change = auto_move(x1, y1, food_x, food_y)

        # 检查是否撞墙
        if x1 >= WINDOW_WIDTH or x1 < 0 or y1 >= WINDOW_HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        window.fill(WHITE)
        pygame.draw.rect(window, BLUE, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # 检查是否撞到自己
        for x in snake_list[:-1]:  # 排除蛇头本身
            if x == snake_head:
                game_close = True

        # 如果游戏结束，进入游戏结束处理逻辑
        if game_close:
            window.fill(WHITE)  # 清除屏幕
            display_message("Game Over! Press Q to Quit or C to Play Again", RED)
            display_score(snake_length - 1)  # 显示最终分数
            pygame.display.update()

            # 等待用户输入
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # 只有在游戏未结束时才绘制蛇和更新分数
        if not game_close:
            draw_snake(SNAKE_BLOCK, snake_list)
            display_score(snake_length - 1)

        pygame.display.update()

        # 检查是否吃到果实
        if not game_close and x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, WINDOW_WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
            food_y = round(random.randrange(0, WINDOW_HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0
            snake_length += 1

        # 确保蛇头不会立即与蛇身碰撞
        if len(snake_list) > 1 and snake_head in snake_list[:-1]:
            game_close = True

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

# 启动游戏
game_loop() 