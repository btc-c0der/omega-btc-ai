
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

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error
import os
import pickle  # For saving the trained model
import xgboost as xgb  # Ensure XGBoost is imported
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from mpl_toolkits.mplot3d import Axes3D

def train_ai():
    """Train AI model on historical Schumann & BTC data with additional features."""
    
    file_path = "data/historical_data.csv"
    if not os.path.exists(file_path):
        print("❌ Missing merged data file! Run `merge_data.py` first.")
        return None

    data = pd.read_csv(file_path)

    if len(data) < 10:  # Ensure enough data for training
        print("⚠️ Not enough data to train AI model.")
        return None

    print("✅ Sufficient data available, training AI model with additional features...")

    # Convert Timestamp to datetime
    data["Timestamp"] = pd.to_datetime(data["Timestamp"])

    # Feature Engineering
    data["Schumann_Lag1"] = data["Schumann"].shift(1)  # Previous Schumann value
    data["Schumann_Lag2"] = data["Schumann"].shift(2)  # Two-time-step lag
    data["BTC_Lag1"] = data["BTC_Price"].shift(1)  # Previous BTC price
    data["BTC_Change"] = data["BTC_Price"].pct_change()  # BTC price percentage change

    # Drop NaN values from lagging
    data.dropna(inplace=True)

    # Prepare dataset for training
    features = ["Schumann", "Schumann_Lag1", "Schumann_Lag2", "BTC_Lag1", "BTC_Change"]
    X = data[features].values  # Input features
    y = data["BTC_Price"].values  # Output: BTC Close Price

    # Split data into training & testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate model performance
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"✅ Model trained with extra features! Mean Absolute Error: {mae:.2f}")

    # Save the trained model for real-time predictions
    with open("data/omega_model.pkl", "wb") as model_file:
        pickle.dump(model, model_file)
    print("✅ Updated AI model saved with new features!")

    return model

def calculate_fibonacci_levels(df):
    """Calculate Fibonacci retracement levels for the BTC price."""
    
    # Define high and low for the period
    period_low = df["BTC_Price"].min()
    period_high = df["BTC_Price"].max()

    # Calculate Fibonacci retracement levels
    diff = period_high - period_low
    fib_levels = {
        "23.6%": period_high - 0.236 * diff,
        "38.2%": period_high - 0.382 * diff,
        "50%": period_high - 0.5 * diff,
        "61.8%": period_high - 0.618 * diff,
        "100%": period_low,
    }

    return fib_levels

def enhance_features_with_fibo(df):
    """Add Fibonacci levels as features to the dataset."""
    
    fib_levels = calculate_fibonacci_levels(df)
    
    # Adding Fibonacci levels to the dataframe
    df["Fib_23_6"] = fib_levels["23.6%"]
    df["Fib_38_2"] = fib_levels["38.2%"]
    df["Fib_50"] = fib_levels["50%"]
    df["Fib_61_8"] = fib_levels["61.8%"]
    df["Fib_100"] = fib_levels["100%"]
    
    return df

def plot_btc_with_fibo(df, fib_levels):
    """Plot BTC Price with Fibonacci levels."""
    
    plt.figure(figsize=(12,6))
    plt.plot(df["Timestamp"], df["BTC_Price"], label="BTC Price", color='blue')

    # Plot Fibonacci levels as horizontal lines
    for level, price in fib_levels.items():
        plt.axhline(price, color='r', linestyle='--', label=f"Fibonacci {level}: {price:.2f}")

    plt.title("BTC Price with Fibonacci Retracement Levels")
    plt.xlabel("Time")
    plt.ylabel("BTC Price (USD)")
    plt.legend()
    plt.show()

