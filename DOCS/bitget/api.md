Please be aware that trading cryptocurrencies and using automated trading scripts involves significant financial risk. **You should only use this script if you fully understand the risks involved and have a good understanding of trading and the Bitget API.**  Always test with a small amount of funds and on a testnet if available before using real money.

This script is a basic example and should be considered a starting point. You'll likely need to adapt and enhance it based on your specific trading strategy and risk management requirements.

Here's a Python script using the `requests` library to interact with the Bitget API to open and handle long and short positions.  This script provides basic functionality and you'll need to customize it further.

```python
import requests
import json
import time
import hmac
import hashlib
import os  # For environment variables

# --- Configuration ---
API_URL = "https://api.bitget.com"  # For mainnet. Use "https://api-testnet.bitget.com" for testnet
API_KEY = os.environ.get("BITGET_API_KEY")  # Set API key as environment variable
SECRET_KEY = os.environ.get("BITGET_SECRET_KEY") # Set secret key as environment variable
PASSPHRASE = os.environ.get("BITGET_PASSPHRASE") # Set passphrase as environment variable
SYMBOL = "BTCUSDT_UMCBL"  # Example: BTC/USDT Perpetual Contract - You might need to adjust this for your market

# --- Authentication Function ---
def generate_signature(timestamp, method, request_path, body=None):
    """Generates the signature required for Bitget API authentication."""
    message = str(timestamp) + method + request_path
    if body:
        message += json.dumps(body)
    hmac_obj = hmac.new(SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256)
    signature = hmac_obj.hexdigest()
    return signature

# --- Function to Place Order ---
def place_order(symbol, side, order_type, price=None, quantity=None, margin_mode="crossed", leverage="20"):
    """
    Places an order on Bitget.

    Args:
        symbol (str): Trading pair symbol (e.g., "BTCUSDT_UMCBL").
        side (str): "buy" for long, "sell" for short.
        order_type (str): "market" or "limit".
        price (str, optional): Limit price if order_type is "limit". Required for limit orders.
        quantity (str, optional): Order quantity (in base currency). Required for market and limit orders.
        margin_mode (str, optional): "crossed" or "isolated". Defaults to "crossed".
        leverage (str, optional): Leverage level. Defaults to "20".

    Returns:
        dict: API response in JSON format, or None if error.
    """

    endpoint = "/api/mix/v1/order/placeOrder"
    method = "POST"
    timestamp = str(int(time.time() * 1000))  # Millisecond timestamp
    params = {
        "symbol": symbol,
        "side": side.upper(), # API expects uppercase "BUY" or "SELL"
        "orderType": order_type.upper(), # API expects uppercase "MARKET" or "LIMIT"
        "marginMode": margin_mode.upper(),
        "leverage": leverage
    }

    if order_type.lower() == "limit":
        if price is None or quantity is None:
            print("Error: Price and quantity are required for limit orders.")
            return None
        params["price"] = price
        params["size"] = quantity  # 'size' is used for quantity in limit orders

    elif order_type.lower() == "market":
        if quantity is None:
            print("Error: Quantity is required for market orders.")
            return None
        params["size"] = quantity # 'size' is used for quantity in market orders


    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": generate_signature(timestamp, method, endpoint, params),
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL + endpoint, headers=headers, json=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error placing order: {e}")
        if response is not None:
            print(f"Response content: {response.text}") # Print response for debugging
        return None

# --- Function to Close Position (Market Close) ---
def close_position(symbol, side, margin_mode="crossed"):
    """
    Closes an existing position at market price.

    Args:
        symbol (str): Trading pair symbol (e.g., "BTCUSDT_UMCBL").
        side (str): "long" to close long position, "short" to close short position.
                     Important: Use the *opposite* side of the position you want to close.
                     To close a long position, use "sell". To close a short position, use "buy".
        margin_mode (str, optional): "crossed" or "isolated". Must match the position's margin mode. Defaults to "crossed".

    Returns:
        dict: API response in JSON format, or None if error.
    """

    endpoint = "/api/mix/v1/order/placeOrder" # Using same endpoint as placeOrder but with specific parameters
    method = "POST"
    timestamp = str(int(time.time() * 1000))
    params = {
        "symbol": symbol,
        "side": "SELL" if side.lower() == "long" else "BUY", # Opposite side to close position
        "orderType": "MARKET", # Closing at market price
        "marginMode": margin_mode.upper(),
        "size": "position_amount" # Special value to close the entire position at market. Check API docs for exact keyword.
    }

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": generate_signature(timestamp, method, endpoint, params),
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL + endpoint, headers=headers, json=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error closing position: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        return None


# --- Example Usage ---
if __name__ == "__main__":
    # --- 1. Open a Long Position (Market Order) ---
    long_order_response = place_order(
        symbol=SYMBOL,
        side="buy",
        order_type="market",
        quantity="0.01" # Example quantity - adjust based on your account and risk
    )

    if long_order_response and long_order_response.get("code") == "00000":
        print("Long market order placed successfully!")
        print(json.dumps(long_order_response, indent=2))
    else:
        print("Failed to place long market order.")
        if long_order_response:
            print(json.dumps(long_order_response, indent=2))


    # --- 2. Open a Short Position (Limit Order) ---
    short_order_response = place_order(
        symbol=SYMBOL,
        side="sell",
        order_type="limit",
        price="26000", # Example limit price - adjust based on market
        quantity="0.01" # Example quantity - adjust based on your account and risk
    )

    if short_order_response and short_order_response.get("code") == "00000":
        print("Short limit order placed successfully!")
        print(json.dumps(short_order_response, indent=2))
    else:
        print("Failed to place short limit order.")
        if short_order_response:
            print(json.dumps(short_order_response, indent=2))

    # --- 3. Close Long Position (Market Close) ---
    close_long_response = close_position(
        symbol=SYMBOL,
        side="long" # To close a long position, use "long" here
    )

    if close_long_response and close_long_response.get("code") == "00000":
        print("Long position closed successfully!")
        print(json.dumps(close_long_response, indent=2))
    else:
        print("Failed to close long position.")
        if close_long_response:
            print(json.dumps(close_long_response, indent=2))


    # --- 4. Close Short Position (Market Close) ---
    close_short_response = close_position(
        symbol=SYMBOL,
        side="short" # To close a short position, use "short" here
    )

    if close_short_response and close_short_response.get("code") == "00000":
        print("Short position closed successfully!")
        print(json.dumps(close_short_response, indent=2))
    else:
        print("Failed to close short position.")
        if close_short_response:
            print(json.dumps(close_short_response, indent=2))
```

