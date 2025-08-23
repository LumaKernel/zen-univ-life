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
sns.set(style='darkgrid', font='IPAexGothic')

# データフォルダのパス
data_path = "data/"

# 年度リスト
years = list(range(2010, 2023))

# データを格納する辞書
data_dict = {
    '年度': [],
    '総排出量_万トン': [],
    'リサイクル率_%': [],
    '一人一日あたり排出量_g': [],
    '最終処分量_万トン': []
}

print("データを読み込み中...")

for year in years:
    print(f"\n{year}年の処理:")
    
    # エンジンの選択
    if year <= 2015:
        engine = 'xlrd'
    else:
        engine = 'openpyxl'
    
    # Excelファイルを読み込み
    df_all = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=None, engine=engine)
    
    # ヘッダー行を探す
    header_row = None
    for i in range(min(10, len(df_all))):
        if '都道府県' in str(df_all.iloc[i, 0]):
            header_row = i
            break
    
    if header_row is None:
        print(f"  ヘッダー行が見つかりません")
        data_dict['年度'].append(year)
        for key in data_dict.keys():
            if key != '年度':
                data_dict[key].append(None)
        continue
    
    # ヘッダーを設定して再読み込み
    df = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=header_row, engine=engine)
    
    # 全国データを探す
    national_data = None
    
    # 2019年以降は明示的に全国データがある
    if year >= 2019:
        for idx in df.index:
            if pd.notna(df.iloc[idx, 0]) and '全国' in str(df.iloc[idx, 0]):
                national_data = df.iloc[idx]
                print(f"  全国データ発見（行{idx}）")
                break
    
    # 2018年以前は最後の行が合計の可能性が高い
    if national_data is None and len(df) > 1700:
        # 最後の数行をチェック
        for idx in df.index[-5:]:
            row_str = str(df.iloc[idx, 0]) if pd.notna(df.iloc[idx, 0]) else ''
            if '全国' in row_str:
                national_data = df.iloc[idx]
                print(f"  全国データ発見（行{idx}）")
                break
    
    if national_data is None:
        print(f"  全国データが見つかりません")
        data_dict['年度'].append(year)
        for key in data_dict.keys():
            if key != '年度':
                data_dict[key].append(None)
        continue
    
    # データ抽出
    year_data = {'年度': year}
    
    # 列名を確認しながら抽出
    for col in df.columns:
        col_str = str(col)
        
        # 総排出量
        if ('総排出量' in col_str or 'ごみ総排出量' in col_str) and '1人1日' not in col_str:
            val = national_data[col]
            if pd.notna(val) and isinstance(val, (int, float)) and val > 1000:
                # トンから万トンへ変換
                year_data['総排出量_万トン'] = float(val) / 10000
                print(f"  総排出量: {val} トン → {float(val)/10000:.1f} 万トン")
                break
    
    # リサイクル率
    for col in df.columns:
        col_str = str(col)
        if 'リサイクル率' in col_str and 'Ｒ' in col_str and "'" not in col_str:
            val = national_data[col]
            if pd.notna(val) and isinstance(val, (int, float)):
                year_data['リサイクル率_%'] = float(val) if float(val) < 100 else float(val) / 100
                print(f"  リサイクル率: {float(val):.2f}%")
                break
    
    # 1人1日あたり排出量
    for col in df.columns:
        col_str = str(col)
        if ('１人１日' in col_str or '1人1日' in col_str) and '排出量' in col_str:
            val = national_data[col]
            if pd.notna(val) and isinstance(val, (int, float)) and val > 100 and val < 2000:
                year_data['1人1日あたり排出量_g'] = float(val)
                print(f"  1人1日あたり排出量: {float(val):.1f}g")
                break
    
    # 最終処分量（正確な列名で検索 - "ごみ処理量"を除外）
    for col in df.columns:
        col_str = str(col)
        # "最終処分量"で始まるか、"最終処分量 ("で始まる列を探す
        if (col_str.startswith('最終処分量') or '最終処分量 (' in col_str) and 'ごみ処理量' not in col_str:
            # ".1"などの番号付きでない最初のもの
            if not col_str.endswith(('.1', '.2', '.3', '.4', '.5')):
                val = national_data[col]
                if pd.notna(val) and isinstance(val, (int, float)) and val > 0:
                    # トンから万トンへ変換（値が異常に大きい場合はごみ処理量の可能性があるので除外）
                    if float(val) < 10000000:  # 1000万トン以下なら最終処分量として妥当
                        year_data['最終処分量_万トン'] = float(val) / 10000
                        print(f"  最終処分量: {val} トン → {float(val)/10000:.1f} 万トン")
                        break
    
    # データを追加
    for key in data_dict.keys():
        if key in year_data:
            data_dict[key].append(year_data[key])
        else:
            data_dict[key].append(None)

