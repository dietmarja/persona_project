# Load required libraries
library(psych)  # for Cronbach's alpha calculation
library(corrplot)  # for correlation plot

setwd("/Users/dietmar/Dropbox/PycharmProjects/persona2interviews/data/outputs/questionnaire")

# Toggle switch to control Cronbach's Alpha calculation
calculate_alpha <- TRUE  # Set to TRUE to calculate Cronbach's Alpha

# Function to process a single CSV file
process_csv <- function(file_path, calculate_alpha) {
  # Read the diversity data
  diversity_data <- read.csv(file_path)

  # Check if the required columns exist
  required_columns <- c("WT", "KS", "WV", "RW")
  if (!all(required_columns %in% colnames(diversity_data))) {
    warning(paste("File", file_path, "does not contain all required columns."))
    return(NULL)
  }

  # Check if all scores are 1
  all_scores_one <- all(diversity_data[, required_columns] == 1)
  if (all_scores_one) {
    overall_diversity <- 1
    cronbach_alpha <- if (calculate_alpha) NA else NULL  # Cronbach's alpha is not applicable in this case
    return(list(file_path = file_path, overall_diversity = overall_diversity, cronbach_alpha = cronbach_alpha))
  }

  # Calculate mean scores for each dimension
  mean_scores <- colMeans(diversity_data[, required_columns])

  # Calculate overall diversity score
  overall_diversity <- mean(mean_scores)

  # Calculate Cronbach's alpha with additional diagnostics if required
  if (calculate_alpha) {
    alpha_result <- tryCatch({
      psych::alpha(diversity_data[, required_columns], check.keys = TRUE)
    }, error = function(e) {
      warning(paste("Error calculating Cronbach's alpha for file", file_path, ":", e$message))
      return(NULL)
    })

    if (is.null(alpha_result)) {
      cronbach_alpha <- NA
    } else {
      cronbach_alpha <- alpha_result$total$raw_alpha
    }
  } else {
    cronbach_alpha <- NA  # Ensure cronbach_alpha is always a numeric value
  }

  # Return the results
  return(list(file_path = file_path, overall_diversity = overall_diversity, cronbach_alpha = cronbach_alpha))
}

# List of CSV files to process, filtering for files starting with "diversity"
csv_files <- list.files(pattern = "^diversity.*\\.csv$")

# Initialize an empty data frame to store results
results_df <- data.frame(file_path = character(), overall_diversity = numeric(), cronbach_alpha = numeric(), stringsAsFactors = FALSE)

# Process each CSV file and store the results
for (file in csv_files) {
  cat("Processing file:", file, "\n")
  result <- process_csv(file, calculate_alpha)
  if (!is.null(result)) {
    results_df <- rbind(results_df, as.data.frame(result, stringsAsFactors = FALSE))
  }
}

# Print the results data frame
print(results_df)

# Optionally, save the results to a CSV file
write.csv(results_df, "results.csv", row.names = FALSE)
