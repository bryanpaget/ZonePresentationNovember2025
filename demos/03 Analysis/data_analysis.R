# R example for data analysis
library(ggplot2)
library(dplyr)
library(caret)

# Create sample data
set.seed(42)
n_samples <- 1000

data <- data.frame(
  feature1 = rnorm(n_samples, 0, 1),
  feature2 = rnorm(n_samples, 1, 2),
  feature3 = rexp(n_samples, 2),
  target = sample(0:1, n_samples, replace = TRUE, prob = c(0.7, 0.3))
)

# Data exploration
cat("Data Overview:\n")
print(summary(data))

cat("\nTarget distribution:\n")
print(table(data$target))

# Visualization
# Feature distributions
p1 <- ggplot(data, aes(x = feature1)) +
  geom_histogram(bins = 30, fill = "steelblue", alpha = 0.7) +
  ggtitle("Feature 1 Distribution")

p2 <- ggplot(data, aes(x = feature2)) +
  geom_histogram(bins = 30, fill = "darkorange", alpha = 0.7) +
  ggtitle("Feature 2 Distribution")

p3 <- ggplot(data, aes(x = feature3)) +
  geom_histogram(bins = 30, fill = "darkgreen", alpha = 0.7) +
  ggtitle("Feature 3 Distribution")

# Target distribution
p4 <- ggplot(data, aes(x = factor(target))) +
  geom_bar(fill = "purple", alpha = 0.7) +
  ggtitle("Target Distribution") +
  xlab("Target")

# Print plots
print(p1)
print(p2)
print(p3)
print(p4)

# Machine Learning
# Split data
train_index <- createDataPartition(data$target, p = 0.8, list = FALSE)
train_data <- data[train_index, ]
test_data <- data[-train_index, ]

# Train model
model <- train(
  factor(target) ~ feature1 + feature2 + feature3,
  data = train_data,
  method = "rf",
  trControl = trainControl(method = "cv", number = 5)
)

# Predictions
predictions <- predict(model, test_data)

# Evaluation
confusion_matrix <- confusionMatrix(predictions, factor(test_data$target))
print(confusion_matrix)

# Feature importance
importance <- varImp(model)
print(importance)
plot(importance, main = "Random Forest Feature Importance")
