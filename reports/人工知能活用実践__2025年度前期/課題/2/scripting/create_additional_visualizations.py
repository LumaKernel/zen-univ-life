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
df = pd.read_csv('official_waste_data.csv')

# 追加データの計算
df['1人1日排出量_g'] = [976, 975, 964, 966, 955, 948, 932, 927, 926, 918, 901, 890, 880]
df['処理残渣量_万トン'] = df['最終処分量_万トン'] - df['焼却残渣量_万トン'] - df['直接最終処分量_万トン']
df['資源化量_万トン'] = df['総排出量_万トン'] * df['リサイクル率_%'] / 100
df['中間処理後再生利用量_万トン'] = df['資源化量_万トン'] * 0.55  # 推定値

# 焼却残渣の再資源化率を計算（推定）
df['焼却残渣再資源化率_%'] = np.linspace(8, 15, len(df))  # 年々向上する推定値

print("データ準備完了:")
print(df.head())

# 図1: 包括的な廃棄物処理状況
fig = plt.figure(figsize=(18, 12))

# 1. 最終処分場の残余容量と残余年数
ax1 = plt.subplot(3, 3, 1)
ax1_twin = ax1.twinx()
line1 = ax1.plot(df['年度'], df['残余容量_万m3']/100, 'o-', linewidth=2, markersize=7, color='#2E86AB', label='残余容量（百万m³）')
line2 = ax1_twin.plot(df['年度'], df['残余年数'], 's-', linewidth=2, markersize=7, color='#A23B72', label='残余年数')
ax1.set_title('最終処分場の残余容量と残余年数', fontsize=14, fontweight='bold')
ax1.set_xlabel('年度', fontsize=11)
ax1.set_ylabel('残余容量（百万m³）', fontsize=11, color='#2E86AB')
ax1_twin.set_ylabel('残余年数（年）', fontsize=11, color='#A23B72')
ax1.tick_params(axis='y', labelcolor='#2E86AB')
ax1_twin.tick_params(axis='y', labelcolor='#A23B72')
ax1.grid(True, alpha=0.3)
ax1.set_xticks(df['年度'][::2])
ax1.set_xticklabels([f'{y}' for y in df['年度'][::2]], rotation=45)
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='best', fontsize=9)

# 2. 年間最終処分量の推移（内訳付き）
ax2 = plt.subplot(3, 3, 2)
bottom = np.zeros(len(df))
colors = ['#C73E1D', '#FF6B6B', '#FFD93D']
labels = ['直接最終処分', '焼却残渣', '処理残渣']
data_cols = ['直接最終処分量_万トン', '焼却残渣量_万トン', '処理残渣量_万トン']

for i, (col, color, label) in enumerate(zip(data_cols, colors, labels)):
    ax2.bar(df['年度'], df[col], bottom=bottom, color=color, label=label, width=0.8)
    bottom += df[col]

ax2.set_title('最終処分量の内訳推移', fontsize=14, fontweight='bold')
ax2.set_xlabel('年度', fontsize=11)
ax2.set_ylabel('処分量（万トン）', fontsize=11)
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_xticks(df['年度'][::2])
ax2.set_xticklabels([f'{y}' for y in df['年度'][::2]], rotation=45)

# 3. ごみ総排出量とリサイクル率
ax3 = plt.subplot(3, 3, 3)
ax3_twin = ax3.twinx()
line1 = ax3.bar(df['年度'], df['総排出量_万トン'], color='#2E86AB', alpha=0.7, label='総排出量')
line2 = ax3_twin.plot(df['年度'], df['リサイクル率_%'], 'o-', linewidth=2, markersize=7, color='#A23B72', label='リサイクル率')
ax3.set_title('総排出量とリサイクル率の推移', fontsize=14, fontweight='bold')
ax3.set_xlabel('年度', fontsize=11)
ax3.set_ylabel('総排出量（万トン）', fontsize=11, color='#2E86AB')
ax3_twin.set_ylabel('リサイクル率（%）', fontsize=11, color='#A23B72')
ax3.tick_params(axis='y', labelcolor='#2E86AB')
ax3_twin.tick_params(axis='y', labelcolor='#A23B72')
ax3.grid(True, alpha=0.3, axis='y')
ax3.set_xticks(df['年度'][::2])
ax3.set_xticklabels([f'{y}' for y in df['年度'][::2]], rotation=45)
ax3_twin.set_ylim(18, 22)

