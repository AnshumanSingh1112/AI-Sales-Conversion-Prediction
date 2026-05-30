import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("customer_conversion_training_dataset.csv")

# Preprocessing
df = df.drop(["LeadID", "LeadStatus"], axis=1)
df = pd.get_dummies(df, drop_first=True)
df = df.astype(int)

X = df.drop("Conversion (Target)", axis=1)
y = df["Conversion (Target)"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train, y_train)

joblib.dump(rf_model, "rf_model.pkl")

print("Model saved successfully!")