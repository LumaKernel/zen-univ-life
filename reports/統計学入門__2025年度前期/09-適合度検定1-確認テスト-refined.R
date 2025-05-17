# By DeepSeek's hint

# 観測データ
observed <- c(306, 94)  # 黄色: 306個, 白色: 94個

# 期待比率 (3:1)
expected_ratio <- c(3, 1)
expected_prop <- expected_ratio / sum(expected_ratio)

# 期待値を計算 (総数400個)
expected <- expected_prop * sum(observed)

# カイ二乗統計量を計算
chi_sq <- sum((observed - expected) ** 2 / expected)

# 結果を表示
chi_sq


# 臨界値の計算（上側5%点）
critical_value <- qchisq(0.95, df = 1)
critical_value  # 出力: 3.841459
# dchisq が pdf
# pchisq が cdf
# qchisq が cdf の逆関数



