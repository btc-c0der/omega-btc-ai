```python
import requests
import json
import time
import hmac
import hashlib
import os  # For environment variables

# --- Bitget Testnet Information ---
BITGET_TESTNET_INFO = """
--- Bitget Testnet Information ---

The Bitget Testnet (Paper Trading environment) is a simulated trading platform
provided by Bitget. It allows you to practice trading strategies and test
API integrations without risking real cryptocurrency funds.

Key characteristics of the Bitget Testnet:

1.  Simulated Funds: You trade with virtual or "paper" money. Any profits or losses
    are not real. This is crucial for risk-free testing.

2.  Separate API Endpoint: The Testnet uses a different API URL than the mainnet:
    - Mainnet API URL:  https://api.bitget.com
    - Testnet API URL: https://api-testnet.bitget.com
    **You must change your API URL in your scripts to point to the Testnet when testing.**

3.  Separate Account: You need to create a separate account specifically for the Testnet.
    You cannot use your main Bitget account credentials on the Testnet.
    You can usually sign up for a Testnet account on the Bitget website or through
    their documentation for API access.

4.  API Keys: You will need to generate new API keys specifically for your Testnet account.
    These Testnet API keys will *only* work on the Testnet API endpoint and not on the mainnet.

5.  Market Conditions Simulation: The Testnet attempts to simulate real market conditions,
    but it's not always perfectly identical to the live market. Liquidity and order book depth
    might differ from the mainnet.

6.  Purpose: The Testnet is ideal for:
    - Testing trading scripts and API integrations.
    - Backtesting strategies in a live-like environment (though not perfect).
    - Practicing manual trading without financial risk.
    - Debugging and error handling in your trading systems.

--- Important Warning ---
Trading on the Bitget Testnet involves *no real financial risk*. However, remember that
trading on the *mainnet* with real funds carries substantial risk of financial loss.
Always thoroughly test and understand your strategies and scripts in the Testnet
environment before deploying them with real capital on the mainnet.
"""

print(BITGET_TESTNET_INFO)


# --- Bitget Testnet API Module (Adaptable for Testnet/Mainnet) ---
class BitgetTestnetAPI:
    def __init__(self, api_key=None, secret_key=None, passphrase=None, use_testnet=True):
        """
        Initializes the BitgetTestnetAPI client.

        Args:
            api_key (str, optional): Bitget API key. Defaults to environment variable "BITGET_TESTNET_API_KEY".
            secret_key (str, optional): Bitget Secret key. Defaults to environment variable "BITGET_TESTNET_SECRET_KEY".
            passphrase (str, optional): Bitget Passphrase. Defaults to environment variable "BITGET_TESTNET_PASSPHRASE".
            use_testnet (bool, optional): If True, uses the Bitget Testnet API endpoint. Defaults to True.
                                           Set to False to use the Mainnet API (for real trading - use with extreme caution!).
        """
        self.use_testnet = use_testnet
        self.api_url = "https://api-testnet.bitget.com" if use_testnet else "https://api.bitget.com"
        self.api_key = api_key if api_key else os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY")
        self.secret_key = secret_key if secret_key else os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY")
        self.passphrase = passphrase if passphrase else os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE")

        if not self.api_key or not self.secret_key or not self.passphrase:
            mode = "Testnet" if use_testnet else "Mainnet"
            print(f"Error: API credentials for {mode} not fully configured.")
            print(f"Please set environment variables: BITGET_{'TESTNET_' if use_testnet else ''}API_KEY, BITGET_{'TESTNET_' if use_testnet else ''}SECRET_KEY, BITGET_{'TESTNET_' if use_testnet else ''}PASSPHRASE")


    def generate_signature(self, timestamp, method, request_path, body=None):
        """Generates the signature required for Bitget API authentication."""
        message = str(timestamp) + method + request_path
        if body:
            message += json.dumps(body)
        hmac_obj = hmac.new(self.secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256)
        signature = hmac_obj.hexdigest()
        return signature

    def place_order(self, symbol, side, order_type, price=None, quantity=None, margin_mode="crossed", leverage="20"):
        """Places an order - adaptable for Testnet or Mainnet based on client initialization."""
        endpoint = "/api/mix/v1/order/placeOrder"
        method = "POST"
        timestamp = str(int(time.time() * 1000))  # Millisecond timestamp
        params = {
            "symbol": symbol,
            "side": side.upper(),
            "orderType": order_type.upper(),
            "marginMode": margin_mode.upper(),
            "leverage": leverage
        }

        if order_type.lower() == "limit":
            if price is None or quantity is None:
                print("Error: Price and quantity are required for limit orders.")
                return None
            params["price"] = price
            params["size"] = quantity

        elif order_type.lower() == "market":
            if quantity is None:
                print("Error: Quantity is required for market orders.")
                return None
            params["size"] = quantity

        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": self.generate_signature(timestamp, method, endpoint, params),
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(self.api_url + endpoint, headers=headers, json=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error placing order: {e}")
            if response is not None:
                print(f"Response content: {response.text}")
            return None


    def close_position(self, symbol, side, margin_mode="crossed"):
        """Closes a position - adaptable for Testnet or Mainnet."""
        endpoint = "/api/mix/v1/order/placeOrder"
        method = "POST"
        timestamp = str(int(time.time() * 1000))
        params = {
            "symbol": symbol,
            "side": "SELL" if side.lower() == "long" else "BUY",
            "orderType": "MARKET",
            "marginMode": margin_mode.upper(),
            "size": "position_amount"
        }

        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": self.generate_signature(timestamp, method, endpoint, params),
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(self.api_url + endpoint, headers=headers, json=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error closing position: {e}")
            if response is not None:
                print(f"Response content: {response.text}")
            return None


# --- Example Usage demonstrating Testnet and Mainnet clients ---
if __name__ == "__main__":
    SYMBOL = "BTCUSDT_UMCBL" # Example Symbol - adjust if needed, Testnet symbols often same as Mainnet

    # --- 1. Initialize Testnet API Client ---
    print("\n--- Testing Bitget Testnet API ---")
    testnet_client = BitgetTestnetAPI(use_testnet=True) # Explicitly use Testnet

    # --- Place a Testnet Long Market Order ---
    testnet_long_order_response = testnet_client.place_order(
        symbol=SYMBOL,
        side="buy",
        order_type="market",
        quantity="0.01" # Example quantity - adjust
    )

    if testnet_long_order_response and testnet_long_order_response.get("code") == "00000":
        print("Testnet Long Market Order placed successfully!")
        print(json.dumps(testnet_long_order_response, indent=2))
    else:
        print("Testnet Failed to place long market order.")
        if testnet_long_order_response:
            print(json.dumps(testnet_long_order_response, indent=2))

    # --- Close Testnet Long Position ---
    if testnet_long_order_response and testnet_long_order_response.get("code") == "00000": # Only attempt to close if order placed
        testnet_close_long_response = testnet_client.close_position(
            symbol=SYMBOL,
            side="long"
        )
        if testnet_close_long_response and testnet_close_long_response.get("code") == "00000":
            print("Testnet Long position closed successfully!")
            print(json.dumps(testnet_close_long_response, indent=2))
        else:
            print("Testnet Failed to close long position.")
            if testnet_close_long_response:
                print(json.dumps(testnet_close_long_response, indent=2))


    # --- 2. Initialize Mainnet API Client (Use with extreme caution!) ---
    print("\n--- Example of using Mainnet API Client (WARNING: REAL MONEY!) ---")
    mainnet_client = BitgetTestnetAPI(use_testnet=False) # Set use_testnet=False for Mainnet

    # --- Example:  (Commented out for safety - DO NOT UNCOMMENT unless you understand the risk) ---
    #  WARNING: The following code will execute REAL trades if uncommented and run on the mainnet!
    #  Only uncomment and run on mainnet if you are absolutely sure and want to trade with real funds.

    # mainnet_long_order_response = mainnet_client.place_order(
    #     symbol=SYMBOL,
    #     side="buy",
    #     order_type="market",
    #     quantity="0.01" # Example quantity - adjust VERY carefully for mainnet!
    # )
    #
    # if mainnet_long_order_response and mainnet_long_order_response.get("code") == "00000":
    #     print("Mainnet Long Market Order (EXAMPLE - COMMENTED OUT FOR SAFETY) would have been placed!")
    #     print(json.dumps(mainnet_long_order_response, indent=2))
    # else:
    #     print("Mainnet Failed to place long market order (EXAMPLE - COMMENTED OUT FOR SAFETY).")
    #     if mainnet_long_order_response:
    #         print(json.dumps(mainnet_long_order_response, indent=2))


    print("\n--- IMPORTANT: Testnet Testing is Crucial ---")
    print("Remember to ALWAYS test your trading scripts thoroughly using the Testnet API")
    print("before even considering using them with real funds on the Mainnet.")
    print("This example script demonstrates how to switch between Testnet and Mainnet using the")
    print("`BitgetTestnetAPI` class and the `use_testnet` parameter.")
    print("Make sure your API keys and environment variables are correctly set for both environments.")
```

