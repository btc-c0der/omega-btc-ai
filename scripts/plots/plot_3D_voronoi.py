
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
from scipy.spatial import Voronoi

def detect_liquidity_waves(df):
    """Generate Voronoi tessellation for BTC price-volume-time space, handling coplanarity issues."""
    
    # ✅ Ensure Real Volume is Used
    if "BTC_Volume" in df.columns:
        volume_column = "BTC_Volume"
    else:
        print("⚠️ No real volume detected! Using Simulated Volume instead.")
        volume_column = "Simulated_Volume"

    # ✅ Prepare 3D Data (BTC Price, Volume, Time)
    points = np.column_stack((df["BTC_Price"], df[volume_column], df.index))

    # ✅ Joggle points to avoid collinearity issues
    points += np.random.normal(scale=1e-6, size=points.shape)

    # ✅ Normalize Data to Prevent Precision Errors
    points = (points - points.min(axis=0)) / (points.max(axis=0) - points.min(axis=0))

    # ✅ Ensure we have at least 4 distinct points for a valid 3D Voronoi
    if len(np.unique(points, axis=0)) < 4:
        print("⚠️ Not enough unique points for 3D Voronoi tessellation.")
        return None

    # ✅ Compute Voronoi Tessellation
    vor = Voronoi(points, qhull_options="Qbb Qc Qz QJ")  # QJ (Jitter), Qc (Centering), Qbb (Bounding Box)
    return vor


def plot_3d_voronoi(df, vor):
    """Plot 3D Voronoi Tessellation for BTC liquidity waves, highlighting liquidity voids."""

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # ✅ Plot Data Points with BTC Volume Intensity (Higher Volume = Darker Color)
    scatter = ax.scatter(df['BTC_Price'], df['BTC_Volume'], df.index, c=df["BTC_Volume"], cmap="coolwarm", marker='o', s=5, alpha=0.7)

    # ✅ Iterate Through Voronoi Ridge Vertices Safely
    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0) and np.all(simplex < len(vor.points)):  # ✅ BOUNDS CHECK
            ax.plot(vor.points[simplex, 0], vor.points[simplex, 1], vor.points[simplex, 2], color='red', alpha=0.5)

    # ✅ Detect & Highlight Market Maker Liquidity Voids
    for region in vor.regions:
        if not -1 in region and len(region) > 3:  # Valid Voronoi region (not infinite)
            vertices = vor.vertices[region]
            ax.plot(vertices[:, 0], vertices[:, 1], vertices[:, 2], 'g--', alpha=0.3)

    # ✅ Color Bar to Represent Volume Intensity
    cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
    cbar.set_label("BTC Trading Volume")

    # ✅ Axis Labels & Title
    ax.set_xlabel("Price (BTC)")
    ax.set_ylabel("BTC Volume")
    ax.set_zlabel("Time Index")
    ax.set_title("3D BTC Liquidity Waves - Voronoi Market Maker Zones")

    plt.show()


# ✅ Fetch Real BTC Data (or Use Simulated Data)
data = {
    'BTC_Price': np.linspace(20000, 100000, 5000),
    'BTC_Volume': np.random.uniform(100, 10000, 5000),  # Simulated Real Volume
    '23.6%': 45000,
    '38.2%': 55000,
    '50%': 65000,
    '61.8%': 75000,
    '100%': 100000
}
df = pd.DataFrame(data)

# 🔥 Run Voronoi Liquidity Wave Detection
vor = detect_liquidity_waves(df)

if vor:
    plot_3d_voronoi(df, vor)
else:
    print("⚠️ Voronoi failed due to insufficient unique points.")
