import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import numpy as np



# Load the dataset
data = pd.read_csv('data/SpamAssasin.csv')
# Only want ones that have at least subject and body
data.dropna(subset=['subject', 'body'], inplace=True)
data.drop_duplicates(inplace=True)

# What are all the fields we have?
print("Columns in dataset:", data.columns.tolist())
# How many samples do we have?
print("Number of samples:", len(data))
print(data['label'].value_counts())

# Start normalizing the data
# Fill NaN values with empty strings and lowercase everything
data['sender'] = data['sender'].fillna('').str.lower()
data['receiver'] = data['receiver'].fillna('').str.lower()
data['subject'] = data['subject'].fillna('').str.lower()
data['body'] = data['body'].fillna('').str.lower()
data['urls'] = data['urls'].fillna('').astype(str)

# Define features and labels
x = data['sender'] + ' ' + data['receiver'] + ' ' + data['subject'] + ' ' + data['body'] + ' ' + data['urls']
y = data['label']

# Reserve 20% of data for testing, stratified by label
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=1, stratify=y
)

# Convert text to features
vectorizer = TfidfVectorizer(
    stop_words='english', max_features=5000, ngram_range=(1,2)
)

# Train the model
X_train_tfidf = vectorizer.fit_transform(x_train)
X_test_tfidf = vectorizer.transform(x_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# Evaluate the model
y_pred = model.predict(X_test_tfidf)
print(classification_report(y_test, y_pred, target_names=["legit", "phishing"]))
cm = confusion_matrix(y_test, y_pred)
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

# Save the model and vectorizer
joblib.dump(model, 'v1/lr_model_v1.joblib')
joblib.dump(vectorizer, 'v1/vectorizer_v1.joblib')