def predict_btc_price(schumann_value, prev_schumann, prev_prev_schumann, prev_btc, btc_change):
    """Predict BTC price using enhanced AI model with additional inputs."""
    try:
        with open("data/omega_model.pkl", "rb") as model_file:
            model = pickle.load(model_file)  # Load trained model
        return model.predict([[schumann_value, prev_schumann, prev_prev_schumann, prev_btc, btc_change]])[0]
    except FileNotFoundError:
        print("⚠️ AI Model is not trained yet! Cannot make predictions.")
        return None
    
def detect_mm_trap(schumann_value, btc_price, prev_btc):
    """
    Detects Market Maker (MM) manipulation based on Schumann Resonance and BTC price action.
    
    Arguments:
    - schumann_value: Current Schumann Resonance value (Hz)
    - btc_price: Current Bitcoin price (USD)
    - prev_btc: Previous Bitcoin price (USD)
    
    Returns:
    - A string alert message indicating whether MM suppression is detected.
    """
    
    # Define thresholds for MM detection
    schumann_threshold = 10  # Schumann value threshold to indicate a potential MM manipulation
    price_drop_threshold = -0.02  # A 2% drop in BTC price could indicate MM manipulation (fakeout, stop hunt)
    
    # Calculate the percentage change in BTC price
    price_change = (btc_price - prev_btc) / prev_btc
    
    # Market Maker suppression detection logic
    if schumann_value > schumann_threshold and price_change < price_drop_threshold:
        return f"⚠️ MM SUPPRESSION DETECTED! BTC dropped {price_change:.2%} after Schumann spike {schumann_value} Hz!"
    
    return "✅ No MM suppression detected."

def train_xgboost_model():
    # Load data
    df = pd.read_csv("data/historical_data.csv")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Feature Engineering (same as before)
    df = enhance_features(df)

    # df["Schumann_Lag1"] = df["Schumann"].shift(1)
    # df["Schumann_Lag2"] = df["Schumann"].shift(2)
    # df["BTC_Lag1"] = df["BTC_Price"].shift(1)
    # df["BTC_Change"] = df["BTC_Price"].pct_change()
    # df.dropna(inplace=True)

    # Prepare dataset
    features = ["Schumann", "Schumann_Lag1", "Schumann_Lag2", "BTC_Lag1", "BTC_Change"]
    X = df[features].values
    y = df["BTC_Price"].values

    # Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define XGBoost model
    model = xgb.XGBRegressor(objective='reg:squarederror')

    # Define parameter grid for GridSearchCV
    param_grid = {
        'learning_rate': [0.01, 0.1, 0.2],  # Learning rate
        'max_depth': [3, 6, 10],  # Max depth of trees
        'n_estimators': [100, 200, 500],  # Number of estimators (trees)
        'subsample': [0.6, 0.8, 1.0],  # Fraction of samples used for training
        'colsample_bytree': [0.6, 0.8, 1.0]  # Fraction of features used for each tree
    }

    # Perform grid search with cross-validation
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='neg_mean_absolute_error', verbose=1)
    grid_search.fit(X_train, y_train)

    # Output best parameters
    print(f"Best parameters found: {grid_search.best_params_}")

    # Evaluate the best model from GridSearchCV
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Optimized MAE for XGBoost: {mae:.2f}")

    # Save the optimized model
    with open("data/xgboost_model_optimized.pkl", "wb") as model_file:
        pickle.dump(best_model, model_file)
    print("✅ XGBoost model trained and optimized with GridSearchCV!")

    return best_model

def add_rsi(df):
    """Add RSI (Relative Strength Index) to the dataframe."""
    df["RSI"] = talib.RSI(df["BTC_Price"], timeperiod=14)  # 14-period RSI
    return df

def calculate_rsi(df, period=14):
    """Manually calculates the Relative Strength Index (RSI) without TA-Lib."""
    delta = df["BTC_Price"].diff(1)  # Calculate price changes
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()  # Avg. gain
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()  # Avg. loss
    rs = gain / loss  # Relative Strength
    df["RSI"] = 100 - (100 / (1 + rs))  # Compute RSI
    df["RSI"].fillna(50, inplace=True)  # Fill NaN values with neutral RSI (50)
    return df

