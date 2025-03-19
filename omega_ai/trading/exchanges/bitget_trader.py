#!/usr/bin/env python3

"""
BitGet Trader Integration for OmegaBTC AI

This module provides the BitGet exchange integration for our trader profiles.
It handles all direct communication with the BitGet API while maintaining
our trader profile system's behavior and risk management.
"""

import logging
import time
import hmac
import hashlib
import json
import requests
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from requests.exceptions import RequestException
import random
from threading import Lock
import base64
import os

from ..profiles.trader_base import TraderProfile, RiskParameters
from ..profiles.aggressive_trader import AggressiveTrader
from ..profiles.strategic_trader import StrategicTrader
from ..profiles.newbie_trader import NewbieTrader
from ..profiles.scalper_trader import ScalperTrader

logger = logging.getLogger(__name__)

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# Add rate limit constants
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 1  # seconds
MAX_RETRY_DELAY = 10  # seconds
REQUEST_RATE_LIMIT = 0.5  # seconds between requests
SHUTDOWN_TIMEOUT = 5  # seconds to wait for shutdown

class RateLimiter:
    """Rate limiter for API requests."""
    def __init__(self, min_interval: float):
        self.min_interval = min_interval
        self.last_request_time = 0
        self.lock = Lock()
    
    def wait(self):
        """Wait if necessary to respect rate limits."""
        with self.lock:
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            if time_since_last < self.min_interval:
                time.sleep(self.min_interval - time_since_last)
            self.last_request_time = time.time()

# Global rate limiter
rate_limiter = RateLimiter(REQUEST_RATE_LIMIT)

def _handle_rate_limit(response: requests.Response, retry_count: int) -> bool:
    """Handle rate limit responses and determine if we should retry."""
    if response.status_code == 429:  # Rate limit hit
        return True
    if response.status_code == 404 and retry_count > 0:  # Potential fake 404
        try:
            error_data = response.json()
            if error_data.get("code") == "40404":  # BitGet's "Request URL NOT FOUND"
                return True
        except:
            pass
    return False

def _get_retry_delay(retry_count: int) -> float:
    """Calculate exponential backoff delay with jitter."""
    delay = min(INITIAL_RETRY_DELAY * (2 ** retry_count), MAX_RETRY_DELAY)
    jitter = random.uniform(0, 0.1 * delay)
    return delay + jitter