**Before running this script:**

1.  **Install the `requests` library:**
    ```bash
    pip install requests
    ```

2.  **Get your Bitget API Credentials:**
    *   Log in to your Bitget account.
    *   Go to the API management section (usually under your profile or security settings).
    *   Create an API key.  Make sure it has the necessary permissions for trading (Futures/Contracts trading permissions).
    *   **Important:**  Store your `API Key`, `Secret Key`, and `Passphrase` securely. **Do not hardcode them directly into the script.** Use environment variables as shown in the example.
    *   **Set Environment Variables:**
        *   Set the following environment variables on your system:
            *   `BITGET_API_KEY` = your API key
            *   `BITGET_SECRET_KEY` = your Secret Key
            *   `BITGET_PASSPHRASE` = your Passphrase

3.  **Choose the Correct `API_URL`:**
    *   For **real trading** on the Bitget mainnet, use: `API_URL = "https://api.bitget.com"`
    *   For **testing** and practicing without real funds, use the Bitget Testnet: `API_URL = "https://api-testnet.bitget.com"`  (You'll need to create a Testnet account separately).

4.  **Set the `SYMBOL`:**
    *   Modify the `SYMBOL` variable to the trading pair you want to trade (e.g., "ETHUSDT_UMCBL", "XRPUSDT_UMCBL", etc.). Ensure it's a valid symbol on Bitget.

5.  **Understand the Functions and Parameters:**
    *   **`place_order()` function:**
        *   `symbol`:  Trading symbol.
        *   `side`: "buy" (long) or "sell" (short).
        *   `order_type`: "market" or "limit".
        *   `price`: (For limit orders) The limit price at which you want to buy or sell.
        *   `quantity`: The amount of the base currency you want to trade.
        *   `margin_mode`: "crossed" or "isolated" (check your Bitget account settings).
        *   `leverage`: Your desired leverage.
    *   **`close_position()` function:**
        *   `symbol`: Trading symbol of the position to close.
        *   `side`:  Crucially, to close a **long** position, you use `"long"` here (the function will internally send a "SELL" order). To close a **short** position, you use `"short"` (and the function sends a "BUY"). This is because closing a long position involves selling, and closing a short position involves buying back.
        *   `margin_mode`: Must match the margin mode of the position you are closing.

6.  **Run the script:**
    ```bash
    python your_script_name.py
    ```

**Important Security and Risk Considerations:**

*   **API Key Security:** Protect your API keys and passphrases like passwords.  **Never hardcode them into your script.** Use environment variables or secure configuration files.
*   **Test in Testnet:**  **Always, always test your script thoroughly on the Bitget Testnet first** with fake money before using it with real funds on the mainnet. This will help you catch errors and understand how the script works without risking real capital.
*   **Error Handling:** The script includes basic error handling, but you should improve it for production use.  Implement more robust error logging, retry mechanisms, and checks for specific API error codes.
*   **Risk Management:**  Implement proper risk management in your trading strategy. This script only handles order placement. You'll need to add logic for:
    *   Position sizing (how much to trade).
    *   Stop-loss orders (to limit potential losses).
    *   Take-profit orders (to secure profits).
    *   Trading strategy logic (when to open and close positions based on market conditions).
*   **API Rate Limits:** Be mindful of Bitget API rate limits.  If you make too many requests too quickly, you might get temporarily blocked. Implement delays or use techniques to manage your request rate.
*   **Market Volatility:** Cryptocurrency markets are highly volatile. Automated trading can lead to rapid losses if not properly managed.
*   **Monitor Your Trades:**  Even with automated trading, it's essential to monitor your trades regularly and be prepared to intervene manually if necessary.

**Disclaimer:** I am an AI and cannot provide financial or trading advice. This script is for educational purposes only. Trading cryptocurrencies is risky, and you could lose money. Use this script at your own risk.  Always do your own research and understand the risks before trading. Consult with a qualified financial advisor if needed.