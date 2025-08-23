#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
import warnings
warnings.filterwarnings('ignore')

# 日本語フォント設定のおまじない（重要：スタイル設定の後で呼ぶ必要がある）

# print(matplotlib.get_cachedir())

# 日本語文字化け対策のおまじない
# IPAexフォントを直接指定
# font_path = './ipaexg00401/ipaexg.ttf'
# font_prop = FontProperties(fname=font_path)
#
# # matplotlibの設定を更新
# plt.rcParams['font.family'] = font_prop.get_name()
# # フォントパスを追加
# fm.fontManager.addfont(font_path)
# plt.rcParams['font.sans-serif'] = [font_prop.get_name()]

# データフォルダのパス
data_path = "data/"

# 年度リスト
years = list(range(2010, 2023))

# 実際の総排出量データ（環境省データより、単位：万トン）
actual_total_waste = {
    2010: 4536,
    2011: 4539,
    2012: 4523,
    2013: 4487,
    2014: 4432,
    2015: 4398,
    2016: 4317,
    2017: 4289,
    2018: 4273,
    2019: 4274,
    2020: 4167,
    2021: 4120,
    2022: 4096
}

# データを格納する辞書
data_dict = {
    '年度': [],
    '総排出量_万トン': [],
    'リサイクル率_%': [],
    '一人一日あたり排出量_g': [],
    '最終処分量_万トン': [],
    '焼却処理量_万トン': [],
    '直接資源化量_万トン': []
}

print("データを読み込み中...")

for year in years:
    try:
        # Excelファイルを読み込み（古いExcel形式に対応）
        if year <= 2015:
            # 古いExcel形式 (.xls) の場合はxlrdを使用
            df_all = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=None, engine='xlrd')
        else:
            # 新しいExcel形式の場合はopenpyxlを使用
            df_all = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=None, engine='openpyxl')
        
        # データの位置を探す（ヘッダー行を見つける）
        # 都道府県名を含む行を探す
        header_row = None
        for i in range(10):
            if '都道府県' in str(df_all.iloc[i, 0]):
                header_row = i
                break
        
        if header_row is None:
            print(f"{year}年: ヘッダー行が見つかりません")
            continue
            
        # ヘッダーを設定（エンジンも指定）
        if year <= 2015:
            df = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=header_row, engine='xlrd')
        else:
            df = pd.read_excel(f"{data_path}{year}.xlsx", sheet_name='ごみ処理概要', header=header_row, engine='openpyxl')
        
        # 全国合計を探す（最後の行または「全国」を含む行）
        total_row = None
        for idx in df.index[-10:]:  # 最後の10行をチェック
            row_str = ' '.join([str(val) for val in df.iloc[idx].values if pd.notna(val)])
            if '全国' in row_str or '合計' in row_str:
                total_row = idx
                break
        
        if total_row is None:
            # 全国が見つからない場合は、都道府県ごとのデータを合計
            # 数値データの列を特定
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            # 都道府県名が含まれる行を抽出（北海道から沖縄まで）
            prefectures = ['北海道', '青森', '岩手', '宮城', '秋田', '山形', '福島',
                          '茨城', '栃木', '群馬', '埼玉', '千葉', '東京', '神奈川',
                          '新潟', '富山', '石川', '福井', '山梨', '長野', '岐阜',
                          '静岡', '愛知', '三重', '滋賀', '京都', '大阪', '兵庫',
                          '奈良', '和歌山', '鳥取', '島根', '岡山', '広島', '山口',
                          '徳島', '香川', '愛媛', '高知', '福岡', '佐賀', '長崎',
                          '熊本', '大分', '宮崎', '鹿児島', '沖縄']
            
            pref_data = pd.DataFrame()
            for pref in prefectures:
                pref_rows = df[df.iloc[:, 0].astype(str).str.contains(pref, na=False)]
                if not pref_rows.empty:
                    # 最初の行を取る（市町村データではなく県データ）
                    if pref_data.empty:
                        pref_data = pref_rows.iloc[[0]]
                    else:
                        pref_data = pd.concat([pref_data, pref_rows.iloc[[0]]])
            
            # 合計を計算
            total_data = pref_data[numeric_cols].sum()
        else:
            total_data = df.iloc[total_row]
        
        # 列名を標準化して抽出
        col_names = df.columns.tolist()
        
        # 総排出量は実際のデータを使用
        total_waste = actual_total_waste.get(year, None)
        
        # リサイクル率を探す
        recycling_rate = None
        for col in col_names:
            if 'リサイクル率' in str(col) or '資源化率' in str(col):
                val = total_data[col] if total_row else total_data.get(col, 0)
                if pd.notna(val) and val != 0:
                    recycling_rate = float(val)
                    if recycling_rate > 100:  # パーセントではなく小数の場合
                        recycling_rate = recycling_rate / 100
                    break
        
        # 一人一日あたり排出量を探す
        per_capita = None
        for col in col_names:
            if '1人1日' in str(col) or '一人一日' in str(col) or '１人１日' in str(col):
                val = total_data[col] if total_row else total_data.get(col, 0)
                if pd.notna(val) and val != 0:
                    per_capita = float(val)
                    break
        
        # 最終処分量を探す
        final_disposal = None
        for col in col_names:
            if '最終処分量' in str(col):
                val = total_data[col] if total_row else total_data.get(col, 0)
                if pd.notna(val) and val != 0:
                    final_disposal = float(val) / 10000  # トンから万トンへ
                    break
        
        # 焼却処理量を探す
        incineration = None
        for col in col_names:
            if '焼却' in str(col) and '処理量' in str(col):
                val = total_data[col] if total_row else total_data.get(col, 0)
                if pd.notna(val) and val != 0:
                    incineration = float(val) / 10000  # トンから万トンへ
                    break
        
        # 直接資源化量を探す
        direct_recycling = None
        for col in col_names:
            if '直接資源化' in str(col):
                val = total_data[col] if total_row else total_data.get(col, 0)
                if pd.notna(val) and val != 0:
                    direct_recycling = float(val) / 10000  # トンから万トンへ
                    break
        
        # データを保存
        data_dict['年度'].append(year)
        data_dict['総排出量_万トン'].append(total_waste)
        data_dict['リサイクル率_%'].append(recycling_rate)
        data_dict['一人一日あたり排出量_g'].append(per_capita)
        data_dict['最終処分量_万トン'].append(final_disposal)
        data_dict['焼却処理量_万トン'].append(incineration)
        data_dict['直接資源化量_万トン'].append(direct_recycling)
        
        print(f"{year}年: データ抽出完了")
        
    except Exception as e:
        print(f"{year}年: エラー - {e}")
        # NaNを追加
        data_dict['年度'].append(year)
        for key in data_dict.keys():
            if key != '年度':
                data_dict[key].append(None)

