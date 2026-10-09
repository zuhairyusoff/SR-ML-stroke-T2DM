# Verification of the pooled C-statistics in R (metafor).
# Reads the data directly from this GitHub repository.
# Verified on R 4.5.2 with metafor 5.2-1: reproduces the Python pooled estimates
# (NewReg 0.704, ML 0.782, RECODe 0.684, UKPDS_RE 0.658, UKPDS_OM2 0.624).

library(metafor)   # install.packages("metafor") if not yet installed

url <- "https://raw.githubusercontent.com/zuhairyusoff/SR-ML-stroke-T2DM/main/data/ma_data_with_se.csv"
d <- read.csv(url)

res <- data.frame()
for (g in c("NewReg", "ML", "RECODe", "UKPDS_RE", "UKPDS_OM2")) {
  s <- subset(d, group == g)
  m <- rma(yi = y, sei = se, data = s, method = "REML", test = "knha")
  p <- predict(m, transf = transf.ilogit)
  res <- rbind(res, data.frame(group = g, k = m$k,
                               C = round(p$pred, 3), lo = round(p$ci.lb, 3), hi = round(p$ci.ub, 3),
                               I2 = round(m$I2, 1)))
}
print(res, row.names = FALSE)
cat("R", R.version$major, ".", R.version$minor, " | metafor ", as.character(packageVersion("metafor")), "\n", sep = "")
