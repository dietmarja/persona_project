# Load required libraries
library(psych)  # for Cronbach's alpha calculation



setwd("/Users/dietmar/Dropbox/PycharmProjects/persona2interviews/data/outputs/questionnaire")

# Read the diversity data
diversity_data <- read.csv("diversity.csv")


# Calculate mean scores for each dimension
mean_scores <- colMeans(diversity_data[, c("WT", "KS", "WV", "RW")])

# Calculate overall diversity score
overall_diversity <- mean(mean_scores)

# szenischen Erzaehlen
#overall_diversity_first <- overall_diversity

# Print basic statistics
cat("Mean scores for each dimension:\n")
print(mean_scores)
cat("\nOverall diversity score:", overall_diversity, "\n")

# Check for items with no variance
no_variance <- sapply(diversity_data[, c("WT", "KS", "WV", "RW")], var) == 0
if(any(no_variance)) {
  cat("\nWarning: The following items have no variance and may cause issues in analysis:\n")
  print(names(no_variance)[no_variance])
}

# Calculate and plot correlation matrix
cor_matrix <- cor(diversity_data[, c("WT", "KS", "WV", "RW")])
cat("\nCorrelation matrix:\n")
print(cor_matrix)

png("correlation_plot.png")
corrplot(cor_matrix, method = "color", type = "upper", order = "hclust", 
         addCoef.col = "black", tl.col = "black", tl.srt = 45, 
         diag = FALSE)
dev.off()

# Calculate Cronbach's alpha with additional diagnostics
alpha_result <- psych::alpha(diversity_data[, c("WT", "KS", "WV", "RW")], check.keys = TRUE)
cat("\nCronbach's alpha:", alpha_result$total$raw_alpha, "\n")
cat("\nCronbach's alpha if item deleted:\n")
print(alpha_result$alpha.drop)

# Calculate within-group agreement (rwg)
calculate_rwg <- function(data) {
  variance <- var(data)
  s2_eu <- ((7-1)^2) / 12  # Uniform distribution variance for 7-point scale
  1 - (variance / s2_eu)
}

rwg_values <- sapply(diversity_data[, c("WT", "KS", "WV", "RW")], calculate_rwg)
cat("\nrwg values for each dimension:\n")
print(rwg_values)
cat("\nMedian rwg:", median(rwg_values), "\n")

# Calculate and print standard deviation for each dimension
sd_scores <- sapply(diversity_data[, c("WT", "KS", "WV", "RW")], sd)
cat("\nStandard deviation for each dimension:\n")
print(sd_scores)
