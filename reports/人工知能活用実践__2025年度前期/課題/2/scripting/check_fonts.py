#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.font_manager as fm

# 利用可能なフォントを確認
fonts = fm.findSystemFonts()
japanese_fonts = []

for font_path in fonts:
    try:
        font_prop = fm.FontProperties(fname=font_path)
        font_name = font_prop.get_name()
        # 日本語フォントらしいものを探す
        if any(keyword in font_name.lower() for keyword in ['hira', 'japan', 'osaka', 'gothic', 'mincho', 'sans gb']):
            japanese_fonts.append((font_name, font_path))
    except:
        pass

print("利用可能な日本語フォント:")
for name, path in sorted(set(japanese_fonts)):
    print(f"  {name}: {path}")

# 推奨フォント
print("\n推奨フォント:")
if japanese_fonts:
    print(f"  使用する: {japanese_fonts[0][0]}")