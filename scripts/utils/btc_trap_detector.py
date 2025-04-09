#!/usr/bin/env python3
"""
BTC Trap Detector - Analyzes price history from JSON to detect MM traps

This script looks for potential market manipulation trap patterns in Bitcoin price data
using algorithms inspired by the MM Trap Detector system.
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any

# ANSI color codes for pretty terminal output
GREEN = "\033[92m"
GREEN_BG = "\033[42;97m"
BLUE = "\033[94m"
BLUE_BG = "\033[44;97m"
YELLOW = "\033[93m"
RED = "\033[91m"
RED_BG = "\033[41;97m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"
LIGHT_ORANGE = "\033[38;5;214m"

# Trading session timeframes (in UTC)
TRADING_SESSIONS = {
    "sydney": {"name": "Sydney", "start_hour": 22, "end_hour": 7},  # 22:00 - 07:00 UTC
    "tokyo": {"name": "Tokyo", "start_hour": 0, "end_hour": 9},     # 00:00 - 09:00 UTC
    "london": {"name": "London", "start_hour": 8, "end_hour": 17},  # 08:00 - 17:00 UTC
    "newyork": {"name": "New York", "start_hour": 13, "end_hour": 22}  # 13:00 - 22:00 UTC
}

def log_message(message, color=BLUE):
    """Print a colorful log message to the console."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] {message}{RESET}")

def format_percentage(value):
    """Format a value as a percentage with color."""
    color = GREEN if value >= 0 else RED
    return f"{color}{value:+.2f}%{RESET}"

def format_price(value):
    """Format a value as a price with color."""
    return f"${value:,.2f}"

