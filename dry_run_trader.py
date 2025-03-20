#!/usr/bin/env python3
"""
OMEGA BTC AI - Dry Run Trader Simulation
=======================================

This script simulates how BitGetLiveTraders would handle an existing position
without executing any real trades. Perfect for testing before going live.

Usage: python dry_run_trader.py
"""

import asyncio
import logging
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders, DateTimeEncoder

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('dry_run_simulation.log')
    ]
)

logger = logging.getLogger("dry_run")

# Terminal colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

class DryRunTrader(BitGetLiveTraders):
    """Modified BitGetLiveTraders that simulates actions without executing them."""
    
    def __init__(self, **kwargs):
        # Add dry run flag
        self.dry_run = True
        self.simulate_position = True
        self.simulated_positions = {}
        self.simulated_candles = []
        self.price_movement = "flat"  # "flat", "up", "down"
        
        # Initialize simulated position data
        self.initial_price = 65000.0  # Simulated entry price for BTC
        self.current_price = 65000.0  # Starting price, will be updated in simulation
        
        # Call parent init with testnet=True to avoid mainnet connections
        kwargs['use_testnet'] = True
        kwargs['enable_pnl_alerts'] = False  # Disable real alerts
        super().__init__(**kwargs)
        
        # Override the traders dict to prevent actual exchange connections
        self.traders = {"strategic": self}
        self.is_initialized = True
        
    async def initialize(self):
        """Skip actual initialization, use simulated data instead."""
        logger.info(f"{CYAN}DryRunTrader initialized with simulated data{RESET}")
        logger.info(f"{CYAN}Simulating BTCUSDT position with 11x leverage{RESET}")
        
        # Create fake candle data
        self._create_simulated_candles(24)  # 24 hourly candles
        
        # Create simulated position
        formatted_symbol = self._format_symbol("BTCUSDT")
        self._create_simulated_position(formatted_symbol)
        
        self.is_running = True
        return True
        
    def _create_simulated_position(self, symbol):
        """Create a simulated 11x long position."""
        # Calculate position size based on initial capital and leverage
        contracts = (self.initial_capital * self.leverage) / self.initial_price
        
        # Create simulated position data structure
        position = {
            "symbol": symbol,
            "side": "long",
            "contracts": contracts,
            "entryPrice": self.initial_price,
            "unrealizedPnl": 0.0,
            "realizedPnl": 0.0,
            "leverage": self.leverage,
            "marginMode": "isolated",
            "liquidationPrice": self.initial_price * 0.91,  # 9% drop for 11x leverage
            "timestamp": datetime.now(timezone.utc)
        }
        
        # Store this by symbol
        self.simulated_positions[symbol] = [position]
        
        logger.info(f"{GREEN}Created simulated 11x long position:{RESET}")
        logger.info(f"  Symbol: {symbol}")
        logger.info(f"  Contracts: {contracts:.8f}")
        logger.info(f"  Entry Price: ${self.initial_price:.2f}")
        logger.info(f"  Liquidation Price: ${position['liquidationPrice']:.2f}")
        
    def _create_simulated_candles(self, num_candles):
        """Create simulated candle data for testing."""
        base_price = self.initial_price
        base_volume = 1000.0
        
        for i in range(num_candles):
            # Simple candle: [timestamp, open, high, low, close, volume]
            candle = [
                int(datetime.now(timezone.utc).timestamp()) - (3600 * (num_candles - i)),  # timestamp
                base_price * (1 - 0.005 + (0.01 * (i % 3))),  # open
                base_price * (1 + 0.01 + (0.005 * (i % 4))),  # high
                base_price * (1 - 0.01 - (0.005 * (i % 3))),  # low
                base_price * (1 - 0.002 + (0.004 * (i % 5))),  # close
                base_volume * (0.8 + (0.4 * (i % 3)))  # volume
            ]
            self.simulated_candles.append(candle)
            
        logger.info(f"{CYAN}Created {num_candles} simulated candles for testing{RESET}")
        
    async def get_market_ticker(self, symbol):
        """Return simulated market data instead of calling the exchange."""
        # Update the price based on the selected movement pattern
        if self.price_movement == "up":
            self.current_price *= 1.001  # Increase by 0.1%
        elif self.price_movement == "down":
            self.current_price *= 0.999  # Decrease by 0.1%
        
        # Return simulated ticker data
        return {
            "symbol": symbol,
            "last": self.current_price,
            "bid": self.current_price * 0.9995,
            "ask": self.current_price * 1.0005,
            "volume": 5000.0,
            "timestamp": datetime.now(timezone.utc).timestamp() * 1000
        }
        
    async def get_positions(self, symbol):
        """Return simulated position data."""
        if symbol in self.simulated_positions and self.simulate_position:
            positions = self.simulated_positions[symbol]
            
            # Update unrealized PnL based on current price
            for pos in positions:
                if pos["side"] == "long":
                    pos["unrealizedPnl"] = (self.current_price - pos["entryPrice"]) * pos["contracts"]
                else:
                    pos["unrealizedPnl"] = (pos["entryPrice"] - self.current_price) * pos["contracts"]
            
            return positions
        return []
        
    async def get_market_candles(self, symbol):
        """Return simulated candle data."""
        return self.simulated_candles
        
    async def place_order(self, symbol, side, amount, order_type):
        """Simulate placing an order without actually executing it."""
        logger.info(f"{MAGENTA}DRY RUN - Order would be placed:{RESET}")
        logger.info(f"  Symbol: {symbol}")
        logger.info(f"  Side: {side}")
        logger.info(f"  Amount: {amount}")
        logger.info(f"  Type: {order_type}")
        logger.info(f"  Current Price: ${self.current_price:.2f}")
        
        # If we're adding to a position, update our simulated position
        if symbol in self.simulated_positions and self.simulate_position:
            positions = self.simulated_positions[symbol]
            
            for pos in positions:
                if (pos["side"] == "long" and side == "buy") or (pos["side"] == "short" and side == "sell"):
                    # Adding to existing position
                    logger.info(f"{GREEN}DRY RUN - Adding {amount} contracts to existing {pos['side']} position{RESET}")
                    pos["contracts"] += amount
                
                    # Calculate new average entry price (for demonstration purposes)
                    pos["entryPrice"] = (pos["entryPrice"] * (pos["contracts"] - amount) + 
                                         self.current_price * amount) / pos["contracts"]
                    
                    logger.info(f"{GREEN}DRY RUN - New position details:{RESET}")
                    logger.info(f"  Total Contracts: {pos['contracts']:.8f}")
                    logger.info(f"  New Avg Entry Price: ${pos['entryPrice']:.2f}")
                    
        return {"id": "dry-run-order-" + datetime.now(timezone.utc).isoformat()}
        
    async def close_position(self, symbol, position):
        """Simulate closing a position without actually executing it."""
        logger.info(f"{YELLOW}DRY RUN - Position would be closed:{RESET}")
        logger.info(f"  Symbol: {symbol}")
        logger.info(f"  Side: {position.get('side', 'unknown')}")
        logger.info(f"  Contracts: {position.get('contracts', 0)}")
        logger.info(f"  Entry Price: ${position.get('entryPrice', 0):.2f}")
        logger.info(f"  Current Price: ${self.current_price:.2f}")
        
        # Calculate PnL
        entry_price = float(position.get('entryPrice', 0))
        contracts = float(position.get('contracts', 0))
        side = position.get('side', '')
        
        pnl = 0
        if side == "long":
            pnl = (self.current_price - entry_price) * contracts
        elif side == "short":
            pnl = (entry_price - self.current_price) * contracts
            
        logger.info(f"{YELLOW}DRY RUN - Closing would result in PnL: ${pnl:.2f}{RESET}")
        
        # Remove from simulated positions if requested
        if symbol in self.simulated_positions and not self.simulate_position:
            self.simulated_positions[symbol] = []
            
        return {"id": "dry-run-close-" + datetime.now(timezone.utc).isoformat()}
        
    async def get_balance(self):
        """Return simulated balance data."""
        # Calculate balance based on initial capital plus any PnL
        total_pnl = 0
        for positions in self.simulated_positions.values():
            for pos in positions:
                total_pnl += float(pos.get('unrealizedPnl', 0))
                
        return {
            "USDT": {
                "free": self.initial_capital + total_pnl,
                "used": 0,
                "total": self.initial_capital + total_pnl
            }
        }
        
    async def setup_trading_config(self, symbol, leverage):
        """Simulate setting up trading configuration."""
        logger.info(f"{CYAN}DRY RUN - Setting up trading config:{RESET}")
        logger.info(f"  Symbol: {symbol}")
        logger.info(f"  Leverage: {leverage}x")
        return True

    def sub_account(self):
        """Return simulated sub account name."""
        return "dry-run-account"
        
    async def start_simulation(self, price_movement="flat", duration=60):
        """
        Run a simulation with the specified price movement pattern.
        
        Args:
            price_movement: "flat", "up", or "down"
            duration: Simulation duration in seconds
        """
        self.price_movement = price_movement
        logger.info(f"{CYAN}Starting dry run simulation with {price_movement} price movement{RESET}")
        logger.info(f"{CYAN}Simulation will run for {duration} seconds{RESET}")
        
        # Initialize
        await self.initialize()
        
        # Run simulation for specified duration
        start_time = datetime.now()
        end_time = start_time.timestamp() + duration
        
        try:
            while datetime.now().timestamp() < end_time and self.is_running:
                # Process each trader (just the strategic one in our case)
                for profile_name, trader in self.traders.items():
                    try:
                        await self._update_trader(trader, profile_name)
                    except Exception as e:
                        logger.error(f"Error in simulation: {str(e)}")
                
                # Wait before next update
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info(f"{YELLOW}Simulation interrupted by user{RESET}")
        finally:
            # Print final state
            await self._print_simulation_summary()
            
    async def _print_simulation_summary(self):
        """Print a summary of the simulation results."""
        logger.info(f"\n{MAGENTA}========== SIMULATION SUMMARY =========={RESET}")
        logger.info(f"{CYAN}Initial Price: ${self.initial_price:.2f}{RESET}")
        logger.info(f"{CYAN}Final Price: ${self.current_price:.2f}{RESET}")
        logger.info(f"{CYAN}Price Change: {((self.current_price - self.initial_price) / self.initial_price * 100):.2f}%{RESET}")
        
        # Print positions
        for symbol, positions in self.simulated_positions.items():
            for pos in positions:
                side = pos.get('side', 'unknown')
                contracts = pos.get('contracts', 0)
                entry_price = pos.get('entryPrice', 0)
                unreal_pnl = pos.get('unrealizedPnl', 0)
                
                logger.info(f"\n{YELLOW}Position:{RESET}")
                logger.info(f"  Symbol: {symbol}")
                logger.info(f"  Side: {side}")
                logger.info(f"  Contracts: {contracts:.8f}")
                logger.info(f"  Entry Price: ${entry_price:.2f}")
                logger.info(f"  Current Price: ${self.current_price:.2f}")
                logger.info(f"  Unrealized PnL: ${unreal_pnl:.2f}")
                
                # Calculate ROI
                roi = 0
                if side == "long":
                    roi = (self.current_price - entry_price) / entry_price * 100 * self.leverage
                elif side == "short":
                    roi = (entry_price - self.current_price) / entry_price * 100 * self.leverage
                    
                logger.info(f"  ROI: {roi:.2f}%")
        
        logger.info(f"{MAGENTA}======================================{RESET}")

