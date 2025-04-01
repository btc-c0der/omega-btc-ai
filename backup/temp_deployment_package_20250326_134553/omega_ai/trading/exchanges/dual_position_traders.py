"""
OMEGA BTC AI - Dual Position Traders Module
==========================================

This module extends the BitGetLiveTraders to support simultaneous long and short positions
on the BitGet exchange. It manages separate trader instances for long and short positions,
allowing hedging and advanced trading strategies.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import asyncio
import logging
import argparse
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
import json
import os
import sys
import traceback
from inspect import getmembers

from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders, DateTimeEncoder
from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT
from omega_ai.alerts.telegram_market_report import send_telegram_alert

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bitget_dual_traders.log')
    ]
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

class DirectionalBitGetTrader(BitGetLiveTraders):
    """
    Extends BitGetLiveTraders to only trade in one direction (long or short).
    """
    
    def __init__(self, direction: str = "long", **kwargs):
        """
        Initialize with direction restriction.
        
        Args:
            direction: Trading direction, either "long" or "short"
            **kwargs: Arguments to pass to BitGetLiveTraders
        """
        super().__init__(**kwargs)
        self.direction = direction
        logger.info(f"{BLUE}Created DirectionalBitGetTrader with {direction.upper()} only direction{RESET}")
    
    async def get_current_price(self, symbol: str) -> float:
        """
        Get the current price of a symbol directly from CCXT.
        
        Args:
            symbol: Trading symbol
            
        Returns:
            float: Current price of the symbol
            
        Raises:
            Exception: If there's an error getting the price
        """
        try:
            if "strategic" not in self.traders:
                raise ValueError("Strategic trader not initialized")
                
            formatted_symbol = self._format_symbol(symbol)
            ticker = await self.traders["strategic"].exchange.exchange.fetch_ticker(formatted_symbol)
            return float(ticker['last'])
        except Exception as e:
            logger.error(f"{RED}Error getting current price: {str(e)}{RESET}")
            raise
    
    async def _check_new_entry(self, trader, current_price):
        """
        Override the entry check to filter by direction.
        
        Args:
            trader: BitGetCCXT instance
            current_price: Current market price
            
        Returns:
            Optional[Dict]: Dict with 'side' key if should enter, None otherwise
        """
        # Call the parent method
        result = await super()._check_new_entry(trader, current_price)
        
        # If no signal, return None
        if result is None:
            return None
        
        # If the signal doesn't have a 'side' key, pass it through
        if 'side' not in result:
            return result
            
        # If signal matches our direction, return it
        if result.get('side') == self.direction:
            return result
            
        # Log that we're filtering out the opposite direction
        logger.info(f"{YELLOW}Filtering out {result.get('side')} signal from {self.direction}-only trader{RESET}")
        return None

class BitGetDualPositionTraders:
    """
    Manages simultaneous long and short positions on BitGet using separate trader instances.
    """
    
    def __init__(self, 
                 use_testnet: bool = True,
                 long_capital: float = 24.0,
                 short_capital: float = 24.0,
                 symbol: str = "BTCUSDT",
                 api_key: str = "",
                 secret_key: str = "",
                 passphrase: str = "",
                 long_leverage: int = 11,
                 short_leverage: int = 11,
                 enable_pnl_alerts: bool = True,
                 pnl_alert_interval: int = 1,
                 account_limit: float = 0.0,
                 long_sub_account: str = "",
                 short_sub_account: str = "fst_short"):
        """
        Initialize the dual position traders system.
        
        Args:
            use_testnet: Whether to use testnet (default: True)
            long_capital: Initial capital for long trader in USDT (default: 24.0)
            short_capital: Initial capital for short trader in USDT (default: 24.0)
            symbol: Trading symbol (default: BTCUSDT)
            api_key: BitGet API key
            secret_key: BitGet secret key
            passphrase: BitGet API passphrase
            long_leverage: Leverage for long positions (default: 11)
            short_leverage: Leverage for short positions (default: 11)
            enable_pnl_alerts: Whether to enable PnL alerts (default: True)
            pnl_alert_interval: Minute interval for PnL alerts (default: 1)
            account_limit: Maximum total capital to use (0.0 means no limit)
            long_sub_account: Sub-account name for long positions (default from env STRATEGIC_SUB_ACCOUNT_NAME)
            short_sub_account: Sub-account name for short positions (default: fst_short)
        """
        self.use_testnet = use_testnet
        self.long_capital = long_capital
        self.short_capital = short_capital
        self.symbol = symbol
        self.long_leverage = long_leverage
        self.short_leverage = short_leverage
        self.enable_pnl_alerts = enable_pnl_alerts
        self.pnl_alert_interval = pnl_alert_interval
        self.account_limit = account_limit
        
        # Look for API credentials in environment variables if not provided
        self.api_key = api_key or os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
        self.secret_key = secret_key or os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
        self.passphrase = passphrase or os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
        
        # Get sub-account names
        self.long_sub_account = long_sub_account or os.environ.get("STRATEGIC_SUB_ACCOUNT_NAME", "")
        if not self.long_sub_account:
            logger.warning(f"{YELLOW}No long sub-account name provided or found in environment variables{RESET}")
            logger.warning(f"{YELLOW}Sub-accounts are needed for dual positions to work properly{RESET}")
            
        # Set the short sub-account name
        self.short_sub_account = short_sub_account
        
        # Initialize separate traders for long and short positions
        self.long_trader = None
        self.short_trader = None
        self.is_running = False
        
        # Track last PnL alert time
        self.last_pnl_alert_time = datetime.now(timezone.utc)
        
        # Log initialization
        logger.info(f"{CYAN}Initializing BitGetDualPositionTraders with parameters:{RESET}")
        logger.info(f"  use_testnet: {use_testnet}")
        logger.info(f"  long_capital: {long_capital}")
        logger.info(f"  short_capital: {short_capital}")
        logger.info(f"  symbol: {symbol}")
        logger.info(f"  long_leverage: {long_leverage}")
        logger.info(f"  short_leverage: {short_leverage}")
        logger.info(f"  enable_pnl_alerts: {enable_pnl_alerts}")
        logger.info(f"  pnl_alert_interval: {pnl_alert_interval}")
        logger.info(f"  account_limit: {account_limit}")
        logger.info(f"  long_sub_account: {self.long_sub_account}")
        logger.info(f"  short_sub_account: {self.short_sub_account}")
        
    async def initialize(self) -> None:
        """Initialize both long and short traders."""
        try:
            # Save the original environment variable value
            orig_strategic_sub_account = os.environ.get("STRATEGIC_SUB_ACCOUNT_NAME", "")
            
            # Set the long sub-account in the environment
            if self.long_sub_account:
                os.environ["STRATEGIC_SUB_ACCOUNT_NAME"] = self.long_sub_account
                logger.info(f"{BLUE}Set environment variable STRATEGIC_SUB_ACCOUNT_NAME={self.long_sub_account}{RESET}")
            
            # Create long position trader with long sub-account
            self.long_trader = DirectionalBitGetTrader(
                direction="long",
                use_testnet=self.use_testnet,
                initial_capital=self.long_capital,
                symbol=self.symbol,
                api_key=self.api_key,
                secret_key=self.secret_key,
                passphrase=self.passphrase,
                strategic_only=True,  # Only use strategic trader for simplicity
                enable_pnl_alerts=False,  # We'll handle alerts ourselves
                leverage=self.long_leverage
            )
            
            # Now set the short sub-account in the environment
            if self.short_sub_account:
                os.environ["STRATEGIC_SUB_ACCOUNT_NAME"] = self.short_sub_account
                logger.info(f"{BLUE}Set environment variable STRATEGIC_SUB_ACCOUNT_NAME={self.short_sub_account}{RESET}")
            
            # Create short position trader with short sub-account
            self.short_trader = DirectionalBitGetTrader(
                direction="short",
                use_testnet=self.use_testnet,
                initial_capital=self.short_capital,
                symbol=self.symbol,
                api_key=self.api_key,
                secret_key=self.secret_key,
                passphrase=self.passphrase,
                strategic_only=True,  # Only use strategic trader for simplicity
                enable_pnl_alerts=False,  # We'll handle alerts ourselves
                leverage=self.short_leverage
            )
            
            # Restore the original environment variable
            if orig_strategic_sub_account:
                os.environ["STRATEGIC_SUB_ACCOUNT_NAME"] = orig_strategic_sub_account
            else:
                os.environ.pop("STRATEGIC_SUB_ACCOUNT_NAME", None)
            
            # Initialize both traders
            await self.long_trader.initialize()
            await self.short_trader.initialize()
            
            logger.info(f"{GREEN}Both long and short traders initialized successfully{RESET}")
            
            # Log important information about sub-accounts
            logger.info(f"{BLUE}IMPORTANT: This implementation uses separate sub-accounts for dual positions{RESET}")
            logger.info(f"{BLUE}Long positions use sub-account: {self.long_sub_account}{RESET}")
            logger.info(f"{BLUE}Short positions use sub-account: {self.short_sub_account}{RESET}")
            logger.info(f"{BLUE}Ensure both sub-accounts exist in your BitGet account{RESET}")
            
        except Exception as e:
            logger.error(f"{RED}Error initializing dual position traders: {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            raise
    
    async def check_account_limit(self) -> bool:
        """
        Check if the total account usage is below the limit.
        
        Returns:
            bool: True if account is below limit, False otherwise
        """
        if self.account_limit <= 0:
            # No limit set, always return True
            return True
            
        try:
            # We need to check both traders since they use separate sub-accounts
            long_balance = short_balance = 0.0
            
            # Get long trader balance
            if self.long_trader and "strategic" in self.long_trader.traders:
                balance = await self.long_trader.traders["strategic"].get_balance()
                if "USDT" in balance:
                    long_balance = float(balance["USDT"].get("total", 0))
            
            # Get short trader balance
            if self.short_trader and "strategic" in self.short_trader.traders:
                balance = await self.short_trader.traders["strategic"].get_balance()
                if "USDT" in balance:
                    short_balance = float(balance["USDT"].get("total", 0))
            
            # Calculate total balance across both sub-accounts
            total_balance = long_balance + short_balance
            logger.info(f"{BLUE}Total account balance: {total_balance} USDT (Long: {long_balance}, Short: {short_balance}){RESET}")
            logger.info(f"{BLUE}Account limit: {self.account_limit} USDT{RESET}")
            
            if total_balance > self.account_limit:
                logger.warning(f"{RED}Account limit of {self.account_limit} USDT exceeded! Current balance: {total_balance} USDT{RESET}")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"{RED}Error checking account limit: {str(e)}{RESET}")
            return True  # In case of error, allow trading to continue
        
    async def start_trading(self) -> None:
        """Start the dual position trading system."""
        # Initialize traders if not already done
        if not self.long_trader or not self.short_trader:
            await self.initialize()
            
        self.is_running = True
        logger.info(f"{CYAN}Starting OMEGA BTC AI Dual Position Traders System{RESET}")
        
        try:
            await asyncio.gather(
                self._run_long_trader(),
                self._run_short_trader(),
                self._monitor_performance()
            )
                
        except KeyboardInterrupt:
            logger.info(f"{YELLOW}Shutting down dual position traders system...{RESET}")
            await self.stop_trading()
            
    async def _run_long_trader(self) -> None:
        """Run the long position trader."""
        if not self.long_trader:
            logger.error(f"{RED}Long trader not initialized{RESET}")
            return
            
        # Ensure the trader is initialized
        await self.long_trader.initialize()
        
        # Start the trader (using the monkey-patched methods)
        await self.long_trader.start_trading()
        
    async def _run_short_trader(self) -> None:
        """Run the short position trader."""
        if not self.short_trader:
            logger.error(f"{RED}Short trader not initialized{RESET}")
            return
            
        # Ensure the trader is initialized
        await self.short_trader.initialize()
        
        # Start the trader (using the monkey-patched methods)
        await self.short_trader.start_trading()
        
    async def _monitor_performance(self) -> None:
        """Monitor and report performance of both traders."""
        while self.is_running:
            try:
                # Check account limit
                if not await self.check_account_limit():
                    # Account limit exceeded, stop trading
                    logger.warning(f"{RED}Account limit exceeded, stopping trading{RESET}")
                    self.is_running = False
                    await self.stop_trading()
                    break
                
                # Get positions and metrics for both traders
                long_positions, long_pnl = await self._get_trader_metrics(self.long_trader)
                short_positions, short_pnl = await self._get_trader_metrics(self.short_trader)
                
                # Calculate combined metrics
                total_positions = len(long_positions) + len(short_positions)
                total_pnl = long_pnl + short_pnl
                
                # Log performance
                logger.info(
                    f"{BLUE}DUAL POSITION PERFORMANCE:{RESET}\n"
                    f"Symbol: {self.symbol}\n"
                    f"Long PnL: {long_pnl:.2f} USDT ({len(long_positions)} positions)\n"
                    f"Short PnL: {short_pnl:.2f} USDT ({len(short_positions)} positions)\n"
                    f"Total PnL: {total_pnl:.2f} USDT ({total_positions} positions)"
                )
                
                # Send PnL alert if enabled
                await self._send_pnl_alert(long_positions, short_positions, long_pnl, short_pnl)
                
                # Wait before next update
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"{RED}Error in performance monitoring: {str(e)}{RESET}")
                await asyncio.sleep(60)  # Wait before trying again
                
    async def _get_trader_metrics(self, trader) -> Tuple[List[Dict], float]:
        """
        Get positions and PnL for a trader.
        
        Args:
            trader: BitGetLiveTraders instance
            
        Returns:
            Tuple[List[Dict], float]: Positions and total PnL
        """
        if not trader:
            return [], 0.0
            
        try:
            formatted_symbol = f"{self.symbol.replace('USDT', '')}/USDT:USDT"
            positions = []
            total_pnl = 0.0
            
            # Get trader instance
            trader_instance = None
            if "strategic" in trader.traders:
                trader_instance = trader.traders["strategic"]
                
            if trader_instance:
                # Get positions
                positions = await trader_instance.get_positions(formatted_symbol)
                
                # Calculate total PnL
                for position in positions:
                    if position['symbol'] == formatted_symbol:
                        total_pnl += float(position.get('unrealizedPnl', 0))
                        
            return positions, total_pnl
            
        except Exception as e:
            logger.error(f"{RED}Error getting trader metrics: {str(e)}{RESET}")
            return [], 0.0
            
    async def _send_pnl_alert(self, long_positions, short_positions, long_pnl, short_pnl) -> None:
        """
        Send PnL alert to Telegram if enabled.
        
        Args:
            long_positions: List of long positions
            short_positions: List of short positions
            long_pnl: Total long PnL
            short_pnl: Total short PnL
        """
        if not self.enable_pnl_alerts:
            return
            
        # Get current time
        current_time = datetime.now(timezone.utc)
        
        # Check if it's time to send an alert
        time_since_last_alert = (current_time - self.last_pnl_alert_time).total_seconds() / 60
        
        if time_since_last_alert >= self.pnl_alert_interval and current_time.second < 5:
            # Calculate total metrics
            total_pnl = long_pnl + short_pnl
            
            # Format positions info
            positions_info = ""
            
            # Add long positions
            if long_positions:
                positions_info += f"📈 *LONG POSITIONS* ({self.long_sub_account})\n"
                for pos in long_positions:
                    side = pos.get('side', 'UNKNOWN').upper()
                    size = float(pos.get('contracts', 0))
                    price = float(pos.get('entryPrice', 0))
                    unreal_pnl = float(pos.get('unrealizedPnl', 0))
                    real_pnl = float(pos.get('realizedPnl', 0))
                    
                    positions_info += f"• {side}: {size:.4f} @ {price:.2f} USD | Unreal: {unreal_pnl:+.2f} | Real: {real_pnl:+.2f}\n"
                    
                positions_info += "\n"
                
            # Add short positions
            if short_positions:
                positions_info += f"📉 *SHORT POSITIONS* ({self.short_sub_account})\n"
                for pos in short_positions:
                    side = pos.get('side', 'UNKNOWN').upper()
                    size = float(pos.get('contracts', 0))
                    price = float(pos.get('entryPrice', 0))
                    unreal_pnl = float(pos.get('unrealizedPnl', 0))
                    real_pnl = float(pos.get('realizedPnl', 0))
                    
                    positions_info += f"• {side}: {size:.4f} @ {price:.2f} USD | Unreal: {unreal_pnl:+.2f} | Real: {real_pnl:+.2f}\n"
                    
                positions_info += "\n"
            
            # Format the status emoji based on PnL
            status_emoji = "🟢" if total_pnl >= 0 else "🔴"
            
            # Create alert message
            alert_msg = (
                f"{status_emoji} DUAL POSITION TRADERS PNL UPDATE\n\n"
                f"📊 *SUMMARY*\n"
                f"Symbol: {self.symbol}\n"
                f"Time: {current_time.strftime('%H:%M:%S UTC')}\n"
                f"Long PnL: {long_pnl:+.2f} USDT ({len(long_positions)} positions)\n"
                f"Short PnL: {short_pnl:+.2f} USDT ({len(short_positions)} positions)\n"
                f"Total PnL: {total_pnl:+.2f} USDT\n\n"
            )
            
            # Add position details if available
            if positions_info:
                alert_msg += f"📈 *POSITION DETAILS*\n{positions_info}"
                
            # Send the alert
            await send_telegram_alert(alert_msg)
            logger.info(f"{GREEN}Sent PnL update to Telegram{RESET}")
            
            # Update the last alert time
            self.last_pnl_alert_time = current_time
            
    async def stop_trading(self) -> None:
        """Stop the dual position trading system."""
        self.is_running = False
        
        # Stop both traders
        try:
            if self.long_trader:
                await self.long_trader.stop_trading()
        except Exception as e:
            logger.error(f"{RED}Error stopping long trader: {str(e)}{RESET}")
            
        try:
            if self.short_trader:
                await self.short_trader.stop_trading()
        except Exception as e:
            logger.error(f"{RED}Error stopping short trader: {str(e)}{RESET}")
            
        # Send shutdown alert
        try:
            alert_msg = (
                f"🛑 DUAL POSITION TRADERS SHUTDOWN\n"
                f"Symbol: {self.symbol}\n"
                f"Time: {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}"
            )
            await send_telegram_alert(alert_msg)
        except Exception as e:
            logger.error(f"{RED}Error sending shutdown alert: {str(e)}{RESET}")
            
        logger.info(f"{GREEN}Dual position traders system stopped successfully{RESET}")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='OMEGA BTC AI Dual Position Traders')
    parser.add_argument('--symbol', type=str, default='BTCUSDT',
                      help='Trading symbol (default: BTCUSDT)')
    parser.add_argument('--testnet', action='store_true',
                      help='Use testnet (default: False)')
    parser.add_argument('--mainnet', action='store_true', default=True,
                      help='Use mainnet (default: True)')
    parser.add_argument('--long-capital', type=float, default=150.0,
                      help='Initial capital for long trader in USDT (default: 150.0)')
    parser.add_argument('--short-capital', type=float, default=200.0,
                      help='Initial capital for short trader in USDT (default: 200.0)')
    parser.add_argument('--api-key', type=str, default='',
                      help='BitGet API key')
    parser.add_argument('--secret-key', type=str, default='',
                      help='BitGet secret key')
    parser.add_argument('--passphrase', type=str, default='',
                      help='BitGet API passphrase')
    parser.add_argument('--long-leverage', type=int, default=11,
                      help='Leverage for long positions (default: 11)')
    parser.add_argument('--short-leverage', type=int, default=11,
                      help='Leverage for short positions (default: 11)')
    parser.add_argument('--no-pnl-alerts', action='store_true',
                      help='Disable PnL alerts (default: False)')
    parser.add_argument('--pnl-alert-interval', type=int, default=1,
                      help='Interval in minutes for PnL alerts (default: 1)')
    parser.add_argument('--account-limit', type=float, default=1500.0,
                      help='Maximum total account value in USDT (default: 1500.0)')
    parser.add_argument('--long-sub-account', type=str, default='',
                      help='Sub-account name for long positions (default from env STRATEGIC_SUB_ACCOUNT_NAME)')
    parser.add_argument('--short-sub-account', type=str, default='fst_short',
                      help='Sub-account name for short positions (default: fst_short)')
    
    return parser.parse_args()

async def main():
    """Main entry point for the dual position traders system."""
    args = parse_args()
    
    # Determine if we should use testnet
    use_testnet = args.testnet or not args.mainnet
    
    # Initialize with command line arguments
    dual_traders = BitGetDualPositionTraders(
        use_testnet=use_testnet,
        long_capital=args.long_capital,
        short_capital=args.short_capital,
        symbol=args.symbol,
        api_key=args.api_key,
        secret_key=args.secret_key,
        passphrase=args.passphrase,
        long_leverage=args.long_leverage,
        short_leverage=args.short_leverage,
        enable_pnl_alerts=not args.no_pnl_alerts,
        pnl_alert_interval=args.pnl_alert_interval,
        account_limit=args.account_limit,
        long_sub_account=args.long_sub_account,
        short_sub_account=args.short_sub_account
    )
    
    try:
        # Start the trading system
        await dual_traders.start_trading()
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Received shutdown signal{RESET}")
    finally:
        await dual_traders.stop_trading()

if __name__ == "__main__":
    asyncio.run(main()) 