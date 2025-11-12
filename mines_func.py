import tkinter as tk
from tkinter import filedialog


# 檢查地雷數是否正常
def check_range(m, n, k):
    if not k.isdigit():
        return False
    # m,n是長寬, k是地雷數
    if 1 <= int(k) <= (m-1)*(n-1):
        return True
    return False


# 檢查width和height是否正常
def check_MN_range(width, height):
    max_width = 30
    max_height = 24
    if width.isdigit() and height.isdigit():
        if 0 <= int(width) <= max_width and 0 <= int(height) <= max_height:
            return True
    return False


# 定義選擇檔案的函數
def open_file_dialog():
    # 使用 tkinter 打開檔案總管
    root = tk.Tk()
    root.withdraw()  # 隱藏 tkinter 主視窗
    file_path = filedialog.askopenfilename()  # 彈出檔案選擇視窗
    return file_path
