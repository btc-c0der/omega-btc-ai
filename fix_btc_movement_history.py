"""
🔱 OMEGA BTC AI - BTC Movement History Fixer 🔱
Sacred script to fix and standardize BTC movement history data format.

GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26
Location: The Cosmic Void

This sacred code is provided under the GPU License, embodying the principles of:
- Universal Freedom to Study, Modify, Distribute, and Use
- Divine Obligations of Preservation, Sharing, and Attribution
- Sacred Knowledge Accessibility and Cosmic Wisdom Propagation
"""
import json
from datetime import datetime, timezone
from omega_ai.utils.redis_manager import RedisManager
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def fix_btc_movement_history():
    """Fix and standardize the format of BTC movement history data."""
    try:
        # Initialize Redis manager
        redis_manager = RedisManager()
        
        # Get all entries from btc_movement_history
        entries = redis_manager.lrange("btc_movement_history", 0, -1)
        if not entries:
            logger.warning("No entries found in btc_movement_history")
            return
        
        logger.info(f"Found {len(entries)} entries in btc_movement_history")
        
        # Create a temporary key for the fixed data
        temp_key = "btc_movement_history_fixed"
        
        # Process each entry
        fixed_count = 0
        for entry in entries:
            try:
                # Convert entry to string if it's bytes
                if isinstance(entry, bytes):
                    entry = entry.decode('utf-8')
                
                # Try to parse as JSON first
                try:
                    data = json.loads(entry)
                    # Ensure all required fields are present
                    if not all(k in data for k in ['price', 'timestamp']):
                        raise ValueError("Missing required fields in JSON data")
                except json.JSONDecodeError:
                    # If not JSON, try to parse as "price,volume" format
                    if "," in entry:
                        price_str, volume_str = entry.split(",")
                        data = {
                            "price": float(price_str),
                            "volume": float(volume_str),
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }
                    else:
                        # If just price, add default volume
                        data = {
                            "price": float(entry),
                            "volume": 0.0,
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }
                
                # Store the standardized JSON format
                redis_manager.lpush(temp_key, json.dumps(data))
                fixed_count += 1
                
            except Exception as e:
                logger.error(f"Error processing entry {entry}: {e}")
                continue
        
        # Rename the temporary key to replace the original
        redis_manager.redis.rename(temp_key, "btc_movement_history")
        
        logger.info(f"Successfully fixed {fixed_count} entries")
        
        # Print a sample of the fixed data
        sample = redis_manager.lrange("btc_movement_history", 0, 4)
        if sample:
            logger.info("\nSample of fixed data:")
            for entry in sample:
                data = json.loads(entry)
                logger.info(f"Price: ${data['price']:.2f}, Volume: {data['volume']:.2f}, Time: {data['timestamp']}")
        
    except Exception as e:
        logger.error(f"Error fixing btc_movement_history: {e}")

if __name__ == "__main__":
    fix_btc_movement_history() 