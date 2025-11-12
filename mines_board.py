from minesweeper import Minesweeper
import pygame
# 設定不同難度的名稱及初始參數(長, 寬, 地雷數)
difficulty_levels = ["Beginner", "Intermediate", "Expert", "Custom-1", "Custom-2", "Custom", "Read setup txt"]
difficulty_settings = {
    # (height, width, 地雷數)
    difficulty_levels[0]: (9, 9, 10),
    difficulty_levels[1]: (16, 16, 40),
    difficulty_levels[2]: (16, 30, 99),
    difficulty_levels[3]: (24, 30, 120),
    difficulty_levels[4]: (24, 30, 360),
    difficulty_levels[5]: (None, None, 0),
    difficulty_levels[6]: (None, None, 0)
}

pygame.init()
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)


class Minesboard(Minesweeper):
    """
    設定gui面板參數
    """
    def __init__(self, height=800, width=1200, BOARD_PADDING = 20, HEIGHT = 8, WIDTH = 8, MINES=8, mines_loc=None):
        super().__init__(HEIGHT, WIDTH, MINES, mines_loc)  # Initialize Minesweeper
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.BOARD_PADDING = BOARD_PADDING
        self.board_origin = (self.BOARD_PADDING, self.BOARD_PADDING)
        self.board_width = 0
        self.board_height = 0
        self.cell_size = 0
        self.set_board_size()

    def set_board_size(self):
        self.board_width = ((2 / 3) * self.width) - (self.BOARD_PADDING * 2)
        self.board_height = self.height - (self.BOARD_PADDING * 2)
        self.cell_size = self.calculate_cell_size()

    def calculate_cell_size(self):
        return int(min(self.board_width / self.WIDTH, self.board_height / self.HEIGHT))

    def set_board(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.set_board_size()

    def board_size(self):
        return self.width, self.height

    def draw_board(self, output_path):
        cell_shape = (self.cell_size, self.cell_size)
        # # Add images
        flag_img = pygame.image.load("assets/images/flag.png")
        flag_img = pygame.transform.scale(flag_img, cell_shape)
        mine_img = pygame.image.load("assets/images/mine.png")
        mine_img = pygame.transform.scale(mine_img, cell_shape)
        mine_red_img = pygame.image.load("assets/images/mine-red.png")
        mine_red_img = pygame.transform.scale(mine_red_img, cell_shape)

        screen = pygame.Surface((self.width, self.height))

        # Draw board
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                # Draw rectangle for cell
                rect = pygame.Rect(
                    self.board_origin[0] + j * self.cell_size,
                    self.board_origin[1] + i * self.cell_size,
                    self.cell_size, self.cell_size
                )
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, WHITE, rect, 3)

                # Add a mine, flag, or number if needed
                if super().is_mine((i, j)):
                    if (i, j) == self.mine_detonated:
                        screen.blit(mine_red_img, rect)
                    else:
                        screen.blit(mine_img, rect)
                elif (i, j) in self.flags:
                    screen.blit(flag_img, rect)
                elif (i, j) in self.revealed:
                    neighbors = smallFont.render(
                        str(super().nearby_mines((i, j))),
                        True, BLACK
                    )
                    neighborsTextRect = neighbors.get_rect()
                    neighborsTextRect.center = rect.center
                    screen.blit(neighbors, neighborsTextRect)

        # Define the part of the screen to capture
        capture_rect = pygame.Rect(self.board_origin[0], self.board_origin[1], self.WIDTH * self.cell_size,
                                   self.HEIGHT * self.cell_size)  # x, y, width, height

        # Get a subsurface of the specified rectangle
        captured_surface = screen.subsurface(capture_rect)

        # 保存生成的圖片
        pygame.image.save(captured_surface, output_path)
