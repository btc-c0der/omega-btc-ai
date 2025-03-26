#!/usr/bin/env python3
"""
OMEGA BTC AI - Risk Management Utilities
======================================

This module provides utility functions for risk management and
position sizing in trading operations.

Features:
- Position size calculation
- Risk-adjusted lot sizing
- Dynamic risk management
- Account risk tracking
"""

from typing import Dict, Optional
import math

def calculate_position_size(
    entry_price: float,
    stop_loss: float,
    risk_percent: float,
    account_size: float,
    leverage: int = 1,
    min_position_size: float = 0.001,
    max_position_size: Optional[float] = None
) -> float:
    """
    Calculate position size based on risk parameters.
    
    Args:
        entry_price: Entry price for the trade
        stop_loss: Stop loss price
        risk_percent: Percentage of account to risk (0-100)
        account_size: Current account size
        leverage: Leverage multiplier
        min_position_size: Minimum allowed position size
        max_position_size: Maximum allowed position size
        
    Returns:
        Position size in base currency
    """
    try:
        # Validate inputs
        if not all([entry_price, stop_loss, risk_percent, account_size]):
            return 0.0
        
        # Convert risk percent to decimal
        risk_decimal = risk_percent / 100.0
        
        # Calculate risk amount
        risk_amount = account_size * risk_decimal
        
        # Calculate price risk (distance to stop)
        price_risk = abs(entry_price - stop_loss)
        
        if price_risk == 0:
            return 0.0
        
        # Calculate base position size
        position_size = (risk_amount / price_risk) * leverage
        
        # Apply minimum position size
        position_size = max(position_size, min_position_size)
        
        # Apply maximum position size if specified
        if max_position_size:
            position_size = min(position_size, max_position_size)
        
        # Round to 3 decimal places
        position_size = round(position_size, 3)
        
        return position_size
        
    except Exception as e:
        print(f"Error calculating position size: {str(e)}")
        return 0.0

def calculate_risk_ratio(
    entry_price: float,
    stop_loss: float,
    take_profit: float
) -> float:
    """
    Calculate risk-to-reward ratio for a trade.
    
    Args:
        entry_price: Entry price for the trade
        stop_loss: Stop loss price
        take_profit: Take profit price
        
    Returns:
        Risk-to-reward ratio (reward/risk)
    """
    try:
        # Calculate distances
        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)
        
        if risk == 0:
            return 0.0
        
        # Calculate ratio
        ratio = reward / risk
        
        return round(ratio, 2)
        
    except Exception as e:
        print(f"Error calculating risk ratio: {str(e)}")
        return 0.0

def calculate_account_risk(
    open_positions: Dict[str, Dict],
    account_size: float
) -> float:
    """
    Calculate total account risk from open positions.
    
    Args:
        open_positions: Dict of open positions with risk details
        account_size: Current account size
        
    Returns:
        Total account risk as percentage
    """
    try:
        total_risk = 0.0
        
        for position in open_positions.values():
            # Get position details
            entry = float(position.get('entry_price', 0))
            stop = float(position.get('stop_loss', 0))
            size = float(position.get('position_size', 0))
            
            if all([entry, stop, size]):
                # Calculate position risk
                price_risk = abs(entry - stop)
                risk_amount = price_risk * size
                
                # Add to total risk
                total_risk += risk_amount
        
        # Convert to percentage
        risk_percent = (total_risk / account_size) * 100
        
        return round(risk_percent, 2)
        
    except Exception as e:
        print(f"Error calculating account risk: {str(e)}")
        return 0.0

def adjust_position_size(
    base_size: float,
    volatility: float,
    trend_strength: float,
    max_adjustment: float = 0.5
) -> float:
    """
    Adjust position size based on market conditions.
    
    Args:
        base_size: Base position size
        volatility: Market volatility metric (0-1)
        trend_strength: Trend strength metric (-1 to 1)
        max_adjustment: Maximum adjustment factor
        
    Returns:
        Adjusted position size
    """
    try:
        # Validate inputs
        volatility = min(max(volatility, 0), 1)
        trend_strength = min(max(trend_strength, -1), 1)
        
        # Calculate adjustment multiplier
        volatility_factor = 1 - volatility  # Reduce size in high volatility
        trend_factor = abs(trend_strength)  # Increase size in strong trends
        
        # Combine factors
        adjustment = 1.0 + (trend_factor * max_adjustment)  # Increase for strong trends
        adjustment *= volatility_factor  # Decrease for high volatility
        
        # Apply adjustment
        adjusted_size = base_size * adjustment
        
        # Round to 3 decimal places
        adjusted_size = round(adjusted_size, 3)
        
        return adjusted_size
        
    except Exception as e:
        print(f"Error adjusting position size: {str(e)}")
        return base_size

def calculate_max_position_size(
    account_size: float,
    max_risk_percent: float = 2.0,
    leverage: int = 1
) -> float:
    """
    Calculate maximum allowed position size.
    
    Args:
        account_size: Current account size
        max_risk_percent: Maximum risk percentage per trade
        leverage: Leverage multiplier
        
    Returns:
        Maximum position size
    """
    try:
        # Convert risk percent to decimal
        max_risk = max_risk_percent / 100.0
        
        # Calculate maximum position value
        max_position = account_size * max_risk * leverage
        
        # Round to 3 decimal places
        max_position = round(max_position, 3)
        
        return max_position
        
    except Exception as e:
        print(f"Error calculating max position size: {str(e)}")
        return 0.0

def validate_risk_parameters(
    risk_percent: float,
    leverage: int,
    account_size: float,
    max_risk_percent: float = 2.0,
    max_leverage: int = 20
) -> bool:
    """
    Validate risk parameters against safety limits.
    
    Args:
        risk_percent: Risk percentage per trade
        leverage: Leverage multiplier
        account_size: Current account size
        max_risk_percent: Maximum allowed risk percentage
        max_leverage: Maximum allowed leverage
        
    Returns:
        True if parameters are valid, False otherwise
    """
    try:
        # Check risk percent
        if risk_percent <= 0 or risk_percent > max_risk_percent:
            return False
        
        # Check leverage
        if leverage < 1 or leverage > max_leverage:
            return False
        
        # Check account size
        if account_size <= 0:
            return False
        
        # Check total exposure
        total_exposure = account_size * leverage * (risk_percent / 100)
        max_exposure = account_size * 2  # Maximum 2x account size
        
        if total_exposure > max_exposure:
            return False
        
        return True
        
    except Exception as e:
        print(f"Error validating risk parameters: {str(e)}")
        return False 