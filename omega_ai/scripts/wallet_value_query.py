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
OMEGA BTC AI - Wallet Value Query
=================================

A script to query wallet value from BitGet using the direct API.
Uses a more thorough authentication approach to avoid signature errors.

Author: OMEGA BTC AI Team
"""

import os
import sys
import json
import hmac
import base64
import time
import hashlib
import requests
import argparse
from typing import Dict, Any, Optional
from urllib.parse import urlencode
from datetime import datetime
from colorama import Fore, Style, init

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Initialize colorama
init(autoreset=True)

class BitGetWalletQuery:
    """Query BitGet wallet information with direct API access."""
    
    def __init__(self, use_testnet=False, api_key=None, secret_key=None, passphrase=None, debug=False):
        """
        Initialize the wallet query.
        
        Args:
            use_testnet: Whether to use testnet (default: False)
            api_key: BitGet API key (if None, will try to get from environment)
            secret_key: BitGet API secret key (if None, will try to get from environment)
            passphrase: BitGet API passphrase (if None, will try to get from environment)
            debug: Enable debug mode (default: False)
        """
        self.use_testnet = use_testnet
        self.debug = debug
        
        # Set API URLs based on testnet or mainnet
        if use_testnet:
            self.api_url = "https://api-testnet.bitget.com"
        else:
            self.api_url = "https://api.bitget.com"
            
        # Get API credentials from parameters or environment variables
        self.api_key = api_key or os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
        self.secret_key = secret_key or os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
        self.passphrase = passphrase or os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
        
        # Verify API credentials
        if not all([self.api_key, self.secret_key, self.passphrase]):
            print(f"{Fore.RED}Error: API credentials missing. Please provide API key, secret key, and passphrase.{Style.RESET_ALL}")
            sys.exit(1)
        
        print(f"{Fore.GREEN}API credentials loaded. API Key: {self.api_key[:5]}...{self.api_key[-3:] if len(self.api_key) > 5 else ''}{Style.RESET_ALL}")

    def generate_signature(self, timestamp, method, request_path, body=None, params=None):
        """
        Generate the signature for BitGet API authentication.
        
        Args:
            timestamp: Timestamp in milliseconds
            method: HTTP method (GET, POST, etc.)
            request_path: API endpoint path
            body: Request body for POST requests
            params: Query parameters for GET requests
            
        Returns:
            base64-encoded HMAC-SHA256 signature
        """
        # Ensure method is uppercase as required by BitGet
        method = method.upper()
        
        # Start with timestamp + method + requestPath
        message = str(timestamp) + method + request_path
        
        # Add query string if present (for GET requests)
        if params and method == "GET":
            # Sort parameters by key as required by BitGet
            sorted_params = sorted(params.items())
            # Create query string
            query_string = "&".join([f"{key}={value}" for key, value in sorted_params])
            # Add to message with question mark
            message += "?" + query_string
        
        # Add request body if present (for POST requests)
        if body and method == "POST":
            if isinstance(body, dict):
                message += json.dumps(body)
            else:
                message += body
                
        if self.debug:
            print(f"{Fore.YELLOW}Pre-signed message: {message}{Style.RESET_ALL}")
            
        # Create signature using HMAC-SHA256
        signature = base64.b64encode(
            hmac.new(
                self.secret_key.encode("utf-8"), 
                message.encode("utf-8"), 
                hashlib.sha256
            ).digest()
        ).decode("utf-8")
        
        return signature
    
    def make_request(self, method, endpoint, params=None, body=None):
        """
        Make an authenticated request to the BitGet API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint to access
            params: Query parameters for GET requests
            body: Request body for POST requests
            
        Returns:
            Response data from the API
        """
        # Prepare the request
        url = self.api_url + endpoint
        timestamp = str(int(time.time() * 1000))
        
        # Generate signature
        signature = self.generate_signature(timestamp, method, endpoint, body, params)
        
        # Prepare headers with authentication
        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json"
        }
        
        if self.debug:
            print(f"\n{Fore.YELLOW}=== API Request Details ==={Style.RESET_ALL}")
            print(f"URL: {url}")
            print(f"Method: {method}")
            print(f"Timestamp: {timestamp}")
            print(f"Params: {params}")
            print(f"Headers: {json.dumps({k: v for k, v in headers.items() if k != 'ACCESS-SIGN'}, indent=2)}")
            print(f"Signature: {signature}")
        
        # Make the request
        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=headers)
            elif method == "POST":
                response = requests.post(url, json=body, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            # Check if response is valid JSON
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = {"error": "Invalid JSON response", "text": response.text}
                
            if self.debug:
                print(f"\n{Fore.YELLOW}=== API Response Details ==={Style.RESET_ALL}")
                print(f"Status Code: {response.status_code}")
                print(f"Response: {json.dumps(response_data, indent=2)}")
                
            # Check for successful response
            if response.status_code == 200 and response_data.get("code") == "00000":
                return response_data.get("data", {})
            else:
                if self.debug:
                    print(f"{Fore.RED}Error response: {response_data}{Style.RESET_ALL}")
                return {"error": response_data.get("msg", "Unknown error")}
                
        except Exception as e:
            error_message = f"Request error: {str(e)}"
            if self.debug:
                print(f"{Fore.RED}{error_message}{Style.RESET_ALL}")
            return {"error": error_message}
    
    def get_account_balance(self):
        """
        Get account balance information.
        
        Returns:
            Account balance data
        """
        endpoint = "/api/mix/v1/account/account"
        params = {
            "productType": "umcbl",  # Mix contract product type
            "marginCoin": "USDT"     # Margin currency
        }
        
        return self.make_request("GET", endpoint, params)
    
    def get_all_positions(self):
        """
        Get all current positions.
        
        Returns:
            List of positions
        """
        endpoint = "/api/mix/v1/position/allPosition"
        params = {
            "productType": "umcbl",  # Mix contract product type
            "marginCoin": "USDT"     # Margin currency
        }
        
        return self.make_request("GET", endpoint, params)
    
    def get_spot_assets(self):
        """
        Get spot wallet assets.
        
        Returns:
            List of spot assets
        """
        endpoint = "/api/spot/v1/account/assets"
        
        return self.make_request("GET", endpoint)
    
    def get_futures_assets(self):
        """
        Get futures wallet assets.
        
        Returns:
            List of futures assets
        """
        endpoint = "/api/mix/v1/account/assets"
        params = {
            "productType": "umcbl"  # Mix contract product type
        }
        
        return self.make_request("GET", endpoint, params)

    def print_wallet_summary(self):
        """Print a summary of the wallet balances and positions."""
        # Get account balance
        account_info = self.get_account_balance()
        
        if isinstance(account_info, dict) and "error" in account_info:
            print(f"{Fore.RED}Error getting account balance: {account_info.get('error', 'Unknown error')}{Style.RESET_ALL}")
            account_info = {}
        
        # Get all positions
        positions = self.get_all_positions()
        
        if isinstance(positions, dict) and "error" in positions:
            print(f"{Fore.RED}Error getting positions: {positions.get('error', 'Unknown error')}{Style.RESET_ALL}")
            positions = []
        elif not isinstance(positions, list):
            positions = []
        
        # Get spot assets
        spot_assets = self.get_spot_assets()
        
        if isinstance(spot_assets, dict) and "error" in spot_assets:
            print(f"{Fore.RED}Error getting spot assets: {spot_assets.get('error', 'Unknown error')}{Style.RESET_ALL}")
            spot_assets = []
        elif not isinstance(spot_assets, list):
            spot_assets = []
        
        # Get futures assets
        futures_assets = self.get_futures_assets()
        
        if isinstance(futures_assets, dict) and "error" in futures_assets:
            print(f"{Fore.RED}Error getting futures assets: {futures_assets.get('error', 'Unknown error')}{Style.RESET_ALL}")
            futures_assets = []
        elif not isinstance(futures_assets, list):
            futures_assets = []
            
        # Calculate total values
        total_futures_equity = sum(float(asset.get("equity", 0)) for asset in (futures_assets or []))
        total_spot_value = sum(float(asset.get("available", 0)) + float(asset.get("frozen", 0)) 
                              for asset in (spot_assets or []) if asset.get("coinName") == "USDT")
        
        # Calculate PnL values with detailed breakdown
        unrealized_pnl_by_symbol = {}
        realized_pnl_by_symbol = {}
        
        for pos in (positions or []):
            symbol = pos.get("symbol", "UNKNOWN")
            unrealized = float(pos.get("unrealizedPL", 0))
            realized = float(pos.get("achievedProfits", 0))
            
            if symbol not in unrealized_pnl_by_symbol:
                unrealized_pnl_by_symbol[symbol] = 0
                realized_pnl_by_symbol[symbol] = 0
                
            unrealized_pnl_by_symbol[symbol] += unrealized
            realized_pnl_by_symbol[symbol] += realized
            
        total_unrealized_pnl = sum(unrealized_pnl_by_symbol.values())
        total_realized_pnl = sum(realized_pnl_by_symbol.values())
        total_pnl = total_unrealized_pnl + total_realized_pnl
        
        # Display wallet address (using API key as identifier)
        wallet_address = f"BitGet:{self.api_key[:8]}..."
        
        # Print summary
        print(f"\n{Fore.CYAN}===== WALLET SUMMARY ====={Style.RESET_ALL}")
        print(f"{Fore.CYAN}Wallet Address: {Fore.GREEN}{wallet_address}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Mode: {Fore.GREEN}{'TESTNET' if self.use_testnet else 'MAINNET'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Time: {Fore.GREEN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        
        # Account information - use safe dictionary access
        if isinstance(account_info, dict):
            try:
                equity = float(account_info.get("equity", 0))
                available = float(account_info.get("available", 0))
                
                print(f"\n{Fore.MAGENTA}--- FUTURES ACCOUNT ---{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}Total Equity: {Fore.GREEN}{equity:.2f} USDT{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}Available: {Fore.GREEN}{available:.2f} USDT{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}In Use: {Fore.YELLOW}{(equity - available):.2f} USDT{Style.RESET_ALL}")
            except (ValueError, TypeError) as e:
                if self.debug:
                    print(f"{Fore.RED}Error parsing account info: {str(e)}{Style.RESET_ALL}")
        
        # PnL summary with detailed breakdown
        if positions:
            print(f"\n{Fore.MAGENTA}===== PNL BREAKDOWN ====={Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}Total Positions: {Fore.CYAN}{len(positions)}{Style.RESET_ALL}")
            
            # Print PnL by symbol
            if unrealized_pnl_by_symbol or realized_pnl_by_symbol:
                print(f"\n{Fore.YELLOW}PnL by Symbol:{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{'Symbol':<12} {'Unrealized':<15} {'Realized':<15} {'Total':<15}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{'------':<12} {'---------':<15} {'--------':<15} {'-----':<15}{Style.RESET_ALL}")
                
                # Get all symbols from both dictionaries
                all_symbols = set(list(unrealized_pnl_by_symbol.keys()) + list(realized_pnl_by_symbol.keys()))
                
                for symbol in sorted(all_symbols):
                    unrealized = unrealized_pnl_by_symbol.get(symbol, 0)
                    realized = realized_pnl_by_symbol.get(symbol, 0)
                    total = unrealized + realized
                    
                    # Format with colors based on values
                    unrealized_color = Fore.GREEN if unrealized >= 0 else Fore.RED
                    realized_color = Fore.GREEN if realized >= 0 else Fore.RED
                    total_color = Fore.GREEN if total >= 0 else Fore.RED
                    
                    print(f"{Fore.CYAN}{symbol:<12} "
                          f"{unrealized_color}{unrealized:+.2f} USDT{Style.RESET_ALL:<4} "
                          f"{realized_color}{realized:+.2f} USDT{Style.RESET_ALL:<4} "
                          f"{total_color}{total:+.2f} USDT{Style.RESET_ALL:<4}")
                
                # Print the totals
                print(f"{Fore.YELLOW}{'-'*60}{Style.RESET_ALL}")
                unrealized_total_color = Fore.GREEN if total_unrealized_pnl >= 0 else Fore.RED
                realized_total_color = Fore.GREEN if total_realized_pnl >= 0 else Fore.RED
                total_color = Fore.GREEN if total_pnl >= 0 else Fore.RED
                
                print(f"{Fore.YELLOW}{'TOTAL':<12} "
                      f"{unrealized_total_color}{total_unrealized_pnl:+.2f} USDT{Style.RESET_ALL:<4} "
                      f"{realized_total_color}{total_realized_pnl:+.2f} USDT{Style.RESET_ALL:<4} "
                      f"{total_color}{total_pnl:+.2f} USDT{Style.RESET_ALL:<4}")
            
            # Display individual positions
            print(f"\n{Fore.MAGENTA}Position Details:{Style.RESET_ALL}")
            for pos in positions:
                symbol = pos.get("symbol", "UNKNOWN")
                side = pos.get("holdSide", "UNKNOWN").upper()
                size = float(pos.get("total", 0))
                entry_price = float(pos.get("averageOpenPrice", 0))
                unrealized_pnl = float(pos.get("unrealizedPL", 0))
                realized_pnl = float(pos.get("achievedProfits", 0))
                leverage = int(pos.get("leverage", 1))
                market_price = float(pos.get("marketPrice", 0))
                
                # Calculate percentage gain/loss
                if entry_price > 0:
                    if side == "LONG":
                        pct_change = ((market_price - entry_price) / entry_price) * 100
                    else:  # SHORT
                        pct_change = ((entry_price - market_price) / entry_price) * 100
                else:
                    pct_change = 0
                
                # Format with color
                side_colored = f"{Fore.GREEN}{side}{Style.RESET_ALL}" if side == "LONG" else f"{Fore.RED}{side}{Style.RESET_ALL}"
                pct_change_colored = f"{Fore.GREEN}+{pct_change:.2f}%{Style.RESET_ALL}" if pct_change >= 0 else f"{Fore.RED}{pct_change:.2f}%{Style.RESET_ALL}"
                unrealized_pnl_colored = f"{Fore.GREEN}+{unrealized_pnl:.2f}{Style.RESET_ALL}" if unrealized_pnl >= 0 else f"{Fore.RED}{unrealized_pnl:.2f}{Style.RESET_ALL}"
                realized_pnl_colored = f"{Fore.GREEN}+{realized_pnl:.2f}{Style.RESET_ALL}" if realized_pnl >= 0 else f"{Fore.RED}{realized_pnl:.2f}{Style.RESET_ALL}"
                
                print(f"  {Fore.CYAN}{symbol}{Style.RESET_ALL}: {side_colored} {size:.4f} @ {entry_price:.2f} → {market_price:.2f} {pct_change_colored}")
                print(f"     {Fore.YELLOW}Leverage:{Style.RESET_ALL} {leverage}x | {Fore.YELLOW}Unrealized:{Style.RESET_ALL} {unrealized_pnl_colored} | {Fore.YELLOW}Realized:{Style.RESET_ALL} {realized_pnl_colored}")
        
        # Overall total value
        total_value = total_futures_equity + total_spot_value
        
        # Add PnL to the total value calculation
        adjusted_total = total_value
        if positions:
            print(f"\n{Fore.CYAN}===== ACCOUNT VALUE SUMMARY ====={Style.RESET_ALL}")
            print(f"{Fore.CYAN}Base Account Value: {Fore.GREEN}{total_value:.2f} USDT{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Unrealized PnL: {Fore.GREEN if total_unrealized_pnl >= 0 else Fore.RED}{total_unrealized_pnl:+.2f} USDT{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Realized PnL: {Fore.GREEN if total_realized_pnl >= 0 else Fore.RED}{total_realized_pnl:+.2f} USDT{Style.RESET_ALL}")
            
            # Calculate adjusted total including PnL
            adjusted_total = total_value + total_pnl
            total_color = Fore.GREEN if adjusted_total >= 0 else Fore.RED
            print(f"{Fore.CYAN}TOTAL VALUE: {total_color}{adjusted_total:.2f} USDT{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.CYAN}===== TOTAL WALLET VALUE ====={Style.RESET_ALL}")
            print(f"{Fore.CYAN}Futures: {Fore.GREEN}{total_futures_equity:.2f} USDT{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Spot (USDT): {Fore.GREEN}{total_spot_value:.2f} USDT{Style.RESET_ALL}")
            print(f"{Fore.CYAN}TOTAL VALUE: {Fore.GREEN}{total_value:.2f} USDT{Style.RESET_ALL}")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="BitGet Wallet Value Query")
    parser.add_argument("--testnet", action="store_true", help="Use testnet (default: False)")
    parser.add_argument("--mainnet", action="store_true", help="Use mainnet (default: True)")
    parser.add_argument("--api-key", type=str, help="BitGet API key")
    parser.add_argument("--secret-key", type=str, help="BitGet secret key")
    parser.add_argument("--passphrase", type=str, help="BitGet API passphrase")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode (default: False)")
    
    return parser.parse_args()

def main():
    """Main entry point for the wallet value query."""
    args = parse_args()
    
    # Determine if we should use testnet
    use_testnet = args.testnet and not args.mainnet
    
    print(f"{Fore.GREEN}BitGet Wallet Value Query{Style.RESET_ALL}")
    print(f"{Fore.GREEN}=============================={Style.RESET_ALL}")
    print(f"{Fore.GREEN}Mode: {'TESTNET' if use_testnet else 'MAINNET'}{Style.RESET_ALL}")
    
    # Initialize wallet query
    wallet_query = BitGetWalletQuery(
        use_testnet=use_testnet,
        api_key=args.api_key,
        secret_key=args.secret_key, 
        passphrase=args.passphrase,
        debug=args.debug
    )
    
    # Print wallet summary
    wallet_query.print_wallet_summary()

if __name__ == "__main__":
    main() 