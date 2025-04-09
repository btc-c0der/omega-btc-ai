"""
OMEGA BTC AI - Advanced Exit Strategy Enhancements (v0.4.0)

This module provides enhanced exit strategies for BitGet positions,
including fee coverage analysis, complementary position recommendations,
and bidirectional Fibonacci level calculations.

Author: OMEGA BTC AI Team
Version: 0.4.0
"""

import logging
from typing import Dict, List, Any, Optional
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('exit_strategy_enhancements')

class ExitStrategyEnhancements:
    """
    Enhanced exit strategies for BitGet positions with advanced techniques.
    
    Features:
    - Fee coverage analysis
    - Complementary position recommendations
    - Bidirectional Fibonacci levels
    - Advanced exit strategy recommendations
    """
    
    def __init__(self, 
                 fee_coverage_threshold: float = 200.0,
                 enable_complementary_positions: bool = True,
                 enable_bidirectional_fibs: bool = True,
                 phi: float = 1.618,
                 inv_phi: float = 0.618):
        """
        Initialize exit strategy enhancements.
        
        Args:
            fee_coverage_threshold: Minimum fee coverage percentage for exit recommendations
            enable_complementary_positions: Whether to enable complementary position calculations
            enable_bidirectional_fibs: Whether to enable bidirectional Fibonacci levels
            phi: Golden Ratio (φ)
            inv_phi: Inverse Golden Ratio (1/φ)
        """
        self.fee_coverage_threshold = fee_coverage_threshold
        self.enable_complementary_positions = enable_complementary_positions
        self.enable_bidirectional_fibs = enable_bidirectional_fibs
        self.PHI = phi
        self.INV_PHI = inv_phi
        
        # Fibonacci levels
        self.FIB_LEVELS = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618]
        
    def calculate_fee_coverage(self, 
                              position: Dict[str, Any],
                              current_price: float, 
                              funding_rate: float = 0.0001) -> Dict[str, Any]:
        """
        Calculate fee coverage for a position.
        
        Args:
            position: Position data
            current_price: Current price
            funding_rate: Current funding rate (default: 0.0001 or 0.01%)
            
        Returns:
            Dictionary with fee coverage metrics
        """
        try:
            # Extract position details
            side = position.get('side', '').lower()
            size = float(position.get('total', 0))
            entry_price = float(position.get('averageOpenPrice', 0))
            leverage = float(position.get('leverage', 1))
            
            if entry_price <= 0 or size <= 0:
                return {}
                
            # Calculate notional value
            notional = size * current_price
            
            # Estimate fees
            # Entry fee: typically 0.05% for market orders
            entry_fee_rate = 0.0005
            entry_fee = notional * entry_fee_rate
            
            # Exit fee: typically 0.05% for market orders
            exit_fee_rate = 0.0005
            exit_fee = notional * exit_fee_rate
            
            # Funding fee: depends on how long position is held
            # Assuming position is held for 8 hours (3 funding intervals)
            funding_intervals = 3
            # For long: negative funding_rate means you receive, positive means you pay
            # For short: positive funding_rate means you receive, negative means you pay
            funding_multiplier = 1 if side == 'long' else -1
            funding_fee = notional * funding_rate * funding_intervals * funding_multiplier
            
            # Calculate total fee
            total_fee = entry_fee + exit_fee + funding_fee
            
            # Calculate current PnL
            if side == 'long':
                price_diff = current_price - entry_price
            else:
                price_diff = entry_price - current_price
                
            unrealized_pnl = price_diff * size
            
            # Calculate fee coverage percentage
            fee_coverage_pct = (unrealized_pnl / total_fee) * 100 if total_fee > 0 else 0
            
            # Calculate breakeven price (including fees)
            if side == 'long':
                breakeven_price = entry_price + (total_fee / size)
            else:
                breakeven_price = entry_price - (total_fee / size)
                
            return {
                'entry_fee': entry_fee,
                'exit_fee': exit_fee,
                'funding_fee': funding_fee,
                'total_fee': total_fee,
                'unrealized_pnl': unrealized_pnl,
                'fee_coverage_pct': fee_coverage_pct,
                'breakeven_price': breakeven_price,
                'is_covered': fee_coverage_pct >= 100
            }
        except Exception as e:
            logger.error(f"Error calculating fee coverage: {e}")
            return {}
            
    def calculate_complementary_position(self, 
                                       position: Dict[str, Any],
                                       current_price: float) -> List[Dict[str, Any]]:
        """
        Calculate complementary position options to hedge unrealized PnL.
        
        Args:
            position: Position data
            current_price: Current price
            
        Returns:
            List of complementary position options
        """
        try:
            if not self.enable_complementary_positions:
                return []
                
            # Extract position details
            side = position.get('side', '').lower()
            size = float(position.get('total', 0))
            entry_price = float(position.get('averageOpenPrice', 0))
            leverage = float(position.get('leverage', 1))
            unrealized_pnl = float(position.get('unrealizedPL', 0))
            
            if entry_price <= 0 or size <= 0 or unrealized_pnl == 0:
                return []
                
            # Complementary side is opposite of current position
            complementary_side = 'long' if side == 'short' else 'short'
            
            # Calculate complementary position options with different entry points
            options = []
            
            # Option 1: Enter at current price (1% retracement)
            options.append({
                'side': complementary_side,
                'entry_price': current_price,
                'entry_type': '1% Retracement',
                'size': abs(unrealized_pnl) / (current_price * 0.01 * leverage),
                'leverage': leverage,
                'hedge_pct': 100.0
            })
            
            # Option 2: Enter at 3.82% retracement (φ * 0.236)
            retracement_pct = 3.82
            if complementary_side == 'long':
                entry_price = current_price * (1 - retracement_pct / 100)
            else:
                entry_price = current_price * (1 + retracement_pct / 100)
                
            options.append({
                'side': complementary_side,
                'entry_price': entry_price,
                'entry_type': '3.82% Retracement',
                'size': abs(unrealized_pnl) / (current_price * (retracement_pct / 100) * leverage),
                'leverage': leverage,
                'hedge_pct': 100.0
            })
            
            # Option 3: Enter at 6.18% retracement (φ * 0.382)
            retracement_pct = 6.18
            if complementary_side == 'long':
                entry_price = current_price * (1 - retracement_pct / 100)
            else:
                entry_price = current_price * (1 + retracement_pct / 100)
                
            options.append({
                'side': complementary_side,
                'entry_price': entry_price,
                'entry_type': '6.18% Retracement',
                'size': abs(unrealized_pnl) / (current_price * (retracement_pct / 100) * leverage),
                'leverage': leverage,
                'hedge_pct': 100.0
            })
            
            # Option 4: Enter at 23.6% retracement (Fibonacci level)
            retracement_pct = 23.6
            if complementary_side == 'long':
                entry_price = current_price * (1 - retracement_pct / 100)
            else:
                entry_price = current_price * (1 + retracement_pct / 100)
                
            options.append({
                'side': complementary_side,
                'entry_price': entry_price,
                'entry_type': '23.6% Retracement',
                'size': abs(unrealized_pnl) / (current_price * (retracement_pct / 100) * leverage),
                'leverage': leverage,
                'hedge_pct': 100.0
            })
            
            return options
        except Exception as e:
            logger.error(f"Error calculating complementary positions: {e}")
            return []
            
    def calculate_bidirectional_fibonacci_levels(self,
                                               current_price: float,
                                               recent_high: float,
                                               recent_low: float) -> Dict[str, Any]:
        """
        Calculate Fibonacci levels for both long and short perspectives.
        
        Args:
            current_price: Current price
            recent_high: Recent high price
            recent_low: Recent low price
            
        Returns:
            Dictionary with Fibonacci levels for both directions
        """
        try:
            if not self.enable_bidirectional_fibs:
                return {}
                
            # Long perspective (retracements from low to high)
            long_levels = {}
            range_long = recent_high - recent_low
            
            for level in self.FIB_LEVELS:
                price = recent_low + (range_long * level)
                distance_pct = ((price - current_price) / current_price) * 100
                
                long_levels[str(level)] = {
                    'price': price,
                    'distance_pct': distance_pct,
                    'is_phi': level in [self.INV_PHI, self.PHI]
                }
                
            # Short perspective (retracements from high to low)
            short_levels = {}
            range_short = recent_high - recent_low
            
            for level in self.FIB_LEVELS:
                price = recent_high - (range_short * level)
                distance_pct = ((price - current_price) / current_price) * 100
                
                short_levels[str(level)] = {
                    'price': price,
                    'distance_pct': distance_pct,
                    'is_phi': level in [self.INV_PHI, self.PHI]
                }
                
            return {
                'long': long_levels,
                'short': short_levels,
                'current_price': current_price,
                'recent_high': recent_high,
                'recent_low': recent_low
            }
        except Exception as e:
            logger.error(f"Error calculating bidirectional Fibonacci levels: {e}")
            return {}
            
    def generate_exit_recommendations(self,
                                    position: Dict[str, Any],
                                    current_price: float,
                                    fee_coverage: Dict[str, Any],
                                    complementary_positions: List[Dict[str, Any]],
                                    fib_levels: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate exit recommendations based on fee coverage, Fibonacci levels, and other factors.
        
        Args:
            position: Position data
            current_price: Current price
            fee_coverage: Fee coverage metrics
            complementary_positions: Complementary position options
            fib_levels: Fibonacci levels
            
        Returns:
            List of exit recommendations
        """
        try:
            recommendations = []
            
            # Extract position details
            side = position.get('side', '').lower()
            size = float(position.get('total', 0))
            entry_price = float(position.get('averageOpenPrice', 0))
            unrealized_pnl = float(position.get('unrealizedPL', 0))
            
            if entry_price <= 0 or size <= 0:
                return []
                
            # Recommendation 1: Exit partially if fees are more than covered
            fee_coverage_pct = fee_coverage.get('fee_coverage_pct', 0)
            
            if fee_coverage_pct >= self.fee_coverage_threshold:
                exit_pct = min(25, int(fee_coverage_pct / 100))  # Exit 1-25% based on coverage
                
                recommendations.append({
                    'type': 'fee_coverage',
                    'description': f"Exit {exit_pct}% of position (fees {int(fee_coverage_pct)}% covered)",
                    'priority': 'medium',
                    'exit_percentage': exit_pct,
                    'exit_price': current_price,
                    'reasoning': f"Fees are {int(fee_coverage_pct)}% covered, securing some profit"
                })
                
            # Recommendation 2: Exit at key Fibonacci level if price is approaching
            if fib_levels and side.lower() in fib_levels:
                side_levels = fib_levels[side.lower()]
                
                # Find closest Fibonacci level that is a resistance (for long) or support (for short)
                closest_key_level = None
                closest_distance = 100.0  # Initialize with a large percentage
                
                for level_key, level_data in side_levels.items():
                    distance_pct = abs(level_data.get('distance_pct', 100))
                    is_phi = level_data.get('is_phi', False)
                    price = level_data.get('price', 0)
                    
                    # Only consider levels in the profitable direction
                    is_profitable = (side == 'long' and price > entry_price) or (side == 'short' and price < entry_price)
                    
                    if is_profitable and distance_pct < 2.0:  # Within 2% of a key level
                        if is_phi or float(level_key) in [0.5, 0.786, 1.0]:  # Key levels
                            if distance_pct < closest_distance:
                                closest_distance = distance_pct
                                closest_key_level = level_data
                                closest_key_level['level'] = level_key
                
                if closest_key_level:
                    level_name = closest_key_level.get('level', '')
                    level_price = closest_key_level.get('price', 0)
                    
                    # Determine exit percentage based on the importance of the level
                    if float(level_name) in [self.INV_PHI, self.PHI]:
                        exit_pct = 50  # Golden ratio levels - exit half
                    elif float(level_name) in [0.5, 0.786, 1.0]:
                        exit_pct = 30  # Key levels - exit a third
                    else:
                        exit_pct = 20  # Minor levels - exit a fifth
                        
                    recommendations.append({
                        'type': 'fibonacci_level',
                        'description': f"Exit {exit_pct}% at {level_name} Fibonacci level (${level_price:.2f})",
                        'priority': 'high' if float(level_name) in [self.INV_PHI, self.PHI] else 'medium',
                        'exit_percentage': exit_pct,
                        'exit_price': level_price,
                        'reasoning': f"Price approaching key Fibonacci level {level_name}"
                    })
                    
            # Recommendation 3: Consider hedging with complementary position if PnL is negative
            if unrealized_pnl < 0 and complementary_positions:
                best_option = complementary_positions[0]  # Default to first option
                
                # Find the option with the Golden Ratio retracement (6.18%)
                for option in complementary_positions:
                    if '6.18%' in option.get('entry_type', ''):
                        best_option = option
                        break
                        
                recommendations.append({
                    'type': 'complementary_hedge',
                    'description': f"Open {best_option.get('side', '').upper()} hedge at {best_option.get('entry_type', '')}",
                    'priority': 'low',
                    'hedge_size': best_option.get('size', 0),
                    'hedge_entry': best_option.get('entry_price', 0),
                    'reasoning': f"Hedge unrealized PnL of ${unrealized_pnl:.2f}"
                })
                
            return sorted(recommendations, key=lambda x: 0 if x['priority'] == 'high' else 1 if x['priority'] == 'medium' else 2)
        except Exception as e:
            logger.error(f"Error generating exit recommendations: {e}")
            return []
            
    def format_fee_coverage_display(self, fee_coverage: Dict[str, Any]) -> str:
        """Format fee coverage information for display."""
        if not fee_coverage:
            return ""
            
        entry_fee = fee_coverage.get('entry_fee', 0)
        exit_fee = fee_coverage.get('exit_fee', 0)
        funding_fee = fee_coverage.get('funding_fee', 0)
        total_fee = fee_coverage.get('total_fee', 0)
        unrealized_pnl = fee_coverage.get('unrealized_pnl', 0)
        fee_coverage_pct = fee_coverage.get('fee_coverage_pct', 0)
        breakeven_price = fee_coverage.get('breakeven_price', 0)
        is_covered = fee_coverage.get('is_covered', False)
        
        # Format the display
        display = "📊 FEE COVERAGE ANALYSIS:\n"
        display += f"  Entry Fee: ${entry_fee:.2f} | Exit Fee: ${exit_fee:.2f} | Funding: ${funding_fee:.2f}\n"
        display += f"  Total Fees: ${total_fee:.2f} | Current PnL: ${unrealized_pnl:.2f}\n"
        display += f"  Fee Coverage: {fee_coverage_pct:.1f}% | Breakeven: ${breakeven_price:.2f}\n"
        
        # Add fee coverage bar
        bar_length = 30
        bar_filled = min(bar_length, int((fee_coverage_pct / 100) * bar_length)) if fee_coverage_pct <= 300 else bar_length
        bar = '█' * bar_filled + '░' * (bar_length - bar_filled)
        
        display += f"  {bar} {min(300, fee_coverage_pct):.1f}%\n"
        
        # Add recommendation
        if fee_coverage_pct >= 200:
            display += "  ✅ Fees are well covered. Consider taking partial profits.\n"
        elif fee_coverage_pct >= 100:
            display += "  ✅ Fees are covered. Position is profitable after fees.\n"
        elif fee_coverage_pct >= 50:
            display += "  ⚠️ Fees are partially covered. Monitor price movement.\n"
        else:
            display += "  ❌ Fees are not covered. Position is underwater after fees.\n"
            
        return display
        
    def format_fibonacci_levels_display(self, position: Dict[str, Any], fib_levels: Dict[str, Any]) -> str:
        """Format Fibonacci levels information for display."""
        if not fib_levels:
            return ""
            
        side = position.get('side', '').lower()
        current_price = fib_levels.get('current_price', 0)
        
        # Determine which side's levels to display primarily
        primary_side = 'short' if side == 'long' else 'long'
        primary_levels = fib_levels.get(primary_side, {})
        secondary_levels = fib_levels.get(side, {})
        
        if not primary_levels and not secondary_levels:
            return ""
            
        # Format the display
        display = f"🔱 FIBONACCI LEVELS ({primary_side.upper()} PERSPECTIVE):\n"
        
        # Filter and sort the most important levels
        key_level_values = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618]
        key_levels = []
        
        for level_val in key_level_values:
            level_key = str(level_val)
            if level_key in primary_levels:
                level_data = primary_levels[level_key]
                level_data['level'] = level_key
                key_levels.append(level_data)
                
        # Sort by distance from current price
        key_levels.sort(key=lambda x: abs(x.get('distance_pct', 100)))
        
        # Display the levels
        for level_data in key_levels:
            level_name = level_data.get('level', '')
            level_price = level_data.get('price', 0)
            distance_pct = level_data.get('distance_pct', 0)
            is_phi = level_data.get('is_phi', False)
            
            # Format the level name
            if level_name == '0.618':
                level_display = "φ⁻¹(0.618)"
            elif level_name == '1.618':
                level_display = "φ(1.618)"
            else:
                level_display = level_name
                
            # Format the direction and symbol
            direction = '↑' if distance_pct > 0 else '↓'
            
            # Format with emphasis for Golden Ratio levels
            if is_phi:
                display += f"  ✨ {level_display}: ${level_price:.2f} ({direction} {abs(distance_pct):.2f}%)\n"
            else:
                display += f"  {level_display}: ${level_price:.2f} ({direction} {abs(distance_pct):.2f}%)\n"
                
        return display
        
    def format_complementary_positions_display(self, complementary_positions: List[Dict[str, Any]]) -> str:
        """Format complementary positions information for display."""
        if not complementary_positions:
            return ""
            
        # Format the display
        display = "🔄 COMPLEMENTARY POSITION OPTIONS:\n"
        
        for option in complementary_positions:
            side = option.get('side', '').upper()
            entry_price = option.get('entry_price', 0)
            entry_type = option.get('entry_type', '')
            size = option.get('size', 0)
            leverage = option.get('leverage', 1)
            hedge_pct = option.get('hedge_pct', 0)
            
            display += f"  {side} at {entry_type} (${entry_price:.2f}):\n"
            display += f"    Size: {size:.4f} | Leverage: {leverage}x | Hedge: {hedge_pct:.1f}%\n"
            
        return display
        
    def format_exit_recommendations(self, recommendations: List[Dict[str, Any]]) -> str:
        """Format exit recommendations for display."""
        if not recommendations:
            return ""
            
        # Format the display
        display = "🚪 EXIT RECOMMENDATIONS:\n"
        
        for i, rec in enumerate(recommendations, 1):
            rec_type = rec.get('type', '')
            description = rec.get('description', '')
            priority = rec.get('priority', '').upper()
            reasoning = rec.get('reasoning', '')
            
            priority_color = "🔴" if priority == "HIGH" else "🟠" if priority == "MEDIUM" else "🟡"
            
            display += f"  {i}. {priority_color} {description}\n"
            display += f"     {reasoning}\n"
            
        return display 