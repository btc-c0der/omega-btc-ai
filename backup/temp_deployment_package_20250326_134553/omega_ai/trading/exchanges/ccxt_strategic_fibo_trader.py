
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
OMEGA BTC AI - CCXT Strategic Fibonacci Trader
=============================================

This module implements a strategic Fibonacci-based trading system using CCXT
to connect to BitGet's strategic sub-account. It uses Fibonacci levels for
entry and exit points, combined with risk management and position sizing.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import asyncio
import logging
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from dotenv import load_dotenv
from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT
from omega_ai.alerts.telegram_market_report import send_telegram_alert

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('ccxt_strategic_fibo.log')
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

class CCXTStrategicFiboTrader:
    """CCXT-based implementation of the strategic Fibonacci trader."""
    
    def __init__(self,
                 symbol: str = "BTCUSDT",
                 initial_capital: float = 24.0,
                 leverage: int = 11,
                 use_testnet: bool = True,
                 api_key: str = "",
                 secret_key: str = "",
                 passphrase: str = "",
                 sub_account: str = ""):
        """
        Initialize the CCXT strategic Fibonacci trader.
        
        Args:
            symbol: Trading symbol (default: BTCUSDT)
            initial_capital: Initial capital in USDT (default: 24.0)
            leverage: Trading leverage (default: 11)
            use_testnet: Whether to use testnet (default: True)
            api_key: BitGet API key
            secret_key: BitGet secret key
            passphrase: BitGet API passphrase
            sub_account: Sub-account name to use for trading
        """
        self.symbol = symbol
        self.initial_capital = initial_capital
        self.leverage = leverage
        self.use_testnet = use_testnet
        
        # Look for API credentials in environment variables if not provided
        self.api_key = api_key or os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
        self.secret_key = secret_key or os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
        self.passphrase = passphrase or os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
        
        # Set sub-account if provided, or try to get from environment
        self.sub_account = sub_account or os.environ.get("STRATEGIC_SUB_ACCOUNT_NAME", "")
        
        # Initialize CCXT instance
        self.exchange = BitGetCCXT(
            api_key=self.api_key,
            secret_key=self.secret_key,
            passphrase=self.passphrase,
            use_testnet=use_testnet,
            sub_account=self.sub_account
        )
        
        # Log initialization
        logger.info(f"{GREEN}Initialized CCXT Strategic Fibonacci Trader{RESET}")
        logger.info(f"{CYAN}Using {'TESTNET' if use_testnet else 'MAINNET'} environment{RESET}")
        if self.sub_account:
            logger.info(f"{CYAN}Using sub-account: {self.sub_account}{RESET}")
            
        # Trading state
        self.is_running = False
        self.current_price = 0.0
        self.last_trade_time = None
        self.fib_levels = {}
        
        # Risk management
        self.max_position_size = (initial_capital * leverage) / 100  # 1% risk per trade
        self.stop_loss_pct = 0.01  # 1% stop loss
        self.take_profit_pct = 0.02  # 2% take profit
        
    async def initialize(self):
        """Initialize the trading system."""
        try:
            await self.exchange.initialize()
            logger.info(f"{GREEN}Exchange connection initialized{RESET}")
            
            # Set up trading configuration
            await self.exchange.setup_trading_config(self.symbol, self.leverage)
            logger.info(f"{GREEN}Trading configuration set up{RESET}")
            
            # Get initial market data
            await self.update_market_data()
            logger.info(f"{GREEN}Initial market data updated{RESET}")
            
        except Exception as e:
            logger.error(f"{RED}Error initializing trader: {str(e)}{RESET}")
            raise
            
    async def update_market_data(self):
        """Update current market data and calculate Fibonacci levels."""
        try:
            # Get current market data
            ticker = await self.exchange.get_market_ticker(f"{self.symbol}/USDT:USDT")
            if ticker and 'last' in ticker:
                self.current_price = float(ticker['last'])
                logger.info(f"{GREEN}Current price: {self.current_price}{RESET}")
                
                # Calculate Fibonacci levels
                # Note: In a real implementation, you would calculate these based on
                # recent price action and market structure
                self.fib_levels = {
                    '0.0': self.current_price * 0.95,  # Example levels
                    '0.236': self.current_price * 0.97,
                    '0.382': self.current_price * 0.98,
                    '0.5': self.current_price,
                    '0.618': self.current_price * 1.02,
                    '0.786': self.current_price * 1.03,
                    '1.0': self.current_price * 1.05
                }
                logger.info(f"{CYAN}Updated Fibonacci levels{RESET}")
            else:
                logger.error(f"{RED}Failed to get market data{RESET}")
                
        except Exception as e:
            logger.error(f"{RED}Error updating market data: {str(e)}{RESET}")
            
    async def check_entry_signals(self) -> Optional[Dict[str, Any]]:
        """
        Check for entry signals based on Fibonacci levels.
        
        Returns:
            Optional[Dict[str, Any]]: Entry signal if conditions are met
        """
        try:
            # Get current positions
            positions = await self.exchange.get_positions(f"{self.symbol}/USDT:USDT")
            open_positions = [p for p in positions if p.get('contracts', 0) > 0]
            
            if open_positions:
                logger.info(f"{YELLOW}Open positions found, skipping entry check{RESET}")
                return None
                
            # Check if price is near a Fibonacci level
            for level, price in self.fib_levels.items():
                price_diff = abs(self.current_price - price) / price
                if price_diff < 0.001:  # Within 0.1% of a Fibonacci level
                    # Determine if we should go long or short
                    # This is a simplified example - you would want more sophisticated logic
                    side = "buy" if float(level) < 0.5 else "sell"
                    
                    logger.info(f"{GREEN}Entry signal at Fibonacci level {level}{RESET}")
                    return {
                        "side": side,
                        "price": self.current_price,
                        "level": level
                    }
                    
            return None
            
        except Exception as e:
            logger.error(f"{RED}Error checking entry signals: {str(e)}{RESET}")
            return None
            
    async def check_exit_signals(self, position: Dict[str, Any]) -> bool:
        """
        Check if a position should be closed based on Fibonacci levels and risk management.
        
        Args:
            position: Current position information
            
        Returns:
            bool: True if position should be closed, False otherwise
        """
        try:
            entry_price = float(position.get('entryPrice', 0))
            side = position.get('side', '')
            contracts = float(position.get('contracts', 0))
            
            if not entry_price or not side or not contracts:
                return False
                
            # Calculate PnL percentage
            if side == "long":
                pnl_percentage = ((self.current_price - entry_price) / entry_price) * 100
            else:
                pnl_percentage = ((entry_price - self.current_price) / entry_price) * 100
                
            # Check stop loss and take profit
            if pnl_percentage <= -self.stop_loss_pct * 100:
                logger.info(f"{RED}Stop loss triggered at {pnl_percentage:.2f}%{RESET}")
                return True
                
            if pnl_percentage >= self.take_profit_pct * 100:
                logger.info(f"{GREEN}Take profit triggered at {pnl_percentage:.2f}%{RESET}")
                return True
                
            # Check if price has moved to an opposite Fibonacci level
            for level, price in self.fib_levels.items():
                if float(level) < 0.5 and side == "short" and self.current_price <= price:
                    logger.info(f"{YELLOW}Exit signal at Fibonacci level {level}{RESET}")
                    return True
                elif float(level) > 0.5 and side == "long" and self.current_price >= price:
                    logger.info(f"{YELLOW}Exit signal at Fibonacci level {level}{RESET}")
                    return True
                    
            return False
            
        except Exception as e:
            logger.error(f"{RED}Error checking exit signals: {str(e)}{RESET}")
            return False
            
    async def execute_trade(self, signal: Dict[str, Any]):
        """
        Execute a trade based on the entry signal.
        
        Args:
            signal: Entry signal containing trade details
        """
        try:
            # Calculate position size
            position_size = self.max_position_size / self.current_price
            
            # Place the order
            order = await self.exchange.place_order(
                symbol=f"{self.symbol}/USDT:USDT",
                side=signal["side"],
                amount=position_size,
                order_type="market"
            )
            
            if order:
                logger.info(f"{GREEN}Order executed successfully: {order}{RESET}")
                
                # Send trade alert
                alert_msg = (
                    f"🎯 NEW TRADE EXECUTED\n\n"
                    f"Symbol: {self.symbol}\n"
                    f"Side: {signal['side'].upper()}\n"
                    f"Size: {position_size:.4f} BTC\n"
                    f"Price: {self.current_price:.2f}\n"
                    f"Fibonacci Level: {signal['level']}\n"
                    f"Time: {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}"
                )
                await send_telegram_alert(alert_msg)
                
        except Exception as e:
            logger.error(f"{RED}Error executing trade: {str(e)}{RESET}")
            
    async def close_position(self, position: Dict[str, Any]):
        """
        Close an existing position.
        
        Args:
            position: Position information to close
        """
        try:
            await self.exchange.close_position(f"{self.symbol}/USDT:USDT", position)
            logger.info(f"{GREEN}Position closed successfully{RESET}")
            
            # Send position close alert
            alert_msg = (
                f"🔒 POSITION CLOSED\n\n"
                f"Symbol: {self.symbol}\n"
                f"Side: {position.get('side', 'UNKNOWN')}\n"
                f"Size: {position.get('contracts', 0)}\n"
                f"Entry: {position.get('entryPrice', 0)}\n"
                f"Exit: {self.current_price:.2f}\n"
                f"PnL: {position.get('unrealizedPnl', 0):.2f} USDT\n"
                f"Time: {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}"
            )
            await send_telegram_alert(alert_msg)
            
        except Exception as e:
            logger.error(f"{RED}Error closing position: {str(e)}{RESET}")
            
    async def start_trading(self):
        """Start the trading system."""
        self.is_running = True
        logger.info(f"{GREEN}Starting CCXT Strategic Fibonacci Trader{RESET}")
        
        try:
            while self.is_running:
                # Update market data
                await self.update_market_data()
                
                # Check for open positions
                positions = await self.exchange.get_positions(f"{self.symbol}/USDT:USDT")
                open_positions = [p for p in positions if p.get('contracts', 0) > 0]
                
                # Handle open positions
                for position in open_positions:
                    if await self.check_exit_signals(position):
                        await self.close_position(position)
                
                # Check for new entries if no open positions
                if not open_positions:
                    entry_signal = await self.check_entry_signals()
                    if entry_signal:
                        await self.execute_trade(entry_signal)
                
                # Wait before next iteration
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info(f"{YELLOW}Shutting down trader...{RESET}")
            await self.stop_trading()
            
    async def stop_trading(self):
        """Stop the trading system and close all positions."""
        self.is_running = False
        
        try:
            # Close all open positions
            positions = await self.exchange.get_positions(f"{self.symbol}/USDT:USDT")
            for position in positions:
                if position.get('contracts', 0) > 0:
                    await self.close_position(position)
                    
            # Close exchange connection
            await self.exchange.close()
            logger.info(f"{GREEN}Trading system stopped successfully{RESET}")
            
        except Exception as e:
            logger.error(f"{RED}Error stopping trading system: {str(e)}{RESET}")

async def main():
    """Main entry point for the CCXT strategic Fibonacci trader."""
    # Load environment variables
    load_dotenv()
    
    # Create trader instance
    trader = CCXTStrategicFiboTrader(
        symbol="BTCUSDT",
        initial_capital=24.0,
        leverage=11,
        use_testnet=True  # Always use testnet for safety
    )
    
    try:
        # Initialize and start trading
        await trader.initialize()
        await trader.start_trading()
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Received shutdown signal{RESET}")
    finally:
        await trader.stop_trading()

if __name__ == "__main__":
    asyncio.run(main()) 