import os.path
from pathlib import Path
import pygame
import sys
import time
import numpy as np
from minesweeper import Minesweeper, MinesweeperAI
from stage import Stage
import mines_func
from mines_board import Minesboard, difficulty_levels, difficulty_settings

HEIGHT = 8
WIDTH = 8
MINES = 8

# 紀錄讀入的txt檔中地雷出現的位置
mines_loc = []
# 要輸出的圖片名稱
pic_name = "test"
# 從標題階段開始，相當於1
stage = Stage.INSTRUCTIONS.value

# # 設定不同難度的名稱及初始參數(長, 寬, 地雷數)
# difficulty_levels = ["Beginner", "Intermediate", "Expert", "Custom", "Read setup txt"]
# difficulty_settings = {
#     difficulty_levels[0]: (9, 9, 10),
#     difficulty_levels[1]: (16, 16, 40),
#     difficulty_levels[2]: (16, 30, 99),
#     difficulty_levels[3]: (24, 30, 0),
#     difficulty_levels[4]: (None, None, 0)
# }

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)
RED = (255, 0, 0)

# Create game
pygame.init()
mines_board = Minesboard()

screen = pygame.display.set_mode(mines_board.board_size())

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Compute board size
width = mines_board.width
height = mines_board.height
BOARD_PADDING = mines_board.BOARD_PADDING
# board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
# board_height = height - (BOARD_PADDING * 2)
# cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
# board_origin = (BOARD_PADDING, BOARD_PADDING)
#
# # Add images
flag_img = pygame.image.load("assets/images/flag.png")
# flag_img = pygame.transform.scale(flag_img, (cell_size, cell_size))
mine_img = pygame.image.load("assets/images/mine.png")
# mine_img = pygame.transform.scale(mine_img, (cell_size, cell_size))
mine_red_img = pygame.image.load("assets/images/mine-red.png")
# mine_red_img = pygame.transform.scale(mine_red_img, (cell_size, cell_size))

# Detonated mine
mine_detonated = None