**Key features of this Testnet module and example:**

1.  **`BITGET_TESTNET_INFO` Constant:**  A string constant that provides detailed information about the Bitget Testnet, its purpose, and key differences from the mainnet. This is printed when you run the script to remind the user about testnet usage.

2.  **`BitgetTestnetAPI` Class:**
    *   **`__init__` Constructor:**
        *   Takes `use_testnet=True` as a parameter (defaulting to True for Testnet). This is the main switch to control whether the client uses the Testnet or Mainnet API.
        *   Sets `self.api_url` based on `use_testnet`.
        *   Retrieves API keys, Secret Keys, and Passphrases using `os.environ.get()`.  Crucially, it now checks for environment variables prefixed with `BITGET_TESTNET_` if `use_testnet` is True, and the standard `BITGET_` prefix if `use_testnet` is False.  This allows you to have *separate* API credentials for Testnet and Mainnet.
        *   Includes error handling to check if API credentials are set for the chosen environment.
    *   **`generate_signature`**, **`place_order`**, **`close_position` Methods:**
        *   These methods are largely the same as in the mainnet script, but they now use `self.api_url`, `self.api_key`, `self.secret_key`, and `self.passphrase` from the class instance, ensuring they use the correct credentials and API endpoint based on whether `use_testnet` was set to True or False during initialization.

