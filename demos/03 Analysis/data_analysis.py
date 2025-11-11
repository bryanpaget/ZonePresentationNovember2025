import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Create sample data
np.random.seed(42)
n_samples = 1000

data = pd.DataFrame({
    'feature1': np.random.normal(0, 1, n_samples),
    'feature2': np.random.normal(1, 2, n_samples),
    'feature3': np.random.exponential(2, n_samples),
    'target': np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
})

# Data exploration
print("Data Overview:")
print(data.describe())
print(f"\nTarget distribution:\n{data['target'].value_counts()}")

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Distribution of features
data[['feature1', 'feature2', 'feature3']].hist(ax=axes[0, :], bins=20)
axes[0, 0].set_title('Feature 1 Distribution')
axes[0, 1].set_title('Feature 2 Distribution')
axes[0, 2].set_title('Feature 3 Distribution')

# Correlation heatmap
corr_matrix = data.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=axes[1, 0])
axes[1, 0].set_title('Correlation Matrix')

# Target distribution
data['target'].value_counts().plot(kind='bar', ax=axes[1, 1])
axes[1, 1].set_title('Target Distribution')

plt.tight_layout()
plt.show()

# Machine Learning
X = data[['feature1', 'feature2', 'feature3']]
y = data['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
print(feature_importance)

# Plot feature importance
plt.figure(figsize=(10, 6))
sns.barplot(data=feature_importance, x='importance', y='feature')
plt.title('Random Forest Feature Importance')
plt.tight_layout()
plt.show()
