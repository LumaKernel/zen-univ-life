#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties

# IPAexフォントを直接指定
font_path = 'ipaexg00401/ipaexg.ttf'
font_prop = FontProperties(fname=font_path)

# フォントを追加
fm.fontManager.addfont(font_path)
plt.rcParams['font.sans-serif'] = ['IPAexGothic']

# テストグラフ
plt.figure(figsize=(8, 6))
plt.plot([1, 2, 3, 4, 5], [10, 25, 15, 30, 20], 'o-')
plt.title('日本語タイトルのテスト（IPAexゴシック）', fontproperties=font_prop)
plt.xlabel('横軸（日本語）', fontproperties=font_prop)
plt.ylabel('縦軸（日本語）', fontproperties=font_prop)
plt.grid(True)

# 保存
plt.savefig('test_ipafont.png', dpi=150, bbox_inches='tight')
print("テスト画像を保存しました: test_ipafont.png")
plt.show()