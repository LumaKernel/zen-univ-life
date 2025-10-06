#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

# 日本語フォントの設定（これがおまじない）
plt.rcParams['font.family'] = 'Hiragino Sans'

# テストデータ
x = [1, 2, 3, 4, 5]
y = [10, 25, 15, 30, 20]

# グラフ作成
plt.figure(figsize=(8, 6))
plt.plot(x, y, 'o-')
plt.title('日本語タイトルのテスト')
plt.xlabel('横軸（日本語）')
plt.ylabel('縦軸（日本語）')
plt.grid(True)

# 保存
plt.savefig('test_japanese.png', dpi=150, bbox_inches='tight')
print("テスト画像を保存しました: test_japanese.png")
plt.show()