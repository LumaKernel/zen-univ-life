#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
import warnings
warnings.filterwarnings('ignore')

# seabornのスタイル設定で日本語フォントを指定
sns.set(style='whitegrid', font='IPAexGothic')

# データを読み込み
df = pd.read_csv('complete_waste_data.csv')
print("データを読み込みました:")
print(df)

# 可視化
fig = plt.figure(figsize=(16, 10))

# 1. 総排出量の推移
ax1 = plt.subplot(2, 2, 1)
ax1.plot(df['年度'], df['総排出量_万トン'], 'o-', linewidth=2, markersize=8, color='#2E86AB')
ax1.set_title('ごみ総排出量の推移', fontsize=16, fontweight='bold')
ax1.set_xlabel('年度', fontsize=12)
ax1.set_ylabel('総排出量（万トン）', fontsize=12)
ax1.grid(True, alpha=0.3)
ax1.set_xticks(df['年度'].values[::2])  # 2年ごとに表示
ax1.set_xticklabels([f'{int(y)}' for y in df['年度'][::2]], rotation=45)
# 減少率を表示
reduction = (df['総排出量_万トン'].iloc[-1] - df['総排出量_万トン'].iloc[0]) / df['総排出量_万トン'].iloc[0] * 100
ax1.text(0.95, 0.95, f'13年間で{reduction:.1f}%減少', 
         transform=ax1.transAxes, ha='right', va='top', fontsize=10, 
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# 2. リサイクル率の推移
ax2 = plt.subplot(2, 2, 2)
ax2.plot(df['年度'], df['リサイクル率_%'], 'o-', linewidth=2, markersize=8, color='#A23B72')
ax2.set_title('リサイクル率の推移', fontsize=16, fontweight='bold')
ax2.set_xlabel('年度', fontsize=12)
ax2.set_ylabel('リサイクル率（%）', fontsize=12)
ax2.grid(True, alpha=0.3)
ax2.set_xticks(df['年度'].values[::2])
ax2.set_xticklabels([f'{int(y)}' for y in df['年度'][::2]], rotation=45)
ax2.set_ylim(18, 22)
# 平均値を表示
mean_rate = df['リサイクル率_%'].mean()
ax2.axhline(y=mean_rate, color='gray', linestyle='--', alpha=0.5)
ax2.text(df['年度'].max(), mean_rate, f'平均: {mean_rate:.1f}%', 
         ha='right', va='bottom', fontsize=9, color='gray')

# 3. 一人一日あたり排出量の推移
ax3 = plt.subplot(2, 2, 3)
ax3.plot(df['年度'], df['1人1日あたり排出量_g'], 'o-', linewidth=2, markersize=8, color='#F18F01')
ax3.set_title('1人1日あたりごみ排出量の推移', fontsize=16, fontweight='bold')
ax3.set_xlabel('年度', fontsize=12)
ax3.set_ylabel('排出量（g/人・日）', fontsize=12)
ax3.grid(True, alpha=0.3)
ax3.set_xticks(df['年度'].values[::2])
ax3.set_xticklabels([f'{int(y)}' for y in df['年度'][::2]], rotation=45)
# 減少量を表示
reduction_g = df['1人1日あたり排出量_g'].iloc[0] - df['1人1日あたり排出量_g'].iloc[-1]
ax3.text(0.95, 0.95, f'13年間で{reduction_g:.0f}g/人・日減少', 
         transform=ax3.transAxes, ha='right', va='top', fontsize=10,
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# 4. 最終処分量の推移
ax4 = plt.subplot(2, 2, 4)
ax4.plot(df['年度'], df['最終処分量_万トン'], 'o-', linewidth=2, markersize=8, color='#C73E1D')
ax4.set_title('最終処分量の推移', fontsize=16, fontweight='bold')
ax4.set_xlabel('年度', fontsize=12)
ax4.set_ylabel('最終処分量（万トン）', fontsize=12)
ax4.grid(True, alpha=0.3)
ax4.set_xticks(df['年度'].values[::2])
ax4.set_xticklabels([f'{int(y)}' for y in df['年度'][::2]], rotation=45)
# 減少率を表示
reduction_final = (df['最終処分量_万トン'].iloc[-1] - df['最終処分量_万トン'].iloc[0]) / df['最終処分量_万トン'].iloc[0] * 100
ax4.text(0.95, 0.95, f'13年間で{reduction_final:.1f}%減少', 
         transform=ax4.transAxes, ha='right', va='top', fontsize=10,
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.suptitle('日本の廃棄物処理状況の推移（2010-2022年）', fontsize=20, fontweight='bold', y=1.02)
plt.tight_layout()

# 画像を保存
plt.savefig('waste_trends_overview.png', dpi=300, bbox_inches='tight')
print("\n画像を保存しました: waste_trends_overview.png")

# 追加の分析グラフ
fig2, axes = plt.subplots(1, 2, figsize=(14, 6))

# 総排出量と最終処分量の相関
ax = axes[0]
ax2_twin = ax.twinx()
line1 = ax.plot(df['年度'], df['総排出量_万トン'], 'o-', linewidth=2, markersize=8, color='#2E86AB', label='総排出量')
line2 = ax2_twin.plot(df['年度'], df['最終処分量_万トン'], 's-', linewidth=2, markersize=8, color='#C73E1D', label='最終処分量')
ax.set_xlabel('年度', fontsize=12)
ax.set_ylabel('総排出量（万トン）', fontsize=12, color='#2E86AB')
ax2_twin.set_ylabel('最終処分量（万トン）', fontsize=12, color='#C73E1D')
ax.tick_params(axis='y', labelcolor='#2E86AB')
ax2_twin.tick_params(axis='y', labelcolor='#C73E1D')
ax.set_title('総排出量と最終処分量の推移', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_xticks(df['年度'].values[::2])
ax.set_xticklabels([f'{int(y)}' for y in df['年度'][::2]], rotation=45)
# 凡例を結合
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax.legend(lines, labels, loc='upper right')

# 削減率の比較
ax = axes[1]
base_year = 2010
indices = {
    '総排出量': (df['総排出量_万トン'] / df['総排出量_万トン'].iloc[0] * 100).values,
    '最終処分量': (df['最終処分量_万トン'] / df['最終処分量_万トン'].iloc[0] * 100).values,
    '1人1日排出量': (df['1人1日あたり排出量_g'] / df['1人1日あたり排出量_g'].iloc[0] * 100).values
}

for label, values in indices.items():
    ax.plot(df['年度'], values, 'o-', linewidth=2, markersize=6, label=label)

ax.set_title('各指標の変化率（2010年=100）', fontsize=14, fontweight='bold')
ax.set_xlabel('年度', fontsize=12)
ax.set_ylabel('指数（2010年=100）', fontsize=12)
ax.axhline(y=100, color='gray', linestyle='--', alpha=0.5)
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xticks(df['年度'].values[::2])
ax.set_xticklabels([f'{int(y)}' for y in df['年度'][::2]], rotation=45)

plt.tight_layout()
plt.savefig('waste_analysis.png', dpi=300, bbox_inches='tight')
print("画像を保存しました: waste_analysis.png")

print("\n分析結果:")
print(f"- 総排出量: {df['総排出量_万トン'].iloc[0]:.0f}万トン（2010）→ {df['総排出量_万トン'].iloc[-1]:.0f}万トン（2022）")
print(f"- 最終処分量: {df['最終処分量_万トン'].iloc[0]:.1f}万トン（2010）→ {df['最終処分量_万トン'].iloc[-1]:.1f}万トン（2022）")
print(f"- リサイクル率: {df['リサイクル率_%'].iloc[0]:.1f}%（2010）→ {df['リサイクル率_%'].iloc[-1]:.1f}%（2022）")
print(f"- 1人1日排出量: {df['1人1日あたり排出量_g'].iloc[0]:.0f}g（2010）→ {df['1人1日あたり排出量_g'].iloc[-1]:.0f}g（2022）")