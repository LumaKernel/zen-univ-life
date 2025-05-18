# データの作成
group <- factor(c("A", "A", "B", "B", "C", "C"))
height <- c(10, 12, 14, 16, 18, 20)

# 群内平方和（SSW）の計算
ssw <- sum(tapply(height, group, function(x) sum((x - mean(x))^2)))
ssw
