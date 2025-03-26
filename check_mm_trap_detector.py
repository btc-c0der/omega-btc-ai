#!/usr/bin/env python3

"""
Diagnostic script for MM Trap Detector components
Helps identify and resolve import issues
"""

import os
import sys
import importlib.util
import traceback
import json
import pkg_resources

def colorize(text, color_code):
    """Add color to terminal output"""
    return f"\033[{color_code}m{text}\033[0m"

def red(text):
    return colorize(text, "91")

def green(text):
    return colorize(text, "92")

def yellow(text):
    return colorize(text, "93")

def blue(text):
    return colorize(text, "94")

def check_python_environment():
    """Check Python version and environment"""
    print(blue("=== Python Environment ==="))
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Current Directory: {os.getcwd()}")
    print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
    print()

def check_module(module_name):
    """Check if a module can be imported"""
    print(blue(f"=== Checking module: {module_name} ==="))
    try:
        module = importlib.import_module(module_name)
        print(green(f"✓ Successfully imported {module_name}"))
        print(f"Module location: {module.__file__}")
        return True, module
    except ImportError as e:
        print(red(f"✗ Import Error: {e}"))
        return False, None
    except Exception as e:
        print(red(f"✗ Unexpected Error: {e}"))
        traceback.print_exc()
        return False, None

def check_redis_connection():
    """Check Redis connectivity"""
    print(blue("=== Checking Redis Connection ==="))
    try:
        import redis
        
        # Get Redis connection details from environment variables or use defaults
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        
        print(f"Connecting to Redis at {redis_host}:{redis_port}...")
        r = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)
        
        # Test connection with ping
        response = r.ping()
        if response:
            print(green("✓ Redis connection successful"))
            
            # Check for MM trap queue
            queue_name = "mm_trap_queue:zset"
            if r.exists(queue_name):
                key_type = r.type(queue_name).decode('utf-8')
                if key_type == 'zset':
                    queue_size = r.zcard(queue_name)
                    print(green(f"✓ Queue exists with {queue_size} items"))
                else:
                    print(yellow(f"! Queue exists but has wrong type: {key_type} (expected 'zset')"))
            else:
                print(yellow("! Queue does not exist yet"))
                
            return True
        else:
            print(red("✗ Redis ping failed"))
            return False
    except ImportError:
        print(red("✗ Redis module not installed"))
        return False
    except Exception as e:
        print(red(f"✗ Redis Error: {e}"))
        traceback.print_exc()
        return False

def check_dependencies():
    """Check required dependencies"""
    print(blue("=== Checking Dependencies ==="))
    required = ["redis", "numpy", "pandas", "websocket-client"]
    missing = []
    
    for package in required:
        try:
            pkg_resources.get_distribution(package)
            print(green(f"✓ {package} is installed"))
        except pkg_resources.DistributionNotFound:
            print(red(f"✗ {package} is not installed"))
            missing.append(package)
    
    if missing:
        print(yellow("\nMissing dependencies. Install with:"))
        print(f"pip install {' '.join(missing)}")
        
    return len(missing) == 0

def check_high_frequency_detector():
    """Check if high_frequency_detector can be imported and initialized"""
    print(blue("=== Checking High Frequency Detector ==="))
    try:
        from omega_ai.mm_trap_detector.high_frequency_detector import HighFrequencyTrapDetector, hf_detector
        
        print(green("✓ HighFrequencyTrapDetector class imported successfully"))
        print(green("✓ hf_detector singleton imported successfully"))
        
        # Check instance properties
        if hasattr(hf_detector, 'price_history_1min') and hasattr(hf_detector, 'price_history_5min'):
            print(green("✓ hf_detector has required properties"))
        else:
            print(yellow("! hf_detector missing some properties"))
            
        # Try calling update_price_data method
        try:
            import datetime
            price = 85000.0
            timestamp = datetime.datetime.now(datetime.UTC)
            hf_detector.update_price_data(price, timestamp)
            print(green("✓ update_price_data method works"))
            
            # Try calling detect_high_freq_trap_mode method
            hf_active, multiplier = hf_detector.detect_high_freq_trap_mode(price)
            print(green(f"✓ detect_high_freq_trap_mode returned: active={hf_active}, multiplier={multiplier}"))
            
            return True
        except Exception as e:
            print(red(f"✗ Error calling methods: {e}"))
            traceback.print_exc()
            return False
            
    except ImportError as e:
        print(red(f"✗ Import Error: {e}"))
        return False
    except Exception as e:
        print(red(f"✗ Unexpected Error: {e}"))
        traceback.print_exc()
        return False

