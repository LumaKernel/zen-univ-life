indep_test_expmat <- function(obs) {
  n <- sum(obs)
  # E <- outer(rowSums(obs) / n, colSums(obs) / n) * n
  # 下のようにも書き換えられる
  E <- outer(rowSums(obs), colSums(obs)) / n
  E
}
indep_test_value <- function(obs) {
  E <- indep_test_expmat(obs)
  sum((obs - E) ** 2 / E)
}

obs <- matrix(c(36, 64, 44, 56), nrow=2)

# 確認テストの 期待度数
indep_test_expmat(obs)[1][1] # 40

# p値も出してみる
v <- indep_test_value(obs)
pchisq(v, df = (2-1) * (2-1), lower.tail = FALSE) # 0.2482131
