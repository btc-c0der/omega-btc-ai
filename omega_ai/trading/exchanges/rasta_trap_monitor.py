"""
OMEGA BTC AI - Rasta Trap Monitor
================================

This module implements real-time monitoring of trap probabilities
and market conditions using BitGet data via CCXT.
"""

import asyncio
import logging
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RastaTrapMonitor:
    """Real-time trap monitoring using BitGet data."""
    
    def __init__(self, symbol: str = "BTC-USDT-UMCBL", update_interval: int = 5):
        """Initialize the RastaTrapMonitor.
        
        Args:
            symbol: Trading symbol (default: BTC-USDT-UMCBL)
            update_interval: Data update interval in seconds (default: 5)
        """
        self.symbol = symbol
        self.update_interval = update_interval
        self.logger = logging.getLogger(__name__)
        
        # Initialize BitGet CCXT client
        self.client = BitGetCCXT(config={
            'options': {
                'defaultType': 'swap',
                'adjustForTimeDifference': True,
                'testnet': False  # Use mainnet
            }
        })
        
        self.last_update = None
        self.last_price = None
        self.last_volume = None
        self.is_running = False
        
        # Initialize trap data structure
        self.trap_data = {
            'probability': 0,
            'type': 'Unknown',
            'trend': 'Neutral',
            'confidence': 0,
            'components': {
                'fibonacci_alignment': 0,
                'price_action': 0,
                'trend_strength': 0,
                'volume_analysis': 0,
                'market_regime': 0
            },
            'timestamp': datetime.now().strftime('%I:%M:%S %p')
        }
        
    async def start_monitor(self):
        """Start the trap monitor."""
        try:
            # Initialize the client
            await self.client.initialize()
            
            # Load markets
            await self.client.load_markets()
            self.logger.info("Successfully loaded markets")
            
            self.is_running = True
            while self.is_running:
                try:
                    # Get current ticker data
                    ticker = await self.client.fetch_ticker(self.symbol)
                    if ticker:
                        self.last_price = float(ticker['last'])
                        self.last_volume = float(ticker['baseVolume'])
                        self.last_update = datetime.now()
                        
                        # Update trap data
                        await self.update_trap_data()
                    else:
                        self.logger.warning(f"Failed to get ticker data for {self.symbol}")
                        
                except Exception as e:
                    self.logger.error(f"Error updating trap data: {str(e)}")
                    
                await asyncio.sleep(self.update_interval)
                
        except Exception as e:
            self.logger.error(f"Error in trap monitor: {str(e)}")
            raise
        
    async def stop(self):
        """Stop the trap monitor."""
        self.is_running = False
        
    async def update_trap_data(self):
        """Update trap probability data."""
        try:
            # Get market data
            ticker = await self.client.fetch_ticker(self.symbol)
            if not ticker:
                self.logger.warning(f"Failed to get ticker data for {self.symbol}")
                return
                
            # Get OHLCV data
            ohlcv = await self.client.fetch_ohlcv(
                symbol=self.symbol,
                timeframe='1h',
                limit=24
            )
            if not ohlcv:
                self.logger.warning(f"Failed to get OHLCV data for {self.symbol}")
                return
                
            # Calculate trap probability components
            components = await self._calculate_components(ticker, ohlcv)
            
            # Calculate overall probability
            weights = {
                'fibonacci_alignment': 0.35,
                'price_action': 0.25,
                'trend_strength': 0.15,
                'volume_analysis': 0.15,
                'market_regime': 0.10
            }
            
            probability = sum(
                components[k] * weights[k]
                for k in weights
            )
            
            # Update trap data
            self.trap_data = {
                'probability': round(probability * 100),
                'type': self._determine_trap_type(components),
                'trend': self._determine_trend(components),
                'confidence': self._calculate_confidence(components),
                'timestamp': datetime.now().strftime('%I:%M:%S %p')
            }
            
            # Log update
            self.logger.info(f"Updated trap data: {json.dumps(self.trap_data, indent=2)}")
            
        except Exception as e:
            self.logger.error(f"Error updating trap data: {str(e)}")
            
    async def _calculate_components(self, ticker: Dict[str, Any], ohlcv: list) -> Dict[str, float]:
        """Calculate trap probability components."""
        try:
            # Initialize components
            components = {
                'fibonacci_alignment': 0,
                'price_action': 0,
                'trend_strength': 0,
                'volume_analysis': 0,
                'market_regime': 0
            }
            
            # Current price
            current_price = float(ticker['last'])
            
            # Extract OHLCV data
            closes = [float(candle[4]) for candle in ohlcv]
            volumes = [float(candle[5]) for candle in ohlcv]
            
            # Simple calculations for demonstration
            if len(closes) > 1:
                # Price action component
                price_change = (closes[-1] - closes[0]) / closes[0]
                components['price_action'] = self._normalize_score(abs(price_change) * 10)
                
                # Trend strength
                trend_direction = 1 if price_change > 0 else -1
                trend_consistency = sum(1 for i in range(1, len(closes)) if 
                                      (closes[i] - closes[i-1]) * trend_direction > 0) / (len(closes) - 1)
                components['trend_strength'] = trend_consistency
                
                # Volume analysis
                avg_volume = sum(volumes) / len(volumes)
                volume_trend = sum(1 for i in range(1, len(volumes)) if volumes[i] > volumes[i-1]) / (len(volumes) - 1)
                components['volume_analysis'] = volume_trend * (volumes[-1] / avg_volume if avg_volume > 0 else 1)
                components['volume_analysis'] = self._normalize_score(components['volume_analysis'])
                
                # Market regime
                volatility = sum(abs(closes[i] - closes[i-1]) / closes[i-1] for i in range(1, len(closes))) / (len(closes) - 1)
                components['market_regime'] = self._normalize_score(volatility * 100)
                
                # Fibonacci alignment
                high = max(closes)
                low = min(closes)
                range_price = high - low
                fib_levels = [low + range_price * level for level in [0.236, 0.382, 0.5, 0.618, 0.786]]
                closest_fib = min(fib_levels, key=lambda x: abs(x - current_price))
                fib_proximity = 1 - (abs(closest_fib - current_price) / range_price)
                components['fibonacci_alignment'] = self._normalize_score(fib_proximity * 2)
            
            return components
            
        except Exception as e:
            self.logger.error(f"Error calculating components: {str(e)}")
            return {
                'fibonacci_alignment': 0,
                'price_action': 0,
                'trend_strength': 0,
                'volume_analysis': 0,
                'market_regime': 0
            }
            
    def _calculate_fib_levels(self, high: float, low: float) -> Dict[str, float]:
        """Calculate Fibonacci retracement levels."""
        diff = high - low
        return {
            '0': low,
            '0.236': low + diff * 0.236,
            '0.382': low + diff * 0.382,
            '0.5': low + diff * 0.5,
            '0.618': low + diff * 0.618,
            '0.786': low + diff * 0.786,
            '1': high
        }
        
    def _check_fib_alignment(self, price: float, levels: Dict[str, float]) -> float:
        """Check how well price aligns with Fibonacci levels."""
        # Find closest Fibonacci level
        distances = [abs(price - level) / price for level in levels.values()]
        min_distance = min(distances)
        
        # Convert distance to alignment score (0 to 1)
        alignment = max(0, 1 - min_distance * 10)
        return alignment
        
    def _calculate_price_action(self, ohlcv: list) -> float:
        """Calculate price action score based on candlestick patterns."""
        if not ohlcv or len(ohlcv) < 3:
            return 0.5
            
        # Simple implementation - can be enhanced with more patterns
        latest = ohlcv[-1]
        prev = ohlcv[-2]
        
        # Calculate basic momentum
        momentum = (latest[4] - prev[4]) / prev[4]  # Close price change
        
        # Convert to score between 0 and 1
        score = 0.5 + momentum  # Center around 0.5
        return max(0, min(1, score))  # Clamp between 0 and 1
        
    def _calculate_trend_strength(self, ohlcv: list) -> float:
        """Calculate trend strength using price movement consistency."""
        if not ohlcv or len(ohlcv) < 12:  # Need at least 12 candles
            return 0
            
        # Calculate directional movement
        moves = [1 if ohlcv[i][4] > ohlcv[i-1][4] else -1 for i in range(1, len(ohlcv))]
        
        # Calculate consistency
        consistency = abs(sum(moves)) / len(moves)
        return consistency
        
    def _analyze_volume(self, ohlcv: list) -> float:
        """Analyze volume patterns."""
        if not ohlcv or len(ohlcv) < 24:
            return 0.5
            
        # Calculate average volume
        volumes = [candle[5] for candle in ohlcv]
        avg_volume = sum(volumes) / len(volumes)
        
        # Compare recent volume to average
        recent_volume = sum(volumes[-3:]) / 3
        volume_ratio = recent_volume / avg_volume
        
        # Convert to score between 0 and 1
        score = 0.5 + (volume_ratio - 1) * 0.25  # Center around 0.5
        return max(0, min(1, score))
        
    def _determine_market_regime(self, ohlcv: list) -> float:
        """Determine current market regime (trending vs ranging)."""
        if not ohlcv or len(ohlcv) < 24:
            return 0.5
            
        # Calculate price movement
        closes = [candle[4] for candle in ohlcv]
        price_range = max(closes) - min(closes)
        avg_price = sum(closes) / len(closes)
        
        # Calculate volatility ratio
        volatility = price_range / avg_price
        
        # Convert to score between 0 and 1
        score = 0.5 + volatility * 2  # Center around 0.5
        return max(0, min(1, score))
        
    def _determine_trap_type(self, components: Dict[str, float]) -> str:
        """Determine the type of trap based on components."""
        # Find strongest component
        strongest = max(components.items(), key=lambda x: x[1])
        
        if strongest[0] == 'fibonacci_alignment':
            return 'Fibonacci Confluence'
        elif strongest[0] == 'price_action':
            return 'Price Action Setup'
        elif strongest[0] == 'trend_strength':
            return 'Trend Reversal'
        elif strongest[0] == 'volume_analysis':
            return 'Volume Pattern'
        else:
            return 'Market Structure'
            
    def _determine_trend(self, components: Dict[str, float]) -> str:
        """Determine current trend direction."""
        if components['trend_strength'] > 0.7:
            return 'Bullish' if components['price_action'] > 0.5 else 'Bearish'
        return 'Neutral'
        
    def _calculate_confidence(self, components: Dict[str, float]) -> int:
        """Calculate confidence level in percentage."""
        # Weight components by their reliability
        weights = {
            'fibonacci_alignment': 0.3,
            'price_action': 0.25,
            'trend_strength': 0.2,
            'volume_analysis': 0.15,
            'market_regime': 0.1
        }
        
        confidence = sum(
            components[k] * weights[k]
            for k in weights
        )
        
        return round(confidence * 100)

    def _normalize_score(self, value: float) -> float:
        """Normalize a score to [0, 1] range."""
        # Clip value between 0 and 1
        return max(0.0, min(1.0, value)) 