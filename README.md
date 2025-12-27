# MineCrypt — A Minesweeper-based Steganography System

本專案以 **踩地雷遊戲 (Minesweeper)** 為核心，結合資訊隱寫術 (Steganography) 與 Entropy 分析，實現「遊戲即嵌密、遊戲結束取密」的概念。

---

## 專案概述

MineCrypt 是一個結合地雷隨機分布與資訊熵（Entropy）分析的隱寫系統。本系統利用地雷排列的不確定性作為載體，將秘密訊息編碼嵌入至地雷盤面中。

**運作流程與情境**：
系統首先根據輸入的秘密訊息生成對應的地雷盤面，並將其封裝為可遊玩的踩地雷遊戲發送給接收端。接收者收到後，如同一般休閒娛樂般進行遊玩；當遊戲通關時，完整的地雷分布隨之顯現，系統即可藉此還原出原始訊息。在此傳輸過程中，即便檔案遭第三方攔截，外觀上僅呈現為一款普通的邏輯遊戲，難以察覺其中隱藏的密文，從而實現資訊的高隱蔽性傳輸。

主要功能：

* **Entropy 分析**：統計地雷分布資訊熵作為隨機性衡量。
* **秘密訊息嵌入 (Embedding)**：將位元資料映射至地雷板中。
* **秘密訊息擷取 (Extraction)**：由標記影像中取回原始資料。
* **辨識與分析 (Recognition & Report)**：驗證取密正確性與熵差異。
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
└── runner.py       # 主控制程式，整合踩地雷遊戲與嵌密取密流程
```

---

## 系統流程

### 1️⃣ 秘密訊息嵌入 (Embedding)

本階段負責讀取 `1-Secre/` 目錄下的訊息，並利用數學編碼將其嵌入至踩地雷的地圖分佈中。

### 難度與容量規格 (Capacity Specification)

系統利用地雷的**排列組合 (Combinations)** 來儲存資訊。隨著地雷數量與地圖大小的增加，排列的可能性呈指數級成長，從而獲得極高的嵌密量。

| Level | Size (n, k)<br><sub>(Cells, Mines)</sub> | Capacity (Bits) | Char Limit<br><sub>(Approx.)</sub> | Note |
| :--- | :--- | :--- | :--- | :--- |
| **Beginner** | (81, 10) | 40 | 5 | 9x9 Grid |
| **Intermediate** | (256, 40) | 156 | 19 | 16x16 Grid |
| **Expert** | (480, 99) | 347 | 43 | 16x30 Grid |
| **Custom-1** | (720, 120) | 463 | 57 | 24x30 Grid |
| **Custom-2** | (720, 360) | **714** | **89** | 24x30 Grid |

---

### 數學原理：組合數字系統 (Combinadics)

我們採用 **組合數字系統 (Combinatorial Number System)** 作為編碼核心。此數學系統建立在自然數與組合之間的一一對應關係（Bijection）。

#### 核心公式
任何一個非負整數 $X$（代表訊息），在固定 $k$ 個地雷的情況下，可以**唯一分解**為 $k$ 個二項式係數的和：

$$
X = \binom{c_k}{k} + \binom{c_{k-1}}{k-1} + \dots + \binom{c_1}{1}
$$

其中 $c_k > c_{k-1} > \dots > c_1 \ge 0$ 即為地雷在地圖上的位置索引。

#### 唯一性定理 (Uniqueness Property)
組合數字系統最強大的特性在於其**唯一性**：
對於任何範圍在 $0 \le X < \binom{n}{k}$ 的整數 $X$，**恰好存在一組**嚴格遞減的整數序列 $\{c_k, \dots, c_1\}$ 滿足上述公式。

這意味著：
1.  **無歧義性**：每一則不同的訊息，都會產生一種截然不同的地雷分佈圖。
2.  **無碰撞**：不同的地雷分佈圖，解碼後絕對不會得到相同的數值。
3.  **全覆蓋**：所有可能的 $k$ 顆地雷排列方式，都能被映射到一個連續的整數區間中，沒有浪費的空間。

### 處理流程
1.  **Serialization**: 將輸入訊息轉換為大整數 $X$。
2.  **Mapping**: 利用組合數字系統的唯一性定理，解出對應的 $k$ 個地雷索引 $c_i$。
3.  **Layout**: 將一維索引映射至二維地圖座標，完成嵌入。
---

### 2️⃣ 遊戲封裝與遊玩 (Gaming)

系統將生成的盤面封裝為遊戲，發送給接收端。接收者如同一般玩家進行踩地雷，通關後即可獲得完整的地雷分佈圖（即密文載體）。

- [Game_Screenshot.jpg](./2-Gaming/Game_Screenshot.jpg)

### 3️⃣ 標記與儲存 (Marking)

當遊戲結束且地雷位置揭曉後，系統將盤面轉換為標記影像檔：

- [Mine_9_9_10_Mark_001.png](./Mine_9_9_10_Mark_001.png)

### 4️⃣ 訊息擷取 (Extraction)

接收端系統讀取標記影像，逆向解析地雷座標並還原原始訊息：

- [MineX_Extra_Char_001.txt](./5-Recog/MineX_Extra_Char_001.txt)

### 5️⃣ 分析與熵值驗證 (Analysis & Entropy)

為了驗證隱寫的安全性與隨機性，系統會分析地雷分佈的資訊熵。

**Entropy 計算原理**：
透過隨機地雷分布模擬 (SN=6000)，統計每格周圍地雷數 0–8 的機率分布，計算熵：

$$
H(x) = -\sum_i p(x_i) \log_2 p(x_i)
$$

此步驟用於確認嵌入訊息後的盤面與隨機生成的盤面在統計特性上無顯著差異。

- [Entropy-Results.txt](./7-Entro/Entropy-Results.txt)

---

## 執行方式

```bash
python runner.py            # 1. 執行踩地雷遊戲並嵌入訊息 (Embedding & Gaming)
python auto_extract.py      # 2. 取出訊息 (Extraction)
python mine-entropy.py      # 3. 熵分析 (Analysis)
```

---

## 特色

* 隱蔽性高：結合遊戲機制與資訊隱寫術，外觀僅為普通遊戲。
* 數學嚴謹：利用組合數字系統確保資訊無損且最大化容量。
* 安全性驗證：以地雷熵衡量版面隨機性，防止統計攻擊。

---