# 4. 焼却残渣の発生量と再資源化
ax4 = plt.subplot(3, 3, 4)
ax4.plot(df['年度'], df['焼却残渣量_万トン'], 'o-', linewidth=2, markersize=7, color='#FF6B6B', label='焼却残渣量')
ax4.plot(df['年度'], df['焼却残渣量_万トン'] * df['焼却残渣再資源化率_%'] / 100, 's-', linewidth=2, markersize=7, color='#4ECDC4', label='再資源化量（推定）')
ax4.set_title('焼却残渣の発生と再資源化', fontsize=14, fontweight='bold')
ax4.set_xlabel('年度', fontsize=11)
ax4.set_ylabel('量（万トン）', fontsize=11)
ax4.legend(loc='best', fontsize=9)
ax4.grid(True, alpha=0.3)
ax4.set_xticks(df['年度'][::2])
ax4.set_xticklabels([f'{y}' for y in df['年度'][::2]], rotation=45)

# 5. 処理方法別の推移
ax5 = plt.subplot(3, 3, 5)
ax5.plot(df['年度'], df['直接焼却量_万トン'], 'o-', linewidth=2, markersize=7, color='#FF6B6B', label='直接焼却')
ax5.plot(df['年度'], df['資源化量_万トン'], 's-', linewidth=2, markersize=7, color='#4ECDC4', label='資源化')
ax5.plot(df['年度'], df['最終処分量_万トン'], '^-', linewidth=2, markersize=7, color='#C73E1D', label='最終処分')
ax5.set_title('処理方法別の推移', fontsize=14, fontweight='bold')
ax5.set_xlabel('年度', fontsize=11)
ax5.set_ylabel('量（万トン）', fontsize=11)
ax5.legend(loc='best', fontsize=9)
ax5.grid(True, alpha=0.3)
ax5.set_xticks(df['年度'][::2])
ax5.set_xticklabels([f'{y}' for y in df['年度'][::2]], rotation=45)

# 6. 削減効果の累積
ax6 = plt.subplot(3, 3, 6)
base_year_disposal = df['最終処分量_万トン'].iloc[0]
cumulative_reduction = [(base_year_disposal - val) * (i+1) for i, val in enumerate(df['最終処分量_万トン'])]
ax6.bar(df['年度'], cumulative_reduction, color='#2E86AB', alpha=0.7)
ax6.set_title('最終処分量削減の累積効果', fontsize=14, fontweight='bold')
ax6.set_xlabel('年度', fontsize=11)
ax6.set_ylabel('累積削減量（万トン）', fontsize=11)
ax6.grid(True, alpha=0.3, axis='y')
ax6.set_xticks(df['年度'][::2])
ax6.set_xticklabels([f'{y}' for y in df['年度'][::2]], rotation=45)

# 7. 1人1日あたり排出量の国際比較イメージ
ax7 = plt.subplot(3, 3, 7)
countries = ['日本\n2022', 'ドイツ\n(参考)', 'フランス\n(参考)', '米国\n(参考)', 'OECD平均\n(参考)']
values = [880, 630, 520, 2200, 1400]  # 参考値
colors_bar = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#4ECDC4']
bars = ax7.bar(countries, values, color=colors_bar)
ax7.set_title('1人1日あたり排出量の国際比較（参考）', fontsize=14, fontweight='bold')
ax7.set_ylabel('排出量（g/人・日）', fontsize=11)
ax7.grid(True, alpha=0.3, axis='y')
for bar, val in zip(bars, values):
    ax7.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
             f'{val}g', ha='center', va='bottom', fontsize=10)

# 8. 処理施設数の推移（推定）
ax8 = plt.subplot(3, 3, 8)
years_facility = [2010, 2015, 2020, 2022]
incinerators = [1221, 1141, 1056, 1028]  # 推定値
recycling_facilities = [348, 355, 362, 368]  # 推定値
final_disposal_sites = [1861, 1661, 1621, 1587]  # 推定値

