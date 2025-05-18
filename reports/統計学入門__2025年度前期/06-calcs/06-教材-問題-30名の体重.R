dat <- scan("./06-calcs/30人の体重.data.txt")
# プロットして外観する
# plot(dat)

n <- length(dat)
# 身長の推定 (不偏推定)
sum(dat) / length(dat)

# 95%信頼区間

## 分散が分かっているとき
sd_sq <- 16

## avg(dat) ~ N(μ, σ^2 / n)
# 95%信頼区間
# qnorm(0.05 / 2, lower.tail = FALSE) # [1] 1.959964
# σ/√n
c(mean(dat) - 1.96 * (sqrt(sd_sq / n)), mean(dat) + 1.96 * (sqrt(sd_sq / n)))
