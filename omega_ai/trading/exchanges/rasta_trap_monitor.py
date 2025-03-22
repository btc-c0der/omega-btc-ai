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
    
    def __init__(self,
                 symbol: str = "BTC/USDT:USDT",
                 update_interval: float = 5.0,
                 use_testnet: bool = True):
        """
        Initialize the trap monitor.
        
        Args:
            symbol: Trading symbol in CCXT format
            update_interval: Data update interval in seconds
            use_testnet: Whether to use testnet
        """
        self.use_testnet = use_testnet
        self.update_interval = update_interval
        
        # Format symbol for testnet if needed
        self.symbol = self._format_symbol(symbol)
        logger.info(f"Initialized RastaTrapMonitor with symbol: {self.symbol}")
        
        # Initialize CCXT client
        self.exchange = BitGetCCXT({
            'enableRateLimit': True,
            'options': {
                'defaultType': 'swap',
                'adjustForTimeDifference': True,
                'testnet': use_testnet
            }
        })
        
        # Initialize state
        self.last_update = 0
        self.running = False
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
            }
        }
        
    def _format_symbol(self, symbol: str) -> str:
        """Format symbol for BitGet API."""
        # Remove any existing formatting
        clean_symbol = symbol.replace('/USDT:USDT', '').replace('USDT', '')
        
        # Add testnet prefix if needed
        prefix = 'S' if self.use_testnet else ''
        
        # Format as BTCUSDT or SBTCUSDT for testnet
        formatted = f"{prefix}{clean_symbol}USDT"
        
        # Convert to CCXT format
        base = formatted[:-4]  # Remove USDT suffix
        formatted = f"{base}/USDT:USDT"
            
        return formatted.upper()
        
    async def start(self):
        """Start the trap monitor."""
        self.running = True
        logger.info(f"Starting trap monitor for {self.symbol}")
        
        # Initialize exchange
        try:
            await self.exchange.load_markets()
            logger.info("Successfully loaded markets")
        except Exception as e:
            logger.error(f"Error loading markets: {str(e)}")
            return
            
        while self.running:
            try:
                # Get current time
                current_time = time.time()
                
                # Check if it's time to update
                if current_time - self.last_update >= self.update_interval:
                    await self._update_trap_data()
                    self.last_update = current_time
                
                # Sleep for a short interval
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in trap monitor: {str(e)}")
                await asyncio.sleep(1)  # Sleep longer on error
                
    async def stop(self):
        """Stop the trap monitor."""
        self.running = False
        
    async def _update_trap_data(self):
        """Update trap probability data."""
        try:
            # Get market data
            ticker = await self.exchange.fetch_ticker(self.symbol)
            if not ticker:
                logger.warning(f"Failed to get ticker data for {self.symbol}")
                return
                
            # Get OHLCV data
            ohlcv = await self.exchange.fetch_ohlcv(
                symbol=self.symbol,
                timeframe='1h',
                limit=24
            )
            if not ohlcv:
                logger.warning(f"Failed to get OHLCV data for {self.symbol}")
                return
                
            # Calculate trap probability components
            self.trap_data['components'] = await self._calculate_components(ticker, ohlcv)
            
            # Calculate overall probability
            weights = {
                'fibonacci_alignment': 0.35,
                'price_action': 0.25,
                'trend_strength': 0.15,
                'volume_analysis': 0.15,
                'market_regime': 0.10
            }
            
            probability = sum(
                self.trap_data['components'][k] * weights[k]
                for k in weights
            )
            
            # Update trap data
            self.trap_data.update({
                'probability': round(probability * 100),
                'type': self._determine_trap_type(),
                'trend': self._determine_trend(),
                'confidence': self._calculate_confidence(),
                'timestamp': datetime.now().strftime('%I:%M:%S %p')
            })
            
            # Log update
            logger.info(f"Updated trap data: {json.dumps(self.trap_data, indent=2)}")
            
        except Exception as e:
            logger.error(f"Error updating trap data: {str(e)}")
            
    async def _calculate_components(self, ticker: Dict[str, Any], ohlcv: list) -> Dict[str, float]:
        """Calculate individual trap probability components."""
        try:
            # Extract price data
            current_price = float(ticker['last'])
            high_24h = float(ticker['high'])
            low_24h = float(ticker['low'])
            volume_24h = float(ticker['baseVolume'])
            
            # Calculate Fibonacci levels
            fib_levels = self._calculate_fib_levels(high_24h, low_24h)
            fib_alignment = self._check_fib_alignment(current_price, fib_levels)
            
            # Calculate price action score
            price_action = self._calculate_price_action(ohlcv)
            
            # Calculate trend strength
            trend_strength = self._calculate_trend_strength(ohlcv)
            
            # Calculate volume analysis
            volume_analysis = self._analyze_volume(ohlcv)
            
            # Calculate market regime
            market_regime = self._determine_market_regime(ohlcv)
            
            return {
                'fibonacci_alignment': fib_alignment,
                'price_action': price_action,
                'trend_strength': trend_strength,
                'volume_analysis': volume_analysis,
                'market_regime': market_regime
            }
            
        except Exception as e:
            logger.error(f"Error calculating components: {str(e)}")
            return {k: 0 for k in self.trap_data['components']}
            
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
        
    def _determine_trap_type(self) -> str:
        """Determine the type of trap based on components."""
        components = self.trap_data['components']
        
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
            
    def _determine_trend(self) -> str:
        """Determine current trend direction."""
        if self.trap_data['components']['trend_strength'] > 0.7:
            return 'Bullish' if self.trap_data['components']['price_action'] > 0.5 else 'Bearish'
        return 'Neutral'
        
    def _calculate_confidence(self) -> int:
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
            self.trap_data['components'][k] * weights[k]
            for k in weights
        )
        
        return round(confidence * 100) 