width = 0.25
x = np.arange(len(years_facility))
ax8.bar(x - width, incinerators, width, label='焼却施設', color='#FF6B6B')
ax8.bar(x, recycling_facilities, width, label='資源化施設', color='#4ECDC4')
ax8.bar(x + width, final_disposal_sites, width, label='最終処分場', color='#C73E1D')
ax8.set_title('処理施設数の推移（推定）', fontsize=14, fontweight='bold')
ax8.set_xlabel('年度', fontsize=11)
ax8.set_ylabel('施設数', fontsize=11)
ax8.set_xticks(x)
ax8.set_xticklabels(years_facility)
ax8.legend(loc='best', fontsize=9)
ax8.grid(True, alpha=0.3, axis='y')

# 9. 将来予測
ax9 = plt.subplot(3, 3, 9)
# 簡単な線形予測
from scipy import stats
slope, intercept, _, _, _ = stats.linregress(df['年度'], df['最終処分量_万トン'])
future_years = list(range(2023, 2031))
future_values = [slope * year + intercept for year in future_years]
future_values = [max(20, val) for val in future_values]  # 最小値を20万トンに設定

ax9.plot(df['年度'], df['最終処分量_万トン'], 'o-', linewidth=2, markersize=7, color='#2E86AB', label='実績')
ax9.plot(future_years, future_values, 'o--', linewidth=2, markersize=6, color='#A23B72', alpha=0.7, label='予測')
ax9.set_title('最終処分量の将来予測', fontsize=14, fontweight='bold')
ax9.set_xlabel('年度', fontsize=11)
ax9.set_ylabel('最終処分量（万トン）', fontsize=11)
ax9.legend(loc='best', fontsize=9)
ax9.grid(True, alpha=0.3)
ax9.set_xlim(2009, 2031)
ax9.axvline(x=2022.5, color='gray', linestyle='--', alpha=0.5)
ax9.text(2022.5, 45, '予測', ha='center', va='bottom', fontsize=9, color='gray')

plt.suptitle('日本の廃棄物処理の詳細分析（2010-2022年）', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('waste_detailed_analysis.png', dpi=300, bbox_inches='tight')
print("\n画像を保存しました: waste_detailed_analysis.png")

# 追加の分析結果を表示
print("\n" + "="*80)
print("重要な分析結果:")
print("="*80)
print(f"1. 最終処分量の削減: {df['最終処分量_万トン'].iloc[0]:.1f}万トン（2010）→ {df['最終処分量_万トン'].iloc[-1]:.1f}万トン（2022）")
print(f"   削減率: {(1 - df['最終処分量_万トン'].iloc[-1]/df['最終処分量_万トン'].iloc[0])*100:.1f}%")
print(f"\n2. 残余年数の改善: {df['残余年数'].iloc[0]:.1f}年（2010）→ {df['残余年数'].iloc[-1]:.1f}年（2022）")
print(f"   改善率: {(df['残余年数'].iloc[-1]/df['残余年数'].iloc[0] - 1)*100:.1f}%")
print(f"\n3. 直接最終処分量の削減: {df['直接最終処分量_万トン'].iloc[0]:.1f}万トン（2010）→ {df['直接最終処分量_万トン'].iloc[-1]:.1f}万トン（2022）")
print(f"   削減率: {(1 - df['直接最終処分量_万トン'].iloc[-1]/df['直接最終処分量_万トン'].iloc[0])*100:.1f}%")
print(f"\n4. 焼却残渣の削減: {df['焼却残渣量_万トン'].iloc[0]:.1f}万トン（2010）→ {df['焼却残渣量_万トン'].iloc[-1]:.1f}万トン（2022）")
print(f"   削減率: {(1 - df['焼却残渣量_万トン'].iloc[-1]/df['焼却残渣量_万トン'].iloc[0])*100:.1f}%")

# データをCSVに保存
df.to_csv('waste_detailed_data.csv', index=False, encoding='utf-8-sig')
print("\nデータをwaste_detailed_data.csvに保存しました")