def add_bollinger_bands(df):
    """Add Bollinger Bands to the dataframe."""
    
    # Ensure data is sorted by time
    df = df.sort_values(by="Timestamp", ascending=True)

    # Ensure we have at least 20 rows to compute rolling indicators
    if len(df) < 20:
        print("⚠️ Not enough data to calculate Bollinger Bands!")
        df["UpperBand"] = df["BTC_Price"]  # Assign BTC Price as fallback
        df["LowerBand"] = df["BTC_Price"]
        return df

    # Compute Bollinger Bands
    df["MA20"] = df["BTC_Price"].rolling(window=20, min_periods=1).mean()
    df["UpperBand"] = df["MA20"] + 2 * df["BTC_Price"].rolling(window=20, min_periods=1).std()
    df["LowerBand"] = df["MA20"] - 2 * df["BTC_Price"].rolling(window=20, min_periods=1).std()

    # Fill missing values to avoid plotting errors
    df["UpperBand"].fillna(method="bfill", inplace=True)
    df["LowerBand"].fillna(method="bfill", inplace=True)

    return df

def add_fibonacci_levels(df):
    """Add Fibonacci levels to the dataframe."""
    fib_levels = calculate_fibonacci_levels(df)
    
    # Adding Fibonacci levels to the dataframe
    df["Fib_23_6"] = fib_levels["23.6%"]
    df["Fib_38_2"] = fib_levels["38.2%"]
    df["Fib_50"] = fib_levels["50%"]
    df["Fib_61_8"] = fib_levels["61.8%"]
    df["Fib_100"] = fib_levels["100%"]
    
    return df

def enhance_features(df):
    """Enhance features with advanced technical indicators without TA-Lib."""
    
    # Calculate RSI manually
    df = calculate_rsi(df)  # New RSI function
    
    df = add_bollinger_bands(df)  # Add Bollinger Bands
    
    # Add Bollinger Bands
    df["MA20"] = df["BTC_Price"].rolling(window=20).mean()
    df["UpperBand"] = df["MA20"] + 2 * df["BTC_Price"].rolling(window=20).std()
    df["LowerBand"] = df["MA20"] - 2 * df["BTC_Price"].rolling(window=20).std()

    # Add Fibonacci Levels
    df = add_fibonacci_levels(df)
    
    # Feature Engineering
    df["Schumann_Lag1"] = df["Schumann"].shift(1)
    df["Schumann_Lag2"] = df["Schumann"].shift(2)
    df["BTC_Lag1"] = df["BTC_Price"].shift(1)
    df["BTC_Change"] = df["BTC_Price"].pct_change()
    
    df.dropna(inplace=True)  # Drop NaN values
    
    return df

def calculate_rsi(df, period=14):
    """Manually calculates the Relative Strength Index (RSI) without TA-Lib."""
    
    delta = df["BTC_Price"].diff(1)  # Calculate price changes
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()  # Avg. gain
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()  # Avg. loss
    
    rs = gain / loss  # Relative Strength
    df["RSI"] = 100 - (100 / (1 + rs))  # Compute RSI
    
    # Replace the old line with:
    df["RSI"] = df["RSI"].fillna(50)  # Assign the result back to df["RSI"]

    return df

def fibonacci_levels(df):
    """Calculate Fibonacci retracement levels for BTC price."""
    high = df["BTC_Price"].max()
    low = df["BTC_Price"].min()
    diff = high - low

    fib_levels = {
        '23.6%': high - 0.236 * diff,
        '38.2%': high - 0.382 * diff,
        '50%': high - 0.5 * diff,
        '61.8%': high - 0.618 * diff,
        '100%': low,
    }

    return fib_levels

