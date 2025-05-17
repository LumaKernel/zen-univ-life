indep_test_expmat <- function(obs) {
  n <- sum(obs)
  # E <- outer(rowSums(obs) / n, colSums(obs) / n) * n
  E <- outer(rowSums(obs) / n, colSums(obs) / n) * n
  E
}
indep_test_value <- function(obs) {
  E <- indep_test_expmat(obs)
  sum((obs - E) ** 2 / E)
}

obs <- matrix(c(36, 64, 44, 56), nrow=2)
indep_test_expmat(obs)[1][1]

# v <- indep_test_value(mat)
# qchisq(v, df = (2-1) * (2-1))
