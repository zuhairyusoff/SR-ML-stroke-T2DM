# Optional verification in R (metafor). Reproduces the Python analysis.
library(metafor)
d <- read.csv("../data/ma_data_with_se.csv")
for (g in unique(d$group)) {
  s <- subset(d, group == g)
  m <- rma(yi = y, sei = se, data = s, method = "REML", test = "knha")
  cat("\n==", g, "==\n"); print(predict(m, transf = transf.ilogit))
  forest(m, transf = transf.ilogit, slab = s$label, xlab = "C statistic", main = g)
}