def enhance_with_geometric_features(df):
    """Enhance features with Fibonacci levels, RSI, Bollinger Bands, and Schumann lags."""
    
    try:
        # ✅ Step 1: Calculate Fibonacci levels & Apply to DataFrame
        fib_levels = fibonacci_levels(df)

        # Convert Fibonacci scalar values into full-length columns
        for level_name, level_value in fib_levels.items():
            df[level_name] = level_value if isinstance(level_value, (int, float)) else np.nan
        
        # ✅ Step 2: Compute RSI & Handle Missing Values
        df["RSI"] = calculate_rsi(df)
        df["RSI"].fillna(50, inplace=True)  # Fill missing RSI values with neutral (50)
        
        # ✅ Step 3: Compute Bollinger Bands & Ensure Full-Length
        df = add_bollinger_bands(df)
        if "UpperBand" in df.columns and "LowerBand" in df.columns:
            df["UpperBand"].fillna(method="bfill", inplace=True)
            df["LowerBand"].fillna(method="bfill", inplace=True)
        else:
            print("⚠️ Warning: Bollinger Bands not properly computed. Check data.")

        # ✅ Step 4: Feature Engineering (Schumann & BTC)
        if "Schumann" in df.columns:
            df["Schumann_Lag1"] = df["Schumann"].shift(1)
            df["Schumann_Lag2"] = df["Schumann"].shift(2)
            df["Schumann_Lag1"].fillna(df["Schumann"].median(), inplace=True)
            df["Schumann_Lag2"].fillna(df["Schumann"].median(), inplace=True)
            print("✅ Schumann data detected. Including in visualization.")
        else:
            print("⚠️ Warning: 'Schumann' column missing! Skipping Schumann-based features.")

        # ✅ Step 5: Compute BTC Price Lag Features & Fill Missing Values
        df["BTC_Lag1"] = df["BTC_Price"].shift(1)
        df["BTC_Change"] = df["BTC_Price"].pct_change()
        df["BTC_Lag1"].fillna(df["BTC_Price"].median(), inplace=True)
        df["BTC_Change"].fillna(0, inplace=True)  # No change if missing first row

        # ✅ Step 6: Volume Handling (Optional)
        if "Volume" not in df.columns:
            print("⚠️ Warning: 'Volume' column missing! Plotting only BTC price vs time.")

        # ✅ Step 7: Drop any remaining NaN values
        df.dropna(inplace=True)

    except Exception as e:
        print(f"⚠️ Warning: Issue while enhancing features: {e}")
        print("⚠️ Proceeding with the raw data.")
    
    return df
    """Enhance features with Fibonacci levels, RSI, Bollinger Bands, and Schumann lags."""
    
    try:
        # ✅ Step 1: Calculate Fibonacci levels & Apply to DataFrame
        fib_levels = fibonacci_levels(df)

        # Convert Fibonacci scalar values into full-length columns
        for level_name, level_value in fib_levels.items():
            df[level_name] = df["BTC_Price"].apply(lambda x: level_value)  

        # ✅ Step 2: Compute RSI & Handle Missing Values
        df["RSI"] = calculate_rsi(df)
        df["RSI"].fillna(50, inplace=True)  # Fill missing RSI values with neutral (50)
        
        # ✅ Step 3: Compute Bollinger Bands & Handle Missing Values
        df = add_bollinger_bands(df)
        if "UpperBand" in df.columns and "LowerBand" in df.columns:
            df["UpperBand"].fillna(method="bfill", inplace=True)
            df["LowerBand"].fillna(method="bfill", inplace=True)
        else:
            print("⚠️ Warning: Bollinger Bands not properly computed. Check data.")

        # ✅ Step 4: Feature Engineering (Schumann & BTC)
        if "Schumann" in df.columns:
            df["Schumann_Lag1"] = df["Schumann"].shift(1)
            df["Schumann_Lag2"] = df["Schumann"].shift(2)
            df["Schumann_Lag1"].fillna(df["Schumann"].median(), inplace=True)
            df["Schumann_Lag2"].fillna(df["Schumann"].median(), inplace=True)
            print("✅ Schumann data detected. Including in visualization.")
        else:
            print("⚠️ Warning: 'Schumann' column missing! Skipping Schumann-based features.")

        # ✅ Step 5: Compute BTC Price Lag Features & Fill Missing Values
        df["BTC_Lag1"] = df["BTC_Price"].shift(1)
        df["BTC_Change"] = df["BTC_Price"].pct_change()
        df["BTC_Lag1"].fillna(df["BTC_Price"].median(), inplace=True)
        df["BTC_Change"].fillna(0, inplace=True)  # No change if missing first row

        # ✅ Step 6: Volume Handling (Optional)
        if "Volume" not in df.columns:
            print("⚠️ Warning: 'Volume' column missing! Plotting only BTC price vs time.")

        # ✅ Step 7: Drop any remaining NaN values
        df.dropna(inplace=True)

    except Exception as e:
        print(f"⚠️ Warning: Issue while enhancing features: {e}")
        print("⚠️ Proceeding with the raw data.")
    
    return df