async def main():
    """Run the dry run simulation."""
    # Create dry run trader
    dry_run = DryRunTrader(
        symbol="BTCUSDT",
        initial_capital=24.0,
        leverage=11
    )
    
    print(f"{CYAN}OMEGA BTC AI - Dry Run Simulation{RESET}")
    print(f"{YELLOW}Choose a price movement scenario:{RESET}")
    print(f"  1. Flat market (small fluctuations)")
    print(f"  2. Uptrend (price gradually increases)")
    print(f"  3. Downtrend (price gradually decreases)")
    print(f"  4. Rapid pump (price increases quickly)")
    print(f"  5. Rapid dump (price decreases quickly)")
    
    choice = input("Enter your choice (1-5): ")
    
    # Set price movement based on choice
    if choice == "1":
        movement = "flat"
    elif choice == "2":
        movement = "up"
        dry_run.current_price = dry_run.initial_price * 0.99  # Start slightly below entry
    elif choice == "3":
        movement = "down"
        dry_run.current_price = dry_run.initial_price * 1.01  # Start slightly above entry
    elif choice == "4":
        movement = "up"
        dry_run.current_price = dry_run.initial_price * 0.97  # Start below entry
    elif choice == "5":
        movement = "down"
        dry_run.current_price = dry_run.initial_price * 1.03  # Start above entry
    else:
        movement = "flat"
    
    # Adjust multiplier based on rapid scenarios
    if choice in ["4", "5"]:
        if movement == "up":
            # For rapid pump, increase at 0.3% per tick
            dry_run.price_movement = "up"
            class_obj = type(dry_run)
            original_get_ticker = dry_run.get_market_ticker
            
            async def faster_ticker(self, symbol):
                result = await original_get_ticker(symbol)
                self.current_price *= 1.003  # 0.3% increase
                result["last"] = self.current_price
                return result
                
            dry_run.get_market_ticker = faster_ticker.__get__(dry_run, class_obj)
        else:
            # For rapid dump, decrease at 0.3% per tick
            dry_run.price_movement = "down"
            class_obj = type(dry_run)
            original_get_ticker = dry_run.get_market_ticker
            
            async def faster_ticker(self, symbol):
                result = await original_get_ticker(symbol)
                self.current_price *= 0.997  # 0.3% decrease
                result["last"] = self.current_price
                return result
                
            dry_run.get_market_ticker = faster_ticker.__get__(dry_run, class_obj)
    else:
        dry_run.price_movement = movement
    
    duration = int(input("Enter simulation duration in seconds (default 60): ") or 60)
    
    # Run simulation
    await dry_run.start_simulation(price_movement=movement, duration=duration)

if __name__ == "__main__":
    asyncio.run(main()) 