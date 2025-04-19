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
btc_gpu_accelerator.py - GPU-accelerated BTC price analysis module
Part of the OMEGA BTC AI DIVINE COLLECTIVE

This module provides GPU-accelerated functions for BTC price analysis
when TensorFlow is available. The module gracefully falls back to CPU
calculation if TensorFlow is not installed.

To enable GPU acceleration:
1. Install TensorFlow: pip install tensorflow
2. Set USE_GPU=true in your environment
3. Uncomment GPU sections in docker-compose.yml
"""

import os
import time
import logging
import numpy as np
from typing import List, Dict, Union, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('btc_gpu_accelerator')

# Try to import TensorFlow but don't fail if it's not available
TF_AVAILABLE = False
tf = None  # Initialize tf as None to avoid unbound variable errors

try:
    import tensorflow as tf  # type: ignore
    TF_AVAILABLE = True
    logger.info("TensorFlow available - GPU acceleration possible")
    
    # Get TensorFlow version
    logger.info(f"TensorFlow version: {tf.__version__}")
    
    # Check for GPU availability
    physical_devices = tf.config.list_physical_devices('GPU')
    if physical_devices:
        logger.info(f"GPU devices available: {len(physical_devices)}")
        # Enable memory growth to avoid allocating all GPU memory at once
        for device in physical_devices:
            try:
                tf.config.experimental.set_memory_growth(device, True)
                logger.info(f"Memory growth enabled for device: {device}")
            except Exception as e:
                logger.warning(f"Failed to set memory growth: {e}")
    else:
        logger.warning("No GPU devices found for TensorFlow - using CPU mode")
except ImportError:
    logger.warning("TensorFlow not available - only CPU calculations will be used")

class GPUAccelerator:
    """
    GPU-accelerated BTC price analysis module.
    Falls back to CPU calculations if GPU is not available.
    """
    
    def __init__(self, use_gpu: bool = True):
        """
        Initialize the accelerator.
        
        Args:
            use_gpu: Whether to use GPU acceleration (if available)
        """
        self.use_gpu = use_gpu and TF_AVAILABLE
        logger.info(f"Initializing with GPU acceleration {'enabled' if self.use_gpu else 'disabled'}")
    
    def test_gpu_performance(self) -> Dict[str, Union[bool, float]]:
        """
        Test GPU performance and return metrics.
        
        Returns:
            Dictionary with GPU performance metrics
        """
        if not self.use_gpu or not TF_AVAILABLE or tf is None:
            return {
                "gpu_available": False,
                "performance_score": 0.0,
                "matrix_mult_time": 0.0
            }
            
        try:
            # Create test matrices for performance testing
            matrix_size = 1000
            start_time = time.time()
            
            with tf.device('/GPU:0'):
                # Create random matrices
                a = tf.random.normal((matrix_size, matrix_size))
                b = tf.random.normal((matrix_size, matrix_size))
                
                # Perform matrix multiplication
                c = tf.matmul(a, b)
                
                # Force computation to complete
                result = c.numpy()
            
            elapsed_time = time.time() - start_time
            
            # Calculate performance score
            performance_score = matrix_size * matrix_size / elapsed_time / 10000
            
            return {
                "gpu_available": True,
                "performance_score": float(performance_score),
                "matrix_mult_time": float(elapsed_time)
            }
        except Exception as e:
            logger.error(f"GPU performance test failed: {e}")
            return {
                "gpu_available": False,
                "performance_score": 0.0,
                "matrix_mult_time": 0.0
            }
    
    def calculate_fibonacci_levels(self, price_history: List[float]) -> Dict[str, Any]:
        """
        Calculate Fibonacci levels for the price history.
        Uses GPU acceleration if available, otherwise CPU.
        
        Args:
            price_history: List of historical prices
            
        Returns:
            Dictionary of Fibonacci levels and possibly error information
        """
        if not price_history or len(price_history) < 2:
            return {}
            
        try:
            # Use TensorFlow if available and GPU enabled
            if self.use_gpu and TF_AVAILABLE and tf is not None:
                # Convert to TensorFlow tensors
                prices = tf.constant(price_history, dtype=tf.float32)
                
                # Calculate high and low
                high = tf.reduce_max(prices)
                low = tf.reduce_min(prices)
                
                # Calculate price range
                range_price = high - low
                
                # Calculate Fibonacci levels
                fib_levels = {
                    "high": float(high.numpy()),
                    "low": float(low.numpy()),
                    "fib_0.0": float(low.numpy()),
                    "fib_0.236": float((low + 0.236 * range_price).numpy()),
                    "fib_0.382": float((low + 0.382 * range_price).numpy()),
                    "fib_0.5": float((low + 0.5 * range_price).numpy()),
                    "fib_0.618": float((low + 0.618 * range_price).numpy()),
                    "fib_0.786": float((low + 0.786 * range_price).numpy()),
                    "fib_1.0": float(high.numpy()),
                    "fib_1.272": float((high + 0.272 * range_price).numpy()),
                    "fib_1.618": float((high + 0.618 * range_price).numpy())
                }
            else:
                # CPU calculation fallback
                high = max(price_history)
                low = min(price_history)
                range_price = high - low
                
                # Calculate Fibonacci levels
                fib_levels = {
                    "high": high,
                    "low": low,
                    "fib_0.0": low,
                    "fib_0.236": low + 0.236 * range_price,
                    "fib_0.382": low + 0.382 * range_price,
                    "fib_0.5": low + 0.5 * range_price,
                    "fib_0.618": low + 0.618 * range_price,
                    "fib_0.786": low + 0.786 * range_price,
                    "fib_1.0": high,
                    "fib_1.272": high + 0.272 * range_price,
                    "fib_1.618": high + 0.618 * range_price
                }
            
            return fib_levels
            
        except Exception as e:
            logger.error(f"Error calculating Fibonacci levels: {e}")
            # Fallback to basic calculation on error
            try:
                high = max(price_history)
                low = min(price_history)
                return {
                    "high": high,
                    "low": low,
                    "error": str(e)
                }
            except:
                return {"error": "Failed to calculate Fibonacci levels"}
    
    def detect_market_maker_traps(self, price_history: List[float]) -> Dict[str, Any]:
        """
        Detect potential market maker traps.
        
        Args:
            price_history: List of historical prices
            
        Returns:
            Dictionary with potential bull and bear traps
        """
        if len(price_history) < 50:
            return {"bull_traps": [], "bear_traps": []}
            
        try:
            # Use simple moving averages and momentum for trap detection
            # This can work with just CPU or with GPU acceleration
            prices = np.array(price_history)
            
            # Calculate price changes
            price_changes = np.diff(prices)
            price_changes = np.append(price_changes, 0)  # Add a 0 at the end to maintain length
            
            # Calculate simple moving averages
            def sma(data, window):
                return np.convolve(data, np.ones(window)/window, mode='valid')
                
            ma20 = sma(prices, 20)
            ma50 = sma(prices, 50)
            
            # Calculate momentum (10-period SMA of price changes)
            momentum = sma(price_changes, 10)
            
            # Pad the beginning of MAs to match original length
            ma20_padded = np.pad(ma20, (len(prices) - len(ma20), 0), 'edge')
            ma50_padded = np.pad(ma50, (len(prices) - len(ma50), 0), 'edge')
            momentum_padded = np.pad(momentum, (len(prices) - len(momentum), 0), 'edge')
            
            # Find potential bull traps (false breakouts to the upside)
            bull_traps = []
            bear_traps = []
            
            # Only process the last 30 price points
            analysis_range = min(30, len(prices) - 3)
            
            for i in range(analysis_range, 3, -1):
                idx = len(prices) - i
                
                # Bull trap detection
                if (momentum_padded[idx] > 0 and 
                    momentum_padded[idx-1] > 0 and 
                    momentum_padded[idx-2] < 0 and 
                    prices[idx] > ma20_padded[idx]):
                    
                    bull_traps.append({
                        "index": idx,
                        "price": float(prices[idx]),
                        "confidence": abs(float(momentum_padded[idx])) * 100,
                        "description": "Potential bull trap: Price rising with increasing momentum above MA20"
                    })
                
                # Bear trap detection
                if (momentum_padded[idx] < 0 and 
                    momentum_padded[idx-1] < 0 and 
                    momentum_padded[idx-2] > 0 and 
                    prices[idx] < ma20_padded[idx]):
                    
                    bear_traps.append({
                        "index": idx,
                        "price": float(prices[idx]),
                        "confidence": abs(float(momentum_padded[idx])) * 100,
                        "description": "Potential bear trap: Price falling with increasing momentum below MA20"
                    })
            
            # Sort traps by confidence
            bull_traps.sort(key=lambda x: x["confidence"], reverse=True)
            bear_traps.sort(key=lambda x: x["confidence"], reverse=True)
            
            return {
                "bull_traps": bull_traps[:5],  # Return top 5 most confident traps
                "bear_traps": bear_traps[:5]
            }
            
        except Exception as e:
            logger.error(f"Error detecting market maker traps: {e}")
            return {"bull_traps": [], "bear_traps": [], "error": str(e)}
    
    def predict_price_movement(self, price_history: List[float]) -> Dict[str, Any]:
        """
        Predict short-term price movement direction.
        Uses a simple algorithm that works without TensorFlow if needed.
        
        Args:
            price_history: List of historical prices
            
        Returns:
            Dictionary with prediction results
        """
        if len(price_history) < 30:
            return {
                "prediction": price_history[-1] if price_history else 0,
                "direction": "unknown",
                "confidence": 0.0,
                "error": "Insufficient data"
            }
            
        try:
            # Use a simple trend-based prediction if TensorFlow isn't available
            # This is much simpler than a deep learning model but provides a baseline
            
            # Get the most recent prices
            recent_prices = price_history[-30:]
            
            # Calculate short and long moving averages
            short_ma = sum(recent_prices[-5:]) / 5
            long_ma = sum(recent_prices[-20:]) / 20
            
            # Calculate momentum
            momentum = recent_prices[-1] - recent_prices[-10]
            
            # Calculate basic slope
            slope = (recent_prices[-1] - recent_prices[-10]) / 10
            
            # Determine direction
            if short_ma > long_ma and momentum > 0:
                direction = "up"
                # Confidence based on how much short MA is above long MA
                confidence = min(0.8, abs((short_ma / long_ma) - 1) * 10)
            elif short_ma < long_ma and momentum < 0:
                direction = "down"
                # Confidence based on how much short MA is below long MA
                confidence = min(0.8, abs((long_ma / short_ma) - 1) * 10)
            else:
                # Mixed signals
                direction = "up" if momentum > 0 else "down"
                confidence = min(0.4, abs(momentum) / recent_prices[-1] * 10)
            
            # Calculate simple prediction based on trend
            current_price = recent_prices[-1]
            prediction = current_price * (1 + (0.005 * slope if direction == "up" else -0.005 * slope))
            
            return {
                "current_price": float(current_price),
                "prediction": float(prediction),
                "direction": direction,
                "confidence": float(confidence),
                "accelerated": self.use_gpu
            }
            
        except Exception as e:
            logger.error(f"Error predicting price movement: {e}")
            return {
                "prediction": price_history[-1] if price_history else 0,
                "direction": "unknown",
                "confidence": 0.0,
                "error": str(e)
            }

# Create a global instance for easy importing
gpu_accelerator = GPUAccelerator(use_gpu=os.environ.get('USE_GPU', 'false').lower() == 'true')

if __name__ == "__main__":
    # Test the accelerator
    logger.info("Testing btc_gpu_accelerator.py")
    
    # GPU performance test
    perf_test = gpu_accelerator.test_gpu_performance()
    logger.info(f"GPU performance test: {perf_test}")
    
    # Create sample price data
    sample_prices = [30000 + i + np.sin(i/10)*500 for i in range(100)]
    
    # Calculate Fibonacci levels
    fib_levels = gpu_accelerator.calculate_fibonacci_levels(sample_prices)
    logger.info(f"Fibonacci levels: {fib_levels}")
    
    # Detect market maker traps
    traps = gpu_accelerator.detect_market_maker_traps(sample_prices)
    logger.info(f"Detected {len(traps['bull_traps'])} bull traps and {len(traps['bear_traps'])} bear traps")
    
    # Predict price movement
    prediction = gpu_accelerator.predict_price_movement(sample_prices)
    logger.info(f"Price prediction: {prediction}")
    
    logger.info("All tests completed.") 