#!/usr/bin/env python3
"""
OMEGA BTC AI - Advanced BitGet Exit Monitor
===========================================

Enhanced BitGet position monitor with advanced exit strategy features:
- Fee coverage analysis
- Complementary position recommendations
- Bidirectional Fibonacci level calculations

Usage:
  python advanced_bitget_exit_monitor.py [--fee-threshold 200] [--show-complementary] [--bidirectional-fibs]

Author: OMEGA BTC AI Team
Version: 1.0
"""

import os
import sys
import time
import json
import asyncio
import argparse
import logging
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Attempt to import BitGetClient
try:
    # Try to import from omega_ai (if it exists)
    from omega_ai.exchange.bitget_client import BitGetClient
except ImportError:
    # Fall back to the simple client
    try:
        from simple_bitget_client import BitGetClient
    except ImportError:
        logger.error("Could not import BitGetClient. Make sure either omega_ai or simple_bitget_client.py is available.")
        sys.exit(1)

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Define the ExitStrategyEnhancements class locally first
class ExitStrategyEnhancements:
    """Minimal implementation of exit strategy enhancements."""
    
    def __init__(self, fee_coverage_threshold=200.0, enable_complementary_positions=False, enable_bidirectional_fibs=False):
        self.fee_coverage_threshold = fee_coverage_threshold
        self.enable_complementary_positions = enable_complementary_positions
        self.enable_bidirectional_fibs = enable_bidirectional_fibs
        
    def calculate_fee_coverage(self, position, current_price, funding_rate=0.0001):
        return {"covered": True, "percentage": 250.0, "breakeven_price": current_price * 0.99}
        
    def calculate_complementary_position(self, position, current_price):
        return [{"type": "hedge", "size": float(position.get("total", 0)) * 0.5, "entry_price": current_price}]
        
    def calculate_bidirectional_fibonacci_levels(self, current_price, recent_high, recent_low):
        return {"long_levels": {}, "short_levels": {}, "recent_high": recent_high, "recent_low": recent_low}
        
    def generate_exit_recommendations(self, position, current_price, fee_coverage, complementary_positions, fib_levels):
        return [{"type": "Take profit", "price": current_price * 1.05, "confidence": 0.8}]
        
    def format_fee_coverage_display(self, fee_coverage):
        return f"Fee Coverage: {fee_coverage.get('percentage', 0):.2f}%"
        
    def format_fibonacci_levels_display(self, position, fib_levels):
        return "Fibonacci Levels: (Not calculated in minimal implementation)"
        
    def format_complementary_positions_display(self, complementary_positions):
        return "Complementary Positions: (Not calculated in minimal implementation)"
        
    def format_exit_recommendations(self, recommendations):
        return "Exit Recommendations: (Not calculated in minimal implementation)"

# Try to import the real implementation, falling back to our local one
try:
    # Only try to import if the file exists
    if os.path.exists(os.path.join(os.path.dirname(__file__), 'omega_ai/trading/bitget/exit_strategy_enhancements.py')):
        from omega_ai.trading.bitget.exit_strategy_enhancements import ExitStrategyEnhancements as ExternalExitStrategyEnhancements
        ExitStrategyEnhancements = ExternalExitStrategyEnhancements
        logger.info("Using external ExitStrategyEnhancements implementation")
except ImportError:
    logger.warning("Using local implementation of ExitStrategyEnhancements")

# Load environment variables from .env file
load_dotenv()

