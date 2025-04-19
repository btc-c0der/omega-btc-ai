#!/usr/bin/env python3

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
OMEGA BTC AI - Wallet Info Retriever
====================================

A simple script to retrieve wallet information from BitGet.
Uses the same authentication approach as the BitGet live traders.

Author: OMEGA BTC AI Team
"""

import os
import sys
import json
import argparse
from colorama import Fore, Style, init
import requests
import hmac
import hashlib
import base64
import time
from urllib.parse import urlencode

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Initialize colorama
init(autoreset=True)

def generate_signature(api_secret, method, endpoint, timestamp, params=None, body=None):
    """Generate signature for BitGet API request."""
    message = timestamp + method + endpoint
    
    # Add query parameters to message if present
    if params and method == 'GET':
        query_string = urlencode(sorted(params.items()))
        message += '?' + query_string
    
    # Add request body to message if present
    if body and method != 'GET':
        message += json.dumps(body)
    
    # Create signature using HMAC-SHA256
    signature = base64.b64encode(
        hmac.new(
            api_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
    ).decode('utf-8')
    
    return signature

def get_wallet_info(use_testnet=False, debug=False):
    """Retrieve wallet information from BitGet."""
    # Get API credentials from environment variables
    api_key = os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
    api_secret = os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
    passphrase = os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
    
    # Check if API credentials are available
    if not api_key or not api_secret or not passphrase:
        print(f"{Fore.RED}Error: API credentials are missing. Please set environment variables.{Style.RESET_ALL}")
        print(f"Required variables: {'BITGET_TESTNET_API_KEY' if use_testnet else 'BITGET_API_KEY'}, " + 
              f"{'BITGET_TESTNET_SECRET_KEY' if use_testnet else 'BITGET_SECRET_KEY'}, " +
              f"{'BITGET_TESTNET_PASSPHRASE' if use_testnet else 'BITGET_PASSPHRASE'}")
        sys.exit(1)
    
    # API endpoint for account information
    api_url = "https://api-testnet.bitget.com" if use_testnet else "https://api.bitget.com"
    endpoint = "/api/mix/v1/account/account"
    method = "GET"
    timestamp = str(int(time.time() * 1000))
    
    # Query parameters
    params = {
        "productType": "umcbl",
        "marginCoin": "USDT"
    }
    
    # Generate signature
    signature = generate_signature(api_secret, method, endpoint, timestamp, params)
    
    # Prepare headers
    headers = {
        "ACCESS-KEY": api_key,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": passphrase,
        "Content-Type": "application/json"
    }
    
    # Prepare URL
    url = api_url + endpoint
    
    # Print debug information if requested
    if debug:
        print(f"{Fore.YELLOW}=== Request Information ==={Style.RESET_ALL}")
        print(f"URL: {url}")
        print(f"Method: {method}")
        print(f"Timestamp: {timestamp}")
        print(f"Params: {params}")
        print(f"Signature: {signature}")
        print(f"Headers: {json.dumps(headers, indent=2)}")
    
    # Make the request
    try:
        response = requests.get(url, params=params, headers=headers)
        
        # Print debug information if requested
        if debug:
            print(f"{Fore.YELLOW}=== Response Information ==={Style.RESET_ALL}")
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
            print(f"Response Body: {json.dumps(response.json(), indent=2) if response.text else 'No response body'}")
        
        # Format the wallet information
        if response.status_code == 200 and response.json().get("code") == "00000":
            data = response.json().get("data", {})
            wallet_info = {
                "wallet_address": f"BitGet:{api_key[:8]}...",
                "total_balance": float(data.get("equity", 0)),
                "available_balance": float(data.get("available", 0)),
                "unrealized_pnl": float(data.get("unrealizedPL", 0)),
                "margin_balance": float(data.get("marginBalance", 0)),
                "margin_coin": data.get("marginCoin", "USDT"),
                "account_mode": "Testnet" if use_testnet else "Mainnet"
            }
            
            return wallet_info
        else:
            error_msg = response.json().get("msg", "Unknown error")
            print(f"{Fore.RED}Error retrieving wallet information: {error_msg}{Style.RESET_ALL}")
            
            # Special handling for sign signature error
            if "sign signature error" in error_msg.lower():
                print(f"{Fore.YELLOW}Authentication error: Signature verification failed.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Please check your API credentials and ensure they have proper permissions.{Style.RESET_ALL}")
            
            # Fallback to minimal wallet info
            return {
                "wallet_address": f"BitGet:{api_key[:8]}...",
                "account_mode": "Testnet" if use_testnet else "Mainnet",
                "error": error_msg
            }
    
    except Exception as e:
        print(f"{Fore.RED}Exception retrieving wallet information: {str(e)}{Style.RESET_ALL}")
        
        # Fallback to minimal wallet info
        return {
            "wallet_address": f"BitGet:{api_key[:8]}...",
            "account_mode": "Testnet" if use_testnet else "Mainnet",
            "error": str(e)
        }

def main():
    """Main entry point for the wallet info script."""
    parser = argparse.ArgumentParser(description="OMEGA BTC AI - Wallet Info Retriever")
    parser.add_argument("--testnet", action="store_true", help="Use testnet (default: False)")
    parser.add_argument("--mainnet", action="store_true", help="Use mainnet (default: True)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode (default: False)")
    args = parser.parse_args()
    
    # Determine if we should use testnet
    use_testnet = args.testnet or not args.mainnet
    
    print(f"{Fore.GREEN}OMEGA BTC AI - Wallet Info Retriever{Style.RESET_ALL}")
    print(f"{Fore.GREEN}==============================={Style.RESET_ALL}")
    print(f"{Fore.CYAN}Mode: {'Testnet' if use_testnet else 'Mainnet'}{Style.RESET_ALL}")
    
    # Get wallet information
    wallet_info = get_wallet_info(use_testnet, args.debug)
    
    # Print wallet information
    print(f"\n{Fore.MAGENTA}===== WALLET INFORMATION ====={Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Wallet Address: {Fore.CYAN}{wallet_info.get('wallet_address', 'Not available')}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Account Mode: {Fore.CYAN}{wallet_info.get('account_mode', 'Unknown')}{Style.RESET_ALL}")
    
    if "error" in wallet_info:
        print(f"{Fore.RED}Error: {wallet_info['error']}{Style.RESET_ALL}")
    else:
        print(f"{Fore.MAGENTA}Total Balance: {Fore.CYAN}{wallet_info.get('total_balance', 0):.2f} {wallet_info.get('margin_coin', 'USDT')}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Available Balance: {Fore.CYAN}{wallet_info.get('available_balance', 0):.2f} {wallet_info.get('margin_coin', 'USDT')}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Unrealized PnL: {Fore.CYAN}{wallet_info.get('unrealized_pnl', 0):.2f} {wallet_info.get('margin_coin', 'USDT')}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Margin Balance: {Fore.CYAN}{wallet_info.get('margin_balance', 0):.2f} {wallet_info.get('margin_coin', 'USDT')}{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 