def load_price_history(json_file):
    """Load price history from a JSON file."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        log_message(f"Successfully loaded price data from {json_file}", GREEN)
        return data
    except Exception as e:
        log_message(f"Error loading price history: {str(e)}", RED)
        return None

def get_timeframe_bounds(timeframe_name: str, now: Optional[datetime] = None) -> Tuple[datetime, datetime]:
    """
    Get the start and end times for a specified trading timeframe.
    
    Args:
        timeframe_name: Name of the timeframe ('sydney', 'tokyo', 'london', 'newyork') 
                        or a custom timeframe in hours ('6h', '12h', '24h', etc.)
        now: Current time reference (defaults to now)
        
    Returns:
        Tuple of (start_time, end_time) as datetime objects
    """
    # Default to current time if not specified
    if now is None:
        now = datetime.now()
    
    # Handle standard trading sessions
    if timeframe_name.lower() in TRADING_SESSIONS:
        session = TRADING_SESSIONS[timeframe_name.lower()]
        
        # Calculate session bounds based on current UTC time
        current_utc = now.utcnow()
        end_time = now
        
        # If current time is outside the session hours, find the most recent session
        if current_utc.hour < session["start_hour"] or current_utc.hour >= session["end_hour"]:
            # Session spans across midnight
            if session["start_hour"] > session["end_hour"]:
                if current_utc.hour >= session["start_hour"]:
                    # After session start on the same day
                    session_date = current_utc.date()
                else:
                    # Before session end, so it started the previous day
                    session_date = (current_utc - timedelta(days=1)).date()
            else:
                # Session is contained within one day, so look at the previous day
                session_date = (current_utc - timedelta(days=1)).date()
        else:
            # Currently in session
            session_date = current_utc.date()
            
        # Session spans across midnight
        if session["start_hour"] > session["end_hour"]:
            start_time = datetime.combine(session_date, datetime.min.time()) + timedelta(hours=session["start_hour"])
            end_time = datetime.combine(session_date + timedelta(days=1), datetime.min.time()) + timedelta(hours=session["end_hour"])
        else:
            start_time = datetime.combine(session_date, datetime.min.time()) + timedelta(hours=session["start_hour"])
            end_time = datetime.combine(session_date, datetime.min.time()) + timedelta(hours=session["end_hour"])
        
        # Convert to local time
        utc_offset = now - now.utcnow()
        start_time = start_time + utc_offset
        end_time = end_time + utc_offset
        
        return start_time, min(end_time, now)
    
    # Handle custom timeframes (e.g., '6h', '12h', '24h')
    elif timeframe_name.lower().endswith('h'):
        try:
            hours = int(timeframe_name[:-1])
            if hours <= 0:
                raise ValueError("Hours must be positive")
            
            end_time = now
            start_time = end_time - timedelta(hours=hours)
            return start_time, end_time
        except (ValueError, IndexError):
            log_message(f"Invalid timeframe format: {timeframe_name}. Using default 15 minutes.", YELLOW)
            return now - timedelta(minutes=15), now
    
    # Default to 15 minutes if timeframe not recognized
    else:
        log_message(f"Unknown timeframe: {timeframe_name}. Using default 15 minutes.", YELLOW)
        return now - timedelta(minutes=15), now

def filter_prices_by_timeframe(prices: List[Dict[str, Any]], start_time: datetime, end_time: datetime) -> List[Dict[str, Any]]:
    """
    Filter price data to only include points within the specified timeframe.
    
    Args:
        prices: List of price data points
        start_time: Start of timeframe
        end_time: End of timeframe
        
    Returns:
        Filtered list of price data points
    """
    filtered_prices = []
    
    for price in prices:
        try:
            timestamp = datetime.fromisoformat(price["timestamp"])
            if start_time <= timestamp <= end_time:
                filtered_prices.append(price)
        except (ValueError, KeyError):
            # Skip entries with invalid timestamps
            continue
    
    return filtered_prices

def calculate_trend(prices: List[Dict[str, Any]]) -> str:
    """
    Calculate the trend direction from price history.
    
    Args:
        prices: List of price data points
        
    Returns:
        str: Trend description (e.g., "Strongly Bullish", "Moderately Bearish", etc.)
    """
    if not prices or len(prices) < 3:
        return "Insufficient Data"
    
    # Sort by timestamp (oldest first to calculate trend correctly)
    sorted_prices = sorted(prices, key=lambda x: x["timestamp"])
    
    # Get oldest and most recent prices
    oldest_price = sorted_prices[0]["price"]
    newest_price = sorted_prices[-1]["price"]
    
    # Calculate total change
    change_pct = ((newest_price - oldest_price) / oldest_price) * 100
    
    # Calculate volatility (standard deviation of price changes)
    changes = []
    for i in range(1, len(sorted_prices)):
        prev_price = sorted_prices[i-1]["price"]
        curr_price = sorted_prices[i]["price"]
        change = ((curr_price - prev_price) / prev_price) * 100
        changes.append(change)
    
    if not changes:
        return "Stable"
    
    volatility = sum(abs(c) for c in changes) / len(changes)
    
    # Determine trend strength based on change and volatility
    if abs(change_pct) < 0.5:
        return "Stable"
    
    # Determine direction and strength
    if change_pct > 0:
        if change_pct > 5 or (change_pct > 2 and volatility > 1):
            return "Strongly Bullish"
        elif change_pct > 1:
            return "Moderately Bullish"
        else:
            return "Slightly Bullish"
    else:
        if change_pct < -5 or (change_pct < -2 and volatility > 1):
            return "Strongly Bearish"
        elif change_pct < -1:
            return "Moderately Bearish"
        else:
            return "Slightly Bearish"

def detect_price_swings(prices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detect significant price swings in the price history.
    
    Args:
        prices: List of price data points
        
    Returns:
        List of significant price swing events
    """
    if not prices or len(prices) < 5:
        return []
    
    # Sort by timestamp (oldest first)
    sorted_prices = sorted(prices, key=lambda x: x["timestamp"])
    
    swings = []
    window_size = min(10, max(5, len(sorted_prices) // 5))
    
    for i in range(window_size, len(sorted_prices)):
        # Get current window
        window = sorted_prices[i-window_size:i]
        current_price = sorted_prices[i]["price"]
        
        # Calculate average price in window
        avg_price = sum(p["price"] for p in window) / len(window)
        
        # Calculate change
        change_pct = ((current_price - avg_price) / avg_price) * 100
        
        # If change is significant, record a swing
        if abs(change_pct) > 1.5:  # Minimum threshold for a significant move
            swing = {
                "timestamp": sorted_prices[i]["timestamp"],
                "price": current_price,
                "change_pct": change_pct,
                "direction": "up" if change_pct > 0 else "down",
                "magnitude": abs(change_pct)
            }
            swings.append(swing)
    
    return swings

def detect_pattern_reversals(prices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detect pattern reversals that could indicate MM traps.
    
    Args:
        prices: List of price data points
        
    Returns:
        List of potential trap events
    """
    if not prices or len(prices) < 10:
        return []
    
    # Sort by timestamp (oldest first)
    sorted_prices = sorted(prices, key=lambda x: x["timestamp"])
    
    reversals = []
    window_size = min(15, max(5, len(sorted_prices) // 4))
    
    for i in range(window_size, len(sorted_prices) - 3):
        # Get current window
        window = sorted_prices[i-window_size:i]
        
        # Calculate trend in window
        window_trend = calculate_trend(window)
        
        # Get prices for potential reversal
        pre_price = sorted_prices[i-1]["price"]
        current_price = sorted_prices[i]["price"]
        post_price = sorted_prices[i+2]["price"]  # Look a bit ahead to confirm reversal
        
        # Calculate changes
        initial_change = ((current_price - pre_price) / pre_price) * 100
        reversal_change = ((post_price - current_price) / current_price) * 100
        
        # Check for reversal pattern
        is_reversal = (initial_change * reversal_change < 0) and abs(reversal_change) > 0.5
        
        # If there's a reversal against the trend, it could be a trap
        if is_reversal:
            # Bull trap: price goes up then quickly down in a bullish trend
            is_bull_trap = "Bullish" in window_trend and initial_change > 0 and reversal_change < 0
            
            # Bear trap: price goes down then quickly up in a bearish trend
            is_bear_trap = "Bearish" in window_trend and initial_change < 0 and reversal_change > 0
            
            if is_bull_trap or is_bear_trap:
                # Calculate confidence based on magnitude of moves
                magnitude = (abs(initial_change) + abs(reversal_change)) / 2
                strength_factor = 1.0 if "Strongly" in window_trend else 0.7 if "Moderately" in window_trend else 0.4
                
                confidence = min(0.95, (magnitude * strength_factor) / 10)
                
                reversal = {
                    "timestamp": sorted_prices[i]["timestamp"],
                    "price": current_price,
                    "initial_change": initial_change,
                    "reversal_change": reversal_change,
                    "type": "Bull Trap" if is_bull_trap else "Bear Trap",
                    "confidence": confidence,
                    "trend": window_trend
                }
                reversals.append(reversal)
    
    return reversals

def detect_possible_mm_traps(prices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detect possible market maker traps in price history.
    
    Args:
        prices: List of price data points
        
    Returns:
        List of potential trap events with descriptions
    """
    if not prices or len(prices) < 10:
        log_message("Insufficient price data to analyze for traps", YELLOW)
        return []
    
    # Get overall trend
    overall_trend = calculate_trend(prices)
    log_message(f"Overall price trend: {overall_trend}", CYAN)
    
    # Get significant price swings
    swings = detect_price_swings(prices)
    
    # Get pattern reversals
    reversals = detect_pattern_reversals(prices)
    
    # Combine results into potential traps
    potential_traps = []
    
    # Process swing events
    for swing in swings:
        # A significant up move in a bearish trend could be a bull trap
        if swing["direction"] == "up" and "Bearish" in overall_trend and swing["magnitude"] > 2.5:
            confidence = min(0.95, swing["magnitude"] / 10)
            trap = {
                "timestamp": swing["timestamp"],
                "price": swing["price"],
                "type": "Bull Trap",
                "confidence": confidence,
                "description": f"Significant upward move of {format_percentage(swing['change_pct'])} in {overall_trend} trend",
                "detection_method": "price_swing"
            }
            potential_traps.append(trap)
        
        # A significant down move in a bullish trend could be a bear trap
        elif swing["direction"] == "down" and "Bullish" in overall_trend and swing["magnitude"] > 2.5:
            confidence = min(0.95, swing["magnitude"] / 10)
            trap = {
                "timestamp": swing["timestamp"],
                "price": swing["price"],
                "type": "Bear Trap",
                "confidence": confidence,
                "description": f"Significant downward move of {format_percentage(swing['change_pct'])} in {overall_trend} trend",
                "detection_method": "price_swing"
            }
            potential_traps.append(trap)
    
    # Add reversal-based traps
    for reversal in reversals:
        trap = {
            "timestamp": reversal["timestamp"],
            "price": reversal["price"],
            "type": reversal["type"],
            "confidence": reversal["confidence"],
            "description": f"Pattern reversal: {format_percentage(reversal['initial_change'])} followed by {format_percentage(reversal['reversal_change'])} in {reversal['trend']} trend",
            "detection_method": "pattern_reversal"
        }
        potential_traps.append(trap)
    
    # Sort by timestamp
    potential_traps.sort(key=lambda x: x["timestamp"])
    
    return potential_traps

def analyze_price_history(data, timeframe=None):
    """
    Analyze price history for potential MM traps.
    
    Args:
        data: Price history data
        timeframe: Optional timeframe specification
        
    Returns:
        Analysis results as a dictionary
    """
    if not data or "prices" not in data:
        log_message("Invalid price data format", RED)
        return None
    
    prices = data["prices"]
    timeframe_str = None
    
    # Apply timeframe filtering if specified
    if timeframe:
        start_time, end_time = get_timeframe_bounds(timeframe)
        timeframe_str = timeframe
        
        # Format timeframe for display
        if timeframe.lower() in TRADING_SESSIONS:
            session_name = TRADING_SESSIONS[timeframe.lower()]["name"]
            timeframe_str = f"{session_name} session"
        
        log_message(f"Filtering data for {timeframe_str} ({start_time.strftime('%Y-%m-%d %H:%M')} to {end_time.strftime('%Y-%m-%d %H:%M')})", BLUE)
        original_count = len(prices)
        prices = filter_prices_by_timeframe(prices, start_time, end_time)
        log_message(f"Filtered from {original_count} to {len(prices)} price points", BLUE)
    else:
        # Default to metadata time window if available
        if "metadata" in data and "time_window_minutes" in data["metadata"]:
            minutes = data["metadata"]["time_window_minutes"]
            timeframe_str = f"{minutes} minutes"
            log_message(f"Using default timeframe from metadata: {minutes} minutes", BLUE)
        else:
            timeframe_str = "15 minutes"
            log_message(f"No timeframe specified, using default ({timeframe_str})", YELLOW)
    
    # Check if we have enough price points
    if len(prices) < 10:
        log_message(f"Insufficient price data points: {len(prices)} (need at least 10)", YELLOW)
        return {
            "analysis_timestamp": datetime.now().isoformat(),
            "timeframe": timeframe_str,
            "price_points_analyzed": len(prices),
            "traps_detected": 0,
            "message": "Insufficient price data for trap detection"
        }
    
    log_message(f"Analyzing {len(prices)} price points for MM traps", CYAN)
    
    # Calculate total price change during the period
    sorted_prices = sorted(prices, key=lambda x: x["timestamp"])
    oldest_price = sorted_prices[0]["price"]
    newest_price = sorted_prices[-1]["price"]
    total_change_pct = ((newest_price - oldest_price) / oldest_price) * 100
    
    log_message(f"Total price change: {format_percentage(total_change_pct)}", CYAN)
    
    # Detect potential MM traps
    traps = detect_possible_mm_traps(prices)
    
    # Format results
    results = {
        "analysis_timestamp": datetime.now().isoformat(),
        "timeframe": timeframe_str,
        "price_points_analyzed": len(prices),
        "high_price": max(p["price"] for p in prices),
        "low_price": min(p["price"] for p in prices),
        "current_price": newest_price,
        "total_price_change_pct": total_change_pct,
        "traps_detected": len(traps),
        "trap_events": traps,
        "overall_trap_risk": calculate_overall_trap_risk(traps, total_change_pct)
    }
    
    return results

def calculate_overall_trap_risk(traps, price_change_pct):
    """Calculate the overall trap risk level based on detected traps."""
    if not traps:
        return {
            "level": "Low",
            "score": 0.1,
            "description": "No potential traps detected in the analyzed time period."
        }
    
    # Calculate weighted average of trap confidences
    total_confidence = sum(trap["confidence"] for trap in traps)
    avg_confidence = total_confidence / len(traps)
    
    # Adjust based on number of traps
    trap_count_factor = min(1.0, len(traps) / 5)  # Caps at 5 traps
    
    # Adjust based on price volatility
    volatility_factor = min(1.0, abs(price_change_pct) / 10)
    
    # Calculate final risk score (0.0 to 1.0)
    risk_score = (avg_confidence * 0.6) + (trap_count_factor * 0.3) + (volatility_factor * 0.1)
    
    # Determine risk level
    if risk_score > 0.7:
        level = "High"
        description = "High risk of market manipulation. Multiple trap patterns detected with high confidence."
    elif risk_score > 0.4:
        level = "Medium"
        description = "Moderate risk of market manipulation. Some trap patterns detected."
    else:
        level = "Low"
        description = "Low risk of market manipulation. Few or low-confidence trap patterns detected."
    
    return {
        "level": level,
        "score": risk_score,
        "description": description
    }

def print_trap_analysis(results):
    """Print the trap analysis results to the console."""
    if not results:
        log_message("No analysis results to display", RED)
        return
    
    print(f"\n{BLUE_BG}{WHITE}{BOLD} BTC MARKET MANIPULATION TRAP ANALYSIS {RESET}")
    print(f"{MAGENTA}{'═' * 60}{RESET}")
    
    # Print timeframe and price range
    print(f"\n{CYAN}{BOLD}Analysis Overview{RESET}")
    print(f"{WHITE}Timeframe: {results.get('timeframe', 'Unknown')}{RESET}")
    print(f"{WHITE}Price Points Analyzed: {results.get('price_points_analyzed', 0)}{RESET}")
    
    # Handle insufficient data case
    if "message" in results:
        print(f"\n{YELLOW}Note: {results['message']}{RESET}")
        print(f"\n{MAGENTA}{'═' * 60}{RESET}")
        return
    
    if "high_price" in results and "low_price" in results:
        print(f"{WHITE}Price Range: {format_price(results['high_price'])} - {format_price(results['low_price'])}{RESET}")
        price_range_pct = ((results['high_price'] - results['low_price']) / results['low_price']) * 100
        print(f"{WHITE}Price Range Amplitude: {format_percentage(price_range_pct)}{RESET}")
    
    if "current_price" in results:
        print(f"{WHITE}Current BTC Price: {format_price(results['current_price'])}{RESET}")
    
    if "total_price_change_pct" in results:
        print(f"{WHITE}Total Price Change: {format_percentage(results['total_price_change_pct'])}{RESET}")
    
    # Print trap risk assessment
    if "overall_trap_risk" in results:
        risk = results["overall_trap_risk"]
        risk_color = GREEN if risk["level"] == "Low" else YELLOW if risk["level"] == "Medium" else RED
        
        print(f"\n{CYAN}{BOLD}MM Trap Risk Assessment{RESET}")
        print(f"{risk_color}Risk Level: {risk['level']}{RESET}")
        print(f"{WHITE}Risk Score: {risk['score']:.2f}{RESET}")
        print(f"{WHITE}Description: {risk['description']}{RESET}")
    
    # Print detected traps
    if "trap_events" in results:
        traps = results["trap_events"]
        if traps:
            print(f"\n{CYAN}{BOLD}Detected Trap Events: {len(traps)}{RESET}")
            
            for i, trap in enumerate(traps, 1):
                # Choose color based on trap type
                trap_color = GREEN if trap["type"] == "Bull Trap" else RED
                trap_bg = GREEN_BG if trap["type"] == "Bull Trap" else RED_BG
                
                # Format confidence with color
                conf_color = GREEN if trap["confidence"] < 0.5 else YELLOW if trap["confidence"] < 0.8 else RED
                
                # Format timestamp
                timestamp = datetime.fromisoformat(trap["timestamp"]).strftime("%H:%M:%S")
                
                print(f"\n{trap_bg}{WHITE}{BOLD} {trap['type']} #{i} {RESET}")
                print(f"{WHITE}Time: {timestamp}{RESET}")
                print(f"{trap_color}Price: {format_price(trap['price'])}{RESET}")
                print(f"{conf_color}Confidence: {trap['confidence']:.2f}{RESET}")
                print(f"{WHITE}Description: {trap['description']}{RESET}")
        else:
            print(f"\n{GREEN}No trap events detected in the analyzed time period.{RESET}")
    
    print(f"\n{MAGENTA}{'═' * 60}{RESET}")

def save_results_to_json(results, output_file=None):
    """Save analysis results to a JSON file."""
    if not output_file:
        timeframe = results.get("timeframe", "").lower().replace(" ", "_")
        if timeframe:
            timeframe = f"_{timeframe}"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"btc_trap_analysis{timeframe}_{timestamp}.json"
    
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        log_message(f"Analysis results saved to {output_file}", GREEN)
        return output_file
    except Exception as e:
        log_message(f"Error saving results to JSON: {str(e)}", RED)
        return None

def main():
    """Main function to analyze BTC price history for MM traps."""
    parser = argparse.ArgumentParser(description="Analyze BTC price history for potential MM traps")
    parser.add_argument("-i", "--input", type=str, required=True, help="Input JSON file with BTC price history")
    parser.add_argument("-o", "--output", type=str, help="Output JSON file for analysis results (default: btc_trap_analysis_<timestamp>.json)")
    parser.add_argument("-t", "--timeframe", type=str, help="Timeframe to analyze: 'sydney', 'tokyo', 'london', 'newyork', or custom in hours (e.g., '6h')")
    parser.add_argument("--gpu", action="store_true", help="Use GPU acceleration if available")
    args = parser.parse_args()
    
    # Check for GPU acceleration if requested
    if args.gpu:
        try:
            import yaml
            import torch
            
            # Check if GPU is available
            gpu_available = torch.cuda.is_available()
            
            if gpu_available:
                device_name = torch.cuda.get_device_name(0)
                log_message(f"GPU acceleration enabled - Using {device_name}", GREEN)
                
                # Try to load GPU configuration if it exists
                try:
                    with open("config/gpu_config.yaml", "r") as f:
                        gpu_config = yaml.safe_load(f)
                    log_message("GPU configuration loaded successfully", GREEN)
                except Exception as e:
                    log_message(f"Could not load GPU configuration: {str(e)}", YELLOW)
                    log_message("Using default GPU settings", YELLOW)
            else:
                log_message("GPU requested but no compatible GPU found. Using CPU mode.", YELLOW)
        except ImportError:
            log_message("GPU acceleration requested but PyTorch or YAML not available. Using CPU mode.", YELLOW)
            log_message("Run 'scripts/utils/install_gpu_acceleration.sh' to set up GPU support", YELLOW)
    
    # Load price history from JSON
    data = load_price_history(args.input)
    if not data:
        return 1
    
    # Analyze price history for traps
    results = analyze_price_history(data, args.timeframe)
    if not results:
        return 1
    
    # Print analysis results
    print_trap_analysis(results)
    
    # Save results to JSON
    save_results_to_json(results, args.output)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 