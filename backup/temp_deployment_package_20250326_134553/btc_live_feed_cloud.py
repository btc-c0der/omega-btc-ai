#!/usr/bin/env python3
"""
btc_live_feed_cloud.py - Real-time BTC price feed optimized for cloud deployment
Part of the OMEGA BTC AI DIVINE COLLECTIVE

This module subscribes to Binance WebSocket and publishes price data to Redis.
It includes TLS support for secure Redis connections and gracefully handles
the case where GPU acceleration is either disabled or not available.
"""

import os
import json
import time
import logging
import traceback
import websocket
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/logs/btc_live_feed.log')
    ]
)
logger = logging.getLogger('btc_live_feed')

# Import Redis Manager
try:
    from redis_manager_cloud import RedisManager
    logger.info("Successfully imported RedisManager")
except ImportError as e:
    logger.error(f"Error importing RedisManager: {e}")
    raise

# Try to import GPU Accelerator
gpu_accelerator = None
try:
    from btc_gpu_accelerator import gpu_accelerator
    logger.info("Successfully imported GPU accelerator module")
    
    # Check if GPU is enabled in environment
    use_gpu = os.environ.get('USE_GPU', 'false').lower() == 'true'
    
    if use_gpu:
        # Test GPU performance
        try:
            perf_metrics = gpu_accelerator.test_gpu_performance()
            if perf_metrics["gpu_available"]:
                logger.info(f"GPU acceleration is ENABLED with performance score: {perf_metrics['performance_score']}")
            else:
                logger.warning("GPU acceleration is DISABLED despite being enabled in config - GPU not available")
                use_gpu = False
        except Exception as e:
            logger.warning(f"GPU performance test failed, falling back to CPU mode: {e}")
            use_gpu = False
    else:
        logger.info("GPU acceleration is DISABLED in configuration")
        
except ImportError as e:
    logger.warning(f"GPU accelerator module not available, using CPU-only mode: {e}")
    use_gpu = False

