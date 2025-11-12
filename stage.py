from enum import Enum

# 區分遊戲進行階段
class Stage(Enum):
    INSTRUCTIONS = 1         # 初始畫面
    CHOOSE_DIFFICULTY = 2    # 選擇難度
    INPUT_MN = 3             # 輸入地雷矩陣長寬
    INPUT_MINES = 4          # 輸入地雷數
    SETUP_GAME_PARAMETER = 5 # 設定遊戲變數
    RUNNING = 6              # 遊戲中

    # # 定義加法操作
    # def __add__(self, other):
    #     if isinstance(other, int):
    #         new_value = self.value + other
    #         # 確保新值在有效範圍內
    #         return Stage(new_value) if new_value in Stage._value2member_map_ else None
    #     return NotImplemented
    #
    # # 定義減法操作
    # def __sub__(self, other):
    #     if isinstance(other, int):
    #         new_value = self.value - other
    #         return Stage(new_value) if new_value in Stage._value2member_map_ else None
    #     return NotImplemented
