import math
import numpy as np
from mines_board import Minesboard
from minesweeper import Minesweeper
from mine_entropy import write_mines_entropy
from constant import *

# 設定不同難度的名稱及初始參數(長, 寬, 地雷數)
difficulty_levels = ["Beginner", "Intermediate", "Expert", "Custom-1", "Custom-2"]
difficulty_settings = {
    # (height, width, 地雷數)
    difficulty_levels[0]: (9, 9, 10),
    difficulty_levels[1]: (16, 16, 40),
    difficulty_levels[2]: (16, 30, 99),
    difficulty_levels[3]: (24, 30, 120),
    difficulty_levels[4]: (24, 30, 360)
}


def get_level_index(level):
    for index, level_name in enumerate(difficulty_levels):
        if level == level_name:
            level_index = index
            return level_index


def get_level_parameters(level):
    height, width, mines = difficulty_settings[level]

    return height, width, mines


# 計算要嵌多少bytes
def get_secret_bits_num(n, mines):
    # n = height * width
    # 算可嵌入bits
    L = math.floor(math.log2(math.comb(n, mines)))

    # 算可嵌入bytes
    r = math.floor(L / 8)
    return L


# string 轉 2進制
def str2bins(string):
    return "".join([format(ord(char), '08b') for char in string])


# 2進製轉10進制
def bins2int(bins):
    return int(bins, 2)


# string合併整數
def str2int(string, n=None):
    if n is None:
        n = len(string) * 8
    bins = str2bins(string)

    combine_int = bins2int(bins)
    return combine_int


def bins2str(bins):
    lens = len(bins)//8
    result = ""

    for i in range(lens):
        byte = bins[i*8:(i+1)*8]
        result += chr(int(byte, 2))

    return result


# combination_system
def unranking(n, k, m):
    coefficient = []
    while m > 0:
        if m >= math.comb(n, k):
            m -= math.comb(n, k)
            coefficient.append(n)
            k -= 1
        n -= 1
    while k > 0:
        coefficient.append(k-1)
        k -= 1
    return coefficient


# rank_combination_system
def rank(coefficient, k):
    total = 0
    for i in range(k):
        total += math.comb(coefficient[i], k-i)
    return total


if __name__ == "__main__":
    # G是一次要嵌幾張圖
    G = 10
    # 讀要嵌的秘密信息
    message_name = "Secret Char1.txt"
    secret_path = os.path.join(secrete_message_dir_path, message_name)

    with open(secret_path, mode="r", encoding="utf-8") as file:
        secret_str = file.read()

    # 對同一秘密信息，用5種不同大小的地雷版各嵌G張
    for game_level in difficulty_levels:
        # 讀是哪個難度
        # game_level = input("Game level:").strip()
        height, width, mines = get_level_parameters(game_level)
        n = height*width

        # 讀此地雷板可嵌幾bits
        secrete_bits_num = get_secret_bits_num(n, mines)

        # 讀總共嵌的bits
        total_secret_bits_num = secrete_bits_num*G
        secrete_chars = secret_str[:math.ceil(total_secret_bits_num/8)]
        total_secret_bits = str2bins(secrete_chars)[:total_secret_bits_num]

        level_index = get_level_index(game_level)
        minesweepers = []
        entropy_arr = np.empty(G)
        # 將bits拆給G張嵌
        for i in range(G):
            # 取出此張圖片要嵌的bits
            start_index = i*secrete_bits_num
            end_index = (i+1)*secrete_bits_num

            secret_bits = total_secret_bits[start_index:end_index]
            combination_number = bins2int(secret_bits)

            #  2-Locat: 儲存各Game level 的地雷數量與位置
            # ---------------------------------------------------------------------
            # 計算地雷嵌入位置
            coefficient = unranking(n, mines, combination_number)
            mines_loc = coefficient

            mine_lacate_path = os.path.join(mines_lacate_dir_path, f"Mine{level_index+1}_{i+1:03}.txt")

            # 輸出地雷版參數到txt檔中
            with open(mine_lacate_path, mode='w', encoding="utf-8-sig") as file:
                file.write(f"{height} {width} {mines}\n")
                file.write(" ".join(map(str, mines_loc)))

            # 4-Embed: 儲存嵌入各Game Level的秘密位元
            # ---------------------------------------------------------------------
            # 輸出嵌密bits
            embeded_message_name = f"Mine{level_index + 1}_Embed_Char_{i + 1:03}.txt"
            encry_bits_path = os.path.join(embeded_message_dir_path, embeded_message_name)

            # 輸出結果到txt檔中
            with open(encry_bits_path, mode='w', encoding="utf-8") as file:
                file.write(f"{secret_bits}\n")
                file.write(f"{str(bins2int(secret_bits))}\n")

            # 3-Marke: 儲存已藏密的踩地雷影像
            # ---------------------------------------------------------------------
            # 讀取地雷版參數
            with open(mine_lacate_path, "r", encoding="utf-8-sig") as f:
                HEIGHT, WIDTH, MINES = [int(i) for i in f.readline().split()]
                mines_loc = [int(i) for i in f.readline().strip().split()]
            # 利用參數產生地雷圖
            mines_board = Minesboard(HEIGHT=HEIGHT, WIDTH=WIDTH, MINES=MINES, mines_loc=mines_loc)
            marked_image_name = f"Mine{level_index+1}_{WIDTH}_{HEIGHT}_{MINES}_Mark_{i + 1:03}.png"
            marked_image_path = os.path.join(marked_image_dir_path, marked_image_name)
            mines_board.draw_board(marked_image_path)

            # 7 - Entro: 儲存 entropy text file
            # 紀錄每個地雷版
            # ---------------------------------------------------------------------
            ms = Minesweeper(HEIGHT=HEIGHT, WIDTH=WIDTH, MINES=MINES, mines_loc=mines_loc)
            minesweepers.append(ms)

        # 7 - Entro: 儲存 entropy text file
        # 將結果統整一起輸出
        # ---------------------------------------------------------------------
        entropy_name = f"Entropy-{WIDTH}-{HEIGHT}-{MINES:03}-{G}.txt"
        entropy_path = os.path.join(entropy_result_dir_path, entropy_name)
        mine_entropy = write_mines_entropy(minesweepers, level_index+1, entropy_path)



