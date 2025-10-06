#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
import warnings
warnings.filterwarnings('ignore')

# seabornのスタイル設定
sns.set(style='whitegrid', font='IPAexGothic')

# 公式データを読み込み
print("公式データを読み込み中...")
df = pd.read_csv('official_waste_data.csv')

print("\n使用データ:")
print(df[['年度', '総排出量_万トン', '最終処分量_万トン', 'リサイクル率_%', '直接焼却量_万トン']])

# メインの可視化
fig = plt.figure(figsize=(16, 10))

# 1. 総排出量の推移
ax1 = plt.subplot(2, 3, 1)
ax1.plot(df['年度'], df['総排出量_万トン'], 'o-', linewidth=2, markersize=8, color='#2E86AB')
ax1.set_title('ごみ総排出量の推移', fontsize=14, fontweight='bold')
ax1.set_xlabel('年度', fontsize=12)
ax1.set_ylabel('総排出量（万トン）', fontsize=12)
ax1.grid(True, alpha=0.3)
ax1.set_xticks(df['年度'][::2])  # 2年ごとに表示

# 2. 最終処分量の推移
ax2 = plt.subplot(2, 3, 2)
ax2.plot(df['年度'], df['最終処分量_万トン'], 's-', linewidth=2, markersize=8, color='#A23B72')
ax2.set_title('最終処分量の推移', fontsize=14, fontweight='bold')
ax2.set_xlabel('年度', fontsize=12)
ax2.set_ylabel('最終処分量（万トン）', fontsize=12)
ax2.grid(True, alpha=0.3)
ax2.set_xticks(df['年度'][::2])

# 3. リサイクル率の推移
ax3 = plt.subplot(2, 3, 3)
ax3.plot(df['年度'], df['リサイクル率_%'], '^-', linewidth=2, markersize=8, color='#4CAF50')
ax3.set_title('リサイクル率の推移', fontsize=14, fontweight='bold')
ax3.set_xlabel('年度', fontsize=12)
ax3.set_ylabel('リサイクル率（％）', fontsize=12)
ax3.grid(True, alpha=0.3)
ax3.set_xticks(df['年度'][::2])
ax3.set_ylim(18, 22)

# 4. 焼却処理の詳細
ax4 = plt.subplot(2, 3, 4)
ax4.plot(df['年度'], df['直接焼却量_万トン'], 'o-', linewidth=2, markersize=7, color='#FF6B6B', label='直接焼却量')
ax4.plot(df['年度'], df['焼却残渣量_万トン'], 's-', linewidth=2, markersize=7, color='#4ECDC4', label='焼却残渣量')
ax4.set_title('焼却処理の詳細', fontsize=14, fontweight='bold')
ax4.set_xlabel('年度', fontsize=12)
ax4.set_ylabel('処理量（万トン）', fontsize=12)
ax4.grid(True, alpha=0.3)
ax4.legend(loc='upper right')
ax4.set_xticks(df['年度'][::2])

# 5. 残余容量と残余年数
ax5 = plt.subplot(2, 3, 5)
ax5_twin = ax5.twinx()
line1 = ax5.plot(df['年度'], df['残余容量_万m3']/100, 'o-', linewidth=2, markersize=7, color='#6C5CE7', label='残余容量')
line2 = ax5_twin.plot(df['年度'], df['残余年数'], 's-', linewidth=2, markersize=7, color='#FD79A8', label='残余年数')
ax5.set_title('最終処分場の状況', fontsize=14, fontweight='bold')
ax5.set_xlabel('年度', fontsize=12)
ax5.set_ylabel('残余容量（百万m³）', fontsize=12, color='#6C5CE7')
ax5_twin.set_ylabel('残余年数（年）', fontsize=12, color='#FD79A8')
ax5.tick_params(axis='y', labelcolor='#6C5CE7')
ax5_twin.tick_params(axis='y', labelcolor='#FD79A8')
ax5.grid(True, alpha=0.3)
ax5.set_xticks(df['年度'][::2])

# 6. 処分量の内訳
ax6 = plt.subplot(2, 3, 6)
width = 0.35
x = np.arange(len(df['年度']))
bars1 = ax6.bar(x - width/2, df['直接最終処分量_万トン'], width, label='直接最終処分', color='#FF7675')
bars2 = ax6.bar(x + width/2, df['焼却残渣量_万トン'], width, label='焼却残渣', color='#74B9FF')
ax6.set_title('最終処分量の内訳', fontsize=14, fontweight='bold')
ax6.set_xlabel('年度', fontsize=12)
ax6.set_ylabel('処分量（万トン）', fontsize=12)
ax6.set_xticks(x[::2])
ax6.set_xticklabels(df['年度'][::2])
ax6.legend()
ax6.grid(True, alpha=0.3, axis='y')

plt.suptitle('日本の廃棄物処理状況の推移（2010-2022年）', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()

# 画像を保存
plt.savefig('waste_trends_overview.png', dpi=150, bbox_inches='tight')
print("\n画像を保存しました: waste_trends_overview.png")

# 主要指標のサマリー
print("\n" + "="*60)
print("主要指標のサマリー（2010年 → 2022年）")
print("="*60)
print(f"総排出量: {df.iloc[0]['総排出量_万トン']:.0f}万トン → {df.iloc[-1]['総排出量_万トン']:.0f}万トン （{(df.iloc[-1]['総排出量_万トン']/df.iloc[0]['総排出量_万トン']-1)*100:.1f}%）")
print(f"最終処分量: {df.iloc[0]['最終処分量_万トン']:.1f}万トン → {df.iloc[-1]['最終処分量_万トン']:.1f}万トン （{(df.iloc[-1]['最終処分量_万トン']/df.iloc[0]['最終処分量_万トン']-1)*100:.1f}%）")
print(f"リサイクル率: {df.iloc[0]['リサイクル率_%']:.1f}% → {df.iloc[-1]['リサイクル率_%']:.1f}%")
print(f"直接焼却量: {df.iloc[0]['直接焼却量_万トン']:.0f}万トン → {df.iloc[-1]['直接焼却量_万トン']:.0f}万トン （{(df.iloc[-1]['直接焼却量_万トン']/df.iloc[0]['直接焼却量_万トン']-1)*100:.1f}%）")
print(f"残余年数: {df.iloc[0]['残余年数']:.1f}年 → {df.iloc[-1]['残余年数']:.1f}年")