import math
import os.path
import cv2
import numpy as np
from mines_board import Minesboard
import mines_func
from mine_unranking import rank, get_secret_bits_num
from constant import *


def find_mines(mines_board_img, mines_board, output_path):
    cell_size = mines_board.cell_size

    # 轉灰階
    gray_mines_board_img = cv2.cvtColor(mines_board_img, cv2.COLOR_BGR2GRAY)

    # 讀比對用的小圖(地雷)
    mine_img_template = cv2.imread('assets/images/mine_with_background.png', cv2.IMREAD_GRAYSCALE)
    # 讀樣本並調整大小
    mine_img_template = cv2.resize(mine_img_template, (cell_size, cell_size), interpolation=cv2.INTER_LINEAR)

    # 進行匹配
    result = cv2.matchTemplate(gray_mines_board_img, mine_img_template, cv2.TM_CCOEFF_NORMED)

    # 設定匹配閥值
    threshold = 0.85
    locations = np.where(result >= threshold)

    mines_loc = []
    loc_seq = []
    # 找到地雷的位置
    for pt in zip(*locations[::-1]):
        x, y = pt

        x += cell_size//2
        y += cell_size//2
        row = y // cell_size
        col = x // cell_size
        if (row, col) not in mines_loc:
            mines_loc.append((row, col))
            loc_seq.append(row*mines_board.WIDTH+col)
            # print(f"地雷在第 {row+1} 列，第 {col+1} 行")

    reverse_loc_seq = sorted(loc_seq, reverse=True)
    # 在圖上框出地雷位置
    for (row, col) in mines_loc:
        cv2.rectangle(mines_board_img, (col*cell_size, row*cell_size), ((col+1)*cell_size, (row+1)*cell_size), (0, 0, 255), 2)

    cv2.imwrite(output_path, mines_board_img)
    # # 顯示結果
    # cv2.imshow('Detected Mines', mines_board_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return reverse_loc_seq


def bins2str(bins):
    lens = len(bins)//8
    result = ""

    for i in range(lens):
        byte = bins[i*8:(i+1)*8]
        result += chr(int(byte, 2))

    return result


# 座標序列 地雷數 地雷版總格數
def extract_secret(loc_seq, mines, n, output_path):
    combination_number = rank(loc_seq, mines)
    # 算實際長度，後續要補0
    bins_len = get_secret_bits_num(n, mines)
    # 先轉2進制
    bins = bin(combination_number)[2:].zfill(bins_len)
    # message = bins2str(bins)
    with open(output_path, mode="w", encoding="utf-8") as file:
        file.write(f"{bins}\n")
        file.write(f"{str(combination_number)}\n")
        # file.write(message)
    return bins


def check_extract_message():
    # 紀錄是否全部信息都正確
    flag = True
    # 比對取出信息是否正確
    embeded_message_names = os.listdir(embeded_message_dir_path)
    extract_message_names = os.listdir(extract_message_dir_path)
    for i in range(len(embeded_message_names)):
        embeded_message_path = os.path.join(embeded_message_dir_path, embeded_message_names[i])
        extract_message_path = os.path.join(extract_message_dir_path, extract_message_names[i])

        with open(embeded_message_path, mode='r', encoding="utf-8") as file:
            embeded_message = file.read()
        with open(extract_message_path, mode='r', encoding="utf-8") as file:
            extract_message = file.read()

        if embeded_message != extract_message:
            print(f"{embeded_message_names[i]}和{extract_message_names[i]}兩個文件內容不同")
            flag = False
    if flag:
        print("所有取出信息皆正確")


if __name__ == "__main__":
    for image_name in os.listdir(marked_image_dir_path):
        # print(image_name)
        WIDTH, HEIGHT, MINES = map(int, image_name.split("_")[1:4])
        image_prename = image_name.split("_")[0]
        image_ID = os.path.splitext(image_name)[0].split("_")[-1]

        #  5-Recog: 儲存經過自動辨識地雷之影像
        # ---------------------------------------------------------------------
        mines_board = Minesboard(HEIGHT=HEIGHT, WIDTH=WIDTH, MINES=MINES)
        # 讀大圖
        marked_image_path = os.path.join(marked_image_dir_path, image_name)
        marked_image = cv2.imread(marked_image_path)
        recog_image_name = f"{image_prename}_{WIDTH}_{HEIGHT}_{MINES}_Mark_Rec_{image_ID}.png"
        recog_image_path = os.path.join(recognized_image_dir_path, recog_image_name)
        loc_seq = find_mines(marked_image, mines_board, recog_image_path)

        #  6-Extra: 儲存取出之秘密訊息text file
        # ---------------------------------------------------------------------
        extract_message_name = f"{image_prename}_Extra_Char_{image_ID}.txt"
        extract_message_path = os.path.join(extract_message_dir_path, extract_message_name)
        extract_message = extract_secret(loc_seq, MINES, HEIGHT * WIDTH, extract_message_path)
        # with open(extract_message_path, mode='w', encoding="utf-8") as file:
        #     file.write(extract_message)

    check_extract_message()