class BTCLiveFeed:
    """
    Real-time BTC price feed optimized for cloud deployment.
    Subscribes to Binance WebSocket and publishes to Redis.
    """
    
    def __init__(self, 
                 redis_manager: Any,
                 symbol: str = 'btcusdt',
                 reconnect_delay: int = 5,
                 version: str = '0.420'):
        """
        Initialize the BTC Live Feed.
        
        Args:
            redis_manager: The Redis manager instance
            symbol: The trading symbol to track
            reconnect_delay: Delay in seconds before reconnecting
            version: The version of this module
        """
        self.redis_manager = redis_manager
        self.symbol = symbol.lower()
        self.reconnect_delay = reconnect_delay
        self.version = version
        self.ws = None
        self.should_run = True
        self.price_history: List[float] = []
        self.price_timestamps: List[int] = []
        self.use_gpu = use_gpu  # Use the global flag determined at import time
        self.binance_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@trade"
        
        # Diagnostic values
        self.message_count = 0
        self.start_time = datetime.now()
        self.last_update_time = None
        
        logger.info(f"BTCLiveFeed initialized with version {version}")
        logger.info(f"GPU acceleration is {'ENABLED' if self.use_gpu else 'DISABLED'}")
    
    def _on_message(self, ws: Any, message: str) -> None:
        """
        Process incoming WebSocket messages from Binance.
        
        Args:
            ws: WebSocket instance
            message: The message data as string
        """
        try:
            data = json.loads(message)
            price = float(data['p'])
            timestamp = int(data['T'])
            
            # Store in price history (keep most recent 5000 points)
            self.price_history.append(price)
            self.price_timestamps.append(timestamp)
            if len(self.price_history) > 5000:
                self.price_history.pop(0)
                self.price_timestamps.pop(0)
            
            # Save to Redis
            self.redis_manager.set('btc:latest_price', price)
            self.redis_manager.set('btc:latest_update', timestamp)
            
            # Periodically add to time series
            self.message_count += 1
            
            # Every 50 messages, update other metrics
            if self.message_count % 50 == 0:
                self._update_statistics()
                
                # Run GPU-accelerated analysis if GPU is available and we have enough data
                if self.use_gpu and gpu_accelerator is not None and len(self.price_history) > 100:
                    try:
                        self._run_gpu_analysis()
                    except Exception as e:
                        logger.error(f"Error in GPU analysis: {e}")
                        # If we repeatedly fail with GPU analysis, disable it
                        self.use_gpu = False
                        logger.warning("Disabled GPU analysis due to repeated errors")
            
            # Every 1000 messages log stats
            if self.message_count % 1000 == 0:
                runtime = (datetime.now() - self.start_time).total_seconds()
                msg_per_sec = self.message_count / runtime if runtime > 0 else 0
                logger.info(f"Processed {self.message_count} messages ({msg_per_sec:.2f}/sec)")
                
                # Save longer-term data points for charts (every 5 minutes)
                if self.last_update_time is None or (datetime.now() - self.last_update_time).seconds > 300:
                    self.redis_manager.rpush('btc:price_history', json.dumps({
                        'price': price,
                        'timestamp': timestamp
                    }))
                    self.redis_manager.ltrim('btc:price_history', -1440, -1)  # Keep last 24 hours (at 5 min intervals)
                    self.last_update_time = datetime.now()
        
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            
    def _update_statistics(self) -> None:
        """Update statistical metrics in Redis."""
        try:
            if len(self.price_history) < 10:
                return
                
            # Calculate basic statistics
            current_price = self.price_history[-1]
            price_high = max(self.price_history[-100:])
            price_low = min(self.price_history[-100:])
            price_open = self.price_history[-100]
            price_change = current_price - price_open
            price_change_pct = (price_change / price_open) * 100 if price_open > 0 else 0
            
            # Save to Redis
            stats = {
                'price': current_price,
                'high': price_high,
                'low': price_low,
                'open': price_open,
                'change': price_change,
                'change_pct': price_change_pct,
                'timestamp': int(time.time())
            }
            self.redis_manager.set('btc:stats', json.dumps(stats))
            
        except Exception as e:
            logger.error(f"Error updating statistics: {e}")
    
    def _run_gpu_analysis(self) -> None:
        """Run GPU-accelerated analysis on price data if available."""
        if not self.use_gpu or gpu_accelerator is None:
            # Skip if GPU is not available or disabled
            return
            
        try:
            # Calculate Fibonacci levels
            fib_levels = gpu_accelerator.calculate_fibonacci_levels(self.price_history)
            if fib_levels:
                self.redis_manager.set('btc:fibonacci_levels', json.dumps(fib_levels))
            
            # Detect market maker traps
            traps = gpu_accelerator.detect_market_maker_traps(self.price_history)
            if traps and ('bull_traps' in traps or 'bear_traps' in traps):
                self.redis_manager.set('btc:market_traps', json.dumps(traps))
            
            # Predict price movement
            prediction = gpu_accelerator.predict_price_movement(self.price_history)
            if prediction and 'prediction' in prediction:
                self.redis_manager.set('btc:price_prediction', json.dumps(prediction))
                
            # Save a status update
            self.redis_manager.set('btc:gpu_status', json.dumps({
                'enabled': True,
                'timestamp': int(time.time()),
                'message': "GPU analysis completed successfully"
            }))
            
        except Exception as e:
            logger.error(f"Error in GPU analysis: {e}\n{traceback.format_exc()}")
            # Save error status
            self.redis_manager.set('btc:gpu_status', json.dumps({
                'enabled': False,
                'error': str(e),
                'timestamp': int(time.time()),
                'message': "GPU analysis failed"
            }))
    
    def _on_error(self, ws: Any, error: Any) -> None:
        """
        Handle WebSocket errors.
        
        Args:
            ws: WebSocket instance
            error: The error
        """
        logger.error(f"WebSocket error: {error}")
    
    def _on_close(self, ws: Any, close_status_code: Optional[int], 
                  close_reason: Optional[str]) -> None:
        """
        Handle WebSocket connection close.
        
        Args:
            ws: WebSocket instance
            close_status_code: Status code for connection close
            close_reason: Reason for connection close
        """
        logger.info(f"WebSocket connection closed: {close_status_code} - {close_reason}")
        if self.should_run:
            logger.info(f"Reconnecting in {self.reconnect_delay} seconds...")
            time.sleep(self.reconnect_delay)
            self.start()
    
    def _on_open(self, ws: Any) -> None:
        """
        Handle WebSocket connection open.
        
        Args:
            ws: WebSocket instance
        """
        logger.info("WebSocket connection established")
        # Send module version to Redis
        self.redis_manager.set('btc_live_feed:version', self.version)
        self.redis_manager.set('btc_live_feed:status', 'running')
        self.redis_manager.set('btc_live_feed:last_start', int(time.time()))
        
    def start(self) -> None:
        """Start the WebSocket connection and message processing."""
        try:
            websocket.enableTrace(False)
            self.ws = websocket.WebSocketApp(self.binance_url,
                                            on_message=self._on_message,
                                            on_error=self._on_error,
                                            on_close=self._on_close,
                                            on_open=self._on_open)
            
            logger.info(f"Connecting to Binance WebSocket: {self.binance_url}")
            self.ws.run_forever()
        except Exception as e:
            logger.error(f"Error starting WebSocket: {e}")
            if self.should_run:
                logger.info(f"Reconnecting in {self.reconnect_delay} seconds...")
                time.sleep(self.reconnect_delay)
                self.start()
    
    def stop(self) -> None:
        """Stop the WebSocket connection."""
        self.should_run = False
        if self.ws:
            self.ws.close()
        logger.info("WebSocket connection stopped")
        self.redis_manager.set('btc_live_feed:status', 'stopped')

def main() -> None:
    """Main function to start the BTC Live Feed."""
    # Initialize feed_instance to None at the beginning to avoid linter error
    feed_instance = None
    
    try:
        # Get environment variables with defaults
        redis_host = os.environ.get('REDIS_HOST', 'localhost')
        redis_port = int(os.environ.get('REDIS_PORT', '6379'))
        redis_password = os.environ.get('REDIS_PASSWORD', '')
        redis_ssl = os.environ.get('REDIS_SSL', 'false').lower() == 'true'
        redis_cert_path = os.environ.get('REDIS_CERT_PATH', '/app/config/redis.crt')
        
        # Initialize Redis manager with SSL support
        # Note: Check the actual parameter names in your RedisManager implementation
        redis_manager = RedisManager(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            ssl=redis_ssl,                   # Parameter name may vary based on your implementation
            ssl_ca_certs=redis_cert_path if redis_ssl else None  # Parameter name may vary
        )
        
        # Log Redis connection details (without password)
        logger.info(f"Connecting to Redis at {redis_host}:{redis_port} with SSL: {redis_ssl}")
        
        # Start the BTC Live Feed
        feed_instance = BTCLiveFeed(redis_manager)
        feed_instance.start()
        
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down")
        if feed_instance:
            feed_instance.stop()
    except Exception as e:
        logger.error(f"Error in main function: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 