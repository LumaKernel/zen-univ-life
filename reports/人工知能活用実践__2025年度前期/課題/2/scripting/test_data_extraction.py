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

# 簡易的にデータを確認
results = []
for year in years:
    try:
        # Excelファイルを読み込み
        df_all = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=None)
        
        # 都道府県名を含む行を探す
        header_row = None
        for i in range(10):
            if '都道府県' in str(df_all.iloc[i, 0]):
                header_row = i
                break
        
        if header_row is None:
            results.append({'年': year, 'ステータス': 'ヘッダー行なし', 'データ行数': df_all.shape[0]})
            continue
            
        # ヘッダーを設定して再読み込み
        df = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=header_row)
        
        # 全国データを探す
        found_national = False
        for idx in df.index:
            row_str = ' '.join([str(val) for val in df.iloc[idx].values if pd.notna(val)])
            if '全国' in row_str:
                found_national = True
                # 総排出量の値を探す
                col_names = df.columns.tolist()
                for col in col_names:
                    if '総排出量' in str(col) or 'ごみ総排出量' in str(col):
                        val = df.iloc[idx][col]
                        if pd.notna(val) and val != 0:
                            results.append({'年': year, 'ステータス': '全国データあり', 'データ行数': df.shape[0], '総排出量': val})
                            break
                break
        
        if not found_national:
            results.append({'年': year, 'ステータス': '全国データなし（都道府県集計必要）', 'データ行数': df.shape[0]})
        
    except Exception as e:
        results.append({'年': year, 'ステータス': f'エラー: {str(e)[:50]}', 'データ行数': 0})

# 結果を表示
df_summary = pd.DataFrame(results)
print("データ読み込み状況:")
print(df_summary)