# DataFrameに変換
df_results = pd.DataFrame(data_dict)
print("\n抽出したデータ:")
print(df_results)

# 可視化
# seabornのスタイル設定で日本語フォントを指定
sns.set(style='darkgrid', font='IPAexGothic')
fig = plt.figure(figsize=(20, 12))

# 1. 総排出量の推移
ax1 = plt.subplot(2, 3, 1)
valid_data = df_results.dropna(subset=['総排出量_万トン'])
ax1.plot(valid_data['年度'], valid_data['総排出量_万トン'], 'o-', linewidth=2, markersize=8, color='#2E86AB')
ax1.set_title('ごみ総排出量の推移', fontsize=16, fontweight='bold')
ax1.set_xlabel('年度', fontsize=12)
ax1.set_ylabel('総排出量（万トン）', fontsize=12)
ax1.grid(True, alpha=0.3)
# x軸の目盛りを整数にする
ax1.set_xticks(valid_data['年度'].values)
ax1.set_xticklabels([f'{int(y)}' for y in valid_data['年度']], rotation=45)
for x, y in zip(valid_data['年度'], valid_data['総排出量_万トン']):
    if pd.notna(y):
        ax1.annotate(f'{y:.0f}', (x, y), textcoords="offset points", xytext=(0,5), ha='center', fontsize=9)

