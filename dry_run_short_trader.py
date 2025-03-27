#!/usr/bin/env python3
"""
OMEGA BTC AI - Dry Run Short Trader Simulation
=============================================

This script simulates how BitGetLiveTraders would handle a short position
without executing any real trades. Perfect for testing before going live.

Usage: python dry_run_short_trader.py
"""

import asyncio
import logging
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders, DateTimeEncoder
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('dry_run_short_simulation.log')
    ]
)

logger = logging.getLogger("dry_run_short")

# Terminal colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

class DryRunShortTrader(BitGetLiveTraders):
    """Modified BitGetLiveTraders that simulates a short position without executing real trades."""
    
    def __init__(self, **kwargs):
        # Add dry run flag
        self.dry_run = True
        self.simulate_position = True
        self.simulated_positions = {}
        self.simulated_candles = []
        self.price_movement = "flat"  # "flat", "up", "down"
        
        # Initialize simulated position data with $84,000 BTC price
        self.initial_price = 84000.0  # Simulated entry price for BTC
        self.current_price = 84000.0  # Starting price, will be updated in simulation
        
        # Call parent init with testnet=True to avoid mainnet connections
        kwargs['use_testnet'] = True
        kwargs['enable_pnl_alerts'] = False  # Disable real alerts
        super().__init__(**kwargs)
        
        # Override the traders dict to prevent actual exchange connections
        self.traders = {"strategic": self}
        self.is_initialized = True
        
    async def initialize(self):
        """Skip actual initialization, use simulated data instead."""
        logger.info(f"{CYAN}DryRunShortTrader initialized with simulated data{RESET}")
        logger.info(f"{CYAN}Simulating BTCUSDT short position with 11x leverage{RESET}")
        logger.info(f"{CYAN}Initial BTC price: ${self.initial_price:.2f}{RESET}")
        
        # Create fake candle data
        self._create_simulated_candles(24)  # 24 hourly candles
        
        # Create simulated position
        formatted_symbol = self._format_symbol("BTCUSDT")
        self._create_simulated_position(formatted_symbol)
        
        self.is_running = True
        return True
        
    def _create_simulated_position(self, symbol):
        """Create a simulated 11x short position."""
        # Calculate position size based on initial capital and leverage
        contracts = (self.initial_capital * self.leverage) / self.initial_price
        
        # Create simulated position data structure
        position = {
            "symbol": symbol,
            "side": "short",  # SHORT position
            "contracts": contracts,
            "entryPrice": self.initial_price,
            "unrealizedPnl": 0.0,
            "realizedPnl": 0.0,
            "leverage": self.leverage,
            "marginMode": "isolated",
            "liquidationPrice": self.initial_price * 1.09,  # 9% rise for 11x leverage
            "timestamp": datetime.now(timezone.utc)
        }
        
        # Store this by symbol
        self.simulated_positions[symbol] = [position]
        
        logger.info(f"{RED}Created simulated 11x short position:{RESET}")
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
                else:  # short position
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
        return "fst_short"  # Use the specific short sub-account name
        
    async def _check_new_entry(self, trader, current_price):
        """
        Override to ensure we only get short entry signals.
        """
        # Always return a short signal for this simulation
        return {"side": "short"}
        
    async def _check_position_close(self, trader, position, current_price):
        """
        Override to check if short position should be closed.
        """
        # Get position details
        entry_price = float(position.get('entryPrice', 0))
        side = position.get('side', '')
        
        if side != "short":
            return False
            
        # Calculate PnL percentage
        pnl_percentage = ((entry_price - current_price) / entry_price) * 100
            
        # Close if PnL is above 2% or below -1%
        if pnl_percentage >= 2.0 or pnl_percentage <= -1.0:
            logger.info(f"{YELLOW}Short position close signal: PnL {pnl_percentage:.2f}%{RESET}")
            return True
            
        return False
        
    async def start_simulation(self, price_movement="flat", duration=60):
        """
        Run a simulation with the specified price movement pattern.
        
        Args:
            price_movement: "flat", "up", or "down"
            duration: Simulation duration in seconds
        """
        self.price_movement = price_movement
        logger.info(f"{CYAN}Starting dry run SHORT simulation with {price_movement} price movement{RESET}")
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
        logger.info(f"\n{MAGENTA}========== SHORT SIMULATION SUMMARY =========={RESET}")
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
    """Run the dry run simulation for a short position."""
    # Create dry run short trader
    dry_run = DryRunShortTrader(
        symbol="BTCUSDT",
        initial_capital=24.0,
        leverage=11
    )
    
    print(f"{CYAN}OMEGA BTC AI - Dry Run SHORT Simulation{RESET}")
    print(f"{YELLOW}Initial BTC Price: ${dry_run.initial_price:.2f}{RESET}")
    print(f"{YELLOW}Choose a price movement scenario:{RESET}")
    print(f"  1. Flat market (small fluctuations)")
    print(f"  2. Uptrend (price gradually increases) - BAD FOR SHORTS")
    print(f"  3. Downtrend (price gradually decreases) - GOOD FOR SHORTS")
    print(f"  4. Rapid pump (price increases quickly) - VERY BAD FOR SHORTS")
    print(f"  5. Rapid dump (price decreases quickly) - VERY GOOD FOR SHORTS")
    print(f"  6. Stepwise dump (drops in distinct steps) - GOOD FOR SHORTS")
    print(f"  7. Flash crash (severe drop followed by partial recovery)")
    print(f"  8. Cascading dump (accelerating downward movement)")
    print(f"  9. Slow bleed (continuous small drops that add up)")
    
    choice = input("Enter your choice (1-9): ")
    
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
    elif choice == "6":
        movement = "stepwise_dump"
        dry_run.current_price = dry_run.initial_price * 1.01  # Start slightly above entry
    elif choice == "7":
        movement = "flash_crash"
        dry_run.current_price = dry_run.initial_price  # Start at entry price
    elif choice == "8":
        movement = "cascading_dump"
        dry_run.current_price = dry_run.initial_price * 1.005  # Start slightly above entry
    elif choice == "9":
        movement = "slow_bleed"
        dry_run.current_price = dry_run.initial_price * 1.005  # Start slightly above entry
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
    elif choice == "6":  # Stepwise dump
        dry_run.price_movement = "stepwise_dump"
        class_obj = type(dry_run)
        original_get_ticker = dry_run.get_market_ticker
        # For stepwise dump: every 5 seconds, drop 1% suddenly
        step_counter = [0]  # Using a list to allow modification in the closure
        
        async def stepwise_ticker(self, symbol):
            result = await original_get_ticker(symbol)
            step_counter[0] += 1
            # Create a step down every 5 ticks
            if step_counter[0] % 5 == 0:
                self.current_price *= 0.99  # 1% sudden drop
                logger.info(f"{RED}STEPWISE DUMP: 1% drop to ${self.current_price:.2f}{RESET}")
            result["last"] = self.current_price
            return result
            
        dry_run.get_market_ticker = stepwise_ticker.__get__(dry_run, class_obj)
    elif choice == "7":  # Flash crash
        dry_run.price_movement = "flash_crash"
        class_obj = type(dry_run)
        original_get_ticker = dry_run.get_market_ticker
        # Flash crash - rapid 15% drop followed by 8% recovery
        crash_states = ["pre-crash", "crashing", "recovering", "post-crash"]
        crash_state = [0]  # Current state index
        crash_counter = [0]  # Tick counter
        orig_price = [dry_run.current_price]  # Original price before crash
        
        async def flash_crash_ticker(self, symbol):
            result = await original_get_ticker(symbol)
            crash_counter[0] += 1
            
            # State machine for flash crash
            if crash_states[crash_state[0]] == "pre-crash" and crash_counter[0] >= 5:
                # After 5 ticks, start the crash
                crash_state[0] = 1  # Move to "crashing" state
                logger.info(f"{RED}FLASH CRASH STARTING FROM ${self.current_price:.2f}{RESET}")
                
            elif crash_states[crash_state[0]] == "crashing":
                # Rapidly drop 3% per tick for 5 ticks (approx 15% total)
                self.current_price *= 0.97
                logger.info(f"{RED}CRASHING: Price now ${self.current_price:.2f}{RESET}")
                if crash_counter[0] >= 10:  # After 5 ticks of crashing
                    crash_state[0] = 2  # Move to "recovering" state
                    logger.info(f"{YELLOW}CRASH COMPLETE: Bottom price ${self.current_price:.2f}{RESET}")
                    
            elif crash_states[crash_state[0]] == "recovering":
                # Recover 2% per tick for 4 ticks (approx 8% recovery)
                self.current_price *= 1.02
                logger.info(f"{GREEN}RECOVERING: Price now ${self.current_price:.2f}{RESET}")
                if crash_counter[0] >= 14:  # After 4 ticks of recovery
                    crash_state[0] = 3  # Move to "post-crash" state
                    logger.info(f"{YELLOW}RECOVERY COMPLETE: Price stabilized at ${self.current_price:.2f}{RESET}")
                    
            # In post-crash state, just small random movements
            if crash_states[crash_state[0]] == "post-crash":
                # Small random movements after crash (0.1% up or down)
                if crash_counter[0] % 2 == 0:
                    self.current_price *= 0.999
                else:
                    self.current_price *= 1.001
                    
            result["last"] = self.current_price
            return result
            
        dry_run.get_market_ticker = flash_crash_ticker.__get__(dry_run, class_obj)
    elif choice == "8":  # Cascading dump
        dry_run.price_movement = "cascading_dump"
        class_obj = type(dry_run)
        original_get_ticker = dry_run.get_market_ticker
        # Cascading dump - starts slow, then accelerates downward
        cascade_counter = [0]
        
        async def cascading_ticker(self, symbol):
            result = await original_get_ticker(symbol)
            cascade_counter[0] += 1
            
            # Calculate drop percentage that increases over time
            # Start with 0.1% drops, gradually increase to 0.5%
            drop_factor = min(0.001 + (cascade_counter[0] * 0.0001), 0.005)
            self.current_price *= (1 - drop_factor)
            
            # Log significant acceleration points
            if cascade_counter[0] == 10:
                logger.info(f"{YELLOW}CASCADING DUMP: Acceleration phase 1, dropping at {drop_factor*100:.3f}% per tick{RESET}")
            elif cascade_counter[0] == 20:
                logger.info(f"{YELLOW}CASCADING DUMP: Acceleration phase 2, dropping at {drop_factor*100:.3f}% per tick{RESET}")
            elif cascade_counter[0] == 30:
                logger.info(f"{RED}CASCADING DUMP: Maximum velocity, dropping at {drop_factor*100:.3f}% per tick{RESET}")
                
            result["last"] = self.current_price
            return result
            
        dry_run.get_market_ticker = cascading_ticker.__get__(dry_run, class_obj)
    elif choice == "9":  # Slow bleed
        dry_run.price_movement = "slow_bleed"
        class_obj = type(dry_run)
        original_get_ticker = dry_run.get_market_ticker
        
        async def slow_bleed_ticker(self, symbol):
            result = await original_get_ticker(symbol)
            # Consistently small drops with tiny random variance
            drop_factor = 0.0015 + (random.random() * 0.0005)  # 0.15% to 0.2% drop per tick
            self.current_price *= (1 - drop_factor)
            result["last"] = self.current_price
            return result
            
        dry_run.get_market_ticker = slow_bleed_ticker.__get__(dry_run, class_obj)
    else:
        dry_run.price_movement = movement
    
    duration = int(input("Enter simulation duration in seconds (default 60): ") or 60)
    
    # Run simulation
    await dry_run.start_simulation(price_movement=movement, duration=duration)

if __name__ == "__main__":
    asyncio.run(main()) 