def train_enhanced_model():
    df = pd.read_csv("data/historical_data.csv")
    
    # Enhance features with geometric patterns and Fibonacci levels
    df = enhance_with_geometric_features(df)
    
    # Prepare dataset for training
    features = ["Schumann", "Schumann_Lag1", "Schumann_Lag2", "BTC_Lag1", "BTC_Change", "Fib_23_6", "Fib_38_2", "Fib_50", "Fib_61_8", "Fib_100"]
    X = df[features].values
    y = df["BTC_Price"].values
    
    # Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train XGBoost model
    model = xgb.XGBRegressor(objective='reg:squarederror')
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Optimized MAE for XGBoost with geometric and Fibonacci features: {mae:.2f}")
    
    # Save the model
    with open("data/xgboost_model_with_geometric_features.pkl", "wb") as model_file:
        pickle.dump(model, model_file)

    print("✅ Model trained and saved with enhanced geometric features!")
    return model

def generate_valid_liquidity_points():
    """Generate valid liquidity points that are non-collinear."""
    # Generate random points for price and volume
    liquidity_points = np.random.rand(5, 2) * [10, 500]  # Generate 5 points, with prices between 0 and 10, volume between 0 and 500
    
    # Ensure that points are not collinear
    while is_collinear(liquidity_points):
        liquidity_points = np.random.rand(5, 2) * [10, 500]  # Regenerate if collinear

    return liquidity_points

def is_collinear(points):
    """Check if the points are collinear."""
    # Check if the points form a flat line using the area of the triangle they create
    p1, p2, p3 = points[0], points[1], points[2]
    area = 0.5 * abs(
        p1[0] * (p2[1] - p3[1]) +
        p2[0] * (p3[1] - p1[1]) +
        p3[0] * (p1[1] - p2[1])
    )
    return area == 0

# def plot_voronoi(liquidity_points):
    """Generate and plot the Voronoi diagram."""
    vor = Voronoi(liquidity_points)
    
    # Plot the Voronoi tessellation
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange', line_width=2)
    
    # Plot the liquidity points with labels
    for i, point in enumerate(liquidity_points):
        ax.scatter(point[0], point[1], color='blue', zorder=5)
        ax.text(point[0] + 0.1, point[1] + 10, f"Price: {point[0]:.2f}\nVolume: {point[1]:.2f}", fontsize=9, color='blue')
    
    # Add axes labels for better understanding
    ax.set_xlabel("Price (BTC)")
    ax.set_ylabel("Volume")
    
    # Add a title
    ax.set_title('BTC Market Liquidity Zones (Voronoi Tessellation)')

    # Show the plot with additional styling
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

    """Generate and plot the Voronoi diagram."""
    vor = Voronoi(liquidity_points)
    
    # Plot the Voronoi tessellation
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange', line_width=2)
    plt.title('BTC Market Liquidity Zones (Voronoi Tessellation)')
    plt.show()

