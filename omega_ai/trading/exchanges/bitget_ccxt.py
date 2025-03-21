"""
OMEGA BTC AI - BitGet CCXT Implementation
=======================================

This module implements CCXT-based trading functionality for BitGet,
providing a robust and standardized interface for market operations.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import asyncio
import logging
import traceback
from datetime import datetime, timezone
from typing import (Any, Dict, List, Literal, Optional, Sequence, TypeVar,
                    Union, cast)
from uuid import uuid4

import ccxt.async_support as ccxt_async
import ccxt.pro as ccxt_pro
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import BadSymbol as InvalidSymbol
from ccxt.base.errors import ExchangeError, NetworkError, RateLimitExceeded
from ccxt.base.types import Order
from ccxt.base.types import OrderSide as CCXTOrderSide
from ccxt.base.types import OrderType as CCXTOrderType
from ccxt.base.types import Position, Ticker

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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

# Define supported order types and sides using Union[Literal] for better compatibility
OrderType = Union[Literal["market", "limit", "stop"], str]
OrderSide = Union[Literal["buy", "sell"], str]

T = TypeVar("T")


def to_dict_list(items: Sequence[Any]) -> List[Dict[str, Any]]:
    """Convert a sequence of objects to a list of dictionaries."""
    return [dict(item) if hasattr(item, "__dict__") else item for item in items]


class BitGetCCXT:
    """CCXT-based implementation for BitGet trading."""

    def __init__(
        self,
        api_key: Optional[str] = "",
        api_secret: Optional[str] = "",
        password: Optional[str] = "",
        use_testnet: bool = True,
        sub_account: str = "",
    ):
        """Initialize BitGet CCXT client.

        Args:
            api_key (Optional[str]): BitGet API key. Defaults to empty string.
            api_secret (Optional[str]): BitGet API secret. Defaults to empty string.
            password (Optional[str]): BitGet API password. Defaults to empty string.
            use_testnet (bool): Whether to use testnet. Defaults to True.
            sub_account (str): Sub-account name to use for trading. Defaults to empty string.
        """
        self.logger = logging.getLogger(__name__)
        self.use_testnet = use_testnet
        self.sub_account = sub_account

        self.exchange = ccxt_async.bitget(
            {
                "apiKey": api_key,
                "secret": api_secret,
                "password": password,
                "options": {
                    "defaultType": "swap",
                },
            }
        )

        if use_testnet:
            self.exchange.set_sandbox_mode(True)

        # Initialize Pro version for websocket support
        self.exchange_pro = getattr(ccxt_pro, "bitget")(
            {
                "apiKey": api_key,
                "secret": api_secret,
                "password": password,
                "enableRateLimit": True,
                "options": {
                    "defaultType": "swap",
                    "adjustForTimeDifference": True,
                    "recvWindow": 60000,
                    "testnet": use_testnet,
                },
            }
        )

        # Position side mapping
        self.position_side_map = {
            "buy": {"open": "long", "close": "short"},
            "sell": {"open": "short", "close": "long"},
        }

        logger.info(
            f"{GREEN}Initialized BitGet CCXT with {'TESTNET' if use_testnet else 'MAINNET'}{RESET}"
        )

    def _format_symbol(self, symbol: Optional[str]) -> str:
        """Format symbol for BitGet futures trading."""
        if symbol is None:
            logger.warning(
                f"{YELLOW}None symbol provided, using default BTCUSDT{RESET}"
            )
            return "BTC/USDT:USDT"

        if not symbol:
            logger.warning(
                f"{YELLOW}Empty symbol provided, using default BTCUSDT{RESET}"
            )
            return "BTC/USDT:USDT"

        # Remove any existing formatting
        base = symbol.replace("USDT", "").replace("/", "").replace(":", "")
        # Format for BitGet futures: BTC/USDT:USDT
        formatted = f"{base}/USDT:USDT"
        logger.debug(f"{CYAN}Formatted symbol: {formatted} (from {symbol}){RESET}")
        return formatted

    async def initialize(self):
        """Initialize the exchange connection and load markets."""
        try:
            await self.exchange.load_markets()
            logger.info(f"{GREEN}Markets loaded successfully{RESET}")

            # Get current position mode
            try:
                mode = await self.exchange.fetch_position_mode()
                self.is_hedge_mode = mode.get(
                    "hedged", False
                )  # Default to one-way mode if can't determine
                logger.info(
                    f"{GREEN}Current position mode: {'hedge' if self.is_hedge_mode else 'one-way'}{RESET}"
                )
            except Exception as e:
                logger.warning(
                    f"{YELLOW}Could not fetch position mode: {str(e)}{RESET}"
                )
                logger.warning(f"{YELLOW}Will proceed with one-way mode{RESET}")
                self.is_hedge_mode = False

        except Exception as e:
            logger.error(f"{RED}Error initializing exchange: {str(e)}{RESET}")
            raise

    async def set_hedge_mode(self):
        """Set up hedge mode for the account."""
        try:
            result = await self.exchange.set_position_mode(True)
            logger.info(f"{GREEN}Hedge mode set successfully: {result}{RESET}")
        except Exception as e:
            logger.error(f"{RED}Error setting hedge mode: {str(e)}{RESET}")
            raise

    async def setup_trading_config(self, symbol: str, leverage: int = 2):
        """Set up trading configuration for a symbol."""
        try:
            formatted_symbol = self._format_symbol(symbol)

            # First check if we have enough margin
            balance = await self.get_balance()
            usdt_balance = float(balance.get("USDT", {}).get("free", 0))

            if usdt_balance < 5:  # Minimum margin requirement for most futures
                logger.warning(
                    f"{YELLOW}Insufficient margin. Current balance: {usdt_balance} USDT{RESET}"
                )
                logger.warning(
                    f"{YELLOW}Please ensure you have at least 5 USDT available{RESET}"
                )
                return

            # Set leverage for both long and short positions
            try:
                await self.exchange.set_leverage(
                    leverage, symbol=formatted_symbol, params={"holdSide": "long"}
                )
                await self.exchange.set_leverage(
                    leverage, symbol=formatted_symbol, params={"holdSide": "short"}
                )
                logger.info(
                    f"{GREEN}Leverage set to {leverage}x for {formatted_symbol} (both sides){RESET}"
                )
            except Exception as e:
                if "40893" in str(e):  # Insufficient margin error
                    logger.warning(
                        f"{YELLOW}Warning: Could not set leverage due to insufficient margin{RESET}"
                    )
                    logger.warning(
                        f"{YELLOW}This might be because you have open positions or insufficient balance{RESET}"
                    )
                else:
                    raise

            # Set cross margin mode
            try:
                await self.exchange.set_margin_mode("cross", symbol=formatted_symbol)
                logger.info(
                    f"{GREEN}Cross margin mode set for {formatted_symbol}{RESET}"
                )
            except Exception as e:
                logger.warning(
                    f"{YELLOW}Warning: Could not set margin mode: {str(e)}{RESET}"
                )
                logger.warning(
                    f"{YELLOW}This might be because you're already in the desired margin mode{RESET}"
                )

        except Exception as e:
            logger.error(f"{RED}Error setting up trading config: {str(e)}{RESET}")
            raise

    async def get_market_ticker(self, symbol: str) -> Dict[str, Any]:
        """Get market ticker for a given symbol.

        Args:
            symbol (str): Trading symbol (e.g. 'BTC/USDT')

        Returns:
            Dict[str, Any]: Market ticker data

        Raises:
            ValueError: If symbol is empty
            InvalidSymbol: If symbol format is invalid
            RateLimitExceeded: If exchange rate limit is exceeded
            NetworkError: If network error occurs
            AuthenticationError: If authentication fails
            ExchangeError: If exchange error occurs
        """
        if not symbol:
            raise ValueError("Symbol cannot be empty")

        try:
            symbol = self._format_symbol(symbol)
            ticker = await self.exchange.fetch_ticker(symbol)
            return dict(ticker)
        except InvalidSymbol as e:
            self.logger.error(f"Invalid symbol format: {symbol}")
            raise
        except (
            RateLimitExceeded,
            NetworkError,
            AuthenticationError,
            ExchangeError,
        ) as e:
            self.logger.error(f"Error fetching ticker for {symbol}: {str(e)}")
            raise

    async def get_positions(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get current positions.

        Args:
            symbol (Optional[str], optional): Trading symbol. Defaults to None.

        Returns:
            List[Dict[str, Any]]: List of positions
        """
        try:
            if symbol:
                formatted_symbol = self._format_symbol(symbol)
                positions = await self.exchange.fetch_positions([formatted_symbol])
            else:
                positions = await self.exchange.fetch_positions()
            return [dict(pos) for pos in positions]
        except Exception as e:
            self.logger.error(f"Error fetching positions: {str(e)}")
            raise

    async def get_balance(self) -> Dict[str, Any]:
        """Get account balance."""
        try:
            balance = await self.exchange.fetch_balance()
            return balance
        except Exception as e:
            logger.error(f"{RED}Error fetching balance: {str(e)}{RESET}")
            raise

    async def get_market_candles(
        self, symbol: str, timeframe: str = "1m", limit: int = 100
    ) -> List[Any]:
        """
        Get historical candle data for a symbol.

        Args:
            symbol: Trading symbol (e.g., "BTC/USDT:USDT")
            timeframe: Timeframe for candles (default: "1m")
            limit: Number of candles to fetch (default: 100)

        Returns:
            List of OHLCV candles data
        """
        try:
            # Format symbol
            formatted_symbol = self._format_symbol(symbol)

            # Fetch candle data
            ohlcv = await self.exchange.fetch_ohlcv(
                formatted_symbol, timeframe=timeframe, limit=limit
            )

            return ohlcv
        except Exception as e:
            logger.error(f"{RED}Error fetching candles for {symbol}: {str(e)}{RESET}")
            return []

    async def place_order(
        self,
        symbol: str,
        side: OrderSide,
        amount: float,
        price: Optional[float] = None,
        order_type: OrderType = "market",
        reduce_only: bool = False,
        stop_price: Optional[float] = None,
        take_profit_price: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Place an order on BitGet.

        Args:
            symbol: Trading symbol (e.g., "BTC/USDT:USDT")
            side: Order side ("buy" or "sell")
            amount: Order amount
            price: Order price (optional, required for limit orders)
            order_type: Order type ("market", "limit", or "stop")
            reduce_only: Whether this is a reduce-only order
            stop_price: Stop loss price (optional)
            take_profit_price: Take profit price (optional)

        Returns:
            Order response from the exchange
        """
        try:
            # Format symbol
            formatted_symbol = self._format_symbol(symbol)

            # Prepare order parameters
            params = {
                "timeInForce": "GTC" if order_type == "limit" else "IOC",
                "reduceOnly": reduce_only,
                "positionSide": (
                    "long" if side == "buy" else "short"
                ),  # Add position side for unilateral mode
            }

            # Add stop loss if specified
            if stop_price:
                params["stopPrice"] = stop_price
                params["stopLoss"] = True

            # Add take profit if specified
            if take_profit_price:
                params["takeProfitPrice"] = take_profit_price
                params["takeProfit"] = True

            # Add sub-account if specified
            if self.sub_account:
                params["subAccount"] = self.sub_account

            # Place the order
            order = await self.exchange.create_order(
                symbol=formatted_symbol,
                type=order_type,
                side=side,
                amount=amount,
                price=price,
                params=params,
            )

            logger.info(f"{GREEN}Order placed successfully: {order}{RESET}")
            return dict(order)  # Convert Order to Dict

        except Exception as e:
            logger.error(f"{RED}Error placing order: {str(e)}{RESET}")
            raise

    async def place_stop_loss(
        self,
        symbol: str,
        side: OrderSide,
        amount: float,
        stop_price: float,
        position_side: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Place a stop loss order.

        Args:
            symbol: Trading symbol
            side: Order side ("buy" or "sell")
            amount: Order amount
            stop_price: Stop loss price
            position_side: Position side ("long" or "short")

        Returns:
            Order response from the exchange
        """
        try:
            formatted_symbol = self._format_symbol(symbol)

            # Determine position side if not provided
            if not position_side:
                position_side = "long" if side == "buy" else "short"

            params = {
                "stopPrice": stop_price,
                "stopLoss": True,
                "positionSide": position_side,
                "reduceOnly": True,
            }

            if self.sub_account:
                params["subAccount"] = self.sub_account

            order = await self.exchange.create_order(
                symbol=formatted_symbol,
                type="stop",  # No need to cast since we use str type
                side=side,  # No need to cast since we use str type
                amount=amount,
                params=params,
            )

            logger.info(f"{GREEN}Stop loss order placed successfully: {order}{RESET}")
            return dict(order)  # Convert Order to Dict

        except Exception as e:
            logger.error(f"{RED}Error placing stop loss order: {str(e)}{RESET}")
            raise

    async def place_take_profit(
        self,
        symbol: str,
        side: OrderSide,
        amount: float,
        take_profit_price: float,
        position_side: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Place a take profit order.

        Args:
            symbol: Trading symbol
            side: Order side ("buy" or "sell")
            amount: Order amount
            take_profit_price: Take profit price
            position_side: Position side ("long" or "short")

        Returns:
            Order response from the exchange
        """
        try:
            formatted_symbol = self._format_symbol(symbol)

            # Determine position side if not provided
            if not position_side:
                position_side = "long" if side == "buy" else "short"

            params = {
                "takeProfitPrice": take_profit_price,
                "takeProfit": True,
                "positionSide": position_side,
                "reduceOnly": True,
            }

            if self.sub_account:
                params["subAccount"] = self.sub_account

            order = await self.exchange.create_order(
                symbol=formatted_symbol,
                type="limit",  # No need to cast since we use str type
                side=side,  # No need to cast since we use str type
                amount=amount,
                price=take_profit_price,
                params=params,
            )

            logger.info(f"{GREEN}Take profit order placed successfully: {order}{RESET}")
            return dict(order)  # Convert Order to Dict

        except Exception as e:
            logger.error(f"{RED}Error placing take profit order: {str(e)}{RESET}")
            raise

    async def get_stop_loss_orders(
        self, symbol: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all active stop loss orders.

        Args:
            symbol: Optional trading symbol to filter orders

        Returns:
            List of stop loss orders
        """
        try:
            orders = await self.get_open_orders(symbol)

            # Filter for stop loss orders
            sl_orders = [
                order
                for order in orders
                if order.get("params", {}).get("stopLoss", False)
            ]

            return sl_orders
        except Exception as e:
            logger.error(f"{RED}Error fetching stop loss orders: {str(e)}{RESET}")
            raise

    async def get_take_profit_orders(
        self, symbol: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all active take profit orders.

        Args:
            symbol: Optional trading symbol to filter orders

        Returns:
            List of take profit orders
        """
        try:
            orders = await self.get_open_orders(symbol)

            # Filter for take profit orders
            tp_orders = [
                order
                for order in orders
                if order.get("params", {}).get("takeProfit", False)
            ]

            return tp_orders
        except Exception as e:
            logger.error(f"{RED}Error fetching take profit orders: {str(e)}{RESET}")
            raise

    async def cancel_stop_loss(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """
        Cancel a stop loss order.

        Args:
            order_id: Order ID to cancel
            symbol: Trading symbol

        Returns:
            Cancellation response from the exchange
        """
        return await self.cancel_order(order_id, symbol)

    async def cancel_take_profit(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """
        Cancel a take profit order.

        Args:
            order_id: Order ID to cancel
            symbol: Trading symbol

        Returns:
            Cancellation response from the exchange
        """
        return await self.cancel_order(order_id, symbol)

    async def close_position(self, symbol: str, side: str) -> Dict[str, Any]:
        """
        Close a position.

        Args:
            symbol: Trading symbol
            side: Position side ("long" or "short")

        Returns:
            Order response from the exchange
        """
        try:
            formatted_symbol = self._format_symbol(symbol)
            close_side = "sell" if side == "long" else "buy"

            # Get current position size
            positions = await self.fetch_positions([formatted_symbol])
            position = next((p for p in positions if p.get("side") == side), None)

            if not position or float(position.get("contracts", 0)) == 0:
                logger.info(f"{YELLOW}No position to close{RESET}")
                return {}

            amount = abs(float(position.get("contracts", 0)))

            # Place market order to close position
            return await self.place_order(
                symbol=formatted_symbol,
                side=close_side,
                amount=amount,
                order_type="market",
                reduce_only=True,
            )

        except Exception as e:
            logger.error(f"{RED}Error closing position: {str(e)}{RESET}")
            raise

    async def cancel_order(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """Cancel an existing order."""
        try:
            formatted_symbol = self._format_symbol(symbol)
            result = await self.exchange.cancel_order(order_id, formatted_symbol)
            logger.info(f"{GREEN}Order cancelled successfully: {result}{RESET}")
            return dict(result)  # Convert Order to Dict
        except Exception as e:
            logger.error(f"{RED}Error cancelling order: {str(e)}{RESET}")
            raise

    async def get_open_orders(
        self, symbol: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all open orders."""
        try:
            if symbol is None:
                orders = await self.exchange.fetch_open_orders()
            else:
                formatted_symbol = self._format_symbol(symbol)
                orders = await self.exchange.fetch_open_orders(formatted_symbol)
            return [dict(order) for order in orders]  # Convert Orders to Dicts
        except Exception as e:
            logger.error(f"{RED}Error fetching open orders: {str(e)}{RESET}")
            raise

    async def watch_orders(self):
        """Watch orders using websocket connection."""
        try:
            while True:
                orders = await self.exchange_pro.watch_orders()
                for order in orders:
                    # Process order update
                    logger.info(f"{CYAN}Order update received: {order}{RESET}")
                    # Add your order processing logic here

        except Exception as e:
            logger.error(f"{RED}Error watching orders: {str(e)}{RESET}")
            raise

    async def close(self):
        """Close the exchange connection."""
        try:
            await self.exchange.close()
            await self.exchange_pro.close()
            logger.info(f"{GREEN}Exchange connections closed{RESET}")
        except Exception as e:
            logger.error(f"{RED}Error closing exchange connections: {str(e)}{RESET}")
            raise

    def __del__(self):
        """Cleanup when the object is destroyed."""
        try:
            asyncio.create_task(self.close())
        except Exception as e:
            logger.error(f"{RED}Error during cleanup: {str(e)}{RESET}")

    async def get_fibonacci_levels(self, symbol: str) -> Dict[str, float]:
        """
        Get current Fibonacci levels for a symbol.

        Args:
            symbol: Trading symbol

        Returns:
            Dictionary of Fibonacci levels and their prices
        """
        try:
            # Get recent high and low
            ohlcv = await self.get_market_candles(symbol, "1h", limit=100)
            if not ohlcv:
                return {}

            # Calculate high and low
            high = max(candle[2] for candle in ohlcv)
            low = min(candle[3] for candle in ohlcv)

            # Calculate Fibonacci levels
            diff = high - low
            levels = {
                "0": low,
                "0.236": low + diff * 0.236,
                "0.382": low + diff * 0.382,
                "0.5": low + diff * 0.5,
                "0.618": low + diff * 0.618,
                "0.786": low + diff * 0.786,
                "1": high,
            }

            return levels

        except Exception as e:
            logger.error(f"{RED}Error getting Fibonacci levels: {str(e)}{RESET}")
            return {}

    async def fetch_ohlcv(
        self, symbol: str, timeframe: str = "1m", limit: int = 100
    ) -> List[Any]:
        """
        Fetch OHLCV data for a symbol.

        Args:
            symbol: Trading symbol
            timeframe: Timeframe for candles
            limit: Number of candles to fetch

        Returns:
            List of OHLCV candles
        """
        try:
            formatted_symbol = self._format_symbol(symbol)
            return await self.exchange.fetch_ohlcv(
                formatted_symbol, timeframe, limit=limit
            )
        except Exception as e:
            logger.error(f"{RED}Error fetching OHLCV data: {str(e)}{RESET}")
            return []

    async def fetch_positions(
        self, symbols: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch current positions.

        Args:
            symbols: Optional list of symbols to filter positions

        Returns:
            List of current positions
        """
        try:
            if symbols:
                positions = []
                for symbol in symbols:
                    if symbol is not None:
                        formatted_symbol = self._format_symbol(symbol)
                        pos = await self.exchange.fetch_positions([formatted_symbol])
                        positions.extend(pos)
                return to_dict_list(positions)  # Use to_dict_list for conversion
            else:
                positions = await self.exchange.fetch_positions()
                return to_dict_list(positions)  # Use to_dict_list for conversion
        except Exception as e:
            logger.error(f"{RED}Error fetching positions: {str(e)}{RESET}")
            return []

    async def create_order(
        self,
        symbol: str,
        type: OrderType,
        side: OrderSide,
        amount: float,
        price: Optional[float] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new order.

        Args:
            symbol (str): Trading symbol
            type (OrderType): Order type ('market', 'limit', or 'stop')
            side (OrderSide): Order side ('buy' or 'sell')
            amount (float): Order amount
            price (Optional[float], optional): Order price. Required for limit orders. Defaults to None.
            params (Optional[Dict[str, Any]], optional): Additional parameters. Defaults to None.

        Returns:
            Dict[str, Any]: Order information
        """
        order = await self.exchange.create_order(
            symbol=symbol,
            type=type,  # CCXT accepts string literals directly
            side=side,  # CCXT accepts string literals directly
            amount=amount,
            price=price,
            params=params or {},
        )
        return dict(order)

    async def create_stop_order(
        self,
        symbol: str,
        side: OrderSide,
        amount: float,
        stop_price: float,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a stop order.

        Args:
            symbol (str): Trading symbol
            side (OrderSide): Order side ('buy' or 'sell')
            amount (float): Order amount
            stop_price (float): Stop price
            params (Optional[Dict[str, Any]], optional): Additional parameters. Defaults to None.

        Returns:
            Dict[str, Any]: Order information
        """
        order = await self.exchange.create_order(
            symbol=symbol,
            type="stop",  # CCXT accepts string literals directly
            side=side,  # CCXT accepts string literals directly
            amount=amount,
            price=stop_price,
            params=params or {},
        )
        return dict(order)


async def main():
    """Example usage of the BitGetCCXT class."""
    # Initialize with your API credentials
    exchange = BitGetCCXT(
        api_key="your_api_key",
        api_secret="your_secret_key",  # Changed from secret_key
        password="your_passphrase",  # Changed from passphrase
        use_testnet=True,
    )

    try:
        # Initialize the exchange
        await exchange.initialize()

        # Get market data
        ticker = await exchange.get_market_ticker("BTC/USDT:USDT")
        print(f"BTC/USDT Ticker: {ticker}")

        # Get positions
        positions = await exchange.get_positions()
        print(f"Current positions: {positions}")

        # Get balance
        balance = await exchange.get_balance()
        print(f"Account balance: {balance}")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await exchange.close()


if __name__ == "__main__":
    asyncio.run(main())
