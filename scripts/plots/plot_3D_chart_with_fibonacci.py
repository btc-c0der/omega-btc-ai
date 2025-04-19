
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
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def fibonacci_levels(df):
    """Calculate Fibonacci retracement levels based on BTC price range."""
    min_price = df["BTC_Price"].min()
    max_price = df["BTC_Price"].max()
    
    levels = {
        "0%": min_price,
        "23.6%": min_price + 0.236 * (max_price - min_price),
        "38.2%": min_price + 0.382 * (max_price - min_price),
        "50%": min_price + 0.5 * (max_price - min_price),
        "61.8%": min_price + 0.618 * (max_price - min_price),
        "100%": max_price,
    }
    return levels

def enhance_with_fibonacci(df):
    """Enhance the dataframe with Fibonacci levels."""
    fib_levels = fibonacci_levels(df)
    
    for level_name, level_value in fib_levels.items():
        df[level_name] = level_value
    
    return df

def generate_simulated_volume(df):
    """Approximate volume using BTC price percentage change."""
    df["Simulated_Volume"] = np.abs(df["BTC_Price"].pct_change()) * 100000
    df["Simulated_Volume"].fillna(df["Simulated_Volume"].median(), inplace=True)  
    return df

def plot_3D_chart(df):
    """Plot the 3D chart for BTC Market Liquidity Zones."""
    df = enhance_with_fibonacci(df)
    df = generate_simulated_volume(df)
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Scatter Plot: BTC Price (X), Volume (Y), Time Index (Z)
    ax.scatter(df["BTC_Price"], df["Simulated_Volume"], df.index, c="b", marker="o")

    # Add Fibonacci Levels as Horizontal Reference Planes
    for level in ["23.6%", "38.2%", "50%", "61.8%", "100%"]:
        ax.plot([df[level].iloc[0]] * len(df), df["Simulated_Volume"], df.index, linestyle="--", color="purple")

    ax.set_xlabel("Price (BTC)")
    ax.set_ylabel("Simulated Volume")
    ax.set_zlabel("Time Index")
    ax.set_title("3D BTC Market Liquidity Zones with Fibonacci Levels")

    plt.show()

def plot_3d_fibonacci(df):
    """Plot a 3D visualization of BTC market liquidity zones with Fibonacci levels."""
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Normalize Schumann Resonance for coloring
    if "Schumann" in df.columns:
        schumann_norm = (df['Schumann'] - df['Schumann'].min()) / (df['Schumann'].max() - df['Schumann'].min())
        colors = plt.cm.coolwarm(schumann_norm)
    else:
        colors = 'b'  # Default to blue if Schumann data is missing
    
    # Scatter BTC price points (X = Price, Y = Simulated Volume, Z = Time)
    scatter = ax.scatter(df['BTC_Price'], df['Simulated_Volume'], df.index, c=colors, marker='o', s=5, alpha=0.7)
    
    # Define Fibonacci levels for visualization
    fib_levels = {
        "23.6%": df["23.6%"].iloc[0],
        "38.2%": df["38.2%"].iloc[0],
        "50%": df["50%"].iloc[0],
        "61.8%": df["61.8%"].iloc[0],
        "100%": df["100%"].iloc[0]
    }
    
    # Fine-tuned Fibonacci Level Planes (Less Density & More Transparency)
    for level_name, level_value in fib_levels.items():
        x_range = np.linspace(df['BTC_Price'].min(), df['BTC_Price'].max(), 10)
        y_range = np.linspace(df['Simulated_Volume'].min(), df['Simulated_Volume'].max(), 10)
        X, Y = np.meshgrid(x_range, y_range)
        Z = np.full_like(X, level_value)
        ax.plot_surface(X, Y, Z, color='purple', alpha=0.3, edgecolor='none')  # More transparent, less clutter
        
        # Add Text Labels for Fibonacci Levels
        ax.text(df['BTC_Price'].max(), df['Simulated_Volume'].max(), level_value, f"{level_name} ({level_value:.2f})",
                color='black', fontsize=10, fontweight='bold', backgroundcolor='white')
    
    # Add Colorbar for Schumann Influence
    if "Schumann" in df.columns:
        cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.coolwarm), ax=ax, shrink=0.6)
        cbar.set_label("Schumann Resonance Intensity")
    
    # Axis labels & title
    ax.set_xlabel('Price (BTC)')
    ax.set_ylabel('Simulated Volume')
    ax.set_zlabel('Time Index')
    ax.set_title('3D BTC Market Liquidity Zones with Fibonacci Levels')
    
    # Adjust viewing angle for better depth perception
    ax.view_init(elev=25, azim=135)
    
    plt.show()


# Example usage with a sample dataframe
data = {
    'BTC_Price': np.linspace(20000, 100000, 50000),
    'Simulated_Volume': np.random.uniform(1000, 20000, 50000),
    'Schumann': np.random.uniform(50, 100, 50000),  # Simulated Schumann data
    '23.6%': 45000,
    '38.2%': 55000,
    '50%': 65000,
    '61.8%': 75000,
    '100%': 100000
}
df = pd.DataFrame(data)
plot_3d_fibonacci(df)


# Example usage with a sample dataframe
data = {
    'BTC_Price': np.linspace(20000, 100000, 50000),
    'Simulated_Volume': np.random.uniform(1000, 20000, 50000),
    '23.6%': 45000,
    '38.2%': 55000,
    '50%': 65000,
    '61.8%': 75000,
    '100%': 100000
}
df = pd.DataFrame(data)
plot_3d_fibonacci(df)


# Load Data
df = pd.read_csv("data/historical_data.csv")  # Update with actual path
# Example usage with a sample dataframe

# data = {
#     'BTC_Price': np.linspace(20000, 100000, 50000),
#     'Simulated_Volume': np.random.uniform(1000, 20000, 50000),
#     '23.6%': 45000,
#     '38.2%': 55000,
#     '50%': 65000,
#     '61.8%': 75000,
#     '100%': 100000
# }
# df = pd.DataFrame(data)
plot_3d_fibonacci(df)

# plot_3D_chart(df)
