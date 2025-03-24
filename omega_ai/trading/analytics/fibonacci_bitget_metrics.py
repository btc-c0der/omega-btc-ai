"""
OMEGA BTC AI - Fibonacci BitGet Metrics
======================================

This module provides Fibonacci Golden Ratio analysis for BitGet positions data.
It calculates metrics based on divine proportions and provides data for the
monitoring dashboard.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import logging
import math
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timezone
import json
import asyncio

from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
from omega_ai.trading.exchanges.dual_position_traders import DirectionalBitGetTrader, BitGetDualPositionTraders
from omega_ai.trading.exchanges.quantum_bitget_trader import QuantumBitGetTrader, BioEnergyState

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
PHI = 1.618033988749895  # Golden Ratio
FIBONACCI_LEVELS = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.272, 1.618, 2.618, 4.236]

class FibonacciMetricsCalculator:
    """Calculate Fibonacci-based metrics for trading positions."""
    
    def __init__(self, api_key: str = "", secret_key: str = "", passphrase: str = "", 
                 use_testnet: bool = False, symbol: str = "BTCUSDT"):
        """
        Initialize the Fibonacci metrics calculator.
        
        Args:
            api_key: BitGet API key
            secret_key: BitGet secret key
            passphrase: BitGet API passphrase
            use_testnet: Whether to use testnet (default: False)
            symbol: Trading symbol (default: BTCUSDT)
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.use_testnet = use_testnet
        self.symbol = symbol
        self.dual_trader = None
        self.quantum_trader = None
        self.history = []
        
    async def initialize(self):
        """Initialize traders."""
        try:
            # Initialize dual position trader for long/short analysis
            self.dual_trader = BitGetDualPositionTraders(
                use_testnet=self.use_testnet,
                api_key=self.api_key,
                secret_key=self.secret_key,
                passphrase=self.passphrase,
                symbol=self.symbol,
                enable_pnl_alerts=False  # We'll handle metrics ourselves
            )
            await self.dual_trader.initialize()
            
            # Initialize quantum trader for bio-energy metrics (if available)
            try:
                self.quantum_trader = QuantumBitGetTrader(
                    api_key=self.api_key,
                    secret_key=self.secret_key,
                    passphrase=self.passphrase,
                    use_testnet=self.use_testnet
                )
                logger.info("Quantum trader initialized for bio-energy metrics")
            except ImportError:
                logger.info("Quantum trader not available, skipping bio-energy metrics")
                self.quantum_trader = None
                
            logger.info("Fibonacci metrics calculator initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing Fibonacci metrics calculator: {str(e)}")
            return False
    
    def calculate_phi_resonance(self, long_positions: List[Dict], short_positions: List[Dict]) -> float:
        """
        Calculate Phi resonance of current positions.
        
        Returns:
            float: Phi resonance value (0.0 to 1.0)
        """
        try:
            # Default to 0.5 if no positions
            if not long_positions and not short_positions:
                return 0.5
                
            total_long_size = sum(float(pos.get('contracts', 0)) for pos in long_positions)
            total_short_size = sum(float(pos.get('contracts', 0)) for pos in short_positions)
            
            # If only one side has positions
            if total_long_size == 0 or total_short_size == 0:
                return 0.618  # Golden ratio as the baseline
                
            # Calculate ratio between long and short positions
            long_short_ratio = total_long_size / total_short_size if total_short_size > 0 else 1.0
            
            # Calculate how close the ratio is to PHI (1.618) or its inverse (0.618)
            phi_alignment = min(
                abs(long_short_ratio - PHI) / PHI,
                abs(long_short_ratio - (1/PHI)) / (1/PHI)
            )
            
            # Normalize to a 0-1 scale where 1 is perfect alignment
            phi_resonance = max(0, 1 - phi_alignment)
            
            # Add additional weighting based on position entry points
            if long_positions and short_positions:
                avg_long_entry = sum(float(pos.get('entryPrice', 0)) for pos in long_positions) / len(long_positions)
                avg_short_entry = sum(float(pos.get('entryPrice', 0)) for pos in short_positions) / len(short_positions)
                
                # Check if entries form Fibonacci relation
                entry_ratio = avg_long_entry / avg_short_entry if avg_short_entry > 0 else 1.0
                entry_phi_alignment = min(
                    abs(entry_ratio - PHI) / PHI,
                    abs(entry_ratio - (1/PHI)) / (1/PHI)
                )
                entry_resonance = max(0, 1 - entry_phi_alignment)
                
                # Weight the final resonance (70% size ratio, 30% entry ratio)
                phi_resonance = (0.7 * phi_resonance) + (0.3 * entry_resonance)
            
            return round(phi_resonance, 3)
            
        except Exception as e:
            logger.error(f"Error calculating phi resonance: {str(e)}")
            return 0.5
    
    def calculate_position_balance(self, long_positions: List[Dict], short_positions: List[Dict]) -> Tuple[float, float]:
        """
        Calculate position balance as a ratio of long:short.
        
        Returns:
            Tuple[float, float]: Position balance as (long_ratio, short_ratio)
        """
        try:
            total_long_size = sum(float(pos.get('contracts', 0)) for pos in long_positions)
            total_short_size = sum(float(pos.get('contracts', 0)) for pos in short_positions)
            
            # If no positions, return balanced ratio
            if total_long_size == 0 and total_short_size == 0:
                return (0.5, 0.5)
                
            total_size = total_long_size + total_short_size
            
            # Calculate ratios
            long_ratio = total_long_size / total_size if total_size > 0 else 0.5
            short_ratio = total_short_size / total_size if total_size > 0 else 0.5
            
            # Normalize to a sum of 1.0
            sum_ratios = long_ratio + short_ratio
            if sum_ratios > 0:
                long_ratio = long_ratio / sum_ratios
                short_ratio = short_ratio / sum_ratios
            
            # Create a golden ratio-styled ratio (0.618 : 1.000)
            if long_ratio >= short_ratio:
                normalized_long = 1.0
                normalized_short = short_ratio / long_ratio if long_ratio > 0 else 0.618
            else:
                normalized_short = 1.0
                normalized_long = long_ratio / short_ratio if short_ratio > 0 else 0.618
            
            return (round(normalized_long, 3), round(normalized_short, 3))
            
        except Exception as e:
            logger.error(f"Error calculating position balance: {str(e)}")
            return (0.618, 1.0)
    
    def calculate_entry_harmony(self, long_positions: List[Dict], short_positions: List[Dict], 
                               current_price: float) -> float:
        """
        Calculate how harmoniously the entries align with Fibonacci levels.
        
        Args:
            long_positions: List of long positions
            short_positions: List of short positions
            current_price: Current market price
            
        Returns:
            float: Entry harmony percentage (0.0 to 1.0)
        """
        try:
            # If no positions, return neutral harmony
            if not long_positions and not short_positions:
                return 0.5
                
            harmony_scores = []
            
            # Process long positions
            for pos in long_positions:
                entry_price = float(pos.get('entryPrice', 0))
                if entry_price > 0:
                    # Find closest Fibonacci level
                    price_diff = abs(current_price - entry_price) / current_price
                    closest_fib = min(FIBONACCI_LEVELS, key=lambda x: abs(x - price_diff))
                    
                    # Calculate harmony score (1.0 = perfect alignment with Fibonacci level)
                    alignment_score = 1.0 - (abs(closest_fib - price_diff) / max(closest_fib, 0.01))
                    harmony_scores.append(alignment_score)
            
            # Process short positions
            for pos in short_positions:
                entry_price = float(pos.get('entryPrice', 0))
                if entry_price > 0:
                    # Find closest Fibonacci level (for shorts, invert the diff)
                    price_diff = abs(entry_price - current_price) / entry_price
                    closest_fib = min(FIBONACCI_LEVELS, key=lambda x: abs(x - price_diff))
                    
                    # Calculate harmony score
                    alignment_score = 1.0 - (abs(closest_fib - price_diff) / max(closest_fib, 0.01))
                    harmony_scores.append(alignment_score)
            
            # Return average harmony score
            if harmony_scores:
                avg_harmony = sum(harmony_scores) / len(harmony_scores)
                return round(avg_harmony, 3)
            else:
                return 0.5
                
        except Exception as e:
            logger.error(f"Error calculating entry harmony: {str(e)}")
            return 0.5
    
    def determine_harmonic_state(self, long_pnl: float, short_pnl: float) -> str:
        """
        Determine the current harmonic state of the market.
        
        Args:
            long_pnl: Total PnL for long positions
            short_pnl: Total PnL for short positions
            
        Returns:
            str: Harmonic state (CHAOS, DISCORD, NEUTRAL, HARMONY, DIVINE)
        """
        try:
            # Calculate total PnL
            total_pnl = long_pnl + short_pnl
            
            # Calculate balance between long and short PnL
            if long_pnl == 0 and short_pnl == 0:
                balance = 0.5  # Neutral if no PnL
            elif long_pnl == 0:
                balance = 0.0 if short_pnl < 0 else 1.0
            elif short_pnl == 0:
                balance = 0.0 if long_pnl < 0 else 1.0
            else:
                # Calculate ratio of positive to negative PnL
                pos_pnl = max(long_pnl, 0) + max(short_pnl, 0)
                neg_pnl = abs(min(long_pnl, 0)) + abs(min(short_pnl, 0))
                
                if pos_pnl == 0 and neg_pnl == 0:
                    balance = 0.5
                elif pos_pnl == 0:
                    balance = 0.0  # All negative
                elif neg_pnl == 0:
                    balance = 1.0  # All positive
                else:
                    pnl_ratio = pos_pnl / neg_pnl if neg_pnl > 0 else float('inf')
                    
                    # Check if ratio is close to PHI (1.618)
                    phi_alignment = abs(pnl_ratio - PHI) / PHI
                    balance = max(0.0, min(1.0, 1.0 - phi_alignment))
            
            # Map balance to harmonic state
            if balance < 0.2:
                return "CHAOS"
            elif balance < 0.4:
                return "DISCORD"
            elif balance < 0.6:
                return "NEUTRAL"
            elif balance < 0.8:
                return "HARMONY"
            else:
                return "DIVINE"
                
        except Exception as e:
            logger.error(f"Error determining harmonic state: {str(e)}")
            return "NEUTRAL"
    
    def format_position_data(self, positions: List[Dict], direction: str) -> Dict[str, Any]:
        """
        Format position data for dashboard display.
        
        Args:
            positions: List of positions
            direction: Position direction ("long" or "short")
            
        Returns:
            Dict: Formatted position data
        """
        try:
            # Return empty data if no positions
            if not positions:
                return {
                    "has_position": False,
                    "size": 0.0,
                    "entry_price": 0.0,
                    "liquidation_price": 0.0,
                    "unrealized_pnl": 0.0,
                    "pnl_percentage": 0.0
                }
            
            # Get the largest position (by size)
            position = max(positions, key=lambda p: float(p.get('contracts', 0)))
            
            # Extract and format position data
            size = float(position.get('contracts', 0))
            entry_price = float(position.get('entryPrice', 0))
            current_price = float(position.get('markPrice', entry_price))
            leverage = float(position.get('leverage', 1))
            unrealized_pnl = float(position.get('unrealizedPnl', 0))
            
            # Calculate PnL percentage
            if direction.lower() == "long":
                pnl_percentage = ((current_price - entry_price) / entry_price) * 100 if entry_price > 0 else 0
                liquidation_price = entry_price * (1 - (1 / leverage)) if leverage > 0 else 0
            else:  # short
                pnl_percentage = ((entry_price - current_price) / entry_price) * 100 if entry_price > 0 else 0
                liquidation_price = entry_price * (1 + (1 / leverage)) if leverage > 0 else 0
            
            # Calculate Fibonacci levels
            fib_levels = {}
            if entry_price > 0:
                if direction.lower() == "long":
                    # For long positions, calculate levels above and below entry
                    range_high = entry_price * 1.1  # 10% above entry
                    range_low = entry_price * 0.9   # 10% below entry
                    
                    for level in FIBONACCI_LEVELS:
                        if level <= 0.5:
                            # Levels below entry (retracement)
                            fib_levels[str(level)] = entry_price - ((entry_price - range_low) * level / 0.5)
                        else:
                            # Levels above entry (extension)
                            normalized_level = (level - 0.5) / 0.5  # Normalize to 0-1 range
                            fib_levels[str(level)] = entry_price + ((range_high - entry_price) * normalized_level)
                else:
                    # For short positions, calculate levels above and below entry
                    range_high = entry_price * 1.1  # 10% above entry
                    range_low = entry_price * 0.9   # 10% below entry
                    
                    for level in FIBONACCI_LEVELS:
                        if level <= 0.5:
                            # Levels above entry (retracement)
                            fib_levels[str(level)] = entry_price + ((range_high - entry_price) * level / 0.5)
                        else:
                            # Levels below entry (extension)
                            normalized_level = (level - 0.5) / 0.5  # Normalize to 0-1 range
                            fib_levels[str(level)] = entry_price - ((entry_price - range_low) * normalized_level)
            
            return {
                "has_position": True,
                "size": round(size, 6),
                "entry_price": round(entry_price, 2),
                "current_price": round(current_price, 2),
                "liquidation_price": round(liquidation_price, 2),
                "unrealized_pnl": round(unrealized_pnl, 2),
                "pnl_percentage": round(pnl_percentage, 2),
                "leverage": int(leverage),
                "margin": round(size * entry_price / leverage, 2) if leverage > 0 else 0,
                "fibonacci_levels": {k: round(v, 2) for k, v in fib_levels.items()}
            }
                
        except Exception as e:
            logger.error(f"Error formatting position data: {str(e)}")
            return {"has_position": False, "error": str(e)}
    
    def get_bio_energy_metrics(self) -> Optional[Dict[str, Any]]:
        """
        Get bio-energy metrics if quantum trader is available.
        
        Returns:
            Optional[Dict]: Bio-energy metrics or None
        """
        if not self.quantum_trader:
            return None
            
        try:
            metrics = self.quantum_trader.get_bio_energy_metrics()
            
            # Convert state to string if it's an enum
            if isinstance(metrics.get("state"), BioEnergyState):
                metrics["state"] = metrics["state"].value
                
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting bio-energy metrics: {str(e)}")
            return None
    
    def calculate_performance_metrics(self) -> Dict[str, Any]:
        """
        Calculate performance metrics from position history.
        
        Returns:
            Dict: Performance metrics
        """
        try:
            if not self.history:
                return {
                    "win_rate": 0.0,
                    "avg_win_loss": 0.0,
                    "profit_factor": 0.0,
                    "sharpe_ratio": 0.0
                }
            
            # Count wins and losses
            wins = sum(1 for h in self.history if h.get("pnl", 0) > 0)
            losses = sum(1 for h in self.history if h.get("pnl", 0) < 0)
            
            # Calculate win rate
            total_trades = wins + losses
            win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0
            
            # Calculate average win/loss ratio
            avg_win = sum(h.get("pnl", 0) for h in self.history if h.get("pnl", 0) > 0) / wins if wins > 0 else 0
            avg_loss = abs(sum(h.get("pnl", 0) for h in self.history if h.get("pnl", 0) < 0) / losses) if losses > 0 else 0
            avg_win_loss = avg_win / avg_loss if avg_loss > 0 else float('inf')
            
            # Calculate profit factor
            gross_profit = sum(h.get("pnl", 0) for h in self.history if h.get("pnl", 0) > 0)
            gross_loss = abs(sum(h.get("pnl", 0) for h in self.history if h.get("pnl", 0) < 0))
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
            
            # Calculate Sharpe ratio (simplified)
            returns = [h.get("pnl", 0) for h in self.history]
            avg_return = sum(returns) / len(returns) if returns else 0
            std_dev = math.sqrt(sum((r - avg_return) ** 2 for r in returns) / len(returns)) if returns else 1
            sharpe_ratio = avg_return / std_dev if std_dev > 0 else 0
            
            return {
                "win_rate": round(win_rate, 1),
                "avg_win_loss": round(avg_win_loss, 3),
                "profit_factor": round(profit_factor, 3),
                "sharpe_ratio": round(sharpe_ratio, 3)
            }
                
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {str(e)}")
            return {
                "win_rate": 0.0,
                "avg_win_loss": 0.0,
                "profit_factor": 0.0,
                "sharpe_ratio": 0.0
            }
    
    async def get_current_price(self) -> float:
        """
        Get current price for the symbol.
        
        Returns:
            float: Current price
        """
        try:
            if self.dual_trader and self.dual_trader.long_trader:
                price = await self.dual_trader.long_trader.get_current_price(self.symbol)
                return float(price)
            return 0.0
        except Exception as e:
            logger.error(f"Error getting current price: {str(e)}")
            return 0.0
    
    async def get_fibonacci_metrics(self) -> Dict[str, Any]:
        """
        Get all Fibonacci metrics for the dashboard.
        
        Returns:
            Dict: Complete Fibonacci metrics
        """
        try:
            # Get metrics for long and short positions
            long_positions, long_pnl = await self.dual_trader._get_trader_metrics(self.dual_trader.long_trader)
            short_positions, short_pnl = await self.dual_trader._get_trader_metrics(self.dual_trader.short_trader)
            
            # Get current price
            current_price = await self.get_current_price()
            
            # Calculate Fibonacci metrics
            phi_resonance = self.calculate_phi_resonance(long_positions, short_positions)
            long_ratio, short_ratio = self.calculate_position_balance(long_positions, short_positions)
            entry_harmony = self.calculate_entry_harmony(long_positions, short_positions, current_price)
            harmonic_state = self.determine_harmonic_state(long_pnl, short_pnl)
            
            # Format position data
            long_position = self.format_position_data(long_positions, "long")
            short_position = self.format_position_data(short_positions, "short")
            
            # Get bio-energy metrics if available
            bio_energy = self.get_bio_energy_metrics()
            
            # Get performance metrics
            performance = self.calculate_performance_metrics()
            
            # Compose complete metrics
            metrics = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "symbol": self.symbol,
                "current_price": current_price,
                
                # Fibonacci metrics
                "phi_resonance": phi_resonance,
                "position_balance": {
                    "long": long_ratio,
                    "short": short_ratio,
                    "display": f"{long_ratio:.3f} : {short_ratio:.3f}"
                },
                "entry_harmony": entry_harmony,
                "harmonic_state": harmonic_state,
                "harmonic_value": self._harmonic_state_to_value(harmonic_state),
                
                # Position data
                "long_position": long_position,
                "short_position": short_position,
                
                # PnL data
                "pnl": {
                    "long": round(long_pnl, 2),
                    "short": round(short_pnl, 2),
                    "total": round(long_pnl + short_pnl, 2)
                },
                
                # Bio-energy metrics
                "bio_energy": bio_energy,
                
                # Performance metrics
                "performance": performance
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting Fibonacci metrics: {str(e)}")
            return {"error": str(e)}
    
    def _harmonic_state_to_value(self, state: str) -> float:
        """Convert harmonic state to a numeric value (0-1)."""
        state_values = {
            "CHAOS": 0.0,
            "DISCORD": 0.25,
            "NEUTRAL": 0.5,
            "HARMONY": 0.75,
            "DIVINE": 1.0
        }
        return state_values.get(state, 0.5)
    
    async def add_position_to_history(self, position_data: Dict[str, Any]) -> None:
        """
        Add closed position to history.
        
        Args:
            position_data: Position data
        """
        try:
            # Add position to history
            self.history.append(position_data)
            
            # Keep only last 100 positions
            if len(self.history) > 100:
                self.history = self.history[-100:]
                
            logger.info(f"Added position to history, now have {len(self.history)} entries")
            
        except Exception as e:
            logger.error(f"Error adding position to history: {str(e)}")
    
    async def get_position_history(self) -> List[Dict[str, Any]]:
        """
        Get position history.
        
        Returns:
            List[Dict]: Position history
        """
        return self.history

