# Python equivalent of the SAS analysis
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Equivalent to SAS data step
np.random.seed(42)
n_samples = 1000

data = pd.DataFrame({
    'feature1': np.random.normal(0, 1, n_samples),
    'feature2': np.random.normal(1, 2, n_samples),
    'feature3': np.random.exponential(2, n_samples),
    'target': np.random.binomial(1, 0.3, n_samples)
})

# Equivalent to PROC MEANS
print("Descriptive Statistics (PROC MEANS equivalent):")
print(data[['feature1', 'feature2', 'feature3']].describe())

# Equivalent to PROC FREQ
print("\nTarget Frequency (PROC FREQ equivalent):")
print(data['target'].value_counts())

# Equivalent to SAS visualization with matplotlib
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Feature distributions with density
for i, feature in enumerate(['feature1', 'feature2', 'feature3']):
    axes[i].hist(data[feature], bins=30, alpha=0.7, density=True)
    data[feature].plot.density(ax=axes[i], color='red')
    axes[i].set_title(f'{feature} Distribution')

plt.tight_layout()
plt.show()

# Equivalent to PROC HPSPLIT
X = data[['feature1', 'feature2', 'feature3']]
y = data['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Random Forest (similar to decision tree in SAS)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Equivalent to SAS output and PROC FREQ for evaluation
print("\nModel Evaluation:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Confusion matrix equivalent
from sklearn.metrics import confusion_matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix (equivalent to SAS output):")
print(conf_matrix)
