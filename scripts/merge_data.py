import pandas as pd
import os

def merge_historical_data():
    """Merges Schumann Resonance & BTC price data into a single dataset."""
    
    schumann_file = "data/historical_schumann.csv"
    btc_file = "data/historical_btc.csv"

    if not os.path.exists(schumann_file) or not os.path.exists(btc_file):
        print("❌ Missing one or both historical data files!")
        return None

    # Load datasets
    schumann_df = pd.read_csv(schumann_file)
    btc_df = pd.read_csv(btc_file)

    # Convert Timestamp to datetime
    schumann_df["Timestamp"] = pd.to_datetime(schumann_df["Timestamp"])
    btc_df["Timestamp"] = pd.to_datetime(btc_df["Timestamp"])

    # Merge datasets on closest timestamps
    merged_df = pd.merge_asof(schumann_df.sort_values("Timestamp"),
                               btc_df.sort_values("Timestamp"),
                               on="Timestamp")

    # Save merged data
    os.makedirs("data", exist_ok=True)
    merged_df.to_csv("data/historical_data.csv", index=False)
    print(f"✅ Merged {len(merged_df)} rows of Schumann & BTC data!")
    return merged_df

# Example usage:
if __name__ == "__main__":
    merged_df = merge_historical_data()