# 2. リサイクル率の推移
ax2 = plt.subplot(2, 3, 2)
valid_data = df_results.dropna(subset=['リサイクル率_%'])
ax2.plot(valid_data['年度'], valid_data['リサイクル率_%'], 'o-', linewidth=2, markersize=8, color='#A23B72')
ax2.set_title('リサイクル率の推移', fontsize=16, fontweight='bold')
ax2.set_xlabel('年度', fontsize=12)
ax2.set_ylabel('リサイクル率（%）', fontsize=12)
ax2.grid(True, alpha=0.3)
# x軸の目盛りを整数にする
ax2.set_xticks(valid_data['年度'].values)
ax2.set_xticklabels([f'{int(y)}' for y in valid_data['年度']], rotation=45)
for x, y in zip(valid_data['年度'], valid_data['リサイクル率_%']):
    if pd.notna(y):
        ax2.annotate(f'{y:.1f}%', (x, y), textcoords="offset points", xytext=(0,5), ha='center', fontsize=9)

# 3. 一人一日あたり排出量の推移
ax3 = plt.subplot(2, 3, 3)
valid_data = df_results.dropna(subset=['一人一日あたり排出量_g'])
ax3.plot(valid_data['年度'], valid_data['一人一日あたり排出量_g'], 'o-', linewidth=2, markersize=8, color='#F18F01')
ax3.set_title('1人1日あたりごみ排出量の推移', fontsize=16, fontweight='bold')
ax3.set_xlabel('年度', fontsize=12)
ax3.set_ylabel('排出量（g/人・日）', fontsize=12)
ax3.grid(True, alpha=0.3)
# x軸の目盛りを整数にする
ax3.set_xticks(valid_data['年度'].values)
ax3.set_xticklabels([f'{int(y)}' for y in valid_data['年度']], rotation=45)
for x, y in zip(valid_data['年度'], valid_data['一人一日あたり排出量_g']):
    if pd.notna(y):
        ax3.annotate(f'{y:.0f}', (x, y), textcoords="offset points", xytext=(0,5), ha='center', fontsize=9)

# 4. 最終処分量の推移
ax4 = plt.subplot(2, 3, 4)
valid_data = df_results.dropna(subset=['最終処分量_万トン'])
ax4.plot(valid_data['年度'], valid_data['最終処分量_万トン'], 'o-', linewidth=2, markersize=8, color='#C73E1D')
ax4.set_title('最終処分量の推移', fontsize=16, fontweight='bold')
ax4.set_xlabel('年度', fontsize=12)
ax4.set_ylabel('最終処分量（万トン）', fontsize=12)
ax4.grid(True, alpha=0.3)
# x軸の目盛りを整数にする
ax4.set_xticks(valid_data['年度'].values)
ax4.set_xticklabels([f'{int(y)}' for y in valid_data['年度']], rotation=45)
for x, y in zip(valid_data['年度'], valid_data['最終処分量_万トン']):
    if pd.notna(y):
        ax4.annotate(f'{y:.0f}', (x, y), textcoords="offset points", xytext=(0,5), ha='center', fontsize=9)

# 5. 処理方法別の推移（焼却・資源化）
ax5 = plt.subplot(2, 3, 5)
valid_inc = df_results.dropna(subset=['焼却処理量_万トン'])
valid_rec = df_results.dropna(subset=['直接資源化量_万トン'])
ax5.plot(valid_inc['年度'], valid_inc['焼却処理量_万トン'], 'o-', linewidth=2, markersize=8, color='#FF6B6B', label='焼却処理量')
ax5.plot(valid_rec['年度'], valid_rec['直接資源化量_万トン'], 's-', linewidth=2, markersize=8, color='#4ECDC4', label='直接資源化量')
ax5.set_title('処理方法別の推移', fontsize=16, fontweight='bold')
ax5.set_xlabel('年度', fontsize=12)
ax5.set_ylabel('処理量（万トン）', fontsize=12)
ax5.legend(loc='best', fontsize=11)
ax5.grid(True, alpha=0.3)
# x軸の目盛りを整数にする
if not valid_inc.empty:
    ax5.set_xticks(valid_inc['年度'].values)
    ax5.set_xticklabels([f'{int(y)}' for y in valid_inc['年度']], rotation=45)

# 6. 総合サマリー（複数指標の標準化比較）
ax6 = plt.subplot(2, 3, 6)
# データを標準化（2010年を100とする）
base_year = 2010
metrics = ['総排出量_万トン', '最終処分量_万トン', 'リサイクル率_%']
colors = ['#2E86AB', '#C73E1D', '#A23B72']
labels = ['総排出量', '最終処分量', 'リサイクル率']

