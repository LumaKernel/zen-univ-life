#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# データフォルダのパス
data_path = "data/"

# 各年のデータ構造を詳しく調査
years = [2010, 2012, 2015, 2018, 2019, 2022]  # 代表的な年をチェック

for year in years:
    print(f"\n{'='*60}")
    print(f"{year}年のデータ調査")
    print('='*60)
    
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
            print(f"ヘッダー行: {header_row}")
            break
    
    if header_row is None:
        print("ヘッダー行が見つかりません")
        continue
    
    # ヘッダーを設定して再読み込み
    df = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=header_row, engine=engine)
    
    print(f"データサイズ: {df.shape}")
    print("\n列名（最初の20列）:")
    for i, col in enumerate(df.columns[:20]):
        print(f"  列{i}: {col}")
    
    # 全国データまたは最終行を確認
    print("\n最後の5行のデータ:")
    for idx in df.index[-5:]:
        row = df.iloc[idx]
        # 最初の列（通常は都道府県名）と数値データを表示
        first_col = row.iloc[0] if pd.notna(row.iloc[0]) else 'NaN'
        print(f"\n行{idx}: {first_col}")
        
        # 重要な列のデータを表示
        for col in df.columns:
            if any(keyword in str(col) for keyword in ['総排出量', '最終処分', '焼却', '資源化', 'リサイクル']):
                val = row[col]
                if pd.notna(val) and val != 0:
                    print(f"  {col}: {val}")
    
    # 全国データを探す
    print("\n全国データの検索:")
    found_national = False
    for idx in df.index:
        row_str = str(df.iloc[idx, 0]) if pd.notna(df.iloc[idx, 0]) else ''
        if '全国' in row_str:
            found_national = True
            print(f"全国データ発見（行{idx}）:")
            row = df.iloc[idx]
            for col in df.columns:
                if any(keyword in str(col) for keyword in ['総排出量', '最終処分', '焼却', '資源化', 'リサイクル', '1人1日']):
                    val = row[col]
                    if pd.notna(val) and val != 0:
                        print(f"  {col}: {val}")
            break
    
    if not found_national:
        print("  全国データは見つかりませんでした（都道府県の合計が必要）")
    
    # 単位を確認するため、いくつかの数値の範囲を確認
    print("\n数値の範囲チェック:")
    for col in df.columns:
        if '排出量' in str(col) or '処分' in str(col) or '焼却' in str(col) or '資源化' in str(col):
            numeric_col = pd.to_numeric(df[col], errors='coerce')
            valid_data = numeric_col[numeric_col.notna() & (numeric_col > 0)]
            if len(valid_data) > 0:
                print(f"  {col}:")
                print(f"    最小値: {valid_data.min():.2f}")
                print(f"    最大値: {valid_data.max():.2f}")
                print(f"    中央値: {valid_data.median():.2f}")