def map_liquidity_to_btc_values(liquidity_points, btc_price_data):
    """Map liquidity points to BTC price values."""
    # Assuming liquidity_points are 2D with [Price, Volume]
    price_mapping = []
    for point in liquidity_points:
        price = point[0]
        volume = point[1]

        # Find the closest BTC price (approximate mapping)
        closest_price = min(btc_price_data, key=lambda x: abs(x - price))  # Approximate to closest BTC price

        price_mapping.append((closest_price, volume))

    return price_mapping

# def plot_voronoi_with_btc_mapping(liquidity_points, btc_price_data):
    """Generate and plot the Voronoi diagram with mapped BTC price and volume."""
    price_mapping = map_liquidity_to_btc_values(liquidity_points, btc_price_data)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange', line_width=2)
    
    # Plot the liquidity points with BTC mapping
    for i, (price, volume) in enumerate(price_mapping):
        ax.scatter(price, volume, color='blue', zorder=5)
        ax.text(price + 0.1, volume + 10, f"BTC: {price:.2f}\nVolume: {volume:.2f}", fontsize=9, color='blue')

    # Add BTC price reference lines
    current_btc_price = np.mean(btc_price_data)  # Use current average price as reference
    ax.axvline(x=current_btc_price, color='green', linestyle='--', label=f'Current BTC Price: ${current_btc_price:.2f}')

    # Add axes labels
    ax.set_xlabel("Price (BTC)")
    ax.set_ylabel("Volume")
    ax.set_title('BTC Market Liquidity Zones (Voronoi Tessellation) with Real BTC Prices')
    
    # Add legend and grid
    ax.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

def generate_voronoi(liquidity_points):
    """Generate Voronoi diagram for the given liquidity points."""
    vor = Voronoi(liquidity_points)
    return vor

def plot_voronoi_with_btc_mapping(liquidity_points, btc_price_data):
    """Generate and plot the Voronoi diagram with mapped BTC price and volume."""
    price_mapping = map_liquidity_to_btc_values(liquidity_points, btc_price_data)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange', line_width=2)
    
    # Plot the liquidity points with BTC mapping
    for i, (price, volume) in enumerate(price_mapping):
        ax.scatter(price, volume, color='blue', zorder=5)
        ax.text(price + 0.1, volume + 10, f"BTC: {price:.2f}\nVolume: {volume:.2f}", fontsize=9, color='blue')

    # Add BTC price reference lines
    current_btc_price = np.mean(btc_price_data)  # Use current average price as reference
    ax.axvline(x=current_btc_price, color='green', linestyle='--', label=f'Current BTC Price: ${current_btc_price:.2f}')

    # Add axes labels
    ax.set_xlabel("Price (BTC)")
    ax.set_ylabel("Volume")
    ax.set_title('BTC Market Liquidity Zones (Voronoi Tessellation) with Real BTC Prices')
    
    # Add legend and grid
    ax.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

def plot_3D_chart():
    df = pd.read_csv("data/historical_data.csv")

    try:
        df = enhance_with_geometric_features(df)
        print(df.head(25))  # Check for missing values
    except Exception as e:
        print(f"⚠️ Warning: Issue while enhancing features: {e}")
        print("⚠️ Proceeding with the raw data.")
    
    # ✅ Ensure Volume Exists
    if "Volume" not in df.columns:
        df["Volume"] = df["BTC_Price"].diff().abs() * 100  # Approximate volume using BTC movement
        print("✅ Volume approximated using BTC price change.")

    # ✅ Create 3D Figure
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # ✅ Plot BTC Price points
    ax.scatter(df["BTC_Price"], df["Volume"], df.index, c='b', marker='o')

    # ✅ Plot RSI if available
    if "RSI" in df.columns:
        fig_rsi, ax_rsi = plt.subplots(figsize=(12, 4))
        ax_rsi.plot(df["RSI"], label="RSI", color="g")
        ax_rsi.axhline(70, linestyle="--", color="r", label="Overbought (70)")
        ax_rsi.axhline(30, linestyle="--", color="r", label="Oversold (30)")
        ax_rsi.legend(loc="upper left")
        ax_rsi.set_title("RSI (Relative Strength Index)")
    else:
        print("⚠️ RSI data missing. Skipping RSI plot.")

    # ✅ Plot Bollinger Bands
    if "UpperBand" in df.columns and "LowerBand" in df.columns:
        ax.plot(df["BTC_Price"], df["UpperBand"], df.index, label="Upper Bollinger Band", color="orange")
        ax.plot(df["BTC_Price"], df["LowerBand"], df.index, label="Lower Bollinger Band", color="red")
    else:
        print("⚠️ Warning: Bollinger Bands not properly computed. Check data.")

    # ✅ Display 3D Visualization
    plt.show()

