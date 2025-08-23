#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# データフォルダのパス
data_path = "data/"

# 2010年と2022年のデータで列名を詳しく確認
for year in [2010, 2022]:
    print(f"\n{'='*60}")
    print(f"{year}年の列構造確認")
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
            break
    
    # ヘッダーを設定して再読み込み
    df = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=header_row, engine=engine)
    
    print(f"\n全列名（{len(df.columns)}列）:")
    for i, col in enumerate(df.columns):
        col_str = str(col)
        # 重要な列のみ表示
        if any(keyword in col_str for keyword in ['最終処分', '焼却', '資源化', 'リサイクル', '総排出', '処理量']):
            print(f"  列{i}: {col}")
    
    # 全国データの行を取得
    national_row = None
    if year >= 2019:
        for idx in df.index:
            if pd.notna(df.iloc[idx, 0]) and '全国' in str(df.iloc[idx, 0]):
                national_row = df.iloc[idx]
                print(f"\n全国データ（行{idx}）の値:")
                break
    else:
        # 最後の数行から全国を探す
        for idx in df.index[-5:]:
            if pd.notna(df.iloc[idx, 0]) and '全国' in str(df.iloc[idx, 0]):
                national_row = df.iloc[idx]
                print(f"\n全国データ（行{idx}）の値:")
                break
    
    if national_row is not None:
        for i, col in enumerate(df.columns):
            col_str = str(col)
            if any(keyword in col_str for keyword in ['最終処分量', '焼却', '資源化']):
                val = national_row[col]
                if pd.notna(val) and isinstance(val, (int, float)) and val > 0:
                    print(f"  {col}: {val:,.0f} ({val/10000:,.1f}万トン)")