# MineCrypt — A Minesweeper-based Steganography System

本專案以 **踩地雷遊戲 (Minesweeper)** 為核心，結合資訊隱寫術 (Steganography) 與 Entropy 分析，實現「遊戲即嵌密、遊戲結束取密」的概念。

---

## 專案概述

MineCrypt 是一個基於地雷隨機分布與熵計算的隱寫系統。透過地雷排列的不確定性，將秘密訊息以位元形式嵌入地雷圖中，並能於之後重建原訊息。

主要功能：

* **Entropy 分析**：統計地雷分布資訊熵作為隨機性衡量。
* **秘密訊息嵌入 (Embedding)**：將位元資料映射至地雷板中。
* **秘密訊息擷取 (Extraction)**：由標記影像中取回原始資料。
* **辨識與分析 (Recognition & Report)**：驗證取密正確率與熵差異。

---

## 系統架構

```text
steganography/
├── 1-Secre/        # 秘密訊息檔案 (Secret_Char1.txt, Secret_Char2.txt)
├── 2-Locat/        # 地雷位置紀錄檔 (mineX_001.txt ... mineX_010.txt)
├── 3-Marke/        # 含秘密訊息之地雷圖像 (Mine_xxx_Mark_###.png)
├── 4-Embed/        # 嵌入位元紀錄檔 (MineX_Embed_Char_###.txt)
├── 5-Recog/        # 經辨識後的地雷圖像 (Mine_xxx_Mark_Rec_###.png)
├── 6-Extra/        # 取出之秘密訊息 (MineX_Extra_Char_###.txt)
├── 7-Entro/        # 熵分析結果 (Entropy-W-H-M-G.txt)
└── main.py         # 主控制程式，整合嵌密與取密流程
```

---

## 系統流程

### 1️⃣ Entropy 計算

透過隨機地雷分布模擬 (SN=6000)，統計每格周圍地雷數 0–8 的機率分布，計算熵：

$$
H(x) = -\sum_i p(x_i) \log_2 p(x_i)
$$

輸出格式： `Entropy-09-09-010-6000.txt`

---

### 2️⃣ 秘密訊息嵌入 (Embedding)

從 `1-Secre/` 讀取訊息，依地雷分布將資料位元嵌入。

| Level        | Size (n, k) | 可嵌入位元 | 每次讀入字元 |
| ------------ | ----------- | ----- | ------ |
| Beginner     | (81, 10)    | 40    | 5      |
| Intermediate | (256, 40)   | 156   | 19     |
| Expert       | (480, 99)   | 347   | 43     |
| Custom-1     | (720, 120)  | 463   | 57     |
| Custom-2     | (720, 360)  | 714   | 89     |

---

### 3️⃣ 標記與儲存 (Marking)

嵌密完成後自動生成影像：

```
Mine_W_H_M_Mark_###.png
```

### 4️⃣ 訊息擷取 (Extraction)

由辨識後的影像 `5-Recog/` 還原訊息：

```
MineX_Extra_Char_###.txt
```

### 5️⃣ 分析與報告 (Analysis)

輸出每關熵值統計及嵌密成功率，生成：

```
7-Entro/Entropy-Results.txt
```

---

## 執行方式

```bash
python mine-entropy.py        # 熵分析
python embed_secret.py        # 嵌入訊息
python extract_secret.py      # 取出訊息
python analyze_entropy.py     # 統計與報告
```

---

## 範例結果

| 原始地雷圖                        | 含密地雷圖                        | 取出結果                               |
| ---------------------------- | ---------------------------- | ---------------------------------- |
| ![](./examples/original.png) | ![](./examples/embedded.png) | ![](./examples/extracted_text.png) |

---

## 特色

* 結合遊戲機制與資訊隱寫術。
* 以地雷熵衡量版面隨機性與資訊容量。
* 完整自動化嵌密與取密流程。
* 可視化輸出影像與報告。

---