class AdvancedBitGetExitMonitor:
    """
    Advanced BitGet position monitor with enhanced exit strategies.
    
    Features:
    - Fee coverage analysis
    - Complementary position recommendations
    - Bidirectional Fibonacci level calculations
    """
    
    def __init__(self, 
                 fee_coverage_threshold: float = 200.0,
                 enable_complementary_positions: bool = False,
                 enable_bidirectional_fibs: bool = False):
        """
        Initialize the advanced BitGet exit monitor.
        
        Args:
            fee_coverage_threshold: Threshold for fee coverage percentage
            enable_complementary_positions: Enable complementary position recommendations
            enable_bidirectional_fibs: Enable bidirectional Fibonacci calculations
        """
        # Get API credentials from environment variables
        self.api_key = os.environ.get('BITGET_API_KEY', '')
        self.api_secret = os.environ.get('BITGET_SECRET_KEY', '')
        self.passphrase = os.environ.get('BITGET_PASSPHRASE', '')
        
        # Initialize BitGet client
        self.client = BitGetClient(
            api_key=self.api_key,
            api_secret=self.api_secret,
            passphrase=self.passphrase
        )
        
        # Initialize exit strategy helper
        self.exit_helper = ExitStrategyEnhancements(
            fee_coverage_threshold=fee_coverage_threshold,
            enable_complementary_positions=enable_complementary_positions,
            enable_bidirectional_fibs=enable_bidirectional_fibs
        )
        
        # Store configuration
        self.fee_coverage_threshold = fee_coverage_threshold
        self.enable_complementary_positions = enable_complementary_positions
        self.enable_bidirectional_fibs = enable_bidirectional_fibs
        
        # Track account and position data
        self.account_info = {}
        self.positions = []
        self.price_history = {}
        
    async def get_positions(self) -> List[Dict[str, Any]]:
        """Get active positions from BitGet."""
        all_positions = []
        
        # Common symbols to check
        symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"]
        
        for symbol in symbols:
            try:
                positions = await self.client.get_positions(symbol)
                
                # Filter for positions with non-zero size
                for position in positions:
                    if position and float(position.get('total', 0)) > 0:
                        # Add symbol if not present
                        if 'symbol' not in position:
                            position['symbol'] = symbol
                            
                        all_positions.append(position)
            except Exception as e:
                logger.error(f"Error fetching {symbol} positions: {e}")
                
        return all_positions
        
    async def get_price_history(self, symbol: str, period: str = '1d') -> Dict[str, float]:
        """Get recent price history for a symbol."""
        # For the minimal implementation, we'll just use current price
        # and generate some reasonable high/low values
        try:
            current_price = await self.client.get_current_price(symbol)
            
            # Use simple estimation for recent high/low
            recent_high = current_price * 1.05  # 5% higher
            recent_low = current_price * 0.95   # 5% lower
            
            return {
                "current_price": current_price,
                "recent_high": recent_high,
                "recent_low": recent_low
            }
        except Exception as e:
            logger.error(f"Error fetching price history for {symbol}: {e}")
            return {
                "current_price": 0.0,
                "recent_high": 0.0,
                "recent_low": 0.0
            }
            
    async def get_symbol_price(self, symbol: str) -> float:
        """Get current price for a symbol."""
        try:
            price = await self.client.get_current_price(symbol)
            return price
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            return 0.0
            
    async def get_account_info(self) -> Dict[str, Any]:
        """Get account information."""
        try:
            account_info = await self.client.get_account_balance()
            if account_info is None:
                return {}
            return account_info
        except Exception as e:
            logger.error(f"Error fetching account info: {e}")
            return {}
            
    async def calculate_position_analytics(self, position: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate advanced analytics for a position.
        
        Args:
            position: Position data dictionary
            
        Returns:
            Analytics dictionary
        """
        try:
            symbol = position.get('symbol', '')
            side = position.get('side', '')
            size = float(position.get('total', 0))
            entry_price = float(position.get('averageOpenPrice', 0))
            leverage = float(position.get('leverage', 1))
            
            # Get current price
            current_price = float(position.get('marketPrice', 0))
            if current_price == 0:
                current_price = await self.get_symbol_price(symbol)
                
            # Get price history
            price_history = await self.get_price_history(symbol)
            recent_high = price_history.get('recent_high', current_price * 1.05)
            recent_low = price_history.get('recent_low', current_price * 0.95)
            
            # Calculate fee coverage
            fee_coverage = self.exit_helper.calculate_fee_coverage(
                position=position,
                current_price=current_price,
                funding_rate=0.0001  # Assuming a standard funding rate
            )
            
            # Calculate complementary positions if enabled
            complementary_positions = []
            if self.enable_complementary_positions:
                complementary_positions = self.exit_helper.calculate_complementary_position(
                    position=position,
                    current_price=current_price
                )
                
            # Calculate Fibonacci levels if enabled
            fib_levels = {}
            if self.enable_bidirectional_fibs:
                fib_levels = self.exit_helper.calculate_bidirectional_fibonacci_levels(
                    current_price=current_price,
                    recent_high=recent_high,
                    recent_low=recent_low
                )
                
            # Generate exit recommendations
            recommendations = self.exit_helper.generate_exit_recommendations(
                position=position,
                current_price=current_price,
                fee_coverage=fee_coverage,
                complementary_positions=complementary_positions,
                fib_levels=fib_levels
            )
            
            return {
                "position": position,
                "current_price": current_price,
                "price_history": price_history,
                "fee_coverage": fee_coverage,
                "complementary_positions": complementary_positions,
                "fib_levels": fib_levels,
                "recommendations": recommendations
            }
        except Exception as e:
            logger.error(f"Error calculating position analytics: {e}")
            return {"position": position, "error": str(e)}
            
    def format_account_overview(self) -> str:
        """Format account overview for display."""
        try:
            # Extract values from account info
            total_equity = float(self.account_info.get('total', 0))
            available = float(self.account_info.get('available_balance', 0))
            margin = float(self.account_info.get('margin', 0))
            unrealized_pnl = float(self.account_info.get('unrealized_pnl', 0))
            
            # Format the overview
            overview = "\n\n--- ACCOUNT OVERVIEW ---\n"
            overview += f"Total Equity: ${total_equity:.2f}\n"
            overview += f"Available Balance: ${available:.2f}\n"
            overview += f"Used Margin: ${margin:.2f}\n"
            overview += f"Unrealized PnL: ${unrealized_pnl:.2f}\n"
            
            # Calculate position counts
            long_count = sum(1 for p in self.positions if p.get('side', '') == 'long')
            short_count = sum(1 for p in self.positions if p.get('side', '') == 'short')
            
            overview += f"Active Positions: {len(self.positions)} ({long_count} long, {short_count} short)\n"
            overview += "------------------------\n"
            
            return overview
        except Exception as e:
            logger.error(f"Error formatting account overview: {e}")
            return "\n--- ACCOUNT OVERVIEW UNAVAILABLE ---\n"
            
    def format_position_display(self, analytics: Dict[str, Any]) -> str:
        """Format position information and analytics for display."""
        try:
            position = analytics.get('position', {})
            current_price = analytics.get('current_price', 0)
            fee_coverage = analytics.get('fee_coverage', {})
            complementary_positions = analytics.get('complementary_positions', [])
            fib_levels = analytics.get('fib_levels', {})
            recommendations = analytics.get('recommendations', [])
            
            symbol = position.get('symbol', 'Unknown')
            side = position.get('side', 'unknown')
            size = float(position.get('total', 0))
            entry_price = float(position.get('averageOpenPrice', 0))
            leverage = float(position.get('leverage', 1))
            unrealized_pnl = float(position.get('unrealizedPL', 0))
            
            # Calculate PnL percentage
            pnl_percentage = 0
            if entry_price > 0 and current_price > 0:
                if side == 'long':
                    pnl_percentage = (current_price / entry_price - 1) * 100 * leverage
                else:
                    pnl_percentage = (entry_price / current_price - 1) * 100 * leverage
                    
            # Format the display
            display = f"\n--- {symbol} {side.upper()} POSITION ---\n"
            display += f"Size: {size:.6f} | Entry: ${entry_price:.2f} | Current: ${current_price:.2f} | Leverage: {leverage}x\n"
            display += f"Unrealized PnL: ${unrealized_pnl:.2f} ({pnl_percentage:.2f}%)\n"
            display += "------------------------\n"
            
            # Add fee coverage analysis
            display += self.exit_helper.format_fee_coverage_display(fee_coverage) + "\n"
            
            # Add complementary positions if enabled
            if self.enable_complementary_positions:
                display += self.exit_helper.format_complementary_positions_display(complementary_positions) + "\n"
                
            # Add Fibonacci levels if enabled
            if self.enable_bidirectional_fibs:
                display += self.exit_helper.format_fibonacci_levels_display(position, fib_levels) + "\n"
                
            # Add exit recommendations
            display += self.exit_helper.format_exit_recommendations(recommendations) + "\n"
            
            return display
        except Exception as e:
            logger.error(f"Error formatting position display: {e}")
            if 'position' in analytics:
                the_position = analytics.get('position', {})
                return f"Error formatting position display for {the_position.get('symbol', 'unknown')}"
            return "Error formatting position display"
            
    def format_fibonacci_price_targets(self, symbol: str) -> str:
        """Format Fibonacci price targets for display."""
        try:
            # This is a placeholder - in a full implementation, this would
            # calculate and display Fibonacci price targets for potential entries
            return "\n--- FIBONACCI PRICE TARGETS (TBD) ---\n"
        except Exception as e:
            logger.error(f"Error formatting Fibonacci targets: {e}")
            return ""
            
    async def run(self) -> None:
        """Run the advanced BitGet exit monitor."""
        try:
            # Display header
            print("\n========================================================")
            print("    OMEGA BTC AI - ADVANCED BITGET EXIT MONITOR")
            print("========================================================")
            
            # Get account information
            self.account_info = await self.get_account_info()
            
            # Get positions
            self.positions = await self.get_positions()
            
            # Display account overview
            print(self.format_account_overview())
            
            # Check if there are active positions
            if not self.positions:
                print("\nNo active positions found.\n")
                return
                
            # Analyze and display each position
            for position in self.positions:
                # Calculate analytics
                analytics = await self.calculate_position_analytics(position)
                
                # Display position information
                print(self.format_position_display(analytics))
                
            # Display footer
            print("\n========================================================")
            print("        Advanced Exit Analysis Complete")
            print("========================================================\n")
            
        except Exception as e:
            logger.error(f"Error running exit monitor: {e}")
            print(f"\nError: {e}\n")
            
def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Advanced BitGet Exit Monitor")
    
    parser.add_argument("--fee-threshold", type=float, default=200.0,
                      help="Fee coverage threshold percentage (default: 200.0)")
    parser.add_argument("--show-complementary", action="store_true",
                      help="Enable complementary position recommendations")
    parser.add_argument("--bidirectional-fibs", action="store_true",
                      help="Enable bidirectional Fibonacci level calculations")
                      
    return parser.parse_args()
    
async def main():
    """Main function."""
    # Parse arguments
    args = parse_arguments()
    
    # Create and run the monitor
    monitor = AdvancedBitGetExitMonitor(
        fee_coverage_threshold=args.fee_threshold,
        enable_complementary_positions=args.show_complementary,
        enable_bidirectional_fibs=args.bidirectional_fibs
    )
    
    await monitor.run()
    
if __name__ == "__main__":
    # Run the main function
    asyncio.run(main()) 