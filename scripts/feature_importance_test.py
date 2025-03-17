import pandas as pd
import pickle
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load the final trained model (ensure the path is correct)
model_path = "data/omega_model.pkl"  # Ensure it's pointing to the correct model file
with open(model_path, "rb") as model_file:
    model = pickle.load(model_file)

# Load the dataset
file_path = "data/historical_data.csv"
df = pd.read_csv(file_path)

# Feature Engineering (same as training)
df["Schumann_Lag1"] = df["Schumann"].shift(1)
df["Schumann_Lag2"] = df["Schumann"].shift(2)
df["BTC_Lag1"] = df["BTC_Price"].shift(1)  # Add missing BTC_Lag1 feature
df["BTC_Change"] = df["BTC_Price"].pct_change()

# Drop NaN values
df.dropna(inplace=True)  # Drop rows with NaN values

# Prepare dataset for testing (ensure features match model training)
features = ["Schumann", "Schumann_Lag1", "Schumann_Lag2", "BTC_Lag1", "BTC_Change"]  # Include BTC_Lag1 here
X = df[features].values
y = df["BTC_Price"].values

# Split into training & test sets
_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Run feature importance test
results = permutation_importance(model, X_test, y_test, scoring='neg_mean_absolute_error')

# Print Feature Importance
print("📊 Feature Importance:")
for feature, importance in zip(features, results.importances_mean):
    print(f"{feature}: {importance:.5f}")





