"""
OMEGA BTC AI - BitGet Live Traders Module
=======================================

This module implements a live trading system with multiple trader profiles on BitGet,
each starting with 24 USDT and trading BTC. The system includes real-time monitoring,
risk management, and performance tracking.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import asyncio
import logging
import argparse
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT
from omega_ai.trading.exchanges.coin_picker import CoinPicker, CoinType, CoinInfo
from omega_ai.trading.profiles import (
    StrategicTrader,
    AggressiveTrader,
    NewbieTrader,
    ScalperTrader
)
from omega_ai.alerts.telegram_market_report import send_telegram_alert
import json
import os
import sys
import traceback
from omega_ai.mm_trap_detector.mm_trap_detector import MMTrapDetector

# Custom JSON encoder for datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for maximum logging
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('bitget_live_trading.log')  # File output
    ]
)

# Set specific loggers to DEBUG level
logging.getLogger('omega_ai.trading.exchanges.bitget_trader').setLevel(logging.DEBUG)
logging.getLogger('omega_ai.trading.exchanges.bitget_live_traders').setLevel(logging.DEBUG)
logging.getLogger('omega_ai.trading.profiles').setLevel(logging.DEBUG)
logging.getLogger('omega_ai.alerts.telegram_market_report').setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

class BitGetLiveTraders:
    """Manages multiple live traders on BitGet with different profiles."""
    
    def __init__(self, 
                 use_testnet: bool = True,
                 initial_capital: float = 24.0,
                 symbol: str = "BTCUSDT",
                 api_key: str = "",
                 secret_key: str = "",
                 passphrase: str = "",
                 use_coin_picker: bool = False,
                 strategic_only: bool = False,
                 enable_pnl_alerts: bool = True,
                 pnl_alert_interval: int = 1,
                 leverage: int = 11):
        """
        Initialize the live traders system.
        
        Args:
            use_testnet: Whether to use testnet (default: True)
            initial_capital: Initial capital per trader in USDT (default: 24.0)
            symbol: Trading symbol (default: BTCUSDT)
            api_key: BitGet API key
            secret_key: BitGet secret key
            passphrase: BitGet API passphrase
            use_coin_picker: Whether to use CoinPicker for symbol verification (default: False)
            strategic_only: Whether to only use the strategic trader profile (default: False)
            enable_pnl_alerts: Whether to enable PnL alerts (default: True)
            pnl_alert_interval: Minute interval for PnL alerts (default: 1, sends every minute)
            leverage: Trading leverage (default: 11)
        """
        self.use_testnet = use_testnet
        self.initial_capital = initial_capital
        self.symbol = symbol
        self.strategic_only = strategic_only
        self.enable_pnl_alerts = enable_pnl_alerts
        self.pnl_alert_interval = pnl_alert_interval
        self.last_pnl_alert_time = datetime.now(timezone.utc)
        self.leverage = leverage
        
        # Log initialization parameters
        logger.debug(f"{CYAN}Initializing BitGetLiveTraders with parameters:{RESET}")
        logger.debug(f"  use_testnet: {use_testnet}")
        logger.debug(f"  initial_capital: {initial_capital}")
        logger.debug(f"  symbol: {symbol}")
        logger.debug(f"  strategic_only: {strategic_only}")
        logger.debug(f"  enable_pnl_alerts: {enable_pnl_alerts}")
        logger.debug(f"  pnl_alert_interval: {pnl_alert_interval}")
        logger.debug(f"  leverage: {leverage}")
        
        # Look for API credentials in environment variables if not provided
        self.api_key = api_key or os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
        self.secret_key = secret_key or os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
        self.passphrase = passphrase or os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
        
        # Log API credentials status (safely)
        if not self.api_key or not self.secret_key or not self.passphrase:
            logger.warning(f"{YELLOW}One or more API credentials are missing. API authentication will fail.{RESET}")
        else:
            logger.info(f"{GREEN}API credentials loaded successfully.{RESET}")
            logger.debug(f"  API Key: {self.api_key[:5]}...{self.api_key[-3:] if len(self.api_key) > 5 else ''}")
            logger.debug(f"  Secret Key Length: {len(self.secret_key)} characters")
            logger.debug(f"  Passphrase Length: {len(self.passphrase)} characters")
            
        self.use_coin_picker = use_coin_picker
        self.traders: Dict[str, BitGetCCXT] = {}
        self.is_running = False
        self.coin_picker = CoinPicker(use_testnet=use_testnet) if use_coin_picker else None
        
        # Log environment information
        logger.debug(f"{CYAN}Environment Information:{RESET}")
        logger.debug(f"  Python Version: {sys.version}")
        logger.debug(f"  OS: {os.name}")
        logger.debug(f"  Working Directory: {os.getcwd()}")
        logger.debug(f"  Environment Variables:")
        for key in ["BITGET_TESTNET_API_KEY", "BITGET_API_KEY", "STRATEGIC_SUB_ACCOUNT_NAME"]:
            if key in os.environ:
                logger.debug(f"    {key}: {'*' * len(os.environ[key])}")
                
    def _format_symbol(self, symbol: str) -> str:
        """Format symbol for CCXT use."""
        # Remove USDT suffix if present
        base = symbol.replace('USDT', '')
        # Format for BitGet futures: BTC/USDT:USDT
        return f"{base}/USDT:USDT"

    async def initialize(self) -> None:
        """Initialize the trading system."""
        # Verify symbol exists and is valid
        if not await self._verify_symbol():
            logger.error(f"{RED}Invalid symbol {self.symbol}. Using default BTCUSDT{RESET}")
            self.symbol = "BTCUSDT"
            
        await self._initialize_traders()
        
    async def _verify_symbol(self) -> bool:
        """Verify if the symbol is valid and available for futures trading."""
        try:
            # Skip verification if CoinPicker is disabled
            if not self.use_coin_picker or not self.coin_picker:
                logger.info(f"{YELLOW}CoinPicker disabled, skipping symbol verification{RESET}")
                # Instead, use CCXT to verify the symbol
                test_exchange = BitGetCCXT(
                    api_key=self.api_key,
                    secret_key=self.secret_key,
                    passphrase=self.passphrase,
                    use_testnet=self.use_testnet
                )
                await test_exchange.initialize()
                try:
                    formatted_symbol = self._format_symbol(self.symbol)
                    await test_exchange.get_market_ticker(formatted_symbol)
                    await test_exchange.close()
                    return True
                except Exception as e:
                    logger.error(f"{RED}Symbol verification failed: {str(e)}{RESET}")
                    return False
                
            # Update coin picker cache
            if not self.coin_picker.update_coins_cache():
                logger.warning(f"{YELLOW}Failed to update coins cache, skipping verification{RESET}")
                return True
                
            # Get symbol info
            symbol_info = self.coin_picker.get_symbol_info(self.symbol)
            if not symbol_info:
                return False
                
            # Verify it's a futures symbol
            if symbol_info.type != CoinType.FUTURES:
                logger.error(f"{RED}Symbol {self.symbol} is not a futures contract{RESET}")
                return False
                
            # Verify it's a USDT contract
            if symbol_info.quote_currency != "USDT":
                logger.error(f"{RED}Symbol {self.symbol} is not a USDT contract{RESET}")
                return False
                
            # Get market analysis
            analysis = self.coin_picker.analyze_symbol(self.symbol)
            if not analysis:
                return False
                
            logger.info(f"{GREEN}Symbol {self.symbol} verified successfully{RESET}")
            logger.info(f"{BLUE}Symbol details:{RESET}")
            logger.info(f"Base currency: {analysis['base_currency']}")
            logger.info(f"Quote currency: {analysis['quote_currency']}")
            logger.info(f"Last price: {analysis['last_price']}")
            logger.info(f"24h volume: {analysis['volume_24h']}")
            logger.info(f"24h price change: {analysis['price_change_24h']}%")
            logger.info(f"Maker fee rate: {analysis['maker_fee_rate']}")
            logger.info(f"Taker fee rate: {analysis['taker_fee_rate']}")
            
            return True
            
        except Exception as e:
            logger.error(f"{RED}Error verifying symbol: {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            return False
        
    async def _initialize_traders(self) -> None:
        """Initialize traders with different profiles."""
        profiles = {
            "strategic": StrategicTrader,
            "aggressive": AggressiveTrader,
            "scalping": ScalperTrader
        }
        
        # For mainnet, only use the main account
        if not self.use_testnet:
            logger.info(f"{CYAN}Using main account only for mainnet trading{RESET}")
            trader = None
            try:
                # Get sub-account name from environment or use empty string
                strategic_sub_account = os.environ.get("STRATEGIC_SUB_ACCOUNT_NAME", "")
                trader = BitGetCCXT(
                    api_key=self.api_key,
                    secret_key=self.secret_key,
                    passphrase=self.passphrase,
                    use_testnet=self.use_testnet,
                    sub_account=strategic_sub_account
                )
                await trader.initialize()
                # Set up trading configuration with current leverage
                await trader.setup_trading_config(self.symbol, self.leverage)
                self.traders["strategic"] = trader
                logger.info(f"{GREEN}Initialized strategic trader{RESET}")
            except Exception as e:
                logger.error(f"{RED}Failed to initialize strategic trader: {str(e)}{RESET}")
                if trader:
                    await trader.close()
                raise
            return
        
        # For testnet, initialize all profiles
        for profile_name, profile_class in profiles.items():
            trader = None
            try:
                # Get sub-account name from environment for strategic trader
                sub_account = ""
                if profile_name == "strategic":
                    sub_account = os.environ.get("STRATEGIC_SUB_ACCOUNT_NAME", "")
                    if sub_account:
                        logger.info(f"{GREEN}Using sub-account: {sub_account}{RESET}")
                
                trader = BitGetCCXT(
                    api_key=self.api_key,
                    secret_key=self.secret_key,
                    passphrase=self.passphrase,
                    use_testnet=self.use_testnet,
                    sub_account=sub_account
                )
                
                await trader.initialize()
                # Set up trading configuration with current leverage
                await trader.setup_trading_config(self.symbol, self.leverage)
                self.traders[profile_name] = trader
                logger.info(f"{GREEN}Initialized {profile_name} trader{RESET}")
                
            except Exception as e:
                logger.error(f"{RED}Failed to initialize {profile_name} trader: {str(e)}{RESET}")
                if trader:
                    await trader.close()
                continue

    async def start_trading(self) -> None:
        """Start the live trading system."""
        # Initialize traders if not already done
        if not self.traders:
            await self.initialize()
            
        self.is_running = True
        logger.info(f"{CYAN}Starting OMEGA BTC AI Live Traders System{RESET}")
        
        try:
            while self.is_running:
                # Update each trader
                for profile_name, trader in self.traders.items():
                    try:
                        await self._update_trader(trader, profile_name)
                    except Exception as e:
                        logger.error(f"{RED}Error updating {profile_name} trader: {str(e)}{RESET}")
            
                # Wait before next update
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info(f"{YELLOW}Shutting down live traders system...{RESET}")
            await self.stop_trading()
            
    async def _update_trader(self, trader: BitGetCCXT, profile_name: str) -> None:
        """Update a single trader's state and execute trading logic."""
        try:
            # Get current market data
            formatted_symbol = self._format_symbol(self.symbol)
            logger.debug(f"{CYAN}Getting market ticker for {formatted_symbol} ({profile_name} trader){RESET}")
            ticker = await trader.get_market_ticker(formatted_symbol)
            
            if ticker and 'last' in ticker:
                current_price = float(ticker['last'])
                logger.debug(f"{GREEN}Current price for {self.symbol}: {current_price}{RESET}")
                logger.debug(f"{CYAN}Full ticker data: {json.dumps(ticker, indent=2, cls=DateTimeEncoder)}{RESET}")
                
                # Update market context
                market_context = {
                    "price": current_price,
                    "symbol": formatted_symbol,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                logger.debug(f"{CYAN}Market context: {json.dumps(market_context, indent=2)}{RESET}")
                
                # Get current positions before executing trade
                logger.debug(f"{CYAN}Getting current positions for {profile_name} trader{RESET}")
                current_positions = await trader.get_positions(formatted_symbol)
                logger.debug(f"{CYAN}Current positions: {json.dumps(current_positions, indent=2, cls=DateTimeEncoder)}{RESET}")
                
                # Check for open positions
                open_positions = [p for p in current_positions if p.get('contracts', 0) > 0]
                
                if open_positions:
                    # Handle existing positions
                    for position in open_positions:
                        # Check if position should be closed based on strategy
                        should_close = await self._check_position_close(trader, position, current_price)
                        if should_close:
                            logger.info(f"{YELLOW}Closing position for {profile_name} trader{RESET}")
                            await trader.close_position(formatted_symbol, position)
                            
                            # Reset position additions count when position is closed
                            position_additions_count = getattr(self, f"_{profile_name}_position_additions_count", {})
                            if formatted_symbol in position_additions_count:
                                logger.info(f"{YELLOW}Resetting position additions count for {profile_name} trader on {formatted_symbol}{RESET}")
                                position_additions_count[formatted_symbol] = 0
                                setattr(self, f"_{profile_name}_position_additions_count", position_additions_count)
                            
                            # Wait for position to be fully closed
                            await asyncio.sleep(2)
                            # Update positions after closing
                            current_positions = await trader.get_positions(formatted_symbol)
                            open_positions = [p for p in current_positions if p.get('contracts', 0) > 0]
                            
                    # Add position scaling logic for strategic trader
                    if profile_name == "strategic" and open_positions:
                        # Import trap detection for market maker trap checking
                        from omega_ai.mm_trap_detector.mm_trap_detector import MMTrapDetector
                        
                        # Check if we should scale the position
                        try:
                            # Get market data for volume confirmation
                            klines = await trader.get_market_candles(formatted_symbol)
                            market_data = {
                                "volume": float(klines[-1][5]) if klines and len(klines) > 0 else 0,
                                "prev_volume": float(klines[-2][5]) if klines and len(klines) > 1 else 0,
                                "price": current_price,
                                "symbol": self.symbol
                            }
                            
                            # Initialize MM Trap Detector for checking traps
                            mm_detector = MMTrapDetector()
                            
                            # Track position additions count
                            position_additions_count = getattr(self, f"_{profile_name}_position_additions_count", {})
                            if formatted_symbol not in position_additions_count:
                                position_additions_count[formatted_symbol] = 0
                            
                            # Maximum allowed additions (from strategic_trader.py)
                            max_additions = 3
                            
                            # Check if we've reached max additions
                            if position_additions_count[formatted_symbol] < max_additions:
                                # Get the first open position
                                position = open_positions[0]
                                entry_price = float(position.get('entryPrice', 0))
                                side = position.get('side', '')
                                
                                # Define Fibonacci scaling levels
                                scaling_fib_levels = [1.618, 2.618, 4.236]
                                scale_proximity_threshold = 0.01  # 1% proximity
                                
                                # Check if current price is near a Fibonacci scaling level
                                for fib_level in scaling_fib_levels:
                                    target_level = None
                                    if side == "long":
                                        # For longs, we scale on dips (entry_price / fib_level)
                                        target_level = entry_price * (1 - 1/fib_level)
                                        price_diff_pct = abs((current_price - target_level) / target_level)
                                        
                                        if price_diff_pct <= scale_proximity_threshold:
                                            # Check for volume confirmation
                                            volume_confirmed = market_data["volume"] > market_data["prev_volume"] * 1.2
                                            
                                            # Check for market maker traps
                                            trap_detected = await mm_detector.analyze_movement(
                                                current_price, entry_price, market_data["volume"]
                                            )
                                            no_trap = "Organic" in trap_detected
                                            
                                            if volume_confirmed and no_trap:
                                                logger.info(f"{GREEN}Position scaling triggered for {profile_name} trader at {fib_level}x Fibonacci level{RESET}")
                                                
                                                # Calculate additional position size (50% of original)
                                                original_contracts = float(position.get('contracts', 0))
                                                additional_contracts = original_contracts * 0.5
                                                
                                                # Place scaling order
                                                logger.info(f"{GREEN}Adding {additional_contracts} contracts to {side} position for {profile_name} trader{RESET}")
                                                await trader.place_order(
                                                    symbol=formatted_symbol,
                                                    side="buy",  # For longs we're adding on dips
                                                    amount=additional_contracts,
                                                    order_type="market"
                                                )
                                                
                                                # Increment additions count
                                                position_additions_count[formatted_symbol] += 1
                                                setattr(self, f"_{profile_name}_position_additions_count", position_additions_count)
                                                
                                                # Wait for order to process
                                                await asyncio.sleep(2)
                                                break
                                    elif side == "short":
                                        # For shorts, we scale on pumps (entry_price * fib_level)
                                        target_level = entry_price * (1 + 1/fib_level)
                                        price_diff_pct = abs((current_price - target_level) / target_level)
                                        
                                        if price_diff_pct <= scale_proximity_threshold:
                                            # Check for volume confirmation
                                            volume_confirmed = market_data["volume"] > market_data["prev_volume"] * 1.2
                                            
                                            # Check for market maker traps
                                            trap_detected = await mm_detector.analyze_movement(
                                                current_price, entry_price, market_data["volume"]
                                            )
                                            no_trap = "Organic" in trap_detected
                                            
                                            if volume_confirmed and no_trap:
                                                logger.info(f"{GREEN}Position scaling triggered for {profile_name} trader at {fib_level}x Fibonacci level{RESET}")
                                                
                                                # Calculate additional position size (50% of original)
                                                original_contracts = float(position.get('contracts', 0))
                                                additional_contracts = original_contracts * 0.5
                                                
                                                # Place scaling order
                                                logger.info(f"{GREEN}Adding {additional_contracts} contracts to {side} position for {profile_name} trader{RESET}")
                                                await trader.place_order(
                                                    symbol=formatted_symbol,
                                                    side="sell",  # For shorts we're adding on pumps
                                                    amount=additional_contracts,
                                                    order_type="market"
                                                )
                                                
                                                # Increment additions count
                                                position_additions_count[formatted_symbol] += 1
                                                setattr(self, f"_{profile_name}_position_additions_count", position_additions_count)
                                                
                                                # Wait for order to process
                                                await asyncio.sleep(2)
                                                break
                            else:
                                logger.debug(f"{YELLOW}Max position additions reached for {profile_name} trader on {formatted_symbol}{RESET}")
                        except Exception as e:
                            logger.error(f"{RED}Error in position scaling for {profile_name} trader: {str(e)}{RESET}")
                
                # If no open positions, check for new entry
                if not open_positions:
                    # Check if we should enter a new position
                    should_enter = await self._check_new_entry(trader, current_price)
                    if should_enter:
                        # Calculate position size based on leverage and capital
                        position_size = (self.initial_capital * self.leverage) / current_price
                        # Place new order
                        side = "buy" if should_enter.get('side') == "long" else "sell"
                        logger.info(f"{GREEN}Placing new {side} order for {profile_name} trader{RESET}")
                        await trader.place_order(
                            symbol=formatted_symbol,
                            side=side,
                            amount=position_size,
                            order_type="market"
                        )
                
                # Update positions
                logger.debug(f"{CYAN}Updating positions for {profile_name} trader{RESET}")
                updated_positions = await trader.get_positions(formatted_symbol)
                logger.debug(f"{CYAN}Updated positions: {json.dumps(updated_positions, indent=2, cls=DateTimeEncoder)}{RESET}")
                
                # Update performance metrics
                await self._update_performance_metrics(trader, profile_name)
            else:
                logger.error(f"{RED}Failed to get ticker data for {self.symbol} ({profile_name} trader){RESET}")
                if ticker:
                    logger.error(f"{RED}Ticker response: {json.dumps(ticker, indent=2, cls=DateTimeEncoder)}{RESET}")
                else:
                    logger.error(f"{RED}No ticker data returned{RESET}")
                
        except Exception as e:
            logger.error(f"{RED}Error in trader update ({profile_name}): {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            logger.error(f"{RED}Exception traceback: {traceback.format_exc()}{RESET}")
            
            # Send error alert for critical failures
            try:
                error_msg = (
                    f"⚠️ ERROR IN {profile_name.upper()} TRADER\n"
                    f"Symbol: {self.symbol}\n"
                    f"Error: {str(e)}\n"
                    f"Type: {type(e).__name__}"
                )
                await send_telegram_alert(error_msg)
                logger.debug(f"{GREEN}Sent error alert to Telegram{RESET}")
            except Exception as alert_error:
                logger.error(f"{RED}Failed to send error alert: {str(alert_error)}{RESET}")
                
    async def _check_position_close(self, trader: BitGetCCXT, position: Dict[str, Any], current_price: float) -> bool:
        """
        Check if a position should be closed based on strategy.
        
        Args:
            trader: BitGetCCXT instance
            position: Current position information
            current_price: Current market price
            
        Returns:
            bool: True if position should be closed, False otherwise
        """
        try:
            # Get position details
            entry_price = float(position.get('entryPrice', 0))
            side = position.get('side', '')
            contracts = float(position.get('contracts', 0))
            
            if not entry_price or not side or not contracts:
                return False
                
            # Calculate PnL percentage
            if side == "long":
                pnl_percentage = ((current_price - entry_price) / entry_price) * 100
            else:
                pnl_percentage = ((entry_price - current_price) / entry_price) * 100
                
            # Implement your position close logic here
            # For example, close if PnL is above 2% or below -1%
            if pnl_percentage >= 2.0 or pnl_percentage <= -1.0:
                logger.info(f"{YELLOW}Position close signal: PnL {pnl_percentage:.2f}%{RESET}")
                return True
                
            return False
            
        except Exception as e:
            logger.error(f"{RED}Error checking position close: {str(e)}{RESET}")
            return False
            
    async def _check_new_entry(self, trader: BitGetCCXT, current_price: float) -> Optional[Dict[str, str]]:
        """
        Check if we should enter a new position based on strategy.
        
        Args:
            trader: BitGetCCXT instance
            current_price: Current market price
            
        Returns:
            Optional[Dict[str, str]]: Dict with 'side' key if should enter, None otherwise
        """
        try:
            # Implement your entry logic here
            # For example, use Fibonacci levels, moving averages, etc.
            
            # This is a simple example - you should replace with your actual strategy
            # For now, we'll just alternate between long and short positions
            last_side = getattr(self, f"_last_{trader.sub_account}_side", None)
            new_side = "short" if last_side == "long" else "long"
            setattr(self, f"_last_{trader.sub_account}_side", new_side)
            
            logger.info(f"{GREEN}New entry signal: {new_side}{RESET}")
            return {"side": new_side}
            
        except Exception as e:
            logger.error(f"{RED}Error checking new entry: {str(e)}{RESET}")
            return None
            
    async def _update_performance_metrics(self, trader: BitGetCCXT, profile_name: str) -> None:
        """Update and log trader performance metrics."""
        try:
            # Get positions and balance
            positions = await trader.get_positions(f"{self.symbol}/USDT:USDT")
            balance = await trader.get_balance()
            
            # Calculate total PnL
            total_pnl = 0
            for position in positions:
                if position['symbol'] == f"{self.symbol}/USDT:USDT":
                    total_pnl += float(position.get('unrealizedPnl', 0))
            
            # Log performance
            logger.info(
                f"{BLUE}{profile_name.upper()} Performance:\n"
                f"Symbol: {self.symbol}\n"
                f"Total PnL: {total_pnl:.2f} USDT\n"
                f"Active Positions: {len(positions)}{RESET}"
            )
            
            # Get current time
            current_time = datetime.now(timezone.utc)
            
            # Check if PnL alerts are enabled and if it's time to send an alert
            if self.enable_pnl_alerts:
                # Determine if we should send an alert based on the interval
                time_since_last_alert = (current_time - self.last_pnl_alert_time).total_seconds() / 60
                
                # Send alert if we've reached the specified interval and we're in the first 5 seconds of a minute
                if time_since_last_alert >= self.pnl_alert_interval and current_time.second < 5:
                    # Get detailed position information
                    positions_info = ""
                    unrealized_pnl = 0
                    realized_pnl = 0
                    
                    # Calculate PnL values with detailed breakdown
                    unrealized_pnl_by_symbol = {}
                    realized_pnl_by_symbol = {}
                    
                    if positions:
                        for pos in positions:
                            symbol = pos.get('symbol', 'UNKNOWN')
                            side = pos.get('side', 'UNKNOWN').upper()
                            size = float(pos.get('contracts', 0))
                            price = float(pos.get('entryPrice', 0))
                            unreal_pnl = float(pos.get('unrealizedPnl', 0))
                            real_pnl = float(pos.get('realizedPnl', 0))
                            
                            # Track by symbol
                            if symbol not in unrealized_pnl_by_symbol:
                                unrealized_pnl_by_symbol[symbol] = 0
                                realized_pnl_by_symbol[symbol] = 0
                                
                            unrealized_pnl_by_symbol[symbol] += unreal_pnl
                            realized_pnl_by_symbol[symbol] += real_pnl
                            unrealized_pnl += unreal_pnl
                            realized_pnl += real_pnl
                            
                            positions_info += f"• {side}: {size:.4f} @ {price:.2f} USD | Unreal: {unreal_pnl:+.2f} | Real: {real_pnl:+.2f}\n"
                    
                    # Calculate total PnL
                    total_combined_pnl = unrealized_pnl + realized_pnl
                    
                    # Format the position status emoji based on PnL
                    status_emoji = "🟢" if total_combined_pnl >= 0 else "🔴"
                    
                    # Create alert message with a detailed breakdown table format
                    alert_msg = (
                        f"{status_emoji} {profile_name.upper()} TRADER PNL UPDATE\n\n"
                        f"📊 *SUMMARY*\n"
                        f"Symbol: {self.symbol}\n"
                        f"Time: {current_time.strftime('%H:%M:%S UTC')}\n"
                        f"Active Positions: {len(positions)}\n"
                        f"Leverage: {self.leverage}x\n\n"
                    )
                    
                    # Add PnL breakdown by symbol if available
                    if unrealized_pnl_by_symbol:
                        alert_msg += f"💰 *PNL BREAKDOWN*\n"
                        # Add header row
                        alert_msg += f"Symbol | Unrealized | Realized | Total\n"
                        alert_msg += f"-------|------------|----------|------\n"
                        
                        # Add data rows for each symbol
                        for symbol in sorted(unrealized_pnl_by_symbol.keys()):
                            unreal = unrealized_pnl_by_symbol[symbol]
                            real = realized_pnl_by_symbol[symbol]
                            total = unreal + real
                            alert_msg += f"{symbol} | {unreal:+.2f} | {real:+.2f} | {total:+.2f}\n"
                        
                        # Add totals row
                        alert_msg += f"-------|------------|----------|------\n"
                        alert_msg += f"TOTAL | {unrealized_pnl:+.2f} | {realized_pnl:+.2f} | {total_combined_pnl:+.2f}\n\n"
                    
                    # Add position details if available
                    if positions_info:
                        alert_msg += f"📈 *POSITION DETAILS*\n{positions_info}"
                        
                    # Send the alert
                    await send_telegram_alert(alert_msg)
                    logger.info(f"{GREEN}Sent PnL update to Telegram{RESET}")
                    
                    # Update the last alert time
                    self.last_pnl_alert_time = current_time
                
        except Exception as e:
            logger.error(f"{RED}Error updating performance metrics for {profile_name}: {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            
    async def stop_trading(self) -> None:
        """Stop the live trading system and close all positions."""
        # First, get all positions that would be closed
        total_positions = 0
        positions_by_trader = {}
        
        for profile_name, trader in self.traders.items():
            try:
                positions = await trader.get_positions(f"{self.symbol}/USDT:USDT")
                if positions:
                    open_positions = [p for p in positions if p.get('contracts', 0) > 0]
                    if open_positions:
                        total_positions += len(open_positions)
                        positions_by_trader[profile_name] = open_positions
            except Exception as e:
                logger.error(f"{RED}Error getting positions for {profile_name} trader: {str(e)}{RESET}")
        
        if total_positions > 0:
            # Send warning message with position details
            warning_msg = (
                f"⚠️ WARNING: {total_positions} OPEN POSITIONS FOUND\n\n"
                f"Traders with open positions:\n"
            )
            
            for profile_name, positions in positions_by_trader.items():
                warning_msg += f"\n{profile_name.upper()} ({len(positions)} positions):\n"
                for pos in positions:
                    warning_msg += f"- {pos.get('side', 'UNKNOWN')} {pos.get('contracts', 0)} BTC @ ${pos.get('entryPrice', 0)}\n"
            
            warning_msg += "\nDo you want to proceed with closing all positions? (yes/no)"
            
            # Send warning to Telegram
            await send_telegram_alert(warning_msg)
            
            # Wait for user confirmation
            confirmation = await self.wait_for_confirmation()
            if not confirmation:
                logger.info(f"{YELLOW}Position closure cancelled by user{RESET}")
                return
        
        self.is_running = False
        
        for profile_name, trader in self.traders.items():
            try:
                logger.info(f"{YELLOW}Shutting down {profile_name} trader...{RESET}")
                
                # Close all open positions
                logger.info(f"{CYAN}Getting positions for {self.symbol} ({profile_name} trader) before shutdown{RESET}")
                positions = await trader.get_positions(f"{self.symbol}/USDT:USDT")
                
                if positions:
                    logger.info(f"{CYAN}Found {len(positions)} positions to close for {profile_name} trader{RESET}")
                    for position in positions:
                        if position.get('contracts', 0) > 0:
                            logger.info(f"{YELLOW}Closing position for {self.symbol} ({profile_name} trader){RESET}")
                            await trader.close_position(f"{self.symbol}/USDT:USDT", position)
                else:
                    logger.info(f"{GREEN}No open positions to close for {profile_name} trader{RESET}")
                            
                # Send shutdown alert
                alert_msg = (
                    f"🛑 {profile_name.upper()} TRADER SHUTDOWN\n"
                    f"Symbol: {self.symbol}\n"
                    f"Final PnL: {sum(float(p.get('unrealizedPnl', 0)) for p in positions if p.get('symbol') == f'{self.symbol}/USDT:USDT'):.2f} USDT"
                )
                await send_telegram_alert(alert_msg)
                
            except Exception as e:
                logger.error(f"{RED}Error during {profile_name} trader shutdown: {str(e)}{RESET}")
                logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
                logger.error(f"{RED}Exception args: {e.args}{RESET}")
                
        logger.info(f"{GREEN}Live traders system stopped successfully{RESET}")

    async def wait_for_confirmation(self) -> bool:
        """Wait for user confirmation via Telegram."""
        # This is a placeholder - you'll need to implement the actual confirmation logic
        # based on your Telegram bot setup
        try:
            # For now, we'll just wait 30 seconds and assume confirmation
            await asyncio.sleep(30)
            return True
        except Exception as e:
            logger.error(f"{RED}Error waiting for confirmation: {str(e)}{RESET}")
            return False

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='OMEGA BTC AI Live Traders')
    parser.add_argument('--symbol', type=str, default='BTCUSDT',
                      help='Trading symbol (default: BTCUSDT)')
    parser.add_argument('--testnet', action='store_true',
                      help='Use testnet (default: True)')
    parser.add_argument('--mainnet', action='store_true',
                      help='Use mainnet (default: False)')
    parser.add_argument('--capital', type=float, default=24.0,
                      help='Initial capital per trader in USDT (default: 24.0)')
    parser.add_argument('--api-key', type=str, default='',
                      help='BitGet API key')
    parser.add_argument('--secret-key', type=str, default='',
                      help='BitGet secret key')
    parser.add_argument('--passphrase', type=str, default='',
                      help='BitGet API passphrase')
    parser.add_argument('--use-coin-picker', action='store_true',
                      help='Use CoinPicker for symbol verification (default: False)')
    parser.add_argument('--strategic-only', action='store_true',
                      help='Only use the strategic fibonacci trader (default: False)')
    parser.add_argument('--no-pnl-alerts', action='store_true',
                      help='Disable PnL alerts (default: False)')
    parser.add_argument('--pnl-alert-interval', type=int, default=1,
                      help='Interval in minutes for PnL alerts (default: 1)')
    parser.add_argument('--leverage', type=int, default=11,
                      help='Trading leverage (default: 11)')
    
    return parser.parse_args()

async def main():
    """Main entry point for the live traders system."""
    args = parse_args()
    
    # Determine if we should use testnet
    use_testnet = args.testnet or not args.mainnet
    
    # Allow debug option to be set from environment
    debug_mode = os.environ.get("BITGET_DEBUG", "").lower() in ("1", "true", "yes")
    if debug_mode:
        print(f"{YELLOW}Debug mode enabled - will show detailed API information{RESET}")
        # Set debug environment variable for BitGetTrader
        os.environ["BITGET_DEBUG"] = "true"
    
    # Initialize with command line arguments
    live_traders = BitGetLiveTraders(
        use_testnet=use_testnet,
        initial_capital=args.capital,
        symbol=args.symbol,
        api_key=args.api_key,
        secret_key=args.secret_key,
        passphrase=args.passphrase,
        use_coin_picker=args.use_coin_picker,
        strategic_only=args.strategic_only,
        enable_pnl_alerts=not args.no_pnl_alerts,
        pnl_alert_interval=args.pnl_alert_interval,
        leverage=args.leverage
    )
    
    try:
        # Start the trading system
        await live_traders.start_trading()
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Received shutdown signal{RESET}")
    finally:
        await live_traders.stop_trading()

if __name__ == "__main__":
    asyncio.run(main()) 