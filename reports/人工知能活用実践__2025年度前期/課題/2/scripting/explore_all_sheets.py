#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# データフォルダのパス
data_path = "data/"

# 代表的な年度でシート構造を調査
test_years = [2010, 2016, 2022]

for year in test_years:
    print(f"\n{'='*80}")
    print(f"{year}年のExcelファイル構造")
    print('='*80)
    
    # エンジンの選択
    if year <= 2015:
        engine = 'xlrd'
    else:
        engine = 'openpyxl'
    
    try:
        # Excelファイルを開く
        xl_file = pd.ExcelFile(f"{data_path}{year}.xlsx", engine=engine)
        print(f"\n利用可能なシート数: {len(xl_file.sheet_names)}")
        print("シート名一覧:")
        for i, sheet_name in enumerate(xl_file.sheet_names):
            print(f"  {i+1}. {sheet_name}")
        
        # 各シートの概要を確認
        print("\n各シートの詳細:")
        for sheet_name in xl_file.sheet_names:
            try:
                df = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name=sheet_name, header=None, engine=engine)
                print(f"\n  【{sheet_name}】")
                print(f"    サイズ: {df.shape}")
                
                # 最初の10行から重要そうなキーワードを探す
                keywords_found = []
                for i in range(min(10, len(df))):
                    row_str = ' '.join([str(val) for val in df.iloc[i].values if pd.notna(val)])
                    important_keywords = ['残余容量', '残余年数', '焼却残渣', '処分場', '施設数', 
                                         '最終処分場', '埋立', '残渣', '灰', '飛灰', '設置']
                    for keyword in important_keywords:
                        if keyword in row_str and keyword not in keywords_found:
                            keywords_found.append(keyword)
                
                if keywords_found:
                    print(f"    重要キーワード: {', '.join(keywords_found)}")
                
                # 最初の数行を表示（データ構造の確認）
                if '処分' in sheet_name or '残' in sheet_name or '施設' in sheet_name:
                    print(f"    最初の3行:")
                    for i in range(min(3, len(df))):
                        row_preview = ' '.join([str(val)[:20] if pd.notna(val) else 'NaN' for val in df.iloc[i].values[:5]])
                        print(f"      行{i}: {row_preview[:100]}...")
                        
            except Exception as e:
                print(f"    エラー: {e}")
    
    except Exception as e:
        print(f"ファイル読み込みエラー: {e}")

print("\n\n" + "="*80)
print("最終処分場関連データの詳細調査")
print("="*80)

# 2022年のデータで最終処分場関連の詳細を調査
year = 2022
engine = 'openpyxl'

try:
    # ごみ処理概要シートから最終処分場関連データを探す
    df = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=None, engine=engine)
    
    print(f"\n{year}年 ごみ処理概要シートの列構造:")
    
    # ヘッダー行を探す
    header_row = None
    for i in range(min(10, len(df))):
        if '都道府県' in str(df.iloc[i, 0]):
            header_row = i
            break
    
    if header_row:
        df_with_header = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', 
                                      header=header_row, engine=engine)
        
        # 全列名を確認
        print(f"\n全{len(df_with_header.columns)}列の中から関連する列:")
        for i, col in enumerate(df_with_header.columns):
            col_str = str(col)
            # 残余容量、残余年数、焼却残渣関連の列を探す
            if any(keyword in col_str for keyword in ['残余', '埋立', '焼却残渣', '飛灰', '処分場']):
                print(f"  列{i}: {col}")
                
                # 全国データの値を確認
                for idx in df_with_header.index[-5:]:
                    if '全国' in str(df_with_header.iloc[idx, 0]):
                        val = df_with_header.iloc[idx][col]
                        if pd.notna(val) and val != 0:
                            print(f"    全国データ: {val}")
                        break

except Exception as e:
    print(f"エラー: {e}")

# ごみフローシートも確認
print("\n\nごみフローシートの確認:")
for year in [2010, 2022]:
    print(f"\n{year}年:")
    engine = 'xlrd' if year <= 2015 else 'openpyxl'
    try:
        df = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみフローシート', header=None, engine=engine)
        print(f"  サイズ: {df.shape}")
        
        # フローシートのデータ構造を確認
        for i in range(min(20, len(df))):
            row_str = ' '.join([str(val) for val in df.iloc[i].values if pd.notna(val)])
            if any(keyword in row_str for keyword in ['焼却残渣', '最終処分', '埋立', '残余']):
                print(f"  行{i}: {row_str[:150]}...")
                
    except Exception as e:
        print(f"  エラー: {e}")