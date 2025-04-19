
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

import logging
from omega_ai.data_feed.btc_live_feed import BtcPriceFeed, PriceSource

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run the BTC live feed."""
    feed = None
    try:
        # Create BTC price feed instance
        feed = BtcPriceFeed(
            sources=[PriceSource.BINANCE],  # Start with just Binance
            update_interval=5.0  # Update every 5 seconds
        )
        
        # Start the feed
        logger.info("Starting BTC live feed...")
        feed.start()
        
        # Keep the main thread alive
        while True:
            pass
            
    except KeyboardInterrupt:
        logger.info("Stopping BTC live feed...")
        if feed:
            feed.stop()
    except Exception as e:
        logger.error(f"Error in BTC live feed: {e}")
        raise

if __name__ == "__main__":
    main() 