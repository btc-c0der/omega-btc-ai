"""
OMEGA BTC AI - BitGet Market Order Executor
===========================================

This script provides a simple way to execute market orders on BitGet exchange.
It can be used to quickly place buy or sell orders for testing or manual trading.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import requests
import time
import hmac
import hashlib
import base64
import json
import argparse
import os
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

class BitGetOrderExecutor:
    """Simple utility for executing market orders on BitGet."""
    
    def __init__(self, 
                api_key: str = "", 
                secret_key: str = "", 
                passphrase: str = "",
                use_testnet: bool = True):
        """
        Initialize the BitGet order executor.
        
        Args:
            api_key: BitGet API key
            secret_key: BitGet secret key
            passphrase: BitGet API passphrase
            use_testnet: Whether to use testnet (default: True)
        """
        # Look for API credentials in environment variables if not provided
        self.api_key = api_key or os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
        self.secret_key = secret_key or os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
        self.passphrase = passphrase or os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
        
        # Set base URL based on testnet or mainnet
        self.base_url = "https://api-testnet.bitget.com" if use_testnet else "https://api.bitget.com"
        self.use_testnet = use_testnet
        
        # Log API credentials status
        if not self.api_key or not self.secret_key or not self.passphrase:
            logger.warning(f"{YELLOW}One or more API credentials are missing. API authentication will fail.{RESET}")
        else:
            logger.info(f"{GREEN}API credentials loaded successfully.{RESET}")
            logger.info(f"{CYAN}Using {'TESTNET' if use_testnet else 'MAINNET'} environment.{RESET}")
    
    def get_signature(self, timestamp: str, method: str, request_path: str, body: str = "") -> str:
        """
        Generate BitGet API signature.
        
        Args:
            timestamp: Current timestamp in milliseconds
            method: HTTP method (GET, POST, etc.)
            request_path: API endpoint path
            body: Request body as JSON string (for POST requests)
            
        Returns:
            Base64 encoded signature
        """
        message = timestamp + method + request_path + body
        return base64.b64encode(
            hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).digest()
        ).decode()
    
    def place_market_order(self, 
                          symbol: str = "BTCUSDT", 
                          size: str = "0.001",
                          side: str = "buy") -> Dict[str, Any]:
        """
        Place a market order on BitGet.
        
        Args:
            symbol: Trading symbol (e.g., "BTCUSDT")
            size: Order size
            side: Order side ("buy" or "sell")
            
        Returns:
            Response from the BitGet API
        """
        # Format symbol for BitGet UMCBL (USDT Margined Contracts)
        formatted_symbol = f"{symbol}_UMCBL"
        
        # Current time for API signature
        timestamp = str(int(time.time() * 1000))
        
        # Define order parameters
        order_payload = {
            "symbol": formatted_symbol,
            "size": size,  # Quantity to buy/sell
            "side": side,  # "buy" or "sell"
            "orderType": "market",  # Market order
            "price": "",  # Not used for market orders
            "force": "gtc"  # Good-Till-Cancelled
        }
        
        # Convert payload to JSON string for signature
        payload_json = json.dumps(order_payload)
        
        # BitGet API request path for futures order
        request_path = "/api/mix/v1/order/placeOrder"
        
        # Generate signature
        signature = self.get_signature(timestamp, "POST", request_path, payload_json)
        
        # Prepare headers
        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json",
        }
        
        # Log order details before sending
        logger.info(f"{BLUE}Placing {'BUY' if side == 'buy' else 'SELL'} order for {size} {symbol}{RESET}")
        logger.info(f"{CYAN}Order payload: {payload_json}{RESET}")
        
        # Execute API request
        try:
            response = requests.post(
                self.base_url + request_path, 
                headers=headers, 
                json=order_payload
            )
            
            # Parse response
            response_data = response.json()
            
            # Log response
            if response.status_code == 200 and response_data.get('code') == '00000':
                logger.info(f"{GREEN}Order placed successfully!{RESET}")
                logger.info(f"{GREEN}Order ID: {response_data.get('data', {}).get('orderId')}{RESET}")
            else:
                logger.error(f"{RED}Order placement failed!{RESET}")
                logger.error(f"{RED}Status code: {response.status_code}{RESET}")
                logger.error(f"{RED}Response: {json.dumps(response_data, indent=2)}{RESET}")
            
            return response_data
            
        except Exception as e:
            logger.error(f"{RED}Error placing order: {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            return {"error": str(e)}
    
    def get_account_balance(self) -> Dict[str, Any]:
        """
        Get account balance from BitGet.
        
        Returns:
            Account balance information
        """
        timestamp = str(int(time.time() * 1000))
        request_path = "/api/mix/v1/account/accounts"
        
        # Generate signature
        signature = self.get_signature(timestamp, "GET", request_path)
        
        # Prepare headers
        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json",
        }
        
        # Execute API request
        try:
            response = requests.get(
                self.base_url + request_path, 
                headers=headers
            )
            
            # Parse response
            response_data = response.json()
            
            # Log response
            if response.status_code == 200 and response_data.get('code') == '00000':
                logger.info(f"{GREEN}Account balance retrieved successfully!{RESET}")
                
                # Format and display balance information
                if 'data' in response_data and isinstance(response_data['data'], list):
                    for account in response_data['data']:
                        symbol = account.get('marginCoin', 'UNKNOWN')
                        available = account.get('available', '0')
                        equity = account.get('equity', '0')
                        
                        logger.info(f"{CYAN}{symbol} Balance:{RESET}")
                        logger.info(f"{CYAN}  Available: {available}{RESET}")
                        logger.info(f"{CYAN}  Equity: {equity}{RESET}")
            else:
                logger.error(f"{RED}Failed to retrieve account balance!{RESET}")
                logger.error(f"{RED}Status code: {response.status_code}{RESET}")
                logger.error(f"{RED}Response: {json.dumps(response_data, indent=2)}{RESET}")
            
            return response_data
            
        except Exception as e:
            logger.error(f"{RED}Error retrieving account balance: {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            return {"error": str(e)}
    
    def get_positions(self, symbol: str = "BTCUSDT") -> Dict[str, Any]:
        """
        Get current positions for a symbol.
        
        Args:
            symbol: Trading symbol (e.g., "BTCUSDT")
            
        Returns:
            Current positions information
        """
        # Format symbol for BitGet UMCBL (USDT Margined Contracts)
        formatted_symbol = f"{symbol}_UMCBL"
        
        timestamp = str(int(time.time() * 1000))
        request_path = f"/api/mix/v1/position/singlePosition?symbol={formatted_symbol}"
        
        # Generate signature
        signature = self.get_signature(timestamp, "GET", request_path)
        
        # Prepare headers
        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json",
        }
        
        # Execute API request
        try:
            response = requests.get(
                self.base_url + request_path, 
                headers=headers
            )
            
            # Parse response
            response_data = response.json()
            
            # Log response
            if response.status_code == 200 and response_data.get('code') == '00000':
                logger.info(f"{GREEN}Positions for {symbol} retrieved successfully!{RESET}")
                
                # Format and display position information
                if 'data' in response_data and isinstance(response_data['data'], list):
                    for position in response_data['data']:
                        side = position.get('holdSide', 'UNKNOWN')
                        size = position.get('total', '0')
                        avg_price = position.get('averageOpenPrice', '0')
                        unrealized_pnl = position.get('unrealizedPL', '0')
                        
                        logger.info(f"{CYAN}Position: {side} {size} {symbol} @ {avg_price}{RESET}")
                        logger.info(f"{CYAN}  Unrealized PnL: {unrealized_pnl}{RESET}")
            else:
                logger.error(f"{RED}Failed to retrieve positions!{RESET}")
                logger.error(f"{RED}Status code: {response.status_code}{RESET}")
                logger.error(f"{RED}Response: {json.dumps(response_data, indent=2)}{RESET}")
            
            return response_data
            
        except Exception as e:
            logger.error(f"{RED}Error retrieving positions: {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            return {"error": str(e)}

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='BitGet Market Order Executor')
    
    parser.add_argument('--symbol', type=str, default='BTCUSDT',
                      help='Trading symbol (default: BTCUSDT)')
    parser.add_argument('--size', type=str, default='0.001',
                      help='Order size (default: 0.001)')
    parser.add_argument('--side', type=str, choices=['buy', 'sell'], default='buy',
                      help='Order side: buy or sell (default: buy)')
    parser.add_argument('--testnet', action='store_true',
                      help='Use testnet (default behavior)')
    parser.add_argument('--mainnet', action='store_true',
                      help='Use mainnet (overrides testnet)')
    parser.add_argument('--api-key', type=str, default='',
                      help='BitGet API key (optional, can use environment variables)')
    parser.add_argument('--secret-key', type=str, default='',
                      help='BitGet secret key (optional, can use environment variables)')
    parser.add_argument('--passphrase', type=str, default='',
                      help='BitGet API passphrase (optional, can use environment variables)')
    parser.add_argument('--check-balance', action='store_true',
                      help='Check account balance before placing order')
    parser.add_argument('--check-positions', action='store_true',
                      help='Check current positions after placing order')
    parser.add_argument('--dry-run', action='store_true',
                      help='Simulate order without actually placing it')
    
    return parser.parse_args()

def main():
    """Main entry point for the script."""
    args = parse_args()
    
    # Determine if we should use testnet
    use_testnet = args.testnet or not args.mainnet
    
    # Create order executor
    executor = BitGetOrderExecutor(
        api_key=args.api_key,
        secret_key=args.secret_key,
        passphrase=args.passphrase,
        use_testnet=use_testnet
    )
    
    # Check balance if requested
    if args.check_balance:
        print(f"{BLUE}Checking account balance...{RESET}")
        balance_response = executor.get_account_balance()
        print(f"{CYAN}Balance response: {json.dumps(balance_response, indent=2)}{RESET}")
    
    # Place order unless dry run
    if not args.dry_run:
        print(f"{YELLOW}Placing {'BUY' if args.side == 'buy' else 'SELL'} order for {args.size} {args.symbol}...{RESET}")
        order_response = executor.place_market_order(
            symbol=args.symbol,
            size=args.size,
            side=args.side
        )
        print(f"{MAGENTA}Order response: {json.dumps(order_response, indent=2)}{RESET}")
    else:
        print(f"{YELLOW}DRY RUN: Would place {'BUY' if args.side == 'buy' else 'SELL'} order for {args.size} {args.symbol}{RESET}")
    
    # Check positions if requested
    if args.check_positions:
        print(f"{BLUE}Checking positions for {args.symbol}...{RESET}")
        positions_response = executor.get_positions(args.symbol)
        print(f"{CYAN}Positions response: {json.dumps(positions_response, indent=2)}{RESET}")

if __name__ == "__main__":
    print(f"{GREEN}BitGet Market Order Executor{RESET}")
    print(f"{CYAN}Use --help for available options{RESET}")
    main() 