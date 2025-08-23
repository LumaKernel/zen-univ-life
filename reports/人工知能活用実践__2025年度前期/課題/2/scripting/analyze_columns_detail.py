#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# データフォルダのパス
data_path = "data/"

# 2022年のデータで詳細な列構造を分析
year = 2022
engine = 'openpyxl'

print(f"{year}年のごみ処理概要シートの詳細分析")
print("="*80)

try:
    # ヘッダーなしで読み込み
    df = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=None, engine=engine)
    
    # ヘッダー行を探す
    header_row = None
    for i in range(min(10, len(df))):
        if '都道府県' in str(df.iloc[i, 0]):
            header_row = i
            print(f"ヘッダー行: {header_row}")
            break
    
    # ヘッダー付きで読み込み
    df_with_header = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', 
                                  header=header_row, engine=engine)
    
    # 全国データの行を探す
    national_idx = None
    for idx in df_with_header.index:
        if '全国' in str(df_with_header.iloc[idx, 0]):
            national_idx = idx
            print(f"全国データ行: {national_idx}")
            break
    
    if national_idx:
        national_data = df_with_header.iloc[national_idx]
        
        print("\n重要な列とその値:")
        print("-"*80)
        
        # 各列を詳細に確認
        for i, col in enumerate(df_with_header.columns):
            col_str = str(col)
            val = national_data[col]
            
            # 重要な列のみ表示
            important_keywords = ['最終処分', '焼却', '残渣', '処理量', '直接', '中間処理']
            if any(keyword in col_str for keyword in important_keywords):
                if pd.notna(val) and val != 0:
                    # 数値の大きさで単位を推定
                    if isinstance(val, (int, float)):
                        if val > 1000000:
                            unit_guess = "トン単位の可能性"
                        elif val > 10000:
                            unit_guess = "トン単位"
                        elif val > 100:
                            unit_guess = "千トン単位の可能性"
                        elif val < 100:
                            unit_guess = "率または万トン単位"
                        
                        print(f"\n列{i}: {col_str[:80]}...")
                        print(f"  値: {val:,.2f}")
                        print(f"  推定単位: {unit_guess}")
                        print(f"  万トン換算: {val/10000:.2f} 万トン")

except Exception as e:
    print(f"エラー: {e}")

# ごみフローシートも詳細確認
print("\n\n" + "="*80)
print("ごみフローシートの詳細分析")
print("="*80)

try:
    df_flow = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみフローシート', 
                           header=None, engine=engine)
    
    print(f"サイズ: {df_flow.shape}")
    print("\n焼却残渣関連のデータ:")
    
    # セル単位で探索
    for i in range(len(df_flow)):
        for j in range(len(df_flow.columns)):
            cell = df_flow.iloc[i, j]
            if pd.notna(cell):
                cell_str = str(cell)
                if '焼却残渣' in cell_str or '最終処分' in cell_str or '埋立' in cell_str:
                    print(f"\n位置({i},{j}): {cell_str}")
                    # 周辺のセルも確認
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < len(df_flow) and 0 <= nj < len(df_flow.columns):
                                neighbor = df_flow.iloc[ni, nj]
                                if pd.notna(neighbor) and isinstance(neighbor, (int, float)) and neighbor > 0:
                                    print(f"  隣接値({ni},{nj}): {neighbor:,.0f}")

except Exception as e:
    print(f"エラー: {e}")

# 2010年と比較
print("\n\n" + "="*80)
print("2010年データとの比較")
print("="*80)

year = 2010
engine = 'xlrd'

try:
    df = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=None, engine=engine)
    
    # ヘッダー行を探す
    header_row = None
    for i in range(min(10, len(df))):
        if '都道府県' in str(df.iloc[i, 0]):
            header_row = i
            break
    
    # ヘッダー付きで読み込み
    df_with_header = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', 
                                  header=header_row, engine=engine)
    
    # 全国データ
    for idx in df_with_header.index[-5:]:
        if '全国' in str(df_with_header.iloc[idx, 0]):
            national_data = df_with_header.iloc[idx]
            
            print(f"\n{year}年の全国データ:")
            for i, col in enumerate(df_with_header.columns):
                col_str = str(col)
                if '最終処分量' in col_str:
                    val = national_data[col]
                    if pd.notna(val) and val != 0:
                        print(f"\n列{i}: {col_str[:80]}...")
                        print(f"  値: {val:,.2f}")
                        print(f"  万トン換算: {val/10000:.2f} 万トン")
            break

except Exception as e:
    print(f"エラー: {e}")