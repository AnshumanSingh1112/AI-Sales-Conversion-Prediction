import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load data
df = pd.read_csv("customer_conversion_training_dataset.csv")

# Cleaning
df = df.drop(["LeadID", "LeadStatus"], axis=1)
df = pd.get_dummies(df, drop_first=True)
df = df.astype(int)

# Split
X = df.drop("Conversion (Target)", axis=1)
y = df["Conversion (Target)"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = LogisticRegression(max_iter=1000)

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))