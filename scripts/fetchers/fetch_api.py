import requests
import time

def fetch_schumann_data():
    """Fetch Schumann Resonance Power Levels from HeartMath API."""

    # Set start and end timestamps (current date range example)
    start_timestamp = int(time.mktime(time.strptime("2025-01-01", "%Y-%m-%d")))  # Example start date
    end_timestamp = int(time.mktime(time.strptime("2025-03-01", "%Y-%m-%d")))  # Example end date

    url = f"https://nocc.heartmath.org/power_levels/public/charts/power_levels.php?start={start_timestamp}&end={end_timestamp}"
    print(f"🔄 Querying Schumann data from: {url}")  # Trace log

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            print(f"✅ Successfully fetched Schumann Resonance data!")  # Trace log
            # Process and print the Schumann Resonance power levels (modify as needed)
            power_levels = data.get("data", [])  # Adjust based on the actual response structure
            if power_levels:
                # Example: Print the last power level
                last_power_level = power_levels[-1]  # Get the latest power level
                print(f"✅ Latest Schumann Power Level: {last_power_level}")
                return last_power_level
            else:
                print("⚠️ No data available for the requested range.")  # Trace log
                return None
        else:
            print(f"❌ Failed to fetch data. Status Code: {response.status_code}")  # Trace log
            return None

    except requests.RequestException as e:
        print(f"❌ Error fetching Schumann data: {e}")  # Trace log
        return None

# Test execution
if __name__ == "__main__":
    schumann_value = fetch_schumann_data()
    print(f"🔍 TEST RUN: Schumann Resonance Power Level = {schumann_value}")
import requests
import time

def fetch_schumann_data():
    """Fetch Schumann Resonance Power Levels from HeartMath API."""

    # Set start and end timestamps (current date range example)
    start_timestamp = int(time.mktime(time.strptime("2025-01-01", "%Y-%m-%d")))  # Example start date
    end_timestamp = int(time.mktime(time.strptime("2025-03-01", "%Y-%m-%d")))  # Example end date

    url = f"https://nocc.heartmath.org/power_levels/public/charts/power_levels.php?start={start_timestamp}&end={end_timestamp}"
    print(f"🔄 Querying Schumann data from: {url}")  # Trace log

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            print(f"✅ Successfully fetched Schumann Resonance data!")  # Trace log
            
            if data:
                last_power_level = data[-1]  # Get the latest power level
                print(f"✅ Latest Schumann Power Level: {last_power_level}")
                return last_power_level
            else:
                print("⚠️ No data available for the requested range.")  # Trace log
                return None
        else:
            print(f"❌ Failed to fetch data. Status Code: {response.status_code}")  # Trace log
            return None

    except requests.RequestException as e:
        print(f"❌ Error fetching Schumann data: {e}")  # Trace log
        return None

# Test execution
if __name__ == "__main__":
    schumann_value = fetch_schumann_data()
    print(f"🔍 TEST RUN: Schumann Resonance Power Level = {schumann_value}")
import requests
import time

def fetch_schumann_data():
    """Fetch Schumann Resonance Power Levels from HeartMath API."""

    # Set start and end timestamps (current date range example)
    start_timestamp = int(time.mktime(time.strptime("2025-01-01", "%Y-%m-%d")))  # Example start date
    end_timestamp = int(time.mktime(time.strptime("2025-03-01", "%Y-%m-%d")))  # Example end date

    url = f"https://nocc.heartmath.org/power_levels/public/charts/power_levels.php?start={start_timestamp}&end={end_timestamp}"
    print(f"🔄 Querying Schumann data from: {url}")  # Trace log

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # The response is expected to be a JSON list
            print(f"✅ Successfully fetched Schumann Resonance data!")  # Trace log
            
            if isinstance(data, list) and data:
                last_power_level = data[-1]  # Get the latest power level
                print(f"✅ Latest Schumann Power Level: {last_power_level}")
                return last_power_level
            else:
                print("⚠️ No data available for the requested range.")  # Trace log
                return None
        else:
            print(f"❌ Failed to fetch data. Status Code: {response.status_code}")  # Trace log
            return None

    except requests.RequestException as e:
        print(f"❌ Error fetching Schumann data: {e}")  # Trace log
        return None

# Test execution
if __name__ == "__main__":
    schumann_value = fetch_schumann_data()
    print(f"🔍 TEST RUN: Schumann Resonance Power Level = {schumann_value}")
import requests
import time

def fetch_schumann_data(verbose=False):
    """Fetch Schumann Resonance Power Levels from HeartMath API."""

    # Set start and end timestamps (current date range example)
    start_timestamp = int(time.mktime(time.strptime("2025-01-01", "%Y-%m-%d")))  # Example start date
    end_timestamp = int(time.mktime(time.strptime("2025-03-01", "%Y-%m-%d")))  # Example end date

    url = f"https://nocc.heartmath.org/power_levels/public/charts/power_levels.php?start={start_timestamp}&end={end_timestamp}"
    
    if verbose:
        print(f"🔄 [DEBUG] Querying Schumann data from: {url}")

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # The response is expected to be a JSON list

            if verbose:
                print(f"✅ [DEBUG] Response Data: {data}")

            if isinstance(data, list) and data:
                last_power_level = data[-1]  # Get the latest power level
                
                if verbose:
                    print(f"✅ [DEBUG] Latest Schumann Power Level: {last_power_level}")
                
                return last_power_level
            else:
                if verbose:
                    print("⚠️ [DEBUG] No data available for the requested range.")
                return None
        else:
            if verbose:
                print(f"❌ [DEBUG] Failed to fetch data. Status Code: {response.status_code}")
            return None

    except requests.RequestException as e:
        if verbose:
            print(f"❌ [DEBUG] Error fetching Schumann data: {e}")
        return None

# Test execution
if __name__ == "__main__":
    schumann_value = fetch_schumann_data(verbose=True)  # Set verbose=True to enable debug prints
    print(f"🔍 TEST RUN: Schumann Resonance Power Level = {schumann_value}")
import requests
import time

def fetch_schumann_data(verbose=False):
    """Fetch Schumann Resonance Power Levels from HeartMath API."""

    # Set start and end timestamps (current date range example)
    start_timestamp = int(time.mktime(time.strptime("2025-01-01", "%Y-%m-%d")))  # Example start date
    end_timestamp = int(time.mktime(time.strptime("2025-03-01", "%Y-%m-%d")))  # Example end date

    url = f"https://nocc.heartmath.org/power_levels/public/charts/power_levels.php?start={start_timestamp}&end={end_timestamp}"
    
    if verbose:
        print(f"🔄 [DEBUG] Querying Schumann data from: {url}")

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # The response is expected to be a JSON list

            if verbose:
                print(f"✅ [DEBUG] Response Data: {data}")

            if isinstance(data, list) and data:
                last_power_level = data[-1]  # Get the latest power level
                
                if verbose:
                    print(f"✅ [DEBUG] Latest Schumann Power Level: {last_power_level}")
                
                return last_power_level
            else:
                if verbose:
                    print("⚠️ [DEBUG] No data available for the requested range.")
                return None
        else:
            if verbose:
                print(f"❌ [DEBUG] Failed to fetch data. Status Code: {response.status_code}")
            return None

    except requests.RequestException as e:
        if verbose:
            print(f"❌ [DEBUG] Error fetching Schumann data: {e}")
        return None

# Test execution
if __name__ == "__main__":
    schumann_value = fetch_schumann_data(verbose=True)  # Set verbose=True to enable debug prints
    print(f"🔍 TEST RUN: Schumann Resonance Power Level = {schumann_value}")
