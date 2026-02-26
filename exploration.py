import pandas as pd

# Load dataset
df = pd.read_csv("creditcard.csv")

print("Dataset Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

print("\nClass Distribution:")
print(df["Class"].value_counts())

print("\nFraud Percentage:")
fraud_percentage = (df["Class"].sum() / len(df)) * 100
print(f"{fraud_percentage:.4f}% Fraud Transactions")