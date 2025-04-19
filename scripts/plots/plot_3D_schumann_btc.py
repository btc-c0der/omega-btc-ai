
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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_3d_schumann_btc(df):
    """Plot a 3D visualization of BTC market liquidity zones with Schumann Resonance Overlay."""
    
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # ✅ LIMIT DATA POINTS TO PREVENT OVERLOAD
    df_sampled = df.iloc[::10]  # Take every 10th row to reduce memory load

    # Normalize Schumann resonance values for color mapping
    df_sampled['Schumann_Normalized'] = (df_sampled['Schumann'] - df_sampled['Schumann'].min()) / (df_sampled['Schumann'].max() - df_sampled['Schumann'].min())

    # Scatter BTC price points (X = Price, Y = Simulated Volume, Z = Time)
    sc = ax.scatter(df_sampled['BTC_Price'], df_sampled['Simulated_Volume'], df_sampled.index, 
                    c=df_sampled['Schumann_Normalized'], cmap='coolwarm', marker='o', s=5, alpha=0.7)

    # Define Fibonacci levels for visualization
    fib_levels = {
        "23.6%": df["23.6%"].iloc[0],
        "38.2%": df["38.2%"].iloc[0],
        "50%": df["50%"].iloc[0],
        "61.8%": df["61.8%"].iloc[0],
        "100%": df["100%"].iloc[0]
    }

    # ✅ OPTIMIZED MESHGRID SIZE TO PREVENT INFINITE LOOP
    mesh_size = min(300, len(df_sampled))  # Keep it manageable
    
    # Fine-tuned Fibonacci Level Planes (Transparent, Less Clutter)
    for level_name, level_value in fib_levels.items():
        x_range = np.linspace(df_sampled['BTC_Price'].min(), df_sampled['BTC_Price'].max(), mesh_size)
        y_range = np.linspace(df_sampled['Simulated_Volume'].min(), df_sampled['Simulated_Volume'].max(), mesh_size)
        X, Y = np.meshgrid(x_range, y_range)
        Z = np.full_like(X, level_value)
        ax.plot_surface(X, Y, Z, color='purple', alpha=0.3)  # Transparent Fibonacci layers

        # Label Fibonacci levels
        ax.text(df_sampled['BTC_Price'].max(), df_sampled['Simulated_Volume'].max(), level_value, 
                f"{level_name} ({level_value:.2f})", color='black', fontsize=10, fontweight='bold')

    # Add colorbar to represent Schumann resonance intensity
    cbar = plt.colorbar(sc, ax=ax, pad=0.1)
    cbar.set_label('Schumann Resonance Intensity')

    # Axis labels & title
    ax.set_xlabel('Price (BTC)')
    ax.set_ylabel('Simulated Volume')
    ax.set_zlabel('Time Index')
    ax.set_title('3D BTC Market Liquidity Zones with Schumann Resonance')

    # Adjust viewing angle for better perception
    ax.view_init(elev=25, azim=135)

    plt.show()

# ✅ TEST WITH OPTIMIZED DATASET
data = {
    'BTC_Price': np.linspace(20000, 100000, 5000),  # Reduced to 5000 points
    'Simulated_Volume': np.random.uniform(1000, 20000, 5000),
    'Schumann': np.random.uniform(5, 40, 5000),  # Simulated Schumann resonance values
    '23.6%': 45000,
    '38.2%': 55000,
    '50%': 65000,
    '61.8%': 75000,
    '100%': 100000
}
df = pd.DataFrame(data)
plot_3d_schumann_btc(df)
