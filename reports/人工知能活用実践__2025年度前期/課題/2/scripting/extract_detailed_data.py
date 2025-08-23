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

# 結果を格納
results = []

print("焼却残渣と最終処分の詳細データを抽出中...")
print("="*80)

for year in years:
    print(f"\n{year}年:")
    
    # エンジンの選択
    if year <= 2015:
        engine = 'xlrd'
    else:
        engine = 'openpyxl'
    
    year_data = {
        '年度': year,
        '直接最終処分量_万トン': None,
        '焼却残渣量_万トン': None,
        '処理残渣量_万トン': None,
        '最終処分量合計_万トン': None,
        '焼却量_万トン': None,
        '焼却残渣の資源化量_万トン': None,
        '焼却残渣の資源化率_%': None
    }
    
    try:
        # 1. ごみ処理概要シートから基本データを取得
        df = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=None, engine=engine)
        
        # ヘッダー行を探す
        header_row = None
        for i in range(min(20, len(df))):
            if '都道府県' in str(df.iloc[i, 0]):
                header_row = i
                break
        
        if header_row:
            df_with_header = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', 
                                          header=header_row, engine=engine)
            
            # 全国データを探す
            national_data = None
            for idx in df_with_header.index:
                if '全国' in str(df_with_header.iloc[idx, 0]):
                    national_data = df_with_header.iloc[idx]
                    print(f"  全国データ発見（ごみ処理概要）")
                    break
            
            # 最後の数行も確認（2018年以前）
            if national_data is None and len(df_with_header) > 1000:
                for idx in df_with_header.index[-5:]:
                    if '全国' in str(df_with_header.iloc[idx, 0]):
                        national_data = df_with_header.iloc[idx]
                        print(f"  全国データ発見（最終行付近）")
                        break
            
            if national_data is not None:
                # 列を順番に確認して詳細データを抽出
                for col in df_with_header.columns:
                    col_str = str(col)
                    
                    # 直接最終処分量を探す
                    if '直接最終処分' in col_str and '率' not in col_str:
                        val = national_data[col]
                        if pd.notna(val) and isinstance(val, (int, float)) and val > 0:
                            year_data['直接最終処分量_万トン'] = float(val) / 10000
                            print(f"    直接最終処分量: {float(val)/10000:.2f} 万トン")
                    
                    # 焼却残渣量を探す
                    elif '焼却残渣' in col_str and '率' not in col_str and '再生' not in col_str:
                        val = national_data[col]
                        if pd.notna(val) and isinstance(val, (int, float)) and val > 0:
                            year_data['焼却残渣量_万トン'] = float(val) / 10000
                            print(f"    焼却残渣量: {float(val)/10000:.2f} 万トン")
                    
                    # 処理残渣量を探す
                    elif '処理残渣' in col_str and '率' not in col_str and '焼却' not in col_str:
                        val = national_data[col]
                        if pd.notna(val) and isinstance(val, (int, float)) and val > 0:
                            year_data['処理残渣量_万トン'] = float(val) / 10000
                            print(f"    処理残渣量: {float(val)/10000:.2f} 万トン")
                    
                    # 焼却量を探す
                    elif ('直接焼却' in col_str or '焼却処理量' in col_str) and '率' not in col_str:
                        val = national_data[col]
                        if pd.notna(val) and isinstance(val, (int, float)) and val > 0:
                            if float(val) > 10000000:  # 1000万トン以上なら妥当な焼却量
                                year_data['焼却量_万トン'] = float(val) / 10000
                                print(f"    焼却量: {float(val)/10000:.2f} 万トン")
        
        # 2. ごみフローシートから詳細データを取得
        try:
            df_flow = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみフローシート', 
                                   header=None, engine=engine)
            
            print(f"  ごみフローシートデータ確認:")
            
            # フローシートから焼却残渣関連データを探す
            for i in range(len(df_flow)):
                for j in range(len(df_flow.columns)):
                    cell_val = str(df_flow.iloc[i, j])
                    
                    # 焼却残渣の埋立を探す
                    if '焼却残渣' in cell_val and '埋立' in cell_val:
                        # 隣接セルから数値を探す
                        for k in range(max(0, j-2), min(j+3, len(df_flow.columns))):
                            val = df_flow.iloc[i, k]
                            if pd.notna(val) and isinstance(val, (int, float)) and val > 1000:
                                print(f"    焼却残渣の埋立（フロー）: {float(val)/10000:.2f} 万トン")
                                if year_data['焼却残渣量_万トン'] is None:
                                    year_data['焼却残渣量_万トン'] = float(val) / 10000
                                break
                    
                    # 直接最終処分量を探す
                    elif '直接最終処分' in cell_val:
                        # 同じ行の数値を探す
                        for k in range(len(df_flow.columns)):
                            val = df_flow.iloc[i, k]
                            if pd.notna(val) and isinstance(val, (int, float)) and val > 1000:
                                print(f"    直接最終処分量（フロー）: {float(val)/10000:.2f} 万トン")
                                if year_data['直接最終処分量_万トン'] is None:
                                    year_data['直接最終処分量_万トン'] = float(val) / 10000
                                break
                                
        except Exception as e:
            print(f"  ごみフローシート読み込みエラー: {e}")
        
        # 3. 資源化量内訳シートから焼却灰の資源化データを取得
        try:
            df_recycle = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='資源化量内訳', 
                                      header=None, engine=engine)
            
            # ヘッダー行を探す
            header_row = None
            for i in range(min(10, len(df_recycle))):
                if '都道府県' in str(df_recycle.iloc[i, 0]):
                    header_row = i
                    break
            
            if header_row:
                df_recycle_with_header = pd.read_excel(f"{data_path}{year}.xlsx", 
                                                      sheet_name='資源化量内訳', 
                                                      header=header_row, engine=engine)
                
                # 全国データを探す
                for idx in df_recycle_with_header.index[-10:]:
                    if '全国' in str(df_recycle_with_header.iloc[idx, 0]) or idx == len(df_recycle_with_header) - 1:
                        national_recycle = df_recycle_with_header.iloc[idx]
                        
                        # 焼却灰・飛灰の資源化量を探す
                        for col in df_recycle_with_header.columns:
                            col_str = str(col)
                            if ('焼却灰' in col_str or '飛灰' in col_str) and '資源化' in col_str:
                                val = national_recycle[col]
                                if pd.notna(val) and isinstance(val, (int, float)) and val > 0:
                                    year_data['焼却残渣の資源化量_万トン'] = float(val) / 10000
                                    print(f"    焼却灰・飛灰の資源化量: {float(val)/10000:.2f} 万トン")
                        break
                        
        except Exception as e:
            print(f"  資源化量内訳読み込みエラー: {e}")
        
        # 最終処分量合計を計算
        if year_data['直接最終処分量_万トン'] or year_data['焼却残渣量_万トン'] or year_data['処理残渣量_万トン']:
            total = 0
            if year_data['直接最終処分量_万トン']:
                total += year_data['直接最終処分量_万トン']
            if year_data['焼却残渣量_万トン']:
                total += year_data['焼却残渣量_万トン']
            if year_data['処理残渣量_万トン']:
                total += year_data['処理残渣量_万トン']
            year_data['最終処分量合計_万トン'] = total
            print(f"    最終処分量合計: {total:.2f} 万トン")
        
        # 焼却残渣の資源化率を計算
        if year_data['焼却残渣量_万トン'] and year_data['焼却残渣の資源化量_万トン']:
            rate = year_data['焼却残渣の資源化量_万トン'] / year_data['焼却残渣量_万トン'] * 100
            year_data['焼却残渣の資源化率_%'] = rate
            print(f"    焼却残渣の資源化率: {rate:.1f}%")
            
    except Exception as e:
        print(f"  エラー: {e}")
    
    results.append(year_data)

# 結果をDataFrameに変換
df_results = pd.DataFrame(results)

print("\n" + "="*80)
print("抽出結果サマリー")
print("="*80)
print(df_results.to_string())

# CSVに保存
df_results.to_csv('detailed_waste_data.csv', index=False, encoding='utf-8-sig')
print("\n結果をdetailed_waste_data.csvに保存しました")