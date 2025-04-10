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
OMEGA BTC AI - Trap Probability Meter Checker
This script checks if the trap probability meter is functioning properly.
"""

import os
import sys
import redis
import json
from datetime import datetime

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

def check_trap_meter():
    """Check if the trap probability meter is functioning properly in Redis."""
    print(f"{CYAN}======================================================{RESET}")
    print(f"{CYAN}= OMEGA BTC AI - Trap Probability Meter Checker      ={RESET}")
    print(f"{CYAN}======================================================{RESET}")
    
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('REDIS_PORT', 6379))
    
    print(f"{CYAN}Redis Host: {redis_host}{RESET}")
    print(f"{CYAN}Redis Port: {redis_port}{RESET}")
    print(f"{CYAN}======================================================{RESET}")
    
    # Check Redis connection
    try:
        r = redis.Redis(host=redis_host, port=redis_port, socket_connect_timeout=5.0)
        
        # Try to ping Redis
        response = r.ping()
        if response:
            print(f"{GREEN}Redis connection: SUCCESS{RESET}")
        else:
            print(f"{RED}Redis connection: FAILED (no ping response){RESET}")
            return False
    except Exception as e:
        print(f"{RED}Redis connection: FAILED with error: {str(e)}{RESET}")
        return False
    
    # Check for trap probability data
    trap_prob_key = "omega:trap_probability"
    trap_components_key = "omega:trap_components"
    trap_analysis_key = "omega:trap_analysis"
    
    # Check trap probability
    try:
        trap_prob = r.get(trap_prob_key)
        if trap_prob is not None:
            prob_value = float(trap_prob.decode('utf-8'))
            print(f"{GREEN}Trap Probability: {prob_value:.2%}{RESET}")
            
            # Indicate if probability is high
            if prob_value > 0.7:
                print(f"{RED}⚠️ High trap probability detected!{RESET}")
            elif prob_value > 0.5:
                print(f"{YELLOW}⚠️ Moderate trap probability detected.{RESET}")
        else:
            print(f"{RED}Trap Probability: NOT FOUND in Redis{RESET}")
            print(f"{YELLOW}Try running the trap probability meter first:{RESET}")
            print(f"python -m omega_ai.tools.trap_probability_meter")
    except Exception as e:
        print(f"{RED}Error checking trap probability: {str(e)}{RESET}")
    
    # Check trap components
    try:
        trap_components = r.get(trap_components_key)
        if trap_components is not None:
            components = json.loads(trap_components.decode('utf-8'))
            print(f"\n{CYAN}Trap Components:{RESET}")
            
            if isinstance(components, dict):
                for name, value in components.items():
                    if isinstance(value, (int, float)):
                        if value > 0.7:
                            color = RED
                        elif value > 0.5:
                            color = YELLOW
                        else:
                            color = GREEN
                        print(f"{CYAN}- {name.replace('_', ' ').title()}: {color}{value:.2%}{RESET}")
            else:
                print(f"{RED}Components data is not in expected format: {components}{RESET}")
        else:
            print(f"{RED}Trap Components: NOT FOUND in Redis{RESET}")
    except Exception as e:
        print(f"{RED}Error checking trap components: {str(e)}{RESET}")
    
    # Check trap analysis
    try:
        trap_analysis = r.get(trap_analysis_key)
        if trap_analysis is not None:
            analysis = json.loads(trap_analysis.decode('utf-8'))
            print(f"\n{CYAN}Trap Analysis:{RESET}")
            
            if isinstance(analysis, dict):
                is_likely = analysis.get('is_trap_likely', False)
                trap_type = analysis.get('trap_type', 'unknown')
                confidence = analysis.get('confidence', 0.0)
                
                if is_likely:
                    print(f"{RED}🚨 Trap Detected: {trap_type.upper()}{RESET}")
                    print(f"{RED}Confidence: {confidence:.2%}{RESET}")
                else:
                    print(f"{GREEN}✅ No traps detected{RESET}")
                    print(f"{GREEN}Confidence: {confidence:.2%}{RESET}")
                
                # Check timestamp
                timestamp = analysis.get('timestamp', '')
                if timestamp:
                    try:
                        dt = datetime.fromisoformat(timestamp)
                        now = datetime.now()
                        age = now - dt
                        print(f"Last updated: {dt.strftime('%Y-%m-%d %H:%M:%S')} ({age.total_seconds():.0f} seconds ago)")
                        
                        if age.total_seconds() > 600:  # 10 minutes
                            print(f"{RED}⚠️ Warning: Data is stale (over 10 minutes old){RESET}")
                    except:
                        print(f"Timestamp: {timestamp}")
            else:
                print(f"{RED}Analysis data is not in expected format: {analysis}{RESET}")
        else:
            print(f"{RED}Trap Analysis: NOT FOUND in Redis{RESET}")
    except Exception as e:
        print(f"{RED}Error checking trap analysis: {str(e)}{RESET}")
    
    # Check all Redis keys related to trap meter
    try:
        print(f"\n{CYAN}All Trap Meter Related Redis Keys:{RESET}")
        keys = r.keys("omega:*")
        
        if keys:
            for key in keys:
                key_str = key.decode('utf-8')
                key_type = r.type(key).decode('utf-8')
                
                if key_type == "string":
                    value = r.get(key)
                    try:
                        # Try to decode as JSON
                        json_value = json.loads(value.decode('utf-8'))
                        value_str = f"(JSON, {len(str(json_value))} chars)"
                    except:
                        # If not JSON, show raw value
                        value_str = value.decode('utf-8')
                        if len(value_str) > 50:
                            value_str = f"{value_str[:50]}... ({len(value_str)} chars)"
                    
                    print(f"  {key_str} ({key_type}): {value_str}")
                else:
                    print(f"  {key_str} ({key_type})")
        else:
            print(f"{RED}No 'omega:*' keys found in Redis{RESET}")
            print(f"{YELLOW}The trap probability meter may not be running.{RESET}")
    except Exception as e:
        print(f"{RED}Error listing Redis keys: {str(e)}{RESET}")
    
    print(f"\n{CYAN}======================================================{RESET}")
    return True

if __name__ == "__main__":
    check_trap_meter() 