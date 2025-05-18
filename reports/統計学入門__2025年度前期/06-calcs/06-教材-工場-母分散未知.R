dat <- scan("./06-calcs/工場.data.txt")
n <- length(dat)

# 母分散が未知なのでt分布
# Z = (avg - mu) / sqrt(S^2 / n)

# t分布の各種関数
# dt(density; pdf), pt(cdf), qt(quantile; cdfの逆関数), rt
# ..t(df = ...); df 自由度

alpha <- 0.05
# qt(alpha / 2) <= Z <= qt(1 - alpha / 2)
# Z = (avg - mu) / sqrt(S^2 / n)

# 不偏分散
avg <- mean(dat)
S_sq <- sum((dat - avg) ** 2) / (n-1)


# 上記を変形して…
c(
  avg - sqrt(S_sq / n) * qt(1 - alpha / 2, df = n - 1),
  # <= mu <=
  avg - sqrt(S_sq / n) * qt(alpha / 2, df = n - 1)
)