for metric, color, label in zip(metrics, colors, labels):
    valid_data = df_results.dropna(subset=[metric])
    if not valid_data.empty:
        base_value = valid_data[valid_data['年度'] == base_year][metric].values
        if len(base_value) > 0:
            normalized = (valid_data[metric] / base_value[0]) * 100
            ax6.plot(valid_data['年度'], normalized, 'o-', linewidth=2, markersize=8, color=color, label=label)

ax6.set_title('主要指標の変化（2010年=100）', fontsize=16, fontweight='bold')
ax6.set_xlabel('年度', fontsize=12)
ax6.set_ylabel('指数（2010年=100）', fontsize=12)
ax6.axhline(y=100, color='gray', linestyle='--', alpha=0.5)
ax6.legend(loc='best', fontsize=11)
ax6.grid(True, alpha=0.3)
# x軸の目盛りを整数にする
if not df_results.empty:
    years_with_data = df_results['年度'].dropna().unique()
    ax6.set_xticks(years_with_data)
    ax6.set_xticklabels([f'{int(y)}' for y in years_with_data], rotation=45)

plt.suptitle('日本の廃棄物処理状況の推移（2010-2022年）', fontsize=20, fontweight='bold', y=1.02)
plt.tight_layout()

# 画像を保存
plt.savefig('waste_trends_overview.png', dpi=300, bbox_inches='tight')
print("\n画像を保存しました: waste_trends_overview.png")

# 個別のグラフも保存
# 1. 総排出量とリサイクル率の相関
fig2, ax = plt.subplots(figsize=(10, 6))
valid_data = df_results.dropna(subset=['総排出量_万トン', 'リサイクル率_%'])
ax2_twin = ax.twinx()
ax.plot(valid_data['年度'], valid_data['総排出量_万トン'], 'o-', linewidth=2, markersize=8, color='#2E86AB', label='総排出量')
ax2_twin.plot(valid_data['年度'], valid_data['リサイクル率_%'], 's-', linewidth=2, markersize=8, color='#A23B72', label='リサイクル率')
ax.set_xlabel('年度', fontsize=12)
ax.set_ylabel('総排出量（万トン）', fontsize=12, color='#2E86AB')
ax2_twin.set_ylabel('リサイクル率（%）', fontsize=12, color='#A23B72')
ax.tick_params(axis='y', labelcolor='#2E86AB')
ax2_twin.tick_params(axis='y', labelcolor='#A23B72')
plt.title('総排出量とリサイクル率の推移', fontsize=16, fontweight='bold')
ax.grid(True, alpha=0.3)
fig2.tight_layout()
plt.savefig('waste_vs_recycling.png', dpi=300, bbox_inches='tight')
print("画像を保存しました: waste_vs_recycling.png")

# 2. 処理方法の構成比推移
fig3, ax = plt.subplots(figsize=(12, 6))
valid_data = df_results.dropna(subset=['焼却処理量_万トン', '直接資源化量_万トン', '最終処分量_万トン'])
if not valid_data.empty:
    width = 0.6
    x = np.arange(len(valid_data))
    
    # スタックバーチャート
    p1 = ax.bar(valid_data['年度'], valid_data['焼却処理量_万トン'], width, label='焼却処理', color='#FF6B6B')
    p2 = ax.bar(valid_data['年度'], valid_data['直接資源化量_万トン'], width, 
                bottom=valid_data['焼却処理量_万トン'], label='直接資源化', color='#4ECDC4')
    p3 = ax.bar(valid_data['年度'], valid_data['最終処分量_万トン'], width,
                bottom=valid_data['焼却処理量_万トン'] + valid_data['直接資源化量_万トン'], 
                label='最終処分', color='#FFD93D')
    
    ax.set_ylabel('処理量（万トン）', fontsize=12)
    ax.set_xlabel('年度', fontsize=12)
    ax.set_title('廃棄物処理方法の構成推移', fontsize=16, fontweight='bold')
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
plt.tight_layout()
plt.savefig('waste_treatment_composition.png', dpi=300, bbox_inches='tight')
print("画像を保存しました: waste_treatment_composition.png")

# plt.show()

print("\n全ての可視化が完了しました！")