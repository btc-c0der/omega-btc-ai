from omega_ai.data_feed.btc_live_feed import BtcPriceFeed
import json
from datetime import datetime
import os

def main():
    # Initialize the BTC price feed
    price_feed = BtcPriceFeed()
    
    # Get 24 hours of price history (using count=1440 for minute-by-minute data)
    history = price_feed.get_price_history(minutes=1440, count=1440)
    
    # Create output directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save to a JSON file with timestamp in filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'data/btc_history_{timestamp}.json'
    
    with open(output_file, 'w') as f:
        json.dump(history, f, indent=2)
    
    print(f"✅ Downloaded {len(history)} price points")
    print(f"📝 Saved to: {output_file}")
    
    # Print sample of the data
    if history:
        print("\n📊 Sample of latest prices:")
        for entry in history[:5]:
            print(f"Time: {entry['timestamp']}, Price: ${entry['price']:,.2f}")

if __name__ == "__main__":
    main() 