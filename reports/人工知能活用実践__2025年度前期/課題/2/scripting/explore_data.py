#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import warnings
warnings.filterwarnings('ignore')

# 日本語フォントの設定
plt.rcParams['font.family'] = 'Hiragino Sans'
plt.rcParams['axes.unicode_minus'] = False

# データフォルダのパス
data_path = "data/"

# 最初に2022年のデータ構造を確認
print("2022年のデータ構造を確認中...")
df_2022 = pd.read_excel(f"{data_path}2022.xlsx", sheet_name=None)
print(f"シート名: {list(df_2022.keys())}")

# 最初のシートのデータを確認
for sheet_name in list(df_2022.keys())[:1]:
    print(f"\n=== {sheet_name} ===")
    df = df_2022[sheet_name]
    print(f"形状: {df.shape}")
    print(f"列名（最初の10列）: {list(df.columns[:10])}")
    print(f"\n最初の5行:")
    print(df.head())

# 2010年のデータ構造も確認（形式が変わっている可能性があるため）
print("\n\n2010年のデータ構造を確認中...")
df_2010 = pd.read_excel(f"{data_path}2010.xlsx", sheet_name=None)
print(f"シート名: {list(df_2010.keys())}")

for sheet_name in list(df_2010.keys())[:1]:
    print(f"\n=== {sheet_name} ===")
    df = df_2010[sheet_name]
    print(f"形状: {df.shape}")
    print(f"列名（最初の10列）: {list(df.columns[:10])}")
    print(f"\n最初の5行:")
    print(df.head())