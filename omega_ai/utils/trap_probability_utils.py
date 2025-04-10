#!/usr/bin/env python3

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
OMEGA BTC AI - Trap Probability Utilities
=========================================

Utility functions for accessing and analyzing trap probability data.
These utilities allow other components to easily access probability data
and integrate it with their own analysis.

Example usage:
    from omega_ai.utils.trap_probability_utils import get_current_trap_probability
    
    # Get the current trap probability
    prob = get_current_trap_probability()
    if prob > 0.7:
        print("High probability of trap formation!")
"""

import json
import redis
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

# Redis connection parameters
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# Initialize Redis connection
_redis_client = None

def get_redis_client():
    """Get or initialize Redis client."""
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = redis.Redis(
                host=REDIS_HOST, 
                port=REDIS_PORT, 
                db=REDIS_DB, 
                decode_responses=True
            )
        except Exception as e:
            print(f"Error connecting to Redis: {e}")
            return None
    return _redis_client

def get_current_trap_probability() -> float:
    """
    Get the current trap probability value.
    
    Returns:
        float: Probability value between 0.0 and 1.0, or 0.0 if not available
    """
    client = get_redis_client()
    if not client:
        return 0.0
        
    try:
        # Get the current probability from Redis
        prob_json = client.get("current_trap_probability")
        if not prob_json:
            return 0.0
            
        # Parse the JSON
        prob_data = json.loads(prob_json)
        
        # Return the probability value
        return float(prob_data.get("probability", 0.0))
        
    except Exception as e:
        print(f"Error getting trap probability: {e}")
        return 0.0

def get_probability_components() -> Dict[str, float]:
    """
    Get the individual components of the trap probability.
    
    Returns:
        Dict[str, float]: Dictionary of component names and their values
    """
    client = get_redis_client()
    if not client:
        return {}
        
    try:
        # Get the current probability from Redis
        prob_json = client.get("current_trap_probability")
        if not prob_json:
            return {}
            
        # Parse the JSON
        prob_data = json.loads(prob_json)
        
        # Return the components - ensure all values are floats
        components = prob_data.get("components", {})
        
        # Validate that components is a dict and all values are floats
        if not isinstance(components, dict):
            print(f"Warning: components is not a dictionary: {type(components)}")
            return {}
            
        # Convert all values to float if possible
        return {k: float(v) if isinstance(v, (int, float, str)) else 0.0 for k, v in components.items()}
        
    except Exception as e:
        print(f"Error getting probability components: {e}")
        return {}

def get_detected_trap_info() -> Tuple[Optional[str], float]:
    """
    Get information about any detected traps.
    
    Returns:
        Tuple[Optional[str], float]: Trap type and confidence, or (None, 0.0) if none detected
    """
    client = get_redis_client()
    if not client:
        return None, 0.0
        
    try:
        # Get the current probability from Redis
        prob_json = client.get("current_trap_probability")
        if not prob_json:
            return None, 0.0
            
        # Parse the JSON
        prob_data = json.loads(prob_json)
        
        # Get trap type and confidence
        trap_type = prob_data.get("trap_type")
        confidence = float(prob_data.get("confidence", 0.0))
        
        return trap_type, confidence
        
    except Exception as e:
        print(f"Error getting trap info: {e}")
        return None, 0.0

def get_probability_trend(minutes: int = 30) -> Dict[str, Any]:
    """
    Get the trend of trap probability over the specified time period.
    
    Args:
        minutes: Number of minutes to look back
        
    Returns:
        Dict containing trend information
    """
    client = get_redis_client()
    if not client:
        return {
            "direction": "unknown",
            "change": 0.0,
            "values": []
        }
        
    try:
        # Get historical probability data
        history_json = client.lrange("trap_probability_history", 0, -1)
        
        if not history_json:
            return {
                "direction": "unknown",
                "change": 0.0,
                "values": []
            }
            
        # Parse historical data
        history = []
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        for entry_json in history_json:
            try:
                entry = json.loads(entry_json)
                entry_time = datetime.fromisoformat(entry.get("timestamp"))
                
                if entry_time >= cutoff_time:
                    history.append(entry)
            except Exception:
                continue
                
        # Sort by timestamp
        history.sort(key=lambda x: x.get("timestamp"))
        
        # Calculate trend
        if len(history) >= 2:
            first_value = history[0].get("probability", 0.0)
            last_value = history[-1].get("probability", 0.0)
            change = last_value - first_value
            
            # Determine direction
            if change > 0.1:
                direction = "rapidly_increasing"
            elif change > 0.05:
                direction = "increasing"
            elif change > 0.02:
                direction = "slightly_increasing"
            elif change < -0.1:
                direction = "rapidly_decreasing"
            elif change < -0.05:
                direction = "decreasing"
            elif change < -0.02:
                direction = "slightly_decreasing"
            else:
                direction = "stable"
                
            values = [entry.get("probability", 0.0) for entry in history]
            
            return {
                "direction": direction,
                "change": change,
                "values": values,
                "first": first_value,
                "last": last_value
            }
        else:
            return {
                "direction": "unknown",
                "change": 0.0,
                "values": []
            }
            
    except Exception as e:
        print(f"Error getting probability trend: {e}")
        return {
            "direction": "unknown",
            "change": 0.0,
            "values": []
        }

def record_trap_feedback(trap_type: str, timestamp: str, was_real: bool, comment: Optional[str] = None) -> bool:
    """
    Record user feedback about a detected trap to improve the model.
    
    Args:
        trap_type: Type of trap
        timestamp: Timestamp of the trap detection
        was_real: Whether the detected trap was a real trap (True) or a false positive (False)
        comment: Optional user comment
        
    Returns:
        bool: Success status
    """
    client = get_redis_client()
    if not client:
        return False
        
    try:
        # Create feedback entry
        feedback = {
            "trap_type": trap_type,
            "detection_time": timestamp,
            "was_real": was_real,
            "comment": comment,
            "feedback_time": datetime.now().isoformat()
        }
        
        # Store in Redis
        client.lpush("trap_detection_feedback", json.dumps(feedback))
        
        # Keep list at a reasonable size
        client.ltrim("trap_detection_feedback", 0, 999)
        
        return True
        
    except Exception as e:
        print(f"Error recording trap feedback: {e}")
        return False

def get_detection_metrics() -> Dict[str, float]:
    """
    Get current trap detection accuracy metrics.
    
    Returns:
        Dict containing accuracy metrics
    """
    client = get_redis_client()
    if not client:
        return {
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "true_positives": 0,
            "false_positives": 0,
            "true_negatives": 0,
            "false_negatives": 0
        }
        
    try:
        # Get metrics from Redis
        metrics_json = client.get("trap_detection_metrics")
        
        if not metrics_json:
            return {
                "accuracy": 0.0,
                "precision": 0.0,
                "recall": 0.0,
                "true_positives": 0,
                "false_positives": 0,
                "true_negatives": 0,
                "false_negatives": 0
            }
            
        # Parse metrics
        metrics = json.loads(metrics_json)
        
        return metrics
        
    except Exception as e:
        print(f"Error getting detection metrics: {e}")
        return {
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "true_positives": 0,
            "false_positives": 0,
            "true_negatives": 0,
            "false_negatives": 0
        }

def get_probability_threshold(trap_type: str) -> float:
    """
    Get the recommended probability threshold for a specific trap type.
    
    Args:
        trap_type: Type of trap
        
    Returns:
        float: Recommended threshold value between 0.0 and 1.0
    """
    # Default thresholds for different trap types
    default_thresholds = {
        "liquidity_grab": 0.70,
        "stop_hunt": 0.75,
        "fake_pump": 0.65,
        "fake_dump": 0.65,
        "bull_trap": 0.70,
        "bear_trap": 0.70
    }
    
    client = get_redis_client()
    if not client:
        return default_thresholds.get(trap_type, 0.60)
        
    try:
        # Try to get dynamically tuned thresholds from Redis
        thresholds_json = client.get("trap_probability_thresholds")
        
        if thresholds_json:
            thresholds = json.loads(thresholds_json)
            return thresholds.get(trap_type, default_thresholds.get(trap_type, 0.60))
        else:
            return default_thresholds.get(trap_type, 0.60)
            
    except Exception as e:
        print(f"Error getting probability threshold: {e}")
        return default_thresholds.get(trap_type, 0.60)

def is_trap_likely() -> Tuple[bool, Optional[str], float]:
    """
    Check if a trap is likely based on current probability and thresholds.
    
    Returns:
        Tuple[bool, Optional[str], float]: 
            - Whether a trap is likely
            - The most likely trap type (or None)
            - The confidence level
    """
    # Get current probability
    probability = get_current_trap_probability()
    
    # Get detected trap info
    trap_type, confidence = get_detected_trap_info()
    
    if trap_type:
        # Get threshold for this trap type
        threshold = get_probability_threshold(trap_type)
        
        # Check if probability exceeds threshold
        if probability >= threshold:
            return True, trap_type, confidence
            
    return False, None, 0.0 