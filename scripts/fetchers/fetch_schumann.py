
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

import os
import pandas as pd
import requests
import time

def fetch_historical_schumann(start_date, end_date, save_path="data/historical_schumann.csv"):
    """Fetch historical Schumann Resonance Power Levels from HeartMath API with pagination."""

    os.makedirs("data", exist_ok=True)  # Ensure data folder exists
    start_timestamp = int(time.mktime(time.strptime(start_date, "%Y-%m-%d")))  # Convert to seconds
    end_timestamp = int(time.mktime(time.strptime(end_date, "%Y-%m-%d")))  # Convert to seconds

    all_data = []

    print(f"🔄 Fetching Schumann Resonance data from {start_date} to {end_date}...")

    while start_timestamp < end_timestamp:
        url = f"https://nocc.heartmath.org/power_levels/public/charts/power_levels.php?start={start_timestamp}&end={start_timestamp + (7 * 24 * 3600)}"  # 7-day chunks
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            
            if not data:
                print("✅ No more Schumann data available.")
                break
            
            # 🔍 DEBUG: Print first few responses to inspect structure
            print(f"🔍 Sample API response: {data[:3]}")  # Print first 3 entries
            
            for entry in data:
                if len(entry) >= 4:  # Ensure at least 4 columns exist
                    timestamp_sec = entry[0] // 1000  # Convert milliseconds to seconds
                    schumann_value = entry[3]  # Extract Schumann power
                    all_data.append([timestamp_sec, schumann_value])
                else:
                    print(f"⚠️ Skipped invalid entry: {entry}")  # Log unexpected structures

            # Move to next 7-day period
            start_timestamp += (7 * 24 * 3600)  # Increment by 7 days
            print(f"✅ Retrieved {len(data)} rows, next start: {pd.to_datetime(start_timestamp, unit='s')}")
            time.sleep(1)  # Prevent hitting API limits

        else:
            print(f"❌ API Request Failed. Status Code: {response.status_code}")
            break

    # Convert to DataFrame
    df = pd.DataFrame(all_data, columns=["Timestamp", "Schumann"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s")  # Convert Unix timestamp to datetime

    # Save to CSV
    df.to_csv(save_path, index=False)
    print(f"✅ Saved full Schumann historical data to {save_path}")

    return df

# Example usage:
if __name__ == "__main__":
    schumann_df = fetch_historical_schumann("2018-01-01", "2025-03-03")
