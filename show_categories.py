import pandas as pd

df = pd.read_csv("customer_conversion_training_dataset.csv")

print("Gender:")
print(df["Gender"].unique())

print("\nLocation:")
print(df["Location"].unique())

print("\nLeadSource:")
print(df["LeadSource"].unique())

print("\nDeviceType:")
print(df["DeviceType"].unique())

print("\nReferralSource:")
print(df["ReferralSource"].unique())

print("\nPaymentHistory:")
print(df["PaymentHistory"].unique())