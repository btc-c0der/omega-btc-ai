"""
OMEGA BTC AI - BitGet Batch Order Operations
===========================================

This module implements high-efficiency batch order operations for BitGet,
optimizing trade execution by processing multiple orders in a single request.
Based on PassivBot's approach but integrated with OMEGA BTC AI's architecture.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import logging
import time
import hmac
import hashlib
import base64
import json
import requests
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum

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

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

class PositionSide(Enum):
    LONG = "long"
    SHORT = "short"

@dataclass
class OrderRequest:
    """Represents a single order request in a batch."""
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    position_side: Optional[PositionSide] = None
    reduce_only: bool = False
    post_only: bool = False
    leverage: str = "20"
    margin_mode: str = "crossed"
    time_in_force: str = "normal"
    custom_id: Optional[str] = None

class BitGetBatchExecutor:
    """Handles batch order operations for BitGet exchange."""
    
    def __init__(self,
                 api_key: str,
                 secret_key: str,
                 passphrase: str,
                 use_testnet: bool = True,
                 max_batch_size: int = 10,
                 rate_limit_delay: float = 0.5):
        """
        Initialize the batch executor.
        
        Args:
            api_key: BitGet API key
            secret_key: BitGet secret key
            passphrase: BitGet API passphrase
            use_testnet: Whether to use testnet (default: True)
            max_batch_size: Maximum number of orders per batch (default: 10)
            rate_limit_delay: Delay between batches in seconds (default: 0.5)
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.use_testnet = use_testnet
        self.base_url = "https://api-testnet.bitget.com" if use_testnet else "https://api.bitget.com"
        self.max_batch_size = max_batch_size
        self.rate_limit_delay = rate_limit_delay
        self.executor = ThreadPoolExecutor(max_workers=1)
        
        # Log initialization
        logger.info(f"{GREEN}Initialized BitGet Batch Executor{RESET}")
        logger.info(f"{CYAN}Using {'TESTNET' if use_testnet else 'MAINNET'} environment{RESET}")
        logger.info(f"{CYAN}Max batch size: {max_batch_size}{RESET}")
        logger.info(f"{CYAN}Rate limit delay: {rate_limit_delay}s{RESET}")
    
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
    
    def format_order_payload(self, order: OrderRequest) -> Dict[str, Any]:
        """
        Format a single order request into BitGet API payload.
        
        Args:
            order: OrderRequest object
            
        Returns:
            Formatted order payload
        """
        # Format symbol for BitGet UMCBL (USDT Margined Contracts)
        formatted_symbol = f"{order.symbol}_UMCBL"
        
        payload = {
            "symbol": formatted_symbol,
            "side": order.side.value.upper(),
            "orderType": order.order_type.value.upper(),
            "marginMode": order.margin_mode.upper(),
            "leverage": order.leverage,
            "timeInForce": order.time_in_force.upper(),
            "reduceOnly": str(order.reduce_only).lower(),
            "postOnly": str(order.post_only).lower(),
            "productType": "USDT-FUTURES"
        }
        
        if order.order_type == OrderType.LIMIT:
            if order.price is None:
                raise ValueError("Price required for limit orders")
            payload["price"] = str(order.price)
            payload["size"] = str(order.quantity)
        else:  # MARKET
            payload["size"] = str(order.quantity)
        
        if order.position_side:
            payload["holdSide"] = order.position_side.value.upper()
        
        if order.custom_id:
            payload["clientOid"] = order.custom_id
        
        return payload
    
    def format_batch_payload(self, orders: List[OrderRequest]) -> List[Dict[str, Any]]:
        """
        Format multiple orders into a batch payload.
        
        Args:
            orders: List of OrderRequest objects
            
        Returns:
            List of formatted order payloads
        """
        return [self.format_order_payload(order) for order in orders]
    
    async def execute_batch_orders(self, orders: List[OrderRequest]) -> List[Dict[str, Any]]:
        """
        Execute multiple orders in batches.
        
        Args:
            orders: List of OrderRequest objects
            
        Returns:
            List of order responses
        """
        if not orders:
            return []
            
        # Split orders into batches
        batches = [orders[i:i + self.max_batch_size] for i in range(0, len(orders), self.max_batch_size)]
        all_responses = []
        
        for batch in batches:
            try:
                # Format batch payload
                batch_payload = self.format_batch_payload(batch)
                
                # Prepare request
                timestamp = str(int(time.time() * 1000))
                request_path = "/api/mix/v1/order/batch-orders"
                payload_json = json.dumps({"orders": batch_payload})
                
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
                
                # Log batch details
                logger.info(f"{BLUE}Executing batch of {len(batch)} orders{RESET}")
                logger.info(f"{CYAN}Batch payload: {payload_json}{RESET}")
                
                # Execute request
                response = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    lambda: requests.post(
                        self.base_url + request_path,
                        headers=headers,
                        json={"orders": batch_payload}
                    )
                )
                
                # Parse response
                response_data = response.json()
                
                # Log response
                if response.status_code == 200 and response_data.get('code') == '00000':
                    logger.info(f"{GREEN}Batch order execution successful!{RESET}")
                    all_responses.extend(response_data.get('data', []))
                else:
                    logger.error(f"{RED}Batch order execution failed!{RESET}")
                    logger.error(f"{RED}Status code: {response.status_code}{RESET}")
                    logger.error(f"{RED}Response: {json.dumps(response_data, indent=2)}{RESET}")
                
                # Respect rate limits
                await asyncio.sleep(self.rate_limit_delay)
                
            except Exception as e:
                logger.error(f"{RED}Error executing batch: {str(e)}{RESET}")
                logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
                logger.error(f"{RED}Exception args: {e.args}{RESET}")
        
        return all_responses
    
    async def cancel_batch_orders(self, order_ids: List[str], symbol: str) -> List[Dict[str, Any]]:
        """
        Cancel multiple orders in batches.
        
        Args:
            order_ids: List of order IDs to cancel
            symbol: Trading symbol
            
        Returns:
            List of cancellation responses
        """
        if not order_ids:
            return []
            
        # Split order IDs into batches
        batches = [order_ids[i:i + self.max_batch_size] for i in range(0, len(order_ids), self.max_batch_size)]
        all_responses = []
        
        for batch in batches:
            try:
                # Prepare request
                timestamp = str(int(time.time() * 1000))
                request_path = "/api/mix/v1/order/batch-cancel"
                
                # Format payload
                payload = {
                    "symbol": f"{symbol}_UMCBL",
                    "orderIds": batch
                }
                payload_json = json.dumps(payload)
                
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
                
                # Log batch details
                logger.info(f"{BLUE}Cancelling batch of {len(batch)} orders{RESET}")
                logger.info(f"{CYAN}Batch payload: {payload_json}{RESET}")
                
                # Execute request
                response = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    lambda: requests.post(
                        self.base_url + request_path,
                        headers=headers,
                        json=payload
                    )
                )
                
                # Parse response
                response_data = response.json()
                
                # Log response
                if response.status_code == 200 and response_data.get('code') == '00000':
                    logger.info(f"{GREEN}Batch cancellation successful!{RESET}")
                    all_responses.extend(response_data.get('data', []))
                else:
                    logger.error(f"{RED}Batch cancellation failed!{RESET}")
                    logger.error(f"{RED}Status code: {response.status_code}{RESET}")
                    logger.error(f"{RED}Response: {json.dumps(response_data, indent=2)}{RESET}")
                
                # Respect rate limits
                await asyncio.sleep(self.rate_limit_delay)
                
            except Exception as e:
                logger.error(f"{RED}Error cancelling batch: {str(e)}{RESET}")
                logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
                logger.error(f"{RED}Exception args: {e.args}{RESET}")
        
        return all_responses
    
    def prioritize_orders(self, orders: List[OrderRequest]) -> List[OrderRequest]:
        """
        Prioritize orders based on type and side.
        
        Args:
            orders: List of OrderRequest objects
            
        Returns:
            Prioritized list of orders
        """
        # Sort orders by priority:
        # 1. Reduce-only orders (highest priority for liquidation protection)
        # 2. Market orders (faster execution)
        # 3. Limit orders
        return sorted(
            orders,
            key=lambda x: (
                not x.reduce_only,  # Reduce-only orders first
                x.order_type != OrderType.MARKET,  # Market orders second
                x.side == OrderSide.SELL  # Sell orders last (for better price discovery)
            )
        )
    
    async def execute_optimized_batch(self, orders: List[OrderRequest]) -> List[Dict[str, Any]]:
        """
        Execute orders in an optimized batch, with proper prioritization.
        
        Args:
            orders: List of OrderRequest objects
            
        Returns:
            List of order responses
        """
        # Prioritize orders
        prioritized_orders = self.prioritize_orders(orders)
        
        # Execute in batches
        return await self.execute_batch_orders(prioritized_orders)
    
    async def close(self):
        """Clean up resources."""
        self.executor.shutdown(wait=True)
        logger.info(f"{GREEN}Batch executor closed{RESET}")

# Example usage
async def main():
    """Example usage of the batch executor."""
    # Initialize executor
    executor = BitGetBatchExecutor(
        api_key="your_api_key",
        secret_key="your_secret_key",
        passphrase="your_passphrase",
        use_testnet=True,
        max_batch_size=10,
        rate_limit_delay=0.5
    )
    
    try:
        # Create some example orders
        orders = [
            OrderRequest(
                symbol="BTCUSDT",
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                quantity=0.001,
                position_side=PositionSide.LONG,
                reduce_only=True  # High priority for liquidation protection
            ),
            OrderRequest(
                symbol="BTCUSDT",
                side=OrderSide.SELL,
                order_type=OrderType.LIMIT,
                quantity=0.001,
                price=50000.0,
                position_side=PositionSide.SHORT
            ),
            # Add more orders as needed
        ]
        
        # Execute orders in optimized batches
        responses = await executor.execute_optimized_batch(orders)
        
        # Print responses
        print(f"{CYAN}Order responses:{RESET}")
        print(json.dumps(responses, indent=2))
        
    finally:
        # Clean up
        await executor.close()

if __name__ == "__main__":
    asyncio.run(main()) 