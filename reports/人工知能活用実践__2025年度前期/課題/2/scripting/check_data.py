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

# 各年のデータを確認
for year in years:
    try:
        df = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=None)
        print(f"\n{year}年: shape={df.shape}")
        
        # 最初の数行を確認
        for i in range(min(10, len(df))):
            row_str = ' '.join([str(val)[:20] for val in df.iloc[i].values[:5] if pd.notna(val)])
            if '全国' in row_str or '合計' in row_str or '総排出' in row_str:
                print(f"  Row {i}: {row_str[:100]}...")
        
    except Exception as e:
        print(f"{year}年: エラー - {e}")