def _make_request(method: str, url: str, **kwargs) -> requests.Response:
    """Make an HTTP request with rate limit handling and retries."""
    retry_count = 0
    last_error = None
    response = None
    
    while retry_count < MAX_RETRIES:
        try:
            # Apply rate limiting
            rate_limiter.wait()
            
            # Log request details
            logger.info(f"{CYAN}=== Request Details ==={RESET}")
            logger.info(f"Method: {method}")
            logger.info(f"URL: {url}")
            logger.info(f"Headers: {json.dumps(kwargs.get('headers', {}), indent=2)}")
            logger.info(f"Body: {json.dumps(kwargs.get('json', {}), indent=2)}")
            
            response = requests.request(method, url, **kwargs)
            
            # Log response details
            logger.info(f"{CYAN}=== Response Details ==={RESET}")
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response Headers: {dict(response.headers)}")
            try:
                logger.info(f"Response Body: {json.dumps(response.json(), indent=2)}")
            except:
                logger.info(f"Response Body: {response.text}")
            
            if _handle_rate_limit(response, retry_count):
                delay = _get_retry_delay(retry_count)
                logger.warning(f"{YELLOW}Rate limit hit or potential fake 404. Retrying in {delay:.2f} seconds... (Attempt {retry_count + 1}/{MAX_RETRIES}){RESET}")
                time.sleep(delay)
                retry_count += 1
                continue
                
            response.raise_for_status()
            return response
            
        except RequestException as e:
            last_error = e
            delay = _get_retry_delay(retry_count)
            logger.warning(f"{YELLOW}Request failed. Retrying in {delay:.2f} seconds... (Attempt {retry_count + 1}/{MAX_RETRIES}){RESET}")
            logger.error(f"{RED}Error details: {str(e)}{RESET}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"{RED}Response status: {e.response.status_code}{RESET}")
                logger.error(f"{RED}Response headers: {dict(e.response.headers)}{RESET}")
                try:
                    logger.error(f"{RED}Response body: {json.dumps(e.response.json(), indent=2)}{RESET}")
                except:
                    logger.error(f"{RED}Response body: {e.response.text}{RESET}")
            time.sleep(delay)
            retry_count += 1
    
    if last_error:
        raise last_error
    if response is None:
        raise RequestException("Failed to make request after all retries")
    return response

class BitGetTrader:
    """BitGet exchange integration for our trader profiles."""
    
    # Class constants
    PRODUCT_TYPE = "USDT-FUTURES"  # Product type for USDT-margined perpetual contracts
    PRODUCT_TYPE_PARAM = "USDT-FUTURES"  # Product type parameter for API v2 endpoints
    
    @classmethod
    def format_symbol(cls, symbol: str, api_version: str = "v2") -> str:
        """Format symbol according to BitGet's API requirements.
        
        Args:
            symbol: Symbol to format, e.g. "BTCUSDT"
            api_version: API version to format for (v1 or v2)
            
        Returns:
            Formatted symbol, e.g. "BTCUSDT_UMCBL" for v1 or "BTCUSDT" for v2
        """
        # For API v1, append _UMCBL suffix if not already present
        if api_version == "v1":
            if symbol.endswith("_UMCBL"):
                return symbol
            return f"{symbol}_UMCBL"
        # For API v2, use symbol as is
        else:
            # Remove _UMCBL suffix if present (in case we're upgrading from v1)
            if symbol.endswith("_UMCBL"):
                return symbol[:-7]
            return symbol
    
    def __init__(self, 
                 profile_type: str = "strategic",
                 api_key: str = "",
                 secret_key: str = "",
                 passphrase: str = "",
                 use_testnet: bool = True,
                 initial_capital: float = 10000.0,
                 margin_mode: str = "fixed",  # "fixed" or "crossed"
                 api_client: Optional[Any] = None,
                 api_version: str = "v1"
                ):
        """
        Initialize the BitGet trader with the specified settings.
        
        Args:
            profile_type: Type of trader profile (strategic, aggressive, newbie, scalper)
            api_key: BitGet API key
            secret_key: BitGet secret key
            passphrase: BitGet API passphrase
            use_testnet: Whether to use testnet (default: True)
            initial_capital: Initial capital in USDT (default: 10000.0)
            margin_mode: Margin mode (fixed or crossed) (default: fixed)
            api_client: Optional external API client for testing
            api_version: API version to use (v1 or v2) (default: v1)
        """
        # API configuration
        self.use_testnet = use_testnet
        self.is_shutting_down = False
        self.symbol = "BTCUSDT"  # Default to BTCUSDT
        self.api_version = api_version
        
        # Look for API credentials in environment variables if not provided
        self.api_key = api_key or os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
        self.secret_key = secret_key or os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
        self.passphrase = passphrase or os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
        
        # Log API credentials status
        if not self.api_key or not self.secret_key or not self.passphrase:
            logger.warning(f"{YELLOW}One or more API credentials are missing. API authentication will fail.{RESET}")
        
        # External API client for testing
        self.api_client = api_client
        
        # Set API base path based on version
        if api_version == "v1":
            self.api_base = "/api/mix/v1"
            self.PRODUCT_TYPE_PARAM = "umcbl"
        else:  # v2
            self.api_base = "/api/v2/mix"
            self.PRODUCT_TYPE_PARAM = "USDT-FUTURES"
        
        # Set different API URLs based on testnet/mainnet
        if self.use_testnet:
            self.api_url = "https://api-testnet.bitget.com"
        else:
            self.api_url = "https://api.bitget.com"
            
        logger.info(f"{CYAN}Initialized BitGetTrader with API {api_version}{RESET}")
        logger.info(f"{CYAN}API Base: {self.api_base}{RESET}")
        logger.info(f"{CYAN}Product Type Param: {self.PRODUCT_TYPE_PARAM}{RESET}")
        
        # Initialize the appropriate trader profile
        self.profile = self._initialize_profile(profile_type, initial_capital)
        
        # Trading state
        self.positions: List[Dict[str, Any]] = []
        self.trade_history: List[Dict[str, Any]] = []
        self.current_price: float = 0.0
        
        # Risk management
        self.risk_params = self.profile._get_risk_parameters()
        
        # Verify symbol
        if not self.verify_symbol():
            raise ValueError(f"Invalid trading symbol for {'testnet' if use_testnet else 'live'} trading")
        
    def _initialize_profile(self, profile_type: str, initial_capital: float) -> TraderProfile:
        """Initialize the appropriate trader profile based on type."""
        profile_map = {
            "aggressive": AggressiveTrader,
            "strategic": StrategicTrader,
            "newbie": NewbieTrader,
            "scalper": ScalperTrader
        }
        
        profile_class = profile_map.get(profile_type.lower(), StrategicTrader)
        return profile_class(initial_capital=initial_capital)
    
    def generate_signature(self, timestamp: str, method: str, request_path: str, body: Optional[Dict[str, Any]] = None) -> str:
        """Generate the signature required for BitGet API authentication."""
        message = str(timestamp) + method + request_path
        if body:
            message += json.dumps(body)
        hmac_obj = hmac.new(
            self.secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        )
        # Use base64 encoding instead of hexdigest as required by BitGet
        return base64.b64encode(hmac_obj.digest()).decode('utf-8')
    
    def _get_auth_headers(self, timestamp: str, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """Generate authentication headers for API requests."""
        # For v2 API, the signature is calculated differently
        message = timestamp + method + endpoint
        
        # Add query params or request body to message
        if params:
            if method == "GET":
                # For GET requests, add query parameters in alphabetical order
                query_params = []
                for key in sorted(params.keys()):
                    query_params.append(f"{key}={params[key]}")
                if query_params:
                    query_string = "&".join(query_params)
                    message += "?" + query_string
            else:
                # For POST requests, add JSON string of body
                message += json.dumps(params)
                
        # Log the exact message being used for signature
        logger.debug(f"Signature message: {message}")
                
        # Calculate signature using base64 encoding
        signature = base64.b64encode(
            hmac.new(
                self.secret_key.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')
        
        logger.debug(f"Calculated signature: {signature}")
        
        # Return headers exactly as specified in BitGet documentation
        return {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json"
        }
    
    def get_account_balance(self, symbol: str = "BTCUSDT") -> Optional[float]:
        """Get current account balance for the specified symbol."""
        # Use external API client if provided
        if self.api_client:
            try:
                response = self.api_client.get_account_balance(symbol)
                if response and response.get("code") == "00000" and response.get("data"):
                    return float(response["data"]["equity"])
                else:
                    logger.error(f"Error fetching account balance: {response.get('msg')}")
                    return None
            except Exception as e:
                logger.error(f"Error getting account balance: {e}")
                return None
        
        # Use internal implementation if no external client
        endpoint = f"{self.api_base}/account/account"
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Set parameters as query params
        params = {
            "productType": self.PRODUCT_TYPE_PARAM,
            "marginCoin": "USDT"  # Required parameter
        }
        
        headers = self._get_auth_headers(timestamp, method, endpoint)
        
        logger.info(f"{CYAN}=== Account Balance Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Query Params: {json.dumps(params, indent=2)}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Timestamp: {timestamp}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            account_data = response.json()
            
            if account_data.get("code") == "00000" and account_data.get("data"):
                logger.info(f"{GREEN}Successfully retrieved account balance{RESET}")
                return float(account_data["data"]["equity"])
            else:
                error_msg = account_data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error fetching account balance: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(account_data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error getting account balance: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None
    
    def place_order(self, 
                   symbol: str,
                   side: str,
                   order_type: str,
                   price: Optional[float] = None,
                   quantity: Optional[float] = None,
                   margin_mode: str = "crossed",
                   leverage: str = "20",
                   time_in_force: str = "normal",
                   reduce_only: bool = False,
                   post_only: bool = False) -> Optional[Dict[str, Any]]:
        """Place a futures order on BitGet."""
        # Use external API client if provided
        if self.api_client:
            try:
                # Format symbol for external client
                formatted_symbol = self.format_symbol(symbol, self.api_version)
                params: Dict[str, Any] = {
                    "symbol": formatted_symbol,
                    "marginCoin": "USDT",  # Required for v1 API
                    "side": side,  # Already mapped to open_long/open_short by caller
                    "orderType": order_type.upper(),
                    "marginMode": margin_mode.upper(),
                    "leverage": leverage,
                    "timeInForceValue": time_in_force,  # Changed from timeInForce to timeInForceValue
                    "reduceOnly": str(reduce_only).lower(),
                    "postOnly": str(post_only).lower(),
                    "productType": self.PRODUCT_TYPE_PARAM,
                    "clientOid": f"omega_{int(time.time() * 1000)}"  # Required unique client order ID
                }
                
                if order_type.lower() == "limit":
                    if price is None or quantity is None:
                        logger.error("Price and quantity required for limit orders")
                        return None
                    params["price"] = str(price)
                    params["size"] = str(quantity)
                elif order_type.lower() == "market":
                    if quantity is None:
                        logger.error("Quantity required for market orders")
                        return None
                    params["size"] = str(quantity)
                
                return self.api_client.place_order(**params)
            except Exception as e:
                logger.error(f"Error placing order: {e}")
                return None
        
        # Use internal implementation if no external client
        endpoint = f"{self.api_base}/order/placeOrder"
        method = "POST"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        params: Dict[str, Any] = {
            "symbol": formatted_symbol,
            "marginCoin": "USDT",  # Required for v1 API
            "side": side,  # Already mapped to open_long/open_short by caller
            "orderType": order_type.upper(),
            "marginMode": margin_mode.upper(),
            "leverage": leverage,
            "timeInForceValue": time_in_force,  # Changed from timeInForce to timeInForceValue
            "reduceOnly": str(reduce_only).lower(),
            "postOnly": str(post_only).lower(),
            "productType": self.PRODUCT_TYPE_PARAM,
            "clientOid": f"omega_{int(time.time() * 1000)}"  # Required unique client order ID
        }
        
        if order_type.lower() == "limit":
            if price is None or quantity is None:
                logger.error("Price and quantity required for limit orders")
                return None
            params["price"] = str(price)
            params["size"] = str(quantity)
        elif order_type.lower() == "market":
            if quantity is None:
                logger.error("Quantity required for market orders")
                return None
            params["size"] = str(quantity)
        
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        
        logger.info(f"{CYAN}=== Order Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"Body: {json.dumps(params, indent=2)}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Timestamp: {timestamp}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, json=params)
            order_data = response.json()
            
            if order_data.get("code") == "00000" and order_data.get("data"):
                logger.info(f"{GREEN}Successfully placed order{RESET}")
                return order_data
            else:
                error_msg = order_data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error placing order: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(order_data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return None
    
    def close_position(self, symbol: str, side: str, margin_mode: str = "crossed") -> Optional[Dict[str, Any]]:
        """Close an existing position."""
        # Use external API client if provided
        if self.api_client:
            try:
                # Format symbol for external client
                formatted_symbol = self.format_symbol(symbol, self.api_version)
                params: Dict[str, Any] = {
                    "symbol": formatted_symbol,
                    "side": "SELL" if side.lower() == "long" else "BUY",
                    "orderType": "MARKET",
                    "marginMode": margin_mode.upper(),
                    "size": "position_amount",
                    "productType": self.PRODUCT_TYPE_PARAM
                }
                return self.api_client.close_position(**params)
            except Exception as e:
                logger.error(f"Error closing position: {e}")
                return None
        
        # Use internal implementation if no external client
        # Different endpoint for different API versions
        if self.api_version == "v1":
            endpoint = f"{self.api_base}/order/close-positions"  # v1 endpoint
        else:
            endpoint = f"{self.api_base}/order/close-positions"  # v2 endpoint
            
        method = "POST"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        # Build parameters based on API version
        if self.api_version == "v1":
            params: Dict[str, Any] = {
                "symbol": formatted_symbol,
                "marginMode": margin_mode.upper(),
                "productType": self.PRODUCT_TYPE_PARAM
            }
            # v1 requires holdSide parameter
            if side.lower() == "long":
                params["holdSide"] = "long"
            else:
                params["holdSide"] = "short"
        else:
            params: Dict[str, Any] = {
                "symbol": formatted_symbol,
                "marginMode": margin_mode.upper(),
                "productType": self.PRODUCT_TYPE_PARAM
            }
        
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        
        logger.info(f"{CYAN}=== Close Position Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"Side: {side}")
        logger.info(f"API Version: {self.api_version}")
        logger.info(f"Body: {json.dumps(params, indent=2)}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Timestamp: {timestamp}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, json=params)
            close_data = response.json()
            
            if close_data.get("code") == "00000" and close_data.get("data"):
                logger.info(f"{GREEN}Successfully closed position{RESET}")
                return close_data
            else:
                error_msg = close_data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error closing position: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(close_data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"Error closing position: {e}")
            return None
    
    def execute_trade(self, market_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute a trade based on the profile's decision."""
        # Get trading decision from profile
        should_trade, reason, direction, leverage = self.profile.should_enter_trade(market_context)
        
        if not should_trade:
            logger.info(f"Profile decided not to trade: {reason}")
            return None
        
        # Calculate position size
        entry_price = market_context.get("price", 0)
        position_size = self.profile.determine_position_size(direction, entry_price)
        
        if position_size <= 0:
            logger.error("Invalid position size calculated")
            return None
        
        # Map direction to BitGet's expected format
        side_mapping = {
            "LONG": "open_long",
            "SHORT": "open_short"
        }
        mapped_side = side_mapping.get(direction, "open_long")
        
        # Place the order with correct side mapping
        order_response = self.place_order(
            symbol=self.symbol,
            side=mapped_side,  # Use mapped side instead of BUY/SELL
            order_type="MARKET",
            quantity=position_size,
            time_in_force="normal",
            leverage=str(leverage)
        )
        
        if not order_response or order_response.get("code") != "00000":
            logger.error(f"Failed to place order: {order_response}")
            return None
        
        # Calculate stop loss and take profit levels
        stop_loss = self.profile.set_stop_loss(direction, entry_price)
        take_profits = self.profile.set_take_profit(direction, entry_price, stop_loss)
        
        # Record the position
        position: Dict[str, Any] = {
            "direction": direction,
            "entry_price": entry_price,
            "size": position_size,
            "leverage": leverage,
            "stop_loss": stop_loss,
            "take_profits": take_profits,
            "entry_time": datetime.now(),
            "order_id": order_response.get("data", {}).get("orderId")
        }
        
        self.positions.append(position)
        return position
    
    def update_positions(self, current_price: float) -> None:
        """Update all positions with current price and check for exits."""
        self.current_price = current_price
        
        for position in self.positions[:]:  # Copy list to allow removal during iteration
            # Check stop loss
            if position["direction"] == "LONG" and current_price <= position["stop_loss"]:
                self._close_position(position, "Stop loss hit")
                continue
            elif position["direction"] == "SHORT" and current_price >= position["stop_loss"]:
                self._close_position(position, "Stop loss hit")
                continue
            
            # Check take profits
            for tp in position["take_profits"]:
                if position["direction"] == "LONG" and current_price >= tp["price"]:
                    self._close_position(position, f"Take profit hit at {tp['price']}")
                    break
                elif position["direction"] == "SHORT" and current_price <= tp["price"]:
                    self._close_position(position, f"Take profit hit at {tp['price']}")
                    break
    
    def _close_position(self, position: Dict[str, Any], reason: str) -> None:
        """Close a position and record the trade result."""
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol("BTCUSDT", self.api_version)
        
        close_response = self.close_position(
            symbol=formatted_symbol,
            side=position["direction"]
        )
        
        if not close_response or close_response.get("code") != "00000":
            logger.error(f"Failed to close position: {close_response}")
            return
        
        # Calculate PnL
        exit_price = float(close_response.get("data", {}).get("price", self.current_price))
        price_diff = exit_price - position["entry_price"]
        if position["direction"] == "SHORT":
            price_diff = -price_diff
        
        pnl = (price_diff / position["entry_price"]) * position["size"] * position["leverage"]
        
        # Record trade history
        trade: Dict[str, Any] = {
            "entry_time": position["entry_time"],
            "exit_time": datetime.now(),
            "direction": position["direction"],
            "entry_price": position["entry_price"],
            "exit_price": exit_price,
            "size": position["size"],
            "leverage": position["leverage"],
            "pnl": pnl,
            "reason": reason
        }
        
        self.trade_history.append(trade)
        
        # Update profile with trade result
        self.profile.process_trade_result(
            pnl,
            (trade["exit_time"] - trade["entry_time"]).total_seconds() / 60  # Duration in minutes
        )
        
        # Remove position from active positions
        self.positions.remove(position)
    
    def get_trade_history(self) -> List[Dict[str, Any]]:
        """Get the complete trade history."""
        return self.trade_history
    
    def get_positions(self, symbol: str = "BTCUSDT") -> Optional[List[Dict[str, Any]]]:
        """Get current positions for the specified symbol."""
        if self.is_shutting_down:
            logger.info(f"{YELLOW}Skipping position check during shutdown{RESET}")
            return None
            
        # Use external API client if provided
        if self.api_client:
            try:
                response = self.api_client.get_positions(symbol)
                if response and response.get("code") == "00000" and response.get("data"):
                    return response["data"]
                else:
                    logger.error(f"Error fetching positions: {response.get('msg')}")
                    return None
            except Exception as e:
                logger.error(f"Error getting positions: {e}")
                return None
        
        # Use internal implementation if no external client
        # Different endpoint based on API version
        if self.api_version == "v1":
            endpoint = f"{self.api_base}/position/allPosition"  # Correct endpoint for v1
        else:
            endpoint = f"{self.api_base}/position/single-position"  # Endpoint for v2
            
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        # Set parameters as query params
        params = {
            "marginCoin": "USDT"  # Required parameter
        }
        
        # Build params based on API version
        if self.api_version == "v1":
            # For v1, we need productType
            params["productType"] = self.PRODUCT_TYPE_PARAM
            
            # For v1, symbol is optional for allPosition - include it if provided
            if symbol:
                params["symbol"] = formatted_symbol
        else:
            # For v2, symbol is required
            params["symbol"] = formatted_symbol
        
        # For proper debugging, log exactly what we're using
        logger.info(f"{CYAN}=== Position Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Timestamp: {timestamp}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"API Version: {self.api_version}")
        logger.info(f"Query Params: {params}")
        
        # Generate signed headers
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        logger.info(f"Headers: {headers}")
        
        # Calculate signature directly for validation
        message = timestamp + method + endpoint
        query_params = []
        for key in sorted(params.keys()):
            query_params.append(f"{key}={params[key]}")
        if query_params:
            query_string = "&".join(query_params)
            message += "?" + query_string
            
        manual_signature = self.generate_signature(timestamp, method, endpoint, params)
        
        logger.info(f"Manual signature calculation:")
        logger.info(f"Message: {message}")
        logger.info(f"Calculated signature: {manual_signature}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            positions_data = response.json()
            
            if positions_data.get("code") == "00000" and positions_data.get("data"):
                logger.info(f"{GREEN}Successfully retrieved positions{RESET}")
                return positions_data["data"]
            else:
                error_msg = positions_data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error fetching positions: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(positions_data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error getting positions: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None
            
    def get_position_risk(self, symbol: str = "BTCUSDT") -> Optional[Dict[str, Any]]:
        """Get position risk information."""
        # Different endpoint based on API version
        if self.api_version == "v1":
            endpoint = f"{self.api_base}/position/allPosition"  # Correct endpoint for v1
        else:
            endpoint = f"{self.api_base}/position/single-position"  # Endpoint for v2
            
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        # Set parameters as query params
        params = {
            "marginCoin": "USDT"  # Required parameter
        }
        
        # Only add symbol for v2 or if explicitly required for v1
        if self.api_version != "v1" or True:  # Always add for now
            params["symbol"] = formatted_symbol
        
        # Add product type for v1
        if self.api_version == "v1":
            params["productType"] = self.PRODUCT_TYPE_PARAM
        
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        
        logger.info(f"{CYAN}=== Position Risk Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"API Version: {self.api_version}")
        logger.info(f"Query Params: {json.dumps(params, indent=2)}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Timestamp: {timestamp}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            data = response.json()
            
            if data.get("code") == "00000" and data.get("data"):
                logger.info(f"{GREEN}Successfully retrieved position risk{RESET}")
                return data["data"]
            else:
                error_msg = data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error fetching position risk: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error getting position risk: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None
            
    def set_leverage(self, symbol: str, leverage: str, margin_mode: str = "crossed") -> Optional[Dict[str, Any]]:
        """Set leverage for a symbol."""
        endpoint = f"{self.api_base}/account/set-leverage"
        method = "POST"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        body = {
            "symbol": formatted_symbol,
            "leverage": leverage,
            "marginMode": margin_mode.upper(),
            "productType": self.PRODUCT_TYPE_PARAM
        }
        
        headers = self._get_auth_headers(timestamp, method, endpoint, body)
        
        logger.info(f"{CYAN}=== Set Leverage Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"Body: {json.dumps(body, indent=2)}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Timestamp: {timestamp}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, json=body)
            leverage_data = response.json()
            
            if leverage_data.get("code") == "00000" and leverage_data.get("data"):
                logger.info(f"{GREEN}Successfully set leverage{RESET}")
                return leverage_data
            else:
                error_msg = leverage_data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error setting leverage: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(leverage_data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error setting leverage: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None
            
    def set_margin_mode(self, symbol: str, margin_mode: str) -> Optional[Dict[str, Any]]:
        """Set margin mode for a symbol."""
        endpoint = f"{self.api_base}/account/set-margin-mode"
        method = "POST"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        body = {
            "symbol": formatted_symbol,
            "marginMode": margin_mode.upper(),
            "productType": self.PRODUCT_TYPE_PARAM
        }
        
        headers = self._get_auth_headers(timestamp, method, endpoint, body)
        
        logger.info(f"{CYAN}=== Set Margin Mode Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"Body: {json.dumps(body, indent=2)}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Timestamp: {timestamp}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, json=body)
            margin_data = response.json()
            
            if margin_data.get("code") == "00000" and margin_data.get("data"):
                logger.info(f"{GREEN}Successfully set margin mode{RESET}")
                return margin_data
            else:
                error_msg = margin_data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error setting margin mode: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(margin_data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error setting margin mode: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None
    
    def get_total_pnl(self) -> float:
        """Calculate total profit/loss from all trades and open positions."""
        # Get realized PnL from trade history
        realized_pnl = sum(trade["pnl"] for trade in self.trade_history if "pnl" in trade)
        
        # Get unrealized PnL from open positions
        unrealized_pnl = 0.0
        
        try:
            if self.symbol:
                positions = self.get_positions(self.symbol)
                if positions:
                    for position in positions:
                        if position and "unrealizedPL" in position:
                            unrealized_pnl += float(position.get("unrealizedPL", 0))
                        # Also include achievedProfits (realized PnL for open positions)
                        if position and "achievedProfits" in position:
                            realized_pnl += float(position.get("achievedProfits", 0))
        except Exception as e:
            logger.error(f"Error calculating unrealized PnL: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
        
        # Return total PnL (realized + unrealized)
        total_pnl = realized_pnl + unrealized_pnl
        
        # Log PnL breakdown for debugging
        logger.debug(f"PnL Breakdown - Realized: {realized_pnl:.2f}, Unrealized: {unrealized_pnl:.2f}, Total: {total_pnl:.2f}")
        
        return total_pnl
    
    def get_market_ticker(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get current market ticker data."""
        # Different endpoint based on API version
        if self.api_version == "v1":
            endpoint = f"{self.api_base}/market/ticker"  # Endpoint for v1
        else:
            endpoint = f"{self.api_base}/market/ticker"  # Endpoint for v2
            
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        # Set parameters as query params - different for each API version
        params = {}
        
        if self.api_version == "v1":
            # For v1, we need symbol and productType
            params = {
                "symbol": formatted_symbol,
                "productType": self.PRODUCT_TYPE_PARAM
            }
        else:
            # For v2, just symbol
            params = {
                "symbol": formatted_symbol
            }
        
        # For proper debugging, log exactly what we're using
        logger.info(f"{CYAN}=== Ticker Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Timestamp: {timestamp}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"API Version: {self.api_version}")
        logger.info(f"Query Params: {params}")
        
        # Generate signed headers
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        logger.info(f"Headers: {headers}")
        
        # Calculate signature directly for validation
        message = timestamp + method + endpoint
        query_params = []
        for key in sorted(params.keys()):
            query_params.append(f"{key}={params[key]}")
        if query_params:
            query_string = "&".join(query_params)
            message += "?" + query_string
            
        manual_signature = self.generate_signature(timestamp, method, endpoint, params)
        
        logger.info(f"Manual signature calculation:")
        logger.info(f"Message: {message}")
        logger.info(f"Calculated signature: {manual_signature}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            data = response.json()
            
            if data.get("code") == "00000" and data.get("data"):
                logger.info(f"{GREEN}Successfully retrieved ticker{RESET}")
                return data["data"]
            else:
                error_msg = data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error fetching ticker: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error getting ticker: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None
            
    def get_orderbook(self, symbol: str, limit: int = 100) -> Optional[Dict[str, Any]]:
        """Get order book data."""
        endpoint = f"{self.api_base}/market/orderbook"
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        # Set parameters as query params
        params = {
            "symbol": formatted_symbol,
            "limit": str(limit)
        }
        
        # Add product type parameter for v1 API
        if self.api_version == "v1":
            params["productType"] = self.PRODUCT_TYPE_PARAM
            
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        
        logger.info(f"{CYAN}=== Orderbook Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"Query Params: {params}")
        logger.info(f"Headers: {headers}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            data = response.json()
            
            if data.get("code") == "00000" and data.get("data"):
                logger.info(f"{GREEN}Successfully retrieved orderbook{RESET}")
                return data["data"]
            else:
                error_msg = data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error fetching orderbook: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error getting orderbook: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None
            
    def get_recent_trades(self, symbol: str, limit: int = 100) -> Optional[List[Dict[str, Any]]]:
        """Get recent trades."""
        endpoint = f"{self.api_base}/market/trades"
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        # Set parameters as query params
        params = {
            "symbol": formatted_symbol,
            "limit": str(limit)
        }
        
        # Add product type parameter for v1 API
        if self.api_version == "v1":
            params["productType"] = self.PRODUCT_TYPE_PARAM
            
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        
        logger.info(f"{CYAN}=== Trades Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"Query Params: {params}")
        logger.info(f"Headers: {headers}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            data = response.json()
            
            if data.get("code") == "00000" and data.get("data"):
                logger.info(f"{GREEN}Successfully retrieved trades{RESET}")
                return data["data"]
            else:
                error_msg = data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error fetching trades: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error getting trades: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None
    
    def verify_symbol(self, symbol: str = "BTCUSDT") -> bool:
        """Verify if the symbol is valid and available for futures trading."""
        logger.info(f"{CYAN}=== Symbol Verification ==={RESET}")
        logger.info(f"Symbol: {symbol}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"API Base: {self.api_base}")
        logger.info(f"API Version: {self.api_version}")
        
        # Use external API client if provided
        if self.api_client:
            try:
                logger.info("Using external API client for verification")
                response = self.api_client.get_symbols()
                if response and response.get("code") == "00000" and response.get("data"):
                    symbols = response["data"]
                    
                    # For API v1, symbols are in format BTCUSDT_UMCBL
                    if self.api_version == "v1":
                        symbol_to_check = f"{symbol}_UMCBL"
                    else:
                        symbol_to_check = symbol
                        
                    logger.info(f"Checking for symbol: {symbol_to_check}")
                    symbol_exists = any(s["symbol"] == symbol_to_check for s in symbols)
                    logger.info(f"Symbol verification result: {symbol_exists}")
                    return symbol_exists
                else:
                    logger.error(f"Error fetching symbols: {response.get('msg')}")
                    return False
            except Exception as e:
                logger.error(f"Error verifying symbol: {e}")
                return False
        
        # Use internal implementation if no external client
        # Different endpoint based on API version
        if self.api_version == "v1":
            endpoint = f"{self.api_base}/market/contracts"  # Endpoint for v1: /api/mix/v1/market/contracts
        else:
            endpoint = f"{self.api_base}/market/contracts"  # Endpoint for v2
        
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Parameters as query params
        params = {
            "productType": self.PRODUCT_TYPE_PARAM
        }
        
        # For proper debugging, log exactly what we're using
        logger.info(f"{CYAN}=== Symbol Verification Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Timestamp: {timestamp}")
        logger.info(f"API Version: {self.api_version}")
        logger.info(f"Query Params: {params}")
        
        # Generate signed headers
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        logger.info(f"Headers: {headers}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            symbols_data = response.json()
            
            if symbols_data.get("code") == "00000" and symbols_data.get("data"):
                symbols = symbols_data["data"]
                logger.info(f"Retrieved {len(symbols)} symbols")
                
                # For API v1, symbols are in format BTCUSDT_UMCBL
                if self.api_version == "v1":
                    symbol_to_check = f"{symbol}_UMCBL"
                else:
                    symbol_to_check = symbol
                    
                logger.info(f"Checking for symbol: {symbol_to_check}")
                
                # Check if our symbol exists in the returned symbols
                # For v1, we check the 'symbol' field
                if self.api_version == "v1":
                    symbol_exists = any(s.get("symbol") == symbol_to_check for s in symbols)
                else:
                    # For v2, format may differ
                    symbol_exists = any(s.get("symbol") == symbol_to_check for s in symbols)
                
                logger.info(f"{GREEN}Symbol verification result: {symbol_exists}{RESET}")
                
                if symbol_exists:
                    # Log a few symbols for reference
                    logger.info(f"{GREEN}Available symbols sample:{RESET}")
                    for s in symbols[:5]:  # Log first 5 symbols as example
                        logger.info(f"  - {s.get('symbol', 'Unknown')}")
                else:
                    # Log the first 10 symbols to help debugging
                    logger.warning(f"{YELLOW}Symbol {symbol_to_check} not found in available symbols.{RESET}")
                    logger.warning(f"{YELLOW}First 10 available symbols:{RESET}")
                    for s in symbols[:10]:
                        logger.warning(f"  - {s.get('symbol', 'Unknown')}")
                    
                    # Check if symbol without suffix exists in a different form
                    for s in symbols[:20]:
                        if symbol in str(s.get("symbol", "")):
                            logger.warning(f"{YELLOW}Found potential match: {s.get('symbol', 'Unknown')}{RESET}")
                
                return symbol_exists
            else:
                error_msg = symbols_data.get("msg", "Unknown error")
                logger.error(f"{RED}Error fetching symbols: {error_msg}{RESET}")
                logger.error(f"Full response: {json.dumps(symbols_data, indent=2)}")
                return False
                
        except Exception as e:
            logger.error(f"{RED}Error verifying symbol: {str(e)}{RESET}")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return False

    async def shutdown(self) -> None:
        """Gracefully shutdown the trader."""
        self.is_shutting_down = True
        logger.info(f"{YELLOW}Shutting down trader...{RESET}")
        
        try:
            # Close all open positions
            positions = self.get_positions()
            if positions:
                for position in positions:
                    if position.get('status') == 'OPEN':
                        self.close_position(
                            symbol=self.symbol,
                            side=position.get('side', 'LONG')
                        )
            
            logger.info(f"{GREEN}Trader shutdown complete{RESET}")
            
        except Exception as e:
            logger.error(f"{RED}Error during trader shutdown: {str(e)}{RESET}")
        finally:
            self.is_shutting_down = False

    def get_all_positions(self, product_type: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get all positions for the account.
        
        Args:
            product_type: Product type (default: None, will use class constant)
            
        Returns:
            List of position information or None if request fails
        """
        # Use external API client if provided
        if self.api_client:
            try:
                response = self.api_client.get_all_positions(product_type or self.PRODUCT_TYPE_PARAM)
                if response and response.get("code") == "00000" and response.get("data"):
                    return response["data"]
                else:
                    logger.error(f"Error fetching all positions: {response.get('msg')}")
                    return None
            except Exception as e:
                logger.error(f"Error getting all positions: {e}")
                return None
        
        # Use internal implementation if no external client
        # Different endpoint based on API version
        if self.api_version == "v1":
            endpoint = f"{self.api_base}/position/allPosition"  # Correct endpoint for v1
        else:
            endpoint = f"{self.api_base}/position/all-position"  # Endpoint for v2
            
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Set parameters as query params
        params = {
            "productType": product_type or self.PRODUCT_TYPE_PARAM,
            "marginCoin": "USDT"  # Required parameter
        }
        
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        
        logger.info(f"{CYAN}=== All Positions Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"API Version: {self.api_version}")
        logger.info(f"Query Params: {json.dumps(params, indent=2)}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Timestamp: {timestamp}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            positions_data = response.json()
            
            if positions_data.get("code") == "00000" and positions_data.get("data"):
                logger.info(f"{GREEN}Successfully retrieved all positions{RESET}")
                return positions_data["data"]
            else:
                error_msg = positions_data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error fetching all positions: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(positions_data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error getting all positions: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None

    def get_historical_positions(self, 
                               symbol: str = "BTCUSDT",
                               start_time: Optional[int] = None,
                               end_time: Optional[int] = None,
                               limit: int = 100,
                               product_type: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get historical positions for the account.
        
        Args:
            symbol: Trading symbol (default: BTCUSDT)
            start_time: Start time in milliseconds (optional)
            end_time: End time in milliseconds (optional)
            limit: Number of records to return (default: 100)
            product_type: Product type (default: None, will use class constant)
            
        Returns:
            List of historical position information or None if request fails
        """
        # Use external API client if provided
        if self.api_client:
            try:
                response = self.api_client.get_historical_positions(
                    symbol=symbol,
                    start_time=start_time,
                    end_time=end_time,
                    limit=limit,
                    product_type=product_type or self.PRODUCT_TYPE_PARAM
                )
                if response and response.get("code") == "00000" and response.get("data"):
                    return response["data"]
                else:
                    logger.error(f"Error fetching historical positions: {response.get('msg')}")
                    return None
            except Exception as e:
                logger.error(f"Error getting historical positions: {e}")
                return None
        
        # Use internal implementation if no external client
        # Different endpoint based on API version
        if self.api_version == "v1":
            endpoint = f"{self.api_base}/position/history"  # Possible endpoint for v1 - may need adjustment
        else:
            endpoint = f"{self.api_base}/position/history-position"  # Endpoint for v2
            
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        # Set parameters as query params
        params = {
            "pageSize": str(limit)
        }
        
        # Add symbol parameter if provided
        if symbol:
            params["symbol"] = formatted_symbol
        
        # Add product type for v1
        if self.api_version == "v1":
            params["productType"] = product_type or self.PRODUCT_TYPE_PARAM
        elif not symbol:
            # If no symbol provided for v2, use productType
            params["productType"] = product_type or self.PRODUCT_TYPE_PARAM
        
        # Add optional parameters if provided
        if start_time is not None:
            params["startTime"] = str(start_time)
        if end_time is not None:
            params["endTime"] = str(end_time)
        
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        
        logger.info(f"{CYAN}=== Historical Positions Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"API Version: {self.api_version}")
        logger.info(f"Query Params: {json.dumps(params, indent=2)}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Timestamp: {timestamp}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            positions_data = response.json()
            
            if positions_data.get("code") == "00000" and positions_data.get("data"):
                logger.info(f"{GREEN}Successfully retrieved historical positions{RESET}")
                # Handle potential differences in response structure between v1 and v2
                if self.api_version == "v1":
                    return positions_data["data"]  # May need adjustment based on actual response
                else:
                    return positions_data["data"]["list"]  # v2 format with list inside data
            else:
                error_msg = positions_data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error fetching historical positions: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(positions_data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error getting historical positions: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None 