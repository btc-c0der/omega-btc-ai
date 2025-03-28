#!/usr/bin/env python3
"""
🔱 OMEGA BTC AI - Corsair RGB Hardware Test
=========================================

Tests the connection and functionality of Corsair RGB devices.
Requires:
- iCUE software installed and running
- Device connected via USB
- Device recognized in iCUE
"""

import os
import sys
import time
import logging
import ctypes
from typing import Optional, Dict, Tuple
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("corsair-test")

# Define constants
LED_ID_ESC = 1
LED_ID_WASD = [26, 30, 31, 32]  # W, A, S, D keys

def find_corsair_sdk():
    """Find the Corsair SDK library on the system."""
    if sys.platform == 'darwin':
        # Common macOS locations
        paths = [
            '/Applications/iCUE.app/Contents/Frameworks/libCorsairSDK.dylib',
            '/Library/Application Support/Corsair/iCUE/libCorsairSDK.dylib',
            os.path.expanduser('~/Library/Application Support/Corsair/iCUE/libCorsairSDK.dylib'),
            './libCorsairSDK.dylib'  # Current directory
        ]
    elif sys.platform == 'win32':
        program_files = os.environ.get('PROGRAMFILES', 'C:\\Program Files')
        paths = [
            os.path.join(program_files, 'Corsair\\iCUE\\CUESDK.x64_2019.dll'),
            '.\\CUESDK.x64_2019.dll'  # Current directory
        ]
    else:  # Linux
        paths = [
            '/usr/lib/libCorsairSDK.so',
            '/usr/local/lib/libCorsairSDK.so',
            './libCorsairSDK.so'  # Current directory
        ]

    for path in paths:
        if os.path.exists(path):
            logger.info(f"Found Corsair SDK at: {path}")
            return path

    return None

class CorsairRGBTester:
    def __init__(self):
        self.connected = False
        self.lib = None
        
        # Try to load the Corsair SDK library
        sdk_path = find_corsair_sdk()
        if not sdk_path:
            logger.error("❌ Could not find Corsair SDK library")
            logger.error("Please ensure iCUE software is installed and running")
            sys.exit(1)
            
        try:
            self.lib = ctypes.CDLL(sdk_path)
            logger.info("✅ Loaded Corsair SDK library")
            
        except Exception as e:
            logger.error(f"❌ Failed to load Corsair SDK: {e}")
            logger.error("Please ensure iCUE software is installed and running")
            sys.exit(1)

    def connect(self) -> bool:
        """Initialize connection to Corsair devices."""
        try:
            # Initialize SDK
            result = self.lib.CorsairConnect()
            if result == 0:
                logger.error("❌ Failed to connect to Corsair SDK")
                return False
                
            # Get device info
            device_count = self.lib.CorsairGetDeviceCount()
            logger.info(f"Found {device_count} Corsair devices")
            
            if device_count > 0:
                self.connected = True
                logger.info("✅ Successfully connected to Corsair device")
                return True
            else:
                logger.error("❌ No Corsair devices found")
                return False
                
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            return False

    def set_led_color(self, led_id: int, r: int, g: int, b: int):
        """Set color for a specific LED."""
        if not self.connected:
            return
            
        try:
            self.lib.CorsairSetLedColor(
                led_id,
                ctypes.c_int(r),
                ctypes.c_int(g),
                ctypes.c_int(b)
            )
        except Exception as e:
            logger.error(f"❌ Failed to set LED color: {e}")

    def test_basic_rgb(self):
        """Test basic RGB functionality on ESC key."""
        if not self.connected:
            logger.error("❌ Device not connected")
            return
            
        try:
            # Test red
            logger.info("Testing RED...")
            self.set_led_color(LED_ID_ESC, 255, 0, 0)
            time.sleep(1)
            
            # Test green
            logger.info("Testing GREEN...")
            self.set_led_color(LED_ID_ESC, 0, 255, 0)
            time.sleep(1)
            
            # Test blue
            logger.info("Testing BLUE...")
            self.set_led_color(LED_ID_ESC, 0, 0, 255)
            time.sleep(1)
            
            # Test white
            logger.info("Testing WHITE...")
            self.set_led_color(LED_ID_ESC, 255, 255, 255)
            time.sleep(1)
            
            # Turn off
            logger.info("Turning off...")
            self.set_led_color(LED_ID_ESC, 0, 0, 0)
            
            logger.info("✅ Basic RGB test completed successfully")
            
        except Exception as e:
            logger.error(f"❌ RGB test failed: {e}")

    def test_wasd_pattern(self):
        """Test WASD keys with a cycling pattern."""
        if not self.connected:
            logger.error("❌ Device not connected")
            return
            
        try:
            logger.info("Testing WASD pattern...")
            
            # Cycle through WASD keys
            colors = [
                (255, 0, 0),    # Red
                (0, 255, 0),    # Green
                (0, 0, 255),    # Blue
                (255, 255, 0)   # Yellow
            ]
            
            for i, led_id in enumerate(LED_ID_WASD):
                r, g, b = colors[i]
                self.set_led_color(led_id, r, g, b)
                time.sleep(0.5)
                
            time.sleep(2)
            
            # Turn off WASD
            for led_id in LED_ID_WASD:
                self.set_led_color(led_id, 0, 0, 0)
                
            logger.info("✅ WASD pattern test completed")
            
        except Exception as e:
            logger.error(f"❌ WASD pattern test failed: {e}")

    def cleanup(self):
        """Clean up resources and turn off LEDs."""
        if self.connected:
            try:
                # Turn off ESC
                self.set_led_color(LED_ID_ESC, 0, 0, 0)
                
                # Turn off WASD
                for led_id in LED_ID_WASD:
                    self.set_led_color(led_id, 0, 0, 0)
                    
                # Disconnect
                self.lib.CorsairDisconnect()
                logger.info("✅ Cleanup completed")
                
            except Exception as e:
                logger.error(f"❌ Cleanup failed: {e}")

def main():
    """Run the hardware test suite."""
    print("\n🔱 OMEGA BTC AI - Corsair RGB Hardware Test")
    print("=========================================\n")
    
    tester = CorsairRGBTester()
    
    # Test connection
    if not tester.connect():
        print("\n❌ Failed to connect to Corsair device")
        print("Please check:")
        print("1. iCUE software is running")
        print("2. Device is connected via USB")
        print("3. Device is recognized in iCUE")
        return
    
    try:
        # Run tests
        tester.test_basic_rgb()
        tester.test_wasd_pattern()
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
    finally:
        tester.cleanup()

if __name__ == "__main__":
    main() 