# Singleton instance for use in API
_calculator_instance = None

async def get_calculator_instance(api_key: str = "", secret_key: str = "", 
                                 passphrase: str = "", use_testnet: bool = False, 
                                 symbol: str = "BTCUSDT") -> FibonacciMetricsCalculator:
    """
    Get or create a singleton instance of the calculator.
    
    Returns:
        FibonacciMetricsCalculator: Calculator instance
    """
    global _calculator_instance
    
    if _calculator_instance is None:
        _calculator_instance = FibonacciMetricsCalculator(
            api_key=api_key,
            secret_key=secret_key,
            passphrase=passphrase,
            use_testnet=use_testnet,
            symbol=symbol
        )
        await _calculator_instance.initialize()
        
    return _calculator_instance

async def main():
    """Test the Fibonacci metrics calculator."""
    # Get API credentials from environment
    import os
    api_key = os.environ.get("BITGET_API_KEY", "")
    secret_key = os.environ.get("BITGET_SECRET_KEY", "")
    passphrase = os.environ.get("BITGET_PASSPHRASE", "")
    
    # Create calculator
    calculator = await get_calculator_instance(
        api_key=api_key,
        secret_key=secret_key,
        passphrase=passphrase,
        use_testnet=True,  # Use testnet for testing
        symbol="BTCUSDT"
    )
    
    # Get metrics
    metrics = await calculator.get_fibonacci_metrics()
    
    # Print metrics (formatted)
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    asyncio.run(main()) 