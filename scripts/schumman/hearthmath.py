
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

"""
HeartMath Schumann Resonance Data Retriever
==========================================

This module fetches and processes Schumann resonance data from the HeartMath Institute's
Global Coherence Initiative website. Schumann resonances are a set of spectrum peaks
in the extremely low frequency (ELF) portion of the Earth's electromagnetic field spectrum.

The module retrieves historical Schumann resonance power level data from the HeartMath
Institute API, processes it into a pandas DataFrame, and provides visualization capabilities.

Key Features
-----------
1. Data Retrieval: Fetches Schumann resonance power level data from HeartMath Institute 
   API by specifying a time range.

2. Data Processing: Parses the API response and converts it into a structured pandas
   DataFrame for analysis.

3. Visualization: Creates plots of Schumann resonance power levels over time for visual
   analysis.

4. Debugging: Provides detailed debugging information about API requests and responses.

5. Error Handling: Implements robust error handling for API communication and data processing.

API Details
----------
The HeartMath API returns data in a specific format:
- Array format: [[timestamp_ms, value1, value2, schumann_power, ...], [...]]
- The Schumann resonance power level is at index 3 in each array
- Timestamps are in milliseconds since the Unix epoch

Usage Examples
-------------
Basic usage to fetch and process recent data:
```
python hearthmath.py
````

Advanced usage with custom date ranges and additional debugging:
````
python hearthmath.py --start-date 2023-03-01 --end-date 2023-03-02 --debug
````

Dependencies
-----------
- requests: For HTTP request handling
- pandas: For data processing
- matplotlib: For data visualization
- json: For parsing API responses

Author: OmegaBTC Team
Version: 1.1
"""

import requests
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import argparse
import sys
import os

def get_heartmath_data(start_timestamp_ms, end_timestamp_ms, debug=False):
    """
    Fetches Schumann resonance power level data from the HeartMath Institute.

    Args:
        start_timestamp_ms: The start timestamp in milliseconds (Unix epoch).
        end_timestamp_ms: The end timestamp in milliseconds (Unix epoch).
        debug: Whether to print additional debugging information.

    Returns:
        A list of arrays containing the data, or None on error.
    """
    url = "https://nocc.heartmath.org/power_levels/public/charts/power_levels.php"
    params = {
        "start": start_timestamp_ms,
        "end": end_timestamp_ms
    }
    
    # Construct and print the full URL for debugging
    full_url = f"{url}?start={start_timestamp_ms}&end={end_timestamp_ms}"
    print(f"🌐 FULL URL: {full_url}")
    
    try:
        print(f"Fetching data from {url} with params: {params}")
        
        # Add timeout to prevent hanging requests
        response = requests.get(url, params=params, timeout=30)
        
        # Print response details for debugging
        if debug:
            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
        
        response.raise_for_status()  # Raise HTTPError for bad requests (4xx or 5xx)

        # Attempt to parse the response as JSON
        data = response.json()
        print(f"Response structure: {type(data)}")
        
        if debug:
            # More detailed output when debug is enabled
            print(f"Response content type: {response.headers.get('Content-Type')}")
            content_preview = response.text[:200] + "..." if len(response.text) > 200 else response.text
            print(f"Raw response preview: {content_preview}")
        
        print(f"First few items: {data[:2] if len(data) >= 2 else data}")
        
        # Check for the special case of [[0]] which indicates no data
        if data == [[0]]:
            print("⚠️ API returned [[0]], which indicates no data available for this time range.")
            print("Try a different time range or check the HeartMath API documentation.")
            return None
            
        return data

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text[:500]}")  # Print first 500 chars
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON: {e}")
        print(f"Response content: {response.text[:500]}...")  # Print first 500 chars
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()  # Print full stack trace for better debugging
        return None

