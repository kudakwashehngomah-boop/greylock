import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load dataset (must contain: Amount, V1, V2, Class)
data = pd.read_csv("backend/model/creditcard.csv")

# Select features
X = data[["Amount", "V1", "V2"]]
y = data["Class"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "backend/model/fraud_model.pkl")

print("✅ Model trained and saved successfully.")