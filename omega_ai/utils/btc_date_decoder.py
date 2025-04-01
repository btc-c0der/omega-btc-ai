#!/usr/bin/env python3
"""
OMEGA BTC AI - Divine BTC Date Decoder
======================================

This module provides advanced timestamp analysis tools that map any 
date to Bitcoin and Fibonacci cycles, revealing cosmic market alignments
and temporal harmonic patterns.

Copyright (C) 2024 OMEGA BTC AI Team
License: GNU General Public License v3.0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import datetime
from typing import Dict, List, Tuple, Any, Optional
import math
import numpy as np
from dateutil.relativedelta import relativedelta
import pytz
import logging
from .fibonacci import GOLDEN_RATIO, FIBONACCI_LEVELS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
BTC_GENESIS_TIMESTAMP = 1231006505  # Bitcoin genesis block timestamp (2009-01-03)
BTC_FIRST_HALVING = datetime.datetime(2012, 11, 28, tzinfo=pytz.UTC)  # First halving date
BTC_SECOND_HALVING = datetime.datetime(2016, 7, 9, tzinfo=pytz.UTC)   # Second halving date
BTC_THIRD_HALVING = datetime.datetime(2020, 5, 11, tzinfo=pytz.UTC)   # Third halving date
BTC_FOURTH_HALVING = datetime.datetime(2024, 4, 20, tzinfo=pytz.UTC)  # Fourth halving date

# Standard cycle lengths in days
MARKET_CYCLES = {
    'micro': 5,           # Very short term cycle
    'short': 13,          # Short term cycle (Fibonacci number)
    'intermediate': 34,   # Medium term cycle (Fibonacci number)
    'primary': 89,        # Primary cycle (Fibonacci number)
    'major': 233,         # Major market cycle (Fibonacci number)
    'grand': 1597,        # Grand super cycle (Fibonacci number)
}

def get_btc_age(timestamp: datetime.datetime) -> relativedelta:
    """
    Calculate Bitcoin's age at the given timestamp.
    
    Args:
        timestamp: Datetime to analyze
        
    Returns:
        RelativeDelta object representing Bitcoin's age
    """
    genesis_date = datetime.datetime.fromtimestamp(BTC_GENESIS_TIMESTAMP, tz=pytz.UTC)
    if timestamp.tzinfo is None:
        timestamp = pytz.UTC.localize(timestamp)
        
    return relativedelta(timestamp, genesis_date)

def get_halving_phase(timestamp: datetime.datetime) -> Dict[str, Any]:
    """
    Determine which Bitcoin halving cycle the timestamp belongs to
    and where it falls within that cycle.
    
    Args:
        timestamp: Datetime to analyze
        
    Returns:
        Dict with halving cycle information
    """
    if timestamp.tzinfo is None:
        timestamp = pytz.UTC.localize(timestamp)
    
    halvings = [
        ("Genesis to First Halving", datetime.datetime.fromtimestamp(BTC_GENESIS_TIMESTAMP, tz=pytz.UTC), BTC_FIRST_HALVING),
        ("First to Second Halving", BTC_FIRST_HALVING, BTC_SECOND_HALVING),
        ("Second to Third Halving", BTC_SECOND_HALVING, BTC_THIRD_HALVING),
        ("Third to Fourth Halving", BTC_THIRD_HALVING, BTC_FOURTH_HALVING),
        ("Post Fourth Halving", BTC_FOURTH_HALVING, datetime.datetime(2028, 5, 1, tzinfo=pytz.UTC))  # Approximate 5th halving
    ]
    
    for cycle_name, start_date, end_date in halvings:
        if start_date <= timestamp < end_date:
            total_days = (end_date - start_date).days
            days_passed = (timestamp - start_date).days
            percentage_complete = (days_passed / total_days) * 100
            days_remaining = total_days - days_passed
            
            # Find where in the Fibonacci cycle this falls
            fib_phase = percentage_complete / 100
            fib_level = "Unknown"
            for i in range(len(FIBONACCI_LEVELS) - 1):
                if FIBONACCI_LEVELS[i] <= fib_phase < FIBONACCI_LEVELS[i+1]:
                    fib_level = f"Between {FIBONACCI_LEVELS[i]} and {FIBONACCI_LEVELS[i+1]}"
                    break
            
            return {
                "cycle_name": cycle_name,
                "start_date": start_date,
                "end_date": end_date,
                "days_passed": days_passed,
                "days_remaining": days_remaining,
                "percentage_complete": percentage_complete,
                "fibonacci_phase": fib_phase,
                "fibonacci_level": fib_level
            }
            
    return {
        "cycle_name": "Unknown future cycle",
        "start_date": None,
        "end_date": None,
        "days_passed": 0,
        "days_remaining": 0,
        "percentage_complete": 0,
        "fibonacci_phase": 0,
        "fibonacci_level": "Unknown"
    }

def calculate_market_cycle_phase(timestamp: datetime.datetime) -> Dict[str, Dict[str, Any]]:
    """
    Calculate where the timestamp falls in different Bitcoin market cycles.
    
    Args:
        timestamp: Datetime to analyze
        
    Returns:
        Dict of cycle information by cycle type
    """
    if timestamp.tzinfo is None:
        timestamp = pytz.UTC.localize(timestamp)
        
    result = {}
    genesis_date = datetime.datetime.fromtimestamp(BTC_GENESIS_TIMESTAMP, tz=pytz.UTC)
    total_days = (timestamp - genesis_date).days
    
    for cycle_name, cycle_length in MARKET_CYCLES.items():
        current_phase = (total_days % cycle_length) / cycle_length
        days_into_cycle = total_days % cycle_length
        days_remaining = cycle_length - days_into_cycle
        
        # Find the corresponding Fibonacci level
        fib_level = "Unknown"
        for i in range(len(FIBONACCI_LEVELS) - 1):
            if FIBONACCI_LEVELS[i] <= current_phase < FIBONACCI_LEVELS[i+1]:
                fib_level = f"Between {FIBONACCI_LEVELS[i]} and {FIBONACCI_LEVELS[i+1]}"
                break
        
        result[cycle_name] = {
            "cycle_length_days": cycle_length,
            "days_into_cycle": days_into_cycle,
            "days_remaining": days_remaining,
            "phase_percentage": current_phase * 100,
            "fibonacci_phase": current_phase,
            "fibonacci_level": fib_level,
            "phase_description": get_phase_description(current_phase)
        }
    
    return result

def get_phase_description(phase: float) -> str:
    """
    Get a qualitative description of a market cycle phase.
    
    Args:
        phase: Phase as fraction (0.0 to 1.0)
        
    Returns:
        String description of the phase
    """
    if phase < 0.236:
        return "Accumulation Phase"
    elif phase < 0.382:
        return "Early Bull Phase"
    elif phase < 0.5:
        return "Mid Bull Phase"
    elif phase < 0.618:
        return "Late Bull Phase"
    elif phase < 0.786:
        return "Distribution Phase"
    elif phase < 0.886:
        return "Early Bear Phase"
    else:
        return "Late Bear Phase"

def calculate_golden_ratio_time_alignment(timestamp: datetime.datetime) -> Dict[str, Any]:
    """
    Calculate how the given timestamp aligns with Golden Ratio time patterns.
    
    Args:
        timestamp: Datetime to analyze
        
    Returns:
        Dict of temporal golden ratio alignments
    """
    if timestamp.tzinfo is None:
        timestamp = pytz.UTC.localize(timestamp)
    
    # Time components
    hour = timestamp.hour
    minute = timestamp.minute
    second = timestamp.second
    day_of_week = timestamp.weekday()
    day_of_month = timestamp.day
    day_of_year = timestamp.timetuple().tm_yday
    
    # Calculate Golden Ratio alignments
    day_cycle_phase = (hour * 3600 + minute * 60 + second) / 86400  # Fraction of day elapsed
    week_cycle_phase = (day_of_week + day_cycle_phase) / 7  # Fraction of week elapsed
    month_phase = (day_of_month - 1 + day_cycle_phase) / 30  # Approximate month phase
    year_phase = (day_of_year - 1 + day_cycle_phase) / 365.25  # Fraction of year elapsed
    
    # Check alignment with golden ratio
    phi = GOLDEN_RATIO
    phi_inverse = 1 / phi
    
    # Calculate proximity to golden ratio points on different time scales
    day_phi_proximity = min(
        abs(day_cycle_phase - phi_inverse), 
        abs(day_cycle_phase - (1 - phi_inverse))
    )
    
    week_phi_proximity = min(
        abs(week_cycle_phase - phi_inverse), 
        abs(week_cycle_phase - (1 - phi_inverse))
    )
    
    month_phi_proximity = min(
        abs(month_phase - phi_inverse), 
        abs(month_phase - (1 - phi_inverse))
    )
    
    year_phi_proximity = min(
        abs(year_phase - phi_inverse), 
        abs(year_phase - (1 - phi_inverse))
    )
    
    # Normalize to a 0-1 scale where 1 is perfect alignment
    day_alignment = 1 - (day_phi_proximity / 0.5)
    week_alignment = 1 - (week_phi_proximity / 0.5)
    month_alignment = 1 - (month_phi_proximity / 0.5)
    year_alignment = 1 - (year_phi_proximity / 0.5)
    
    # Calculate overall golden ratio time harmony
    overall_harmony = (day_alignment + week_alignment + month_alignment + year_alignment) / 4
    
    return {
        "day_cycle_phase": day_cycle_phase,
        "week_cycle_phase": week_cycle_phase,
        "month_phase": month_phase,
        "year_phase": year_phase,
        "day_golden_ratio_alignment": day_alignment,
        "week_golden_ratio_alignment": week_alignment,
        "month_golden_ratio_alignment": month_alignment,
        "year_golden_ratio_alignment": year_alignment,
        "overall_temporal_harmony": overall_harmony,
        "harmony_description": get_harmony_description(overall_harmony)
    }

def get_harmony_description(harmony_score: float) -> str:
    """
    Get a qualitative description of temporal harmony.
    
    Args:
        harmony_score: Harmony score from 0 to 1
        
    Returns:
        String description of harmony
    """
    if harmony_score > 0.9:
        return "Perfect Divine Alignment"
    elif harmony_score > 0.8:
        return "Strong Sacred Harmony"
    elif harmony_score > 0.7:
        return "Clear Golden Flow"
    elif harmony_score > 0.6:
        return "Moderate Temporal Alignment"
    elif harmony_score > 0.5:
        return "Slight Fibonacci Resonance"
    else:
        return "Minimal Temporal Harmony"

def analyze_date(date_str: Optional[str] = None, timestamp: Optional[datetime.datetime] = None) -> Dict[str, Any]:
    """
    Comprehensive analysis of a date string or timestamp in relation to 
    Bitcoin and Fibonacci cycles.
    
    Args:
        date_str: Date string in YYYY-MM-DD or YYYY-MM-DD HH:MM:SS format
        timestamp: Datetime object
        
    Returns:
        Dict with comprehensive cycle analysis
    """
    if timestamp is None and date_str is None:
        timestamp = datetime.datetime.now(pytz.UTC)
    elif date_str is not None and timestamp is None:
        try:
            # Try to parse with time
            timestamp = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # Try to parse date only
            try:
                timestamp = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                logger.error(f"Invalid date format: {date_str}. Use YYYY-MM-DD or YYYY-MM-DD HH:MM:SS")
                return {"error": f"Invalid date format: {date_str}"}
        
        timestamp = pytz.UTC.localize(timestamp)
    
    # Ensure timestamp is not None at this point
    if timestamp is None:
        # This should not happen given the logic above, but just to satisfy the type checker
        timestamp = datetime.datetime.now(pytz.UTC)
    
    # Perform all analyses with guaranteed non-None timestamp
    btc_age = get_btc_age(timestamp)
    halving_phase = get_halving_phase(timestamp)
    market_cycles = calculate_market_cycle_phase(timestamp)
    time_alignment = calculate_golden_ratio_time_alignment(timestamp)
    
    # Calculate divine date score (0-1 scale)
    # This is a combined score of various alignments
    harmony_score = time_alignment["overall_temporal_harmony"] * 0.4
    
    # Add halving cycle contribution
    halving_phase_contribution = 0
    if halving_phase["percentage_complete"]:
        halving_phase_value = halving_phase["percentage_complete"] / 100
        # Higher score when closer to phi or 1-phi
        halving_phase_contribution = 1 - min(
            abs(halving_phase_value - (1/GOLDEN_RATIO)), 
            abs(halving_phase_value - (1 - 1/GOLDEN_RATIO))
        ) * 2
    harmony_score += halving_phase_contribution * 0.3
    
    # Add market cycle contribution 
    cycle_contribution = 0
    for cycle_info in market_cycles.values():
        cycle_phase = cycle_info["fibonacci_phase"]
        # Higher score when closer to phi or 1-phi
        cycle_alignment = 1 - min(
            abs(cycle_phase - (1/GOLDEN_RATIO)), 
            abs(cycle_phase - (1 - 1/GOLDEN_RATIO))
        ) * 2
        cycle_contribution += cycle_alignment
    
    harmony_score += (cycle_contribution / len(market_cycles)) * 0.3
    
    # Ensure score is between 0 and 1
    harmony_score = max(0, min(1, harmony_score))
    
    # Timestamp is guaranteed to be non-None at this point
    genesis_date = datetime.datetime.fromtimestamp(BTC_GENESIS_TIMESTAMP, tz=pytz.UTC)
    
    return {
        "timestamp": timestamp,
        "date_str": timestamp.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "btc_age": {
            "years": btc_age.years,
            "months": btc_age.months,
            "days": btc_age.days,
            "total_days": (timestamp - genesis_date).days
        },
        "halving_phase": halving_phase,
        "market_cycles": market_cycles,
        "time_alignment": time_alignment,
        "divine_date_score": harmony_score,
        "divine_date_rating": get_divine_date_rating(harmony_score)
    }

def get_divine_date_rating(score: float) -> str:
    """
    Get a qualitative rating for the divine date score.
    
    Args:
        score: Divine date score from 0 to 1
        
    Returns:
        String rating
    """
    if score > 0.85:
        return "⭐⭐⭐⭐⭐ COSMIC PERFECTION"
    elif score > 0.7:
        return "⭐⭐⭐⭐ DIVINE HARMONY"
    elif score > 0.55:
        return "⭐⭐⭐ SACRED ALIGNMENT"
    elif score > 0.4:
        return "⭐⭐ RESONANT"
    elif score > 0.25:
        return "⭐ MILD HARMONY"
    else:
        return "MUNDANE TEMPORAL POSITION"

def analyze_october_29_2023() -> Dict[str, Any]:
    """
    Special analysis function for October 29, 2023 - 
    An example of a day with specific BTC significance.
    
    Returns:
        Dict with comprehensive cycle analysis
    """
    # Create datetime for October 29, 2023
    timestamp = datetime.datetime(2023, 10, 29, 12, 0, 0)
    timestamp = pytz.UTC.localize(timestamp)
    
    # Get general analysis
    analysis = analyze_date(timestamp=timestamp)
    
    # Add specific information about this date
    analysis["specific_btc_data"] = {
        "closing_price": 34535.77,
        "market_cap": 674.46e9,  # in USD billions
        "24h_change": 1.3,  # percentage
        "significant_events": [
            "Bitcoin experienced a 'golden cross' pattern (50-day MA crossed above 200-day MA)",
            "Price reached new highs for 2023",
            "Marked potential end to mild bear market"
        ],
        "numerological_significance": [
            "Closing price contains repeating digits 3 and 5, which are consecutive Fibonacci numbers",
            "The pattern suggests harmony and balance in market cycles"
        ],
        "market_cycle_context": [
            "Positioned in pre-bull run phase leading to 2024 halving",
            "Historical pattern suggests onset of new bullish cycle"
        ]
    }
    
    return analysis

# Example usage
if __name__ == "__main__":
    # Analyze current date
    current_analysis = analyze_date()
    print(f"Current date analysis: {current_analysis}")
    
    # Analyze specific date - October 29, 2023
    oct_analysis = analyze_october_29_2023()
    print(f"October 29, 2023 analysis: {oct_analysis}") 