def process_heartmath_data(data, debug=False):
    """
    Process the HeartMath data which comes as arrays.
    
    The structure appears to be:
    [timestamp_ms, value1, value2, schumann_power, ...]
    
    Args:
        data: List of arrays from the HeartMath API
        debug: Whether to print additional debugging information
        
    Returns:
        Pandas DataFrame with processed data
    """
    if not data or len(data) == 0:
        print("No data to process")
        return None
        
    # Check if we have valid data structure
    if data == [[0]] or (isinstance(data[0], list) and len(data[0]) <= 1):
        print("Invalid or empty data format received")
        return None
    
    # Filter out invalid entries (should have at least 4 elements)
    valid_data = [entry for entry in data if isinstance(entry, list) and len(entry) >= 4]
    
    filtered_count = len(data) - len(valid_data)
    if filtered_count > 0:
        print(f"⚠️ Filtered out {filtered_count} invalid entries")
    
    if not valid_data:
        print("No valid data entries found")
        return None
    
    # Create dataframe from arrays
    try:
        # Extract columns we need: timestamp and schumann power (index 3)
        timestamps = [entry[0] for entry in valid_data]  # First element is timestamp in ms
        power_values = [entry[3] for entry in valid_data]  # Fourth element is schumann power
        
        if debug:
            # Show timestamp range for debugging
            first_time = datetime.fromtimestamp(timestamps[0]/1000)
            last_time = datetime.fromtimestamp(timestamps[-1]/1000)
            print(f"Data time range: {first_time} to {last_time}")
            print(f"Min power value: {min(power_values)}, Max power value: {max(power_values)}")
        
        # Convert to DataFrame
        df = pd.DataFrame({
            'timestamp_ms': timestamps,
            'schumann_power': power_values
        })
        
        # Convert timestamps to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp_ms'], unit='ms')
        
        # Sort by timestamp to ensure chronological order
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        return df
    
    except Exception as e:
        print(f"❌ Error processing data: {e}")
        import traceback
        traceback.print_exc()
        return None

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Fetch and analyze Schumann resonance data")
    parser.add_argument('--start-date', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end-date', type=str, help='End date in YYYY-MM-DD format')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--output', type=str, default='schumann_power_levels.png', 
                        help='Output file path for the plot')
    return parser.parse_args()

def main():
    """Main execution function."""
    args = parse_args()
    debug_mode = args.debug
    
    # Determine time range based on command line arguments or defaults
    if args.start_date and args.end_date:
        try:
            # Convert dates to timestamps
            start_time = int(datetime.strptime(args.start_date, "%Y-%m-%d").timestamp() * 1000)
            end_time = int(datetime.strptime(args.end_date, "%Y-%m-%d").timestamp() * 1000)
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.")
            return
    else:
        # Default to last 24 hours
        end_time = int(time.time() * 1000)  # Current time in milliseconds
        start_time = end_time - (24 * 60 * 60 * 1000)  # 24 hours ago

    print(f"📅 Fetching data from {datetime.fromtimestamp(start_time/1000)} to {datetime.fromtimestamp(end_time/1000)}")

    # Fetch data
    data = get_heartmath_data(start_time, end_time, debug=debug_mode)

    if data:
        print(f"✅ Received {len(data)} data points.")
        
        # Process the data into a DataFrame
        df = process_heartmath_data(data, debug=debug_mode)
        
        if df is not None and not df.empty:
            # Print information about the data
            print("\n📊 Data Summary:")
            print(f"- Time range: {df['timestamp'].min()} to {df['timestamp'].max()}")
            print(f"- Number of readings: {len(df)}")
            print(f"- Average Schumann power: {df['schumann_power'].mean():.2f}")
            print(f"- Maximum Schumann power: {df['schumann_power'].max():.2f}")
            print(f"- Minimum Schumann power: {df['schumann_power'].min():.2f}")
            
            # Print the first few rows
            print("\n📋 First few readings:")
            print(df.head())
            
            # Create a simple plot
            plt.figure(figsize=(14, 8))
            plt.plot(df['timestamp'], df['schumann_power'], marker='o', linestyle='-', markersize=3)
            
            # Add reference line for mean
            mean_value = df['schumann_power'].mean()
            plt.axhline(y=mean_value, color='r', linestyle='--', alpha=0.6, 
                       label=f'Mean: {mean_value:.2f}')
            
            plt.title('Schumann Resonance Power Levels')
            plt.xlabel('Time')
            plt.ylabel('Power')
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            
            # Save the plot to a file
            output_dir = os.path.dirname(args.output)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            plt.savefig(args.output, dpi=300)
            print(f"\n🖼️ Plot saved to {args.output}")
            
            # Show the plot
            plt.show()
        else:
            print("❌ Failed to process data.")
    else:
        print("❌ Failed to retrieve data.")

# Run the main function when script is executed directly
if __name__ == "__main__":
    main()