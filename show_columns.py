import pandas as pd

df = pd.read_csv("customer_conversion_training_dataset.csv")

df = df.drop(["LeadID", "LeadStatus"], axis=1)

df = pd.get_dummies(df, drop_first=True)

print(df.columns.tolist())