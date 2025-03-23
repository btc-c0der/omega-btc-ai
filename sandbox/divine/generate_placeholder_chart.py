import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime, timedelta
import os

# Create sample data
days = 365 * 7  # 7 years
dates = [datetime.now() - timedelta(days=x) for x in range(days)]
dates.reverse()
dates = mdates.date2num(dates)  # Convert datetime objects to matplotlib dates

# Generate synthetic BTC price data with an upward trend and some volatility
base = np.linspace(1000, 65000, days)  # Base trend from 1000 to 65000
noise = np.random.normal(0, 2000, days)  # Add some noise
btc_price = base + noise

# Create the plot
plt.figure(figsize=(12, 6))
plt.plot_date(dates, btc_price, color='#F7931A', linewidth=1.5, linestyle='-')  # Bitcoin orange color

# Customize the plot
plt.title('BTC/USD 7-Year Price Chart (Placeholder)', fontsize=14, pad=20)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price (USD)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Format x-axis dates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)

# Add Golden Ratio lines (placeholder)
plt.axhline(y=34000, color='gold', linestyle='--', alpha=0.5, label='Golden Ratio 0.618')
plt.axhline(y=49000, color='silver', linestyle='--', alpha=0.5, label='Golden Ratio 0.382')
plt.legend()

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Ensure the images directory exists
os.makedirs('assets/images', exist_ok=True)

# Save the plot
plt.savefig('assets/images/btc_golden_ratio_7yr_latest.png', dpi=300, bbox_inches='tight')
plt.close()

print("Placeholder chart generated successfully!") 