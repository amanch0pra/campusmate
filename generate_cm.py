import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, classification_report
import os
import re

# Load dataset
df = pd.read_csv('data/master_dataset.csv')

# Preprocessing (Simple version for metrics)
def preprocess(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

df['processed_question'] = df['Question'].apply(preprocess)

# Train-test split
tfidf = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
X = tfidf.fit_transform(df['processed_question'])
y = df['Mode']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = MultinomialNB()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Confusion Matrix
labels = sorted(df['Mode'].unique())
cm = confusion_matrix(y_test, y_pred, labels=labels)

# Plotting
plt.figure(figsize=(12, 10))
sns.set_theme(style="white")
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=labels, yticklabels=labels)
plt.title('Campus Mate - Classification Confusion Matrix', fontsize=16, pad=20)
plt.ylabel('Actual Category', fontsize=12)
plt.xlabel('Predicted Category', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()

# Save image
os.makedirs('static/metrics', exist_ok=True)
plt.savefig('static/metrics/confusion_matrix.png', dpi=300)
print("✓ Confusion matrix image saved to static/metrics/confusion_matrix.png")

# Generate Markdown Table
print("\n### Confusion Matrix Table\n")
header = "| Actual \\ Predicted | " + " | ".join(labels) + " |"
separator = "| " + "--- | " * (len(labels) + 1)
print(header)
print(separator)

for i, label in enumerate(labels):
    row = f"| **{label}** | " + " | ".join(map(str, cm[i])) + " |"
    print(row)

# Print Classification Report
print("\n### Classification Report\n")
report = classification_report(y_test, y_pred, target_names=labels)
print("```")
print(report)
print("```")
