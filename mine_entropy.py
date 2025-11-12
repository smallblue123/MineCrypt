import cv2
import numpy as np
from scipy.stats import entropy
from minesweeper import Minesweeper


def write_mines_entropy(minesweepers, level, output_path):
    # 原始數據
    data = "No. Level 0 1 2 3 4 5 6 7 8 9 Entropy"
    # 拆分數據為列表
    data_list = data.split()
    # 使用 ljust 或 rjust 格式化每個字元
    formatted_data = [item.rjust(5) for item in data_list]
    # 將格式化後的數據合併為一個字串
    title = ' '.join(formatted_data)+"\n"

    G = len(minesweepers)
    # 紀錄每次遞迴中個地雷數字出現次數
    mines_num_arr = np.zeros((G, 10), dtype=np.int32)
    # 紀錄每次遞迴的entropy
    entropy_arr = np.empty(G)

    # 結果輸出到txt
    with open(output_path, "w") as f:
        f.write(title)
        for i in range(len(minesweepers)):
            mine_entropy, mine_num_arr = calculate_mines_entropy(minesweepers[i])
            entropy_arr[i] = mine_entropy
            mines_num_arr[i] = mine_num_arr

            data = " ".join([f"{x:>5d}" for x in mine_num_arr])
            f.write(f"{i+1:>5d} {level:>5d} {data} {mine_entropy:.4f}\n")

        # 計算entropy的平均值和標準差
        entropys_mean = np.mean(entropy_arr, axis=0)
        mines_mean = np.mean(mines_num_arr, axis=0)
        print(f"level{level} avarage entropy:")
        print(mines_mean, entropys_mean)
        data = " ".join([f"{x:>5.2f}" for x in mines_mean])
        f.write(f"  Ave {level:>5d} {data} {entropys_mean:>.4f}")


def calculate_mines_entropy(ms: Minesweeper):

    # 紀錄每次遞迴中個地雷數字出現次數
    mine_num_arr = np.zeros(10,  dtype=np.int32)

    for i in range(ms.HEIGHT):
        for j in range(ms.WIDTH):
            if ms.is_mine((i, j)):
                mine_num_arr[9] += 1
            else:
                nearby_mines = ms.nearby_mines((i, j))
                mine_num_arr[nearby_mines] += 1
    # 計算entropy
    mine_entropy = entropy(mine_num_arr, base=2)

    return mine_entropy, mine_num_arr