# Create game and AI agent
game = Minesweeper(HEIGHT=HEIGHT, WIDTH=WIDTH, MINES=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
lost = False
win = False
# # Show instructions initially
# instructions = True

# 控制地雷輸入框顏色
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
input_data = ''

# 控制長寬m, n輸入框
color_m = color_inactive
color_n = color_inactive
active_m = False
active_n = False
text_m = ''
text_n = ''

# 記錄錯誤信息
error_message = ""
# 紀錄開始時間
error_display_time = 0
# 顯示持續時間
error_display_duration = 1000

# Autoplay game
autoplay = False
autoplaySpeed = 0.3
makeAiMove = False

# Show Safe and Mine Cells
showInference = False

# 設定各區域所需的框
# Stage.INSTRUCTIONS
# Stage.CHOOSE_DIFFICULTY
# Stage.INPUT_MINES
# Stage.RUNNING
while True:
    screen.fill(BLACK)

    # Show game instructions
    if stage == Stage.INSTRUCTIONS.value:
        # Check if game quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Title
        title = largeFont.render("Play Minesweeper", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        rules = [
            "Click a cell to reveal it.",
            "Right-click a cell to mark it as a mine.",
            "Mark all mines successfully to win!"
        ]
        for i, rule in enumerate(rules):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)

        # Play game button
        buttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
        buttonText = mediumFont.render("Play Game", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                # instructions = False
                stage += 1
                time.sleep(0.3)
                continue
        pygame.display.flip()
    # 讓玩家選擇要使用的難度，或直接讀入地雷檔案
    elif stage == Stage.CHOOSE_DIFFICULTY.value:
        # Check if game quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        levels = len(difficulty_levels)
        buttonRects = np.empty(len(difficulty_levels), dtype=object)
        # 繪製幾種難度的框
        for i in range(levels):
            buttonRects[i] = pygame.Rect((width / 4), ((1 / 12) + (i/levels)) * height, width / 2, 50)
            buttonText = mediumFont.render(difficulty_levels[i], True, BLACK)
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = buttonRects[i].center
            pygame.draw.rect(screen, WHITE, buttonRects[i])
            screen.blit(buttonText, buttonTextRect)

        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            for i in range(levels):
                if buttonRects[i].collidepoint(mouse):
                    HEIGHT, WIDTH, MINES = difficulty_settings[difficulty_levels[i]]
                    print(HEIGHT, WIDTH, MINES)
                    # instructions = False
                    # 自訂模式
                    if i == levels-2:
                        stage += 1
                    # 讀外部地雷檔案
                    elif i == levels-1:
                        # 開啟檔案總管
                        file_path = mines_func.open_file_dialog()
                        if file_path:
                            pic_name = Path(file_path).stem
                            print(pic_name)
                            with open(file_path, "r") as f:
                                HEIGHT, WIDTH, MINES = [int(i) for i in f.readline().split()]
                                mines_loc = [int(i) for i in f.readline().strip().split()]
                            stage += 3
                    else:
                        stage += 3
                    time.sleep(0.3)
                    break
        pygame.display.flip()
    # 輸入自訂長寬
    elif stage == Stage.INPUT_MN.value:
        back_rect = pygame.Rect((3 / 4) * width, (3 / 4) * height, width / 5, 50)
        enter_rect = pygame.Rect((3 / 4) * width, (3 / 4) * height-60, width / 5, 50)

        # 定義兩個輸入框的位置和大小
        input_box_m = pygame.Rect((1/8)*width, (1/3)*height, 140, 40)
        input_box_n = pygame.Rect((5/8)*width, (1/3)*height, 140, 40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # 若點擊back則返回上一階段
                if back_rect.collidepoint(event.pos):
                    stage -= 1
                    text_m = ""
                    text_n = ""
                # 若點擊enter輸入長寬
                elif enter_rect.collidepoint(event.pos):
                    if mines_func.check_MN_range(text_m, text_n):
                        stage += 1
                        WIDTH = int(text_m)
                        HEIGHT = int(text_n)
                    else:
                        text_m = ""
                        text_n = ""
                        error_message = "Error:Please enter valid numbers"
                        error_display_time = pygame.time.get_ticks()
                # 點擊偵測輸入框是否被選中
                if input_box_m.collidepoint(event.pos):
                    active_m = not active_m
                    active_n = False
                elif input_box_n.collidepoint(event.pos):
                    active_n = not active_n
                    active_m = False
                else:
                    active_m = False
                    active_n = False

                # 根據是否點擊變更顏色
                color_m = color_active if active_m else color_inactive
                color_n = color_active if active_n else color_inactive

            if event.type == pygame.KEYDOWN:
                # active判斷是否已點擊此輸入框
                if active_m:
                    if event.key == pygame.K_BACKSPACE:
                        text_m = text_m[:-1]
                    else:
                        text_m += event.unicode
                elif active_n:
                    if event.key == pygame.K_BACKSPACE:
                        text_n = text_n[:-1]
                    else:
                        text_n += event.unicode

        # 顯示提示文字
        label_m = mediumFont.render("Enter width:", True, WHITE)
        label_n = mediumFont.render("Enter height:", True, WHITE)
        screen.blit(label_m, (input_box_m.x, input_box_m.y - 50))
        screen.blit(label_n, (input_box_n.x, input_box_n.y - 50))

        # 渲染文字
        txt_surface_m = mediumFont.render(text_m, True, WHITE)
        txt_surface_n = mediumFont.render(text_n, True, WHITE)
        screen.blit(txt_surface_m, (input_box_m.x + 5, input_box_m.y + 5))
        screen.blit(txt_surface_n, (input_box_n.x + 5, input_box_n.y + 5))

        # 畫輸入框
        pygame.draw.rect(screen, color_m, input_box_m, 2)
        pygame.draw.rect(screen, color_n, input_box_n, 2)

        # 返回鍵
        back_text = mediumFont.render("Back", True, BLACK)
        back_text_rect = back_text.get_rect()
        back_text_rect.center = back_rect.center
        pygame.draw.rect(screen, WHITE, back_rect)
        screen.blit(back_text, back_text_rect)

        # 輸入鍵
        enter_text = mediumFont.render("Enter", True, BLACK)
        enter_text_rect = enter_text.get_rect()
        enter_text_rect.center = enter_rect.center
        pygame.draw.rect(screen, WHITE, enter_rect)
        screen.blit(enter_text, enter_text_rect)

        # 更新輸入框寬度以配合使用者輸入
        input_box_m.w = max(140, txt_surface_m.get_width() + 10)
        input_box_n.w = max(140, txt_surface_n.get_width() + 10)

        # 如果有錯誤訊息，則顯示
        if error_message and pygame.time.get_ticks() - error_display_time < error_display_duration:
            print("error")
            error_text = largeFont.render(error_message, True, RED)
            error_rect = error_text.get_rect(center=(width // 2, height // 2))
            screen.blit(error_text, error_rect)
            pygame.display.update()  # 更新畫面

        pygame.display.flip()
    # 輸入需要的地雷數
    elif stage == Stage.INPUT_MINES.value:
        txt_rect = pygame.Rect((width / 3), (1 / 3) * height, 200, 50)
        back_rect = pygame.Rect((3 / 4) * width, (3 / 4) * height, width / 5, 50)
        enter_rect = pygame.Rect((3 / 4) * width, (3 / 4) * height - 60, width / 5, 50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 是否點擊輸入框
                if txt_rect.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
                if back_rect.collidepoint(event.pos):
                    stage -= 2
                    input_data = ""
                elif enter_rect.collidepoint(event.pos):
                    if mines_func.check_range(WIDTH, HEIGHT, input_data):
                        MINES = int(input_data)
                        stage += 1
                    else:
                        input_data = ""
                        error_message = "Error:Please enter valid numbers"
                        error_display_time = pygame.time.get_ticks()
            if event.type == pygame.KEYDOWN:
                # active判斷是否以點擊此輸入框
                if active:
                    # 也可鍵盤直接按enter
                    if event.key == pygame.K_RETURN:
                        if mines_func.check_range(WIDTH, HEIGHT, int(input_data)):
                            MINES = int(input_data)
                            stage += 1
                        else:
                            input_data = ""
                            error_message = "Error:Please enter valid numbers"
                            error_display_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_BACKSPACE:
                        input_data = input_data[:-1]
                    else:
                        input_data += event.unicode

        # tips
        title = largeFont.render("Enter the number of mines", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), (1 / 4) * height)
        screen.blit(title, titleRect)

        # 輸入鍵
        enter_text = mediumFont.render("Enter", True, BLACK)
        enter_text_rect = enter_text.get_rect()
        enter_text_rect.center = enter_rect.center
        pygame.draw.rect(screen, WHITE, enter_rect)
        screen.blit(enter_text, enter_text_rect)

        # 返回鍵
        back_text = mediumFont.render("Back", True, BLACK)
        backTextRect = back_text.get_rect()
        backTextRect.center = back_rect.center
        pygame.draw.rect(screen, WHITE, back_rect)
        screen.blit(back_text, backTextRect)

        # 輸入mines框
        txt_surface = mediumFont.render(input_data, True, color)
        rect_width = max(200, txt_surface.get_width() + 10)
        txt_rect.w = rect_width
        screen.blit(txt_surface, (txt_rect.x + 5, txt_rect.y + 5))
        pygame.draw.rect(screen, color, txt_rect, 2)

        # 如果有錯誤訊息，則顯示
        if error_message and pygame.time.get_ticks() - error_display_time < error_display_duration:
            print("error")
            error_text = largeFont.render(error_message, True, RED)
            error_rect = error_text.get_rect(center=(width // 2, height // 2))
            screen.blit(error_text, error_rect)
            pygame.display.update()  # 更新畫面

        pygame.display.flip()
        # pygame.display.update()
    # 本階段根據之前得到的參數更新地雷表及圖片大小等等
    elif stage == Stage.SETUP_GAME_PARAMETER.value:
        # # Calculate cell size
        # cell_size = 30
        #
        # # Calculate board size based on cells and padding
        # board_width = WIDTH * cell_size + BOARD_PADDING * 2
        # board_height = HEIGHT * cell_size + BOARD_PADDING * 2
        #
        # # 重設長寬
        # width = (board_width + 2 * BOARD_PADDING) * 3 / 2
        # height = board_height + 2 * BOARD_PADDING
        ## 重新設定視窗大小
        # pygame.display.set_mode((width, height))

        mines_board.set_board(WIDTH, HEIGHT)
        board_width = mines_board.board_width
        board_height = mines_board.board_height
        cell_size = mines_board.cell_size
        board_origin = mines_board.board_origin
        print(cell_size)
        # set images size
        flag_img = pygame.transform.scale(flag_img, (cell_size, cell_size))
        mine_img = pygame.transform.scale(mine_img, (cell_size, cell_size))
        mine_red_img = pygame.transform.scale(mine_red_img, (cell_size, cell_size))

        # Create game and AI agent
        game = Minesweeper(HEIGHT=HEIGHT, WIDTH=WIDTH, MINES=MINES, mines_loc=mines_loc)
        ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
        stage += 1
    # 遊戲執行階段
    elif stage == Stage.RUNNING.value:
        # Check if game quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Draw board
        cells = []
        for i in range(HEIGHT):
            row = []
            for j in range(WIDTH):
                # Draw rectangle for cell
                rect = pygame.Rect(
                    board_origin[0] + j * cell_size,
                    board_origin[1] + i * cell_size,
                    cell_size, cell_size
                )
                row.append(rect)
            cells.append(row)

        # Autoplay Button
        autoplayBtn = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING, BOARD_PADDING,
            (width / 3) - BOARD_PADDING * 2, 50
        )
        bText = "Autoplay" if not autoplay else "Stop"
        buttonText = mediumFont.render(bText, True, BLACK)
        buttonRect = buttonText.get_rect()
        buttonRect.center = autoplayBtn.center
        pygame.draw.rect(screen, WHITE, autoplayBtn)
        screen.blit(buttonText, buttonRect)

        # AI Move button
        aiButton = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING, BOARD_PADDING + 70,
            (width / 3) - BOARD_PADDING * 2, 50
        )
        buttonText = mediumFont.render("AI Move", True, BLACK)
        buttonRect = buttonText.get_rect()
        buttonRect.center = aiButton.center
        if not autoplay:
            pygame.draw.rect(screen, WHITE, aiButton)
            screen.blit(buttonText, buttonRect)

        # Reset button
        resetButton = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING, BOARD_PADDING + 140,
            (width / 3) - BOARD_PADDING * 2, 50
        )
        buttonText = mediumFont.render("Reset", True, BLACK)
        buttonRect = buttonText.get_rect()
        buttonRect.center = resetButton.center
        if not autoplay:
            pygame.draw.rect(screen, WHITE, resetButton)
            screen.blit(buttonText, buttonRect)

        # Display text
        text = "Lost" if lost else "Won" if game.mines == flags else ""
        text = mediumFont.render(text, True, WHITE)
        textRect = text.get_rect()
        textRect.center = ((5 / 6) * width, BOARD_PADDING + 232)
        screen.blit(text, textRect)

        # Show Safes and Mines button
        safesMinesButton = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING, BOARD_PADDING + 280,
            (width / 3) - BOARD_PADDING * 2, 50
        )
        bText = "Show Inference" if not showInference else "Hide Inference"
        buttonText = smallFont.render(bText, True, BLACK)
        buttonRect = buttonText.get_rect()
        buttonRect.center = safesMinesButton.center
        if not autoplay:
            pygame.draw.rect(screen, WHITE, safesMinesButton)
            screen.blit(buttonText, buttonRect)

        move = None

        left, _, right = pygame.mouse.get_pressed()

        # Check for a right-click to toggle flagging
        if right == 1 and not lost and not win and not autoplay:
            mouse = pygame.mouse.get_pos()
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                        if (i, j) in flags:
                            flags.remove((i, j))
                        else:
                            flags.add((i, j))
                            game.flags.add((i,j))
                        time.sleep(0.2)

        elif left == 1:
            mouse = pygame.mouse.get_pos()

            # If Autoplay button clicked, toggle autoplay
            if autoplayBtn.collidepoint(mouse):
                if not lost:
                    autoplay = not autoplay
                else:
                    autoplay = False
                time.sleep(0.2)
                continue

            # If AI button clicked, make an AI move
            elif aiButton.collidepoint(mouse) and not lost:
                makeAiMove = True
                time.sleep(0.2)

            # Reset game state
            elif resetButton.collidepoint(mouse):
                game = Minesweeper(HEIGHT=HEIGHT, WIDTH=WIDTH, MINES=MINES)
                ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
                game.reset()
                revealed = set()
                flags = set()
                lost = False
                win = False
                mine_detonated = None
                continue

            # If Inference button clicked, toggle showInference
            elif safesMinesButton.collidepoint(mouse):
                showInference = not showInference
                time.sleep(0.2)

            # User-made move
            elif not lost:
                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        if (cells[i][j].collidepoint(mouse)
                                and (i, j) not in flags
                                and (i, j) not in revealed):
                            move = (i, j)

        # If autoplay, make move with AI
        if autoplay or makeAiMove:
            if makeAiMove:
                makeAiMove = False
            move = ai.make_safe_move()
            if move is None:
                move = ai.make_random_move()
                if move is None:
                    flags = ai.mines.copy()
                    print("No moves left to make.")
                    autoplay = False
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")

            # Add delay for autoplay
            if autoplay:
                time.sleep(autoplaySpeed)

        # Make move and update AI knowledge
        if move:
            if game.is_mine(move):
                lost = True
                mine_detonated = move
                autoplay = False
            else:
                nearby = game.nearby_mines(move)
                revealed.add(move)
                game.revealed.add(move)
                ai.add_knowledge(move, nearby)

        if game.won():
            flags = game.mines
        # Draw board
        for i in range(HEIGHT):
            for j in range(WIDTH):
                rect = cells[i][j]
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, WHITE, rect, 3)

                # Add a mine, flag, or number if needed
                if game.is_mine((i, j)) and lost:
                    if (i, j) == mine_detonated:
                        screen.blit(mine_red_img, rect)
                        # # Get a subsurface of the specified rectangle
                        # captured_surface = screen.subsurface(rect)
                        # # 保存生成的圖片
                        # pygame.image.save(captured_surface, f"./pic/red_mine_with_background.png")
                    else:
                        screen.blit(mine_img, rect)
                        # # Get a subsurface of the specified rectangle
                        # captured_surface = screen.subsurface(rect)
                        # # 保存生成的圖片
                        # pygame.image.save(captured_surface, f"./pic/mine_with_background.png")

                elif (i, j) in flags:
                    screen.blit(flag_img, rect)
                elif (i, j) in revealed:
                    neighbors = smallFont.render(
                        str(game.nearby_mines((i, j))),
                        True, BLACK
                    )
                    neighborsTextRect = neighbors.get_rect()
                    neighborsTextRect.center = rect.center
                    screen.blit(neighbors, neighborsTextRect)
                elif (i, j) in ai.safes and showInference:
                    pygame.draw.rect(screen, PINK, rect)
                    pygame.draw.rect(screen, WHITE, rect, 3)
                elif (i, j) in ai.mines and showInference:
                    pygame.draw.rect(screen, RED, rect)
                    pygame.draw.rect(screen, WHITE, rect, 3)

        # -------------------------------------------------------
        # 若遊戲失敗或是獲勝，則輸出此時的結果圖
        if move:
            if lost or game.won():
                # 當遊戲結束時輸出圖片

                # Define the part of the screen to capture
                capture_rect = pygame.Rect(board_origin[0], board_origin[1], WIDTH*cell_size, HEIGHT*cell_size)  # x, y, width, height

                # Get a subsurface of the specified rectangle
                captured_surface = screen.subsurface(capture_rect)

                # 保存生成的圖片
                pygame.image.save(captured_surface, f"./Mark_pic/Mine_{WIDTH}_{HEIGHT}_{MINES}_Mark.png")

        pygame.display.flip()
