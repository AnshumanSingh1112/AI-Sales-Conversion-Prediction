import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
import joblib

print("SMOTE TRAINING RUNNING")

# Load dataset
df = pd.read_csv("customer_conversion_training_dataset.csv")

# Preprocessing
df = df.drop(["LeadID", "LeadStatus"], axis=1)
df = pd.get_dummies(df, drop_first=True)
df = df.astype(int)

# Features and Target
X = df.drop("Conversion (Target)", axis=1)
y = df["Conversion (Target)"]

print("\nBefore SMOTE:")
print(y.value_counts())

# Apply SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

print("\nAfter SMOTE:")
print(y_resampled.value_counts())

# Train-Test Split using balanced data
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled,
    y_resampled,
    test_size=0.2,
    random_state=42
)

# Random Forest Model
rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train Model
rf_model.fit(X_train, y_train)

# Predictions
y_pred = rf_model.predict(X_test)

# Classification Report
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# Save Model
joblib.dump(rf_model, "rf_model.pkl")

print("\nModel saved successfully!")