import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import matplotlib.pyplot as plt
import numpy as np

# Model to test
model = joblib.load('v1/lr_model_v1.joblib')
vectorizer = joblib.load('v1/vectorizer_v1.joblib')

# Load the dataset
data = pd.read_csv('data/Ling.csv')

x = data['subject'].fillna('').str.lower() + ' ' + data['body'].fillna('').str.lower()
y = data['label']

# Convert text to features
X_tfidf = vectorizer.transform(x)
# Make predictions
y_pred = model.predict(X_tfidf)
print(classification_report(y, y_pred, target_names=["legit", "phishing"]))
cm = confusion_matrix(y, y_pred)
print(cm)

# Plot the models performance
labels = ["Legit", "Phishing"]

fig, ax = plt.subplots()
im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
ax.figure.colorbar(im, ax=ax)

# Labels, titles, and ticks
ax.set(
    xticks=np.arange(len(labels)),
    yticks=np.arange(len(labels)),
    xticklabels=labels,
    yticklabels=labels,
    ylabel="True label",
    xlabel="Predicted label",
    title="Confusion Matrix"
)

# Add text annotations
fmt = 'd'
thresh = cm.max() / 2.
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        ax.text(j, i, format(cm[i, j], fmt),
                ha="center", va="center",
                color="white" if cm[i, j] > thresh else "black")

plt.show()