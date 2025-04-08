import requests
import pandas as pd
import time
import os

import os
import time
import requests
import pandas as pd

def fetch_historical_btc(start_date, end_date, save_path="data/historical_btc_extended.csv"):
    """Fetch historical BTC price, volume & market data from Binance API with pagination (500-row limit bypass)."""

    os.makedirs("data", exist_ok=True)  # Ensure data folder exists
    start_timestamp = int(time.mktime(time.strptime(start_date, "%Y-%m-%d"))) * 1000  # Convert to milliseconds
    end_timestamp = int(time.mktime(time.strptime(end_date, "%Y-%m-%d"))) * 1000  # Convert to milliseconds

    all_data = []

    print(f"🔄 Fetching BTC historical data from Binance starting at {start_date}...")

    while start_timestamp < end_timestamp:
        url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&startTime={start_timestamp}&limit=500"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if not data:
                print("✅ No more data to fetch.")
                break

            # Process data and append to list
            for entry in data:
                all_data.append([
                    entry[0],   # Timestamp
                    float(entry[1]),   # Open Price
                    float(entry[2]),   # High Price
                    float(entry[3]),   # Low Price
                    float(entry[4]),   # Close Price (BTC_USDT)
                    float(entry[5]),   # Volume (BTC traded in that hour)
                    float(entry[7]),   # Quote Asset Volume (USD traded)
                    int(entry[8]),     # Number of Trades
                    float(entry[9]),   # Taker Buy Volume (BTC)
                    float(entry[10])   # Taker Buy Quote Volume (USD)
                ])

            # Update start_timestamp for next batch
            start_timestamp = data[-1][0] + 1  # Move to next timestamp

            print(f"✅ Retrieved {len(data)} rows, next start: {pd.to_datetime(start_timestamp, unit='ms')}")
            time.sleep(0.8)  # Prevent hitting API rate limits

        else:
            print(f"❌ API Request Failed. Status Code: {response.status_code}")
            break

    # Convert to DataFrame
    df = pd.DataFrame(all_data, columns=[
        "Timestamp", "Open", "High", "Low", "Close", "BTC_Volume",
        "Quote_Volume", "Trades", "Taker_Buy_Volume", "Taker_Buy_Quote_Volume"
    ])
    
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="ms")  # Convert to datetime

    # Save to CSV
    df.to_csv(save_path, index=False)
    print(f"✅ Saved full BTC historical data to {save_path}")

    return df

if __name__ == "__main__":
    btc_df = fetch_historical_btc("2017-01-01", "2025-03-04")