def check_fibonacci_detector():
    """Check if fibonacci_detector can be imported and initialized"""
    print(blue("=== Checking Fibonacci Detector ==="))
    try:
        from omega_ai.mm_trap_detector.fibonacci_detector import (
            FibonacciDetector, fibonacci_detector,
            check_fibonacci_level, update_fibonacci_data
        )
        
        print(green("✓ Fibonacci detector components imported successfully"))
        
        # Try calling check_fibonacci_level
        try:
            result = check_fibonacci_level(85000.0)
            print(green(f"✓ check_fibonacci_level returned result"))
            return True
        except Exception as e:
            print(red(f"✗ Error calling methods: {e}"))
            traceback.print_exc()
            return False
            
    except ImportError as e:
        print(red(f"✗ Import Error: {e}"))
        return False
    except Exception as e:
        print(red(f"✗ Unexpected Error: {e}"))
        traceback.print_exc()
        return False

def check_btc_live_feed():
    """Check if btc_live_feed imports the mm_trap_detector correctly"""
    print(blue("=== Checking BTC Live Feed Integration ==="))
    try:
        from omega_ai.data_feed.btc_live_feed import mm_trap_detector_available, hf_detector
        
        if mm_trap_detector_available and hf_detector:
            print(green("✓ BTC live feed successfully imports MM trap detector"))
            return True
        else:
            print(yellow("! BTC live feed cannot access MM trap detector"))
            print(f"mm_trap_detector_available: {mm_trap_detector_available}")
            print(f"hf_detector: {hf_detector}")
            return False
            
    except ImportError as e:
        print(red(f"✗ Import Error: {e}"))
        return False
    except Exception as e:
        print(red(f"✗ Unexpected Error: {e}"))
        traceback.print_exc()
        return False

def main():
    """Run all diagnostic checks"""
    print(blue("========================"))
    print(blue("MM TRAP DETECTOR DIAGNOSTICS"))
    print(blue("========================\n"))
    
    check_python_environment()
    
    dependencies_ok = check_dependencies()
    redis_ok = check_redis_connection()
    
    # Check modules
    mm_trap_detector_ok, _ = check_module("omega_ai.mm_trap_detector")
    high_freq_detector_ok, _ = check_module("omega_ai.mm_trap_detector.high_frequency_detector")
    fibonacci_detector_ok, _ = check_module("omega_ai.mm_trap_detector.fibonacci_detector")
    mm_trap_consumer_ok, _ = check_module("omega_ai.mm_trap_detector.mm_trap_consumer")
    btc_live_feed_ok, _ = check_module("omega_ai.data_feed.btc_live_feed")
    
    # Check components
    hfd_ok = check_high_frequency_detector() if high_freq_detector_ok else False
    fibonacci_ok = check_fibonacci_detector() if fibonacci_detector_ok else False
    btc_integration_ok = check_btc_live_feed() if btc_live_feed_ok else False
    
    # Print summary
    print(blue("\n=== DIAGNOSTIC SUMMARY ==="))
    print(f"Dependencies: {green('OK') if dependencies_ok else red('FAILED')}")
    print(f"Redis Connection: {green('OK') if redis_ok else red('FAILED')}")
    print(f"MM Trap Detector Module: {green('OK') if mm_trap_detector_ok else red('FAILED')}")
    print(f"High Frequency Detector: {green('OK') if hfd_ok else red('FAILED')}")
    print(f"Fibonacci Detector: {green('OK') if fibonacci_ok else red('FAILED')}")
    print(f"MM Trap Consumer: {green('OK') if mm_trap_consumer_ok else red('FAILED')}")
    print(f"BTC Live Feed: {green('OK') if btc_live_feed_ok else red('FAILED')}")
    print(f"BTC Live Feed Integration: {green('OK') if btc_integration_ok else red('FAILED')}")
    
    # Overall status
    overall_ok = (dependencies_ok and redis_ok and mm_trap_detector_ok and 
                 hfd_ok and fibonacci_ok and mm_trap_consumer_ok and 
                 btc_live_feed_ok and btc_integration_ok)
    
    print(blue("\n=== OVERALL STATUS ==="))
    if overall_ok:
        print(green("✓ All systems operational"))
        print(green("MM Trap Detector is available to BTC Live Feed"))
    else:
        print(yellow("! Some components have issues"))
        print(yellow("Check the details above for specific problems"))

if __name__ == "__main__":
    main() 