3.  **Example Usage in `if __name__ == "__main__":`:**
    *   **Testnet Example:**
        *   Initializes `testnet_client = BitgetTestnetAPI(use_testnet=True)`.
        *   Places a testnet long market order and then attempts to close it.
        *   Prints clear messages indicating "Testnet" operations.
    *   **Mainnet Example (Commented out for safety):**
        *   Initializes `mainnet_client = BitgetTestnetAPI(use_testnet=False)`.
        *   Includes *commented-out* example code to place a mainnet long market order.
        *   **Important Warning:**  The mainnet example code is deliberately commented out and includes strong warnings to prevent accidental real trading when running the script.  **Users must understand the risks and uncomment/modify the mainnet example code very carefully if they intend to use it for real trading.**

**To use this Testnet module:**

1.  **Install `requests` library:** (if you haven't already)
    ```bash
    pip install requests
    ```

2.  **Get Bitget Testnet API Credentials:**
    *   You need to create a **separate account** on the Bitget Testnet platform.  Look for a "Testnet" or "Paper Trading" option on the Bitget website or documentation to sign up.
    *   Once you have a Testnet account, generate **Testnet API keys** from the API management section of your Testnet account.

3.  **Set Environment Variables for Testnet API Credentials:**
    *   Set the following environment variables for your **Testnet API keys**:
        ```bash
        export BITGET_TESTNET_API_KEY=your_testnet_api_key_value
        export BITGET_TESTNET_SECRET_KEY=your_testnet_secret_key_value
        export BITGET_TESTNET_PASSPHRASE=your_testnet_passphrase_value
        ```
        *(Replace `your_testnet_api_key_value`, etc., with your actual Testnet API credentials)*

    *   **If you want to run the Mainnet example (with extreme caution), also set your Mainnet API credentials as environment variables:**
        ```bash
        export BITGET_API_KEY=your_mainnet_api_key_value
        export BITGET_SECRET_KEY=your_mainnet_secret_key_value
        export BITGET_PASSPHRASE=your_mainnet_passphrase_value
        ```

4.  **Run the script:**
    ```bash
    python your_script_name.py
    ```
    This will:
    *   Print the Bitget Testnet information.
    *   Initialize a `BitgetTestnetAPI` client in Testnet mode.
    *   Attempt to place a testnet long market order and close it.
    *   Show an example of how to initialize a Mainnet client (but the mainnet trading example is commented out for safety).

**Key takeaways for Testnet testing:**

*   **Separate API Endpoint:**  Always use `https://api-testnet.bitget.com` for Testnet.
*   **Separate Accounts and API Keys:**  Use Testnet-specific accounts and API keys.
*   **Environment Variables:** Use environment variables to manage both Testnet and Mainnet API credentials, clearly distinguishing them with prefixes like `BITGET_TESTNET_`.
*   **`use_testnet` Parameter:** Utilize the `use_testnet` parameter in the `BitgetTestnetAPI` class to easily switch between Testnet and Mainnet API calls.
*   **Thorough Testing:**  Test all aspects of your trading script extensively on the Testnet before even considering real trading on the mainnet.

This module provides a robust and adaptable way to interact with both the Bitget Testnet and Mainnet APIs from your Python scripts, emphasizing the importance of risk-free testing before live trading.