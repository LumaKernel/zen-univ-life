#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# データフォルダのパス
data_path = "data/"

# 年度リスト
years = list(range(2010, 2023))

# 各年のデータを詳細に確認して抽出
all_data = []

for year in years:
    print(f"\n=== {year}年のデータ処理 ===")
    
    # ファイル読み込み（engine指定）
    if year <= 2015:
        engine = 'xlrd'
    else:
        engine = 'openpyxl'
    
    # まず、シート名を確認
    xl_file = pd.ExcelFile(f"{data_path}{year}.xlsx", engine=engine)
    print(f"利用可能なシート: {xl_file.sheet_names}")
    
    # ごみ処理概要シートを読み込み
    df = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=None, engine=engine)
    print(f"データサイズ: {df.shape}")
    
    # ヘッダー行を探す（都道府県や全国を含む行）
    header_row = None
    for i in range(min(20, len(df))):
        row_str = ' '.join([str(val) for val in df.iloc[i].values if pd.notna(val)])
        if '都道府県' in row_str or '全国' in row_str:
            print(f"  キーワード発見 (行{i}): {row_str[:100]}...")
            if header_row is None:
                header_row = i
    
    # 全国データを探す（複数の方法で試行）
    total_waste = None
    recycling_amount = None
    
    # 方法1: "全国"という文字列を含む行を探す
    for i in range(len(df)):
        row = df.iloc[i]
        if any('全国' in str(val) for val in row.values if pd.notna(val)):
            print(f"  全国データ候補 (行{i})")
            # この行から数値を抽出
            for val in row.values:
                if pd.notna(val) and isinstance(val, (int, float)) and val > 1000:
                    if total_waste is None:
                        total_waste = val
                        print(f"    総排出量候補: {val}")
                        break
    
    # 方法2: 最後の数行に合計がある場合
    if total_waste is None:
        for i in range(max(0, len(df)-10), len(df)):
            row = df.iloc[i]
            # 大きな数値を探す（総排出量は通常大きい）
            for val in row.values:
                if pd.notna(val) and isinstance(val, (int, float)) and val > 10000:
                    total_waste = val
                    print(f"  総排出量（末尾から）: {val}")
                    break
            if total_waste:
                break
    
    # 方法3: 列名から推測
    if total_waste is None and header_row is not None:
        df_with_header = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', 
                                       header=header_row, engine=engine)
        # 総排出量を含む列を探す
        for col in df_with_header.columns:
            if '総排出' in str(col) or 'ごみ総排出' in str(col):
                # その列の最大値または合計値を取得
                col_data = pd.to_numeric(df_with_header[col], errors='coerce')
                if not col_data.isna().all():
                    total_waste = col_data.max()
                    print(f"  総排出量（列から）: {total_waste}")
                    break
    
    # データを保存
    if total_waste is not None:
        all_data.append({
            '年度': year,
            '総排出量（千t）': total_waste,
            'データ行数': df.shape[0]
        })
        print(f"  ✓ データ抽出成功: 総排出量={total_waste}")
    else:
        print(f"  ✗ データ抽出失敗")

# 結果を表示
print("\n=== 抽出結果サマリー ===")
df_result = pd.DataFrame(all_data)
print(df_result)

# CSVに保存
df_result.to_csv('extracted_data.csv', index=False, encoding='utf-8-sig')
print("\n抽出データをextracted_data.csvに保存しました")