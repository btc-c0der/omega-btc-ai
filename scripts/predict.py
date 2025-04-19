
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

from omega_ai import predict_btc_price

test_schumann = 8.2
prev_schumann = 8.1
prev_prev_schumann = 8.0
prev_btc = 38500  # Example previous BTC price
btc_change = -0.02  # Example BTC percentage change (-2%)

predicted_price = predict_btc_price(test_schumann, prev_schumann, prev_prev_schumann, prev_btc, btc_change)

if predicted_price:
    print(f"🔮 Updated AI Prediction for BTC Price at Schumann {test_schumann} Hz: ${predicted_price:.2f}")
else:
    print("⚠️ AI Prediction could not be made.")


import pickle
import pandas as pd

# Load the trained model
with open("data/xgboost_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Load the data (use latest Schumann data for prediction)
df = pd.read_csv("data/historical_data.csv")
latest_schumann = df["Schumann"].iloc[-1]
prev_schumann = df["Schumann"].iloc[-2]
prev_btc = df["BTC_Price"].iloc[-1]
btc_change = (df["BTC_Price"].iloc[-1] - df["BTC_Price"].iloc[-2]) / df["BTC_Price"].iloc[-2]

# Prepare the features for prediction
features = [latest_schumann, prev_schumann, prev_btc, btc_change]
predicted_btc = model.predict([features])[0]

print(f"🔮 Predicted BTC Price: ${predicted_btc:.2f}")
print(f"Features: {features}")
print(f"Number of Features: {len(features)}")