if __name__ == "__main__":
    ## Train the model
    # train_ai()
    # train_xgboost_model()

    ## Example prediction with sample values
    test_schumann = 8.2
    prev_schumann = 8.1
    prev_prev_schumann = 8.0
    prev_btc = 90000  # Example previous BTC price
    btc_change = -0.02  # Example BTC percentage change (-2%)

    predicted_price = predict_btc_price(test_schumann, prev_schumann, prev_prev_schumann, prev_btc, btc_change)
    if predicted_price:
        print(f"🔮 Updated AI Prediction for BTC Price at Schumann {test_schumann} Hz: ${predicted_price:.2f}")
    else:
        print("⚠️ AI Prediction could not be made.")

    # Generate valid liquidity points (avoiding collinearity)
    # liquidity_points = generate_valid_liquidity_points()

    # Plot Voronoi diagram for liquidity zones
    # plot_voronoi(liquidity_points)

    # # Sample BTC price data for reference
    # btc_price_data = [75000, 80000, 85000, 90000, 95000, 100000]  # This would be actual historical data

    # # Generate valid liquidity points (avoiding collinearity)
    # liquidity_points = generate_valid_liquidity_points()
 
    # Generate Voronoi diagram
    # vor = generate_voronoi(liquidity_points)

    # # Plot Voronoi diagram with BTC price mapping
    # plot_voronoi_with_btc_mapping(liquidity_points, btc_price_data)

    # Assuming liquidity_points = [(price, volume, time)]
    # liquidity_points = np.array([[4.40, 259.37, 1], [5.67, 224.05, 2], [7.24, 197.13, 3],
    #                             [7.14, 53.93, 4], [7.99, 42.61, 5]])
    
    # vor = generate_voronoi(liquidity_points)

    # # Create Voronoi diagram in 3D
    # fig = plt.figure(figsize=(12, 10))
    # ax = fig.add_subplot(111, projection='3d')

    # # Extract Price, Volume, Time from liquidity points
    # prices = liquidity_points[:, 0]
    # volumes = liquidity_points[:, 1]
    # times = liquidity_points[:, 2]

    # # Scatter plot the liquidity points
    # ax.scatter(prices, volumes, times, c='blue', marker='o', label="Liquidity Points")

    # # Map out Voronoi diagram in 3D
    # vor = Voronoi(liquidity_points[:, :2])  # Voronoi needs only 2D points
    # for simplex in vor.ridge_vertices:
    #     simplex = np.array(simplex)
    #     if np.all(simplex >= 0):
    #         ax.plot([vor.vertices[simplex[0]][0], vor.vertices[simplex[1]][0]],
    #                 [vor.vertices[simplex[0]][1], vor.vertices[simplex[1]][1]],
    #                 zs=[times[simplex[0]], times[simplex[1]]], color='orange')

    # Labels and title
    # ax.set_xlabel('Price (BTC)')
    # ax.set_ylabel('Volume')
    # ax.set_zlabel('Time')
    # ax.set_title('3D BTC Market Liquidity Zones (Voronoi with Time)')

    # plt.show()

    plot_3D_chart()