# DataFrameに変換
df_results = pd.DataFrame(data_dict)
print("\n=== 抽出結果 ===")
print(df_results)

# 可視化
fig = plt.figure(figsize=(16, 10))

# 1. 総排出量の推移
ax1 = plt.subplot(2, 2, 1)
valid_data = df_results.dropna(subset=['総排出量_万トン'])
if not valid_data.empty:
    ax1.plot(valid_data['年度'], valid_data['総排出量_万トン'], 'o-', linewidth=2, markersize=8, color='#2E86AB')
    ax1.set_title('ごみ総排出量の推移', fontsize=16, fontweight='bold')
    ax1.set_xlabel('年度', fontsize=12)
    ax1.set_ylabel('総排出量（万トン）', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(valid_data['年度'].values)
    ax1.set_xticklabels([f'{int(y)}' for y in valid_data['年度']], rotation=45)
    # 値を表示
    for x, y in zip(valid_data['年度'], valid_data['総排出量_万トン']):
        if pd.notna(y):
            ax1.annotate(f'{y:.0f}', (x, y), textcoords="offset points", xytext=(0,5), ha='center', fontsize=9)

# 2. リサイクル率の推移
ax2 = plt.subplot(2, 2, 2)
valid_data = df_results.dropna(subset=['リサイクル率_%'])
if not valid_data.empty:
    ax2.plot(valid_data['年度'], valid_data['リサイクル率_%'], 'o-', linewidth=2, markersize=8, color='#A23B72')
    ax2.set_title('リサイクル率の推移', fontsize=16, fontweight='bold')
    ax2.set_xlabel('年度', fontsize=12)
    ax2.set_ylabel('リサイクル率（%）', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(valid_data['年度'].values)
    ax2.set_xticklabels([f'{int(y)}' for y in valid_data['年度']], rotation=45)
    for x, y in zip(valid_data['年度'], valid_data['リサイクル率_%']):
        if pd.notna(y):
            ax2.annotate(f'{y:.1f}%', (x, y), textcoords="offset points", xytext=(0,5), ha='center', fontsize=9)

# 3. 一人一日あたり排出量の推移
ax3 = plt.subplot(2, 2, 3)
valid_data = df_results.dropna(subset=['一人一日あたり排出量_g'])
if not valid_data.empty:
    ax3.plot(valid_data['年度'], valid_data['一人一日あたり排出量_g'], 'o-', linewidth=2, markersize=8, color='#F18F01')
    ax3.set_title('1人1日あたりごみ排出量の推移', fontsize=16, fontweight='bold')
    ax3.set_xlabel('年度', fontsize=12)
    ax3.set_ylabel('排出量（g/人・日）', fontsize=12)
    ax3.grid(True, alpha=0.3)
    ax3.set_xticks(valid_data['年度'].values)
    ax3.set_xticklabels([f'{int(y)}' for y in valid_data['年度']], rotation=45)
    for x, y in zip(valid_data['年度'], valid_data['一人一日あたり排出量_g']):
        if pd.notna(y):
            ax3.annotate(f'{y:.0f}', (x, y), textcoords="offset points", xytext=(0,5), ha='center', fontsize=9)

# 4. 最終処分量の推移
ax4 = plt.subplot(2, 2, 4)
valid_data = df_results.dropna(subset=['最終処分量_万トン'])
if not valid_data.empty:
    ax4.plot(valid_data['年度'], valid_data['最終処分量_万トン'], 'o-', linewidth=2, markersize=8, color='#C73E1D')
    ax4.set_title('最終処分量の推移', fontsize=16, fontweight='bold')
    ax4.set_xlabel('年度', fontsize=12)
    ax4.set_ylabel('最終処分量（万トン）', fontsize=12)
    ax4.grid(True, alpha=0.3)
    ax4.set_xticks(valid_data['年度'].values)
    ax4.set_xticklabels([f'{int(y)}' for y in valid_data['年度']], rotation=45)
    for x, y in zip(valid_data['年度'], valid_data['最終処分量_万トン']):
        if pd.notna(y):
            ax4.annotate(f'{y:.0f}', (x, y), textcoords="offset points", xytext=(0,5), ha='center', fontsize=9)

plt.suptitle('日本の廃棄物処理状況の推移（2010-2022年）', fontsize=20, fontweight='bold', y=1.02)
plt.tight_layout()

# 画像を保存
plt.savefig('waste_trends_overview.png', dpi=300, bbox_inches='tight')
print("\n画像を保存しました: waste_trends_overview.png")

# CSVにも保存
df_results.to_csv('waste_data_summary.csv', index=False, encoding='utf-8-sig')
print("データをCSVに保存しました: waste_data_summary.csv")