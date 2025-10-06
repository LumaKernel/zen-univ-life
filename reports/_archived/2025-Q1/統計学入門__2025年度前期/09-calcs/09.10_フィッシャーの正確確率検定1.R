# クロス集計表の作成
tbl <- matrix(c(1, 4, 4, 1), nrow = 2, byrow = TRUE)
colnames(tbl) <- c("覚醒", "眠気")
rownames(tbl) <- c("Blend X", "Blend Y")

# フィッシャーの正確性検定
fisher.test(tbl)
