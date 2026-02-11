#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# グリッドの設定
N = 50
x = np.linspace(-1, 1, N)
y = np.linspace(-1, 1, N)
X, Y = np.meshgrid(x, y)

# 境界条件の設定（枠の形）
# 例: 馬の鞍（サドル）のような形状を作る境界
# z = x^2 - y^2 は調和関数の代表例です
Z = X**2 - Y**2

# グラフの描画
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# サーフェスのプロット
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, edgecolor='none')

# 境界（枠）を強調して描画
ax.plot(x, np.full_like(x, -1), x**2 - (-1)**2, color='red', linewidth=3, label='Boundary (Wire frame)')
ax.plot(x, np.full_like(x, 1), x**2 - (1)**2, color='red', linewidth=3)
ax.plot(np.full_like(y, -1), y, (-1)**2 - y**2, color='red', linewidth=3)
ax.plot(np.full_like(y, 1), y, (1)**2 - y**2, color='red', linewidth=3)

# 見た目の調整
ax.set_title("Visualization of Dirichlet's Principle\n(Harmonic Function: $z = x^2 - y^2$)", fontsize=14)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('u(x, y)')
fig.colorbar(surf, shrink=0.5, aspect=10)

plt.savefig('dirichlet.png', dpi=150, bbox_inches='tight')
print("Saved to dirichlet.png")
