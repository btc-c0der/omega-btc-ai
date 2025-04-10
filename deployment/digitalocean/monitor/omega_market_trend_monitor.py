
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
OMEGA MARKET TREND MONITOR
A unified divine market analysis system for BTC price monitoring.
"""

from datetime import datetime, timezone, timedelta
import time
from typing import Dict, Any, List, Optional, Tuple, Union, Type, Protocol, cast, TypedDict, runtime_checkable, TYPE_CHECKING, NotRequired
import numpy as np
from numpy.typing import NDArray
import numpy.typing as npt
import os
import sys

# Add the project root to Python path to resolve imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(project_root)

# Local imports with proper type hints
if TYPE_CHECKING:
    from deployment.digitalocean.utils.redis_manager import RedisManager as ExternalRedisManager
    from deployment.digitalocean.logging.omega_logger import OmegaLogger as ExternalLogger
    from deployment.digitalocean.ai.market_trends_ai_model import MarketTrendsAIModel as ExternalAIModel
    from deployment.digitalocean.quantum.gamon_trinity_matrix import GAMONTrinityMatrix as ExternalTrinityMatrix

# ANSI color codes for divine visualization
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
PURPLE = "\033[35m"
RESET = "\033[0m"

class PriceData(TypedDict):
    """Type definition for price data."""
    price: str
    timestamp: str

class FibonacciLevels(TypedDict):
    """Type definition for Fibonacci levels."""
    zero: float
    two_three_six: float
    three_eight_two: float
    five_hundred: float
    six_one_eight: float
    seven_eight_six: float
    one_thousand: float

class MMTrap(TypedDict, total=False):
    """Type definition for market maker trap data."""
    detected: bool
    probability: float
    type: str
    timeframe: str
    trend: str
    change: float

class MarketAnalysis(TypedDict):
    """Type definition for market analysis result."""
    trend: str
    energy: float
    alignment: float
    current_price: float
    fibonacci_levels: FibonacciLevels
    quantum_state: float
    mm_trap: Optional[Dict[str, Any]]
    temporal_data: List[Dict[str, Any]]
    energy_shift: float
    timestamp: str
    price_change: float
    fibonacci_alignment: float

class MarketAnalysisWithError(TypedDict):
    """Type definition for market analysis with error."""
    error: str
    timestamp: str
    trend: str
    current_price: float
    fibonacci_levels: FibonacciLevels
    quantum_state: float
    temporal_data: List[Dict[str, Any]]
    energy_shift: float
    energy: float
    alignment: float
    mm_trap: Optional[Dict[str, Any]]
    fibonacci_alignment: float
    price_change: float

MarketAnalysisResult = Union[MarketAnalysis, MarketAnalysisWithError]

class TrinityStates(TypedDict):
    """Type definition for Trinity Matrix states."""
    quantum_state: float
    temporal_data: List[Dict[str, Any]]
    energy_shift: float
    alignment_score: float

class MarketAnalysisWithQuantum(MarketAnalysis):
    """Type definition for market analysis result with quantum data."""
    trinity_states: TrinityStates

@runtime_checkable
class RedisManagerProtocol(Protocol):
    """Protocol for RedisManager interface."""
    def get_price_history(self, limit: int) -> List[PriceData]: ...
    def get_current_price(self) -> float: ...
    def log_error(self, error: str) -> None: ...
    def log_info(self, message: str) -> None: ...

@runtime_checkable
class LoggerProtocol(Protocol):
    """Protocol for Logger interface."""
    def log_error(self, error: str) -> None: ...
    def log_info(self, message: str) -> None: ...
    def log_warning(self, message: str) -> None: ...

class RedisManager:
    """Mock Redis manager for testing."""
    def __init__(self, host='localhost', port=6379):
        self.host = host
        self.port = port
        
    def get_price_history(self, limit=100):
        """Mock method to get price history."""
        return []
        
    def get_current_price(self):
        """Mock method to get current price."""
        return 0.0

class MarketTrendsAIModelMock:
    """Mock AI model for testing purposes."""
    def predict_trend(self, history):
        return "Neutral", 0.7
        
    def predict_price(self, history):
        if not history:
            return 0, 0
        current = history[0]["price"]
        return current * 1.01, 0.8
        
    def predict_trap_probability(self, timeframe, trend, price_change):
        return 0.5
        
    def generate_market_insight(self, history):
        return "The market appears to be consolidating with potential bullish divergence forming."

class GAMONTrinityMatrix:
    """GAMON Trinity Matrix for quantum market analysis."""
    
    def __init__(self):
        """Initialize the Trinity Matrix."""
        self.quantum_state = 0.0
        self.temporal_data = []
        self.energy_shift = 0.0
        self.alignment_score = 0.0
    
    def update_states(self, price_history: List[float]) -> None:
        """Update quantum states based on price history."""
        if len(price_history) < 2:
            self.quantum_state = 0.0
            self.energy_shift = 0.0
            self.temporal_data = []
            return
        
        # Calculate price changes
        price_changes = np.diff(price_history)
        
        # Update quantum state with mean of changes
        self.quantum_state = float(np.mean(price_changes))
        
        # Calculate energy shift using standard deviation of changes
        self.energy_shift = float(np.std(price_changes))
        
        # Update temporal data
        self.temporal_data = []
        for i, price in enumerate(price_history):
            data = {
                "price": float(price),
                "timestamp": i,
                "energy": float(np.abs(price_changes[i-1])) if i > 0 else 0.0
            }
            self.temporal_data.append(data)
    
    def calculate_alignment_score(self) -> float:
        """Calculate divine alignment score."""
        if not self.temporal_data:
            return 0.0
        
        # Calculate alignment based on energy distribution
        energies = [d["energy"] for d in self.temporal_data]
        if not energies:
            return 0.0
        
        # Normalize energy values
        max_energy = max(energies)
        if max_energy == 0:
            return 0.0
        
        normalized_energies = [float(e / max_energy) for e in energies]
        
        # Calculate alignment score (0 to 1)
        self.alignment_score = float(np.mean(normalized_energies))
        return self.alignment_score

class OmegaMarketTrendMonitor:
    """OMEGA MARKET TREND MONITOR - The unified divine market analysis system."""
    
    def __init__(
        self,
        redis_manager: RedisManagerProtocol,
        logger: LoggerProtocol,
        analysis_interval: int = 300,
        use_ai: bool = True,
        quantum_mode: bool = False
    ):
        """Initialize the market trend monitor."""
        self.redis_manager = redis_manager
        self.logger = logger
        self.analysis_interval = analysis_interval
        self.use_ai = use_ai
        self.quantum_mode = quantum_mode
        self.consecutive_errors = 0
        
        # Initialize models
        if use_ai:
            from deployment.digitalocean.ai.market_trends_ai_model import MarketTrendsAIModel
            self.ai_model: Optional[MarketTrendsAIModel] = MarketTrendsAIModel()
        else:
            self.ai_model = None
            
        if quantum_mode:
            from deployment.digitalocean.quantum.gamon_trinity_matrix import GAMONTrinityMatrix
            self.trinity_matrix: Optional[GAMONTrinityMatrix] = GAMONTrinityMatrix()
        else:
            self.trinity_matrix = None
        
        # Initialize logger
        from deployment.digitalocean.logging.omega_logger import OmegaLogger
        self.logger = OmegaLogger(log_dir="logs/omega_market_monitor")
        self.logger.log_info("OMEGA Market Trend Monitor initialized successfully")
        
        # Initialize state
        self.previous_price: Optional[float] = None

    def _process_price_data(self, price_history: Union[List[PriceData], List[float]]) -> List[float]:
        """Process price data into a list of floats."""
        prices: List[float] = []
        for p in price_history:
            if isinstance(p, dict) and "price" in p:
                prices.append(float(p["price"]))
            elif isinstance(p, (int, float)):
                prices.append(float(p))
        return prices

    def analyze_market(self) -> MarketAnalysis:
        """Analyze market trends and patterns."""
        try:
            # Get price history
            price_history = self.get_btc_price_history()
            if not price_history:
                self.consecutive_errors += 1
                return {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "trend": "Error",
                    "error": "No price data available"
                }
            
            # Reset consecutive errors on successful analysis
            self.consecutive_errors = 0
            
            # Update quantum states
            prices = [float(p["price"]) for p in price_history]
            if self.quantum_mode and self.trinity_matrix:
                self.trinity_matrix.update_states(prices)
                quantum_state = float(self.trinity_matrix.quantum_state)
                energy_shift = float(self.trinity_matrix.energy_shift)
                temporal_data = self.trinity_matrix.temporal_data
                trinity_states = {
                    "quantum_state": quantum_state,
                    "energy_shift": energy_shift,
                    "alignment_score": float(self.trinity_matrix.calculate_alignment_score()),
                    "temporal_data": temporal_data
                }
            else:
                quantum_state = None
                energy_shift = None
                temporal_data = None
                trinity_states = None
            
            # Calculate price changes
            current_price = float(price_history[-1]["price"])
            price_change = ((current_price - float(price_history[0]["price"])) / float(price_history[0]["price"])) * 100
            
            # Determine trend
            if price_change > 2.0:
                trend = "Strongly Bullish"
            elif price_change > 0.5:
                trend = "Bullish"
            elif price_change < -2.0:
                trend = "Strongly Bearish"
            elif price_change < -0.5:
                trend = "Bearish"
            else:
                trend = "Neutral"
            
            # Calculate Fibonacci levels
            levels = self.calculate_fibonacci_levels(prices)
            
            # Detect Fibonacci alignment
            alignment = self.detect_fibonacci_alignment(current_price, levels)
            
            # Detect market maker trap
            mm_trap = self.detect_mm_trap("1h", trend.lower(), price_change)
            
            # Ensure mm_trap is not None
            if mm_trap is None:
                mm_trap = {
                    "detected": False,
                    "probability": 0.0,
                    "type": "none",
                    "timeframe": "1h",
                    "trend": trend.lower(),
                    "change": price_change
                }
            
            return {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "current_price": current_price,
                "price_change": price_change,
                "trend": trend,
                "fibonacci_levels": levels,
                "fibonacci_alignment": alignment,
                "mm_trap": mm_trap,
                "quantum_state": quantum_state,
                "energy_shift": energy_shift,
                "temporal_data": temporal_data,
                "trinity_states": trinity_states
            }
        except Exception as e:
            self.consecutive_errors += 1
            self.logger.log_error(f"Error analyzing market: {str(e)}")
            return {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "trend": "Error",
                "error": str(e)
            }
    
    def _analyze_trend(self, prices: List[float], current_price: float) -> str:
        """Analyze price trend with enhanced thresholds."""
        if not prices or len(prices) < 2:
            return "Error"
        
        # Calculate price changes
        changes = np.diff(prices)
        mean_change = np.mean(changes)
        std_change = np.std(changes)
        
        # Get Trinity alignment if available
        trinity_alignment = 0.5  # Default neutral alignment
        if self.quantum_mode and self.trinity_matrix:
            trinity_alignment = self.trinity_matrix.calculate_alignment_score()
        
        # Adjust thresholds based on Trinity alignment
        threshold_multiplier = 1.0 + trinity_alignment
        
        # Define thresholds
        strong_threshold = 0.5 * threshold_multiplier
        moderate_threshold = 0.2 * threshold_multiplier
        
        # Calculate percentage change
        change_pct = (current_price - prices[0]) / prices[0] * 100
        
        # Determine trend
        if abs(change_pct) > strong_threshold:
            if change_pct > 0:
                return "Strongly Bullish"
            else:
                return "Strongly Bearish"
        elif abs(change_pct) > moderate_threshold:
            if change_pct > 0:
                return "Moderately Bullish"
            else:
                return "Moderately Bearish"
        else:
            return "Neutral"
    
    def format_trend_output(self, interval: str, trend: str, change_pct: float) -> str:
        """Format trend output with colors and indicators."""
        # Define colors
        GREEN = "\033[92m"
        RED = "\033[91m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        PURPLE = "\033[95m"
        RESET = "\033[0m"
        
        # Define trend indicators
        indicators = {
            "Strongly Bullish": f"{GREEN}📈{RESET}",
            "Moderately Bullish": f"{GREEN}↗️{RESET}",
            "Strongly Bearish": f"{RED}📉{RESET}",
            "Moderately Bearish": f"{RED}↘️{RESET}",
            "Neutral": f"{YELLOW}➡️{RESET}",
            "Error": f"{RED}⚠️{RESET}"
        }
        
        # Get indicator
        indicator = indicators.get(trend, indicators["Neutral"])
        
        # Format change percentage
        if change_pct > 0:
            change_str = f"{GREEN}+{change_pct:.2f}%{RESET}"
        elif change_pct < 0:
            change_str = f"{RED}{change_pct:.2f}%{RESET}"
        else:
            change_str = f"{YELLOW}{change_pct:.2f}%{RESET}"
        
        # Format trend
        if "Bullish" in trend:
            trend_str = f"{GREEN}{trend}{RESET}"
        elif "Bearish" in trend:
            trend_str = f"{RED}{trend}{RESET}"
        else:
            trend_str = f"{YELLOW}{trend}{RESET}"
        
        # Combine all elements
        return f"{indicator} {PURPLE}{interval}{RESET} Trend: {trend_str} ({change_str}) {PURPLE}⚛{RESET}"
    
    def run_monitor(self) -> None:
        """Run the market trend monitor."""
        try:
            while True:
                # Get current BTC price
                try:
                    btc_price = self.redis_manager.get_current_price()
                    if btc_price > 0:
                        self.previous_price = btc_price
                except Exception as e:
                    self.logger.log_error(f"Error getting BTC price: {e}")
                
                if self.previous_price == 0:
                    self.logger.log_warning("No current price available, attempting market analysis...")
                
                # Perform market analysis
                analysis = self.analyze_market()
                
                # Log results
                if analysis["trend"] != "Error":
                    self.logger.log_info(
                        self.format_trend_output(
                            interval=f"{self.analysis_interval//60}min",
                            trend=analysis["trend"],
                            change_pct=(analysis["current_price"] - self.previous_price) / self.previous_price * 100 if self.previous_price else 0
                        )
                    )
                else:
                    self.logger.log_error(f"Market analysis error: {analysis.get('error', 'Unknown error')}")
                
                # Update previous price
                self.previous_price = analysis["current_price"]
                
                # Sleep for the analysis interval
                time.sleep(self.analysis_interval)
                
        except KeyboardInterrupt:
            self.logger.log_info("Market trend monitor stopped by user")
        except Exception as e:
            self.logger.log_error(f"Error in market trend monitor: {e}")

    def _calculate_fibonacci_levels(self, price_data: List[float]) -> FibonacciLevels:
        """Calculate Fibonacci retracement levels."""
        if not price_data or len(price_data) < 2:
            return {
                'zero': 0.0,
                'two_three_six': 0.0,
                'three_eight_two': 0.0,
                'five_hundred': 0.0,
                'six_one_eight': 0.0,
                'seven_eight_six': 0.0,
                'one_thousand': 0.0
            }
            
        high = max(price_data)
        low = min(price_data)
        diff = high - low
        
        return {
            'zero': low,
            'two_three_six': low + diff * 0.236,
            'three_eight_two': low + diff * 0.382,
            'five_hundred': low + diff * 0.500,
            'six_one_eight': low + diff * 0.618,
            'seven_eight_six': low + diff * 0.786,
            'one_thousand': high
        }

    def detect_fibonacci_alignment(self, current_price: float, levels: FibonacciLevels) -> Optional[Dict[str, Any]]:
        """Detect if current price aligns with Fibonacci levels."""
        if not levels:
            return None
        
        # Convert current price to float if it isn't already
        current_price = float(current_price)
        
        # Create a mapping from internal keys to display keys
        key_mapping = {
            'zero': '0',
            'two_three_six': '0.236',
            'three_eight_two': '0.382',
            'five_hundred': '0.500',
            'six_one_eight': '0.618',
            'seven_eight_six': '0.786',
            'one_thousand': '1.000'
        }
        
        # Find closest level
        closest_level = min(levels.items(), key=lambda x: abs(float(x[1]) - current_price))
        difference_pct = abs(closest_level[1] - current_price) / current_price * 100
        
        # Check if price is aligned (within 0.5% of a Fibonacci level)
        if difference_pct <= 0.5:
            return {
                "level": key_mapping[closest_level[0]],
                "price": closest_level[1],
                "difference_pct": difference_pct,
                "is_aligned": True,
                "type": "Retracement"
            }
        
        return None

    def get_btc_price_history(self, limit: int = 100) -> List[PriceData]:
        """Get BTC price history from Redis."""
        try:
            history = self.redis_manager.get_price_history(limit)
            if not history:
                raise ValueError("No price data available")
            return history
        except Exception as e:
            self.logger.log_error(f"Error getting BTC price history: {e}")
            if "Redis connection failed" in str(e):
                raise ValueError("Redis connection failed")
            raise  # Re-raise the exception to be caught by analyze_market
    
    def detect_mm_trap(self, timeframe: str, trend: str, price_change: float) -> Optional[Dict[str, Any]]:
        """Detect potential market maker traps."""
        try:
            # Get trap probability from AI model
            trap_probability = self.ai_model.predict_trap_probability(timeframe, trend, price_change)
            
            # Define trap thresholds
            if trap_probability > 0.7:
                # A bull trap occurs when price appears to be breaking out of a downtrend
                # A bear trap occurs when price appears to be breaking out of an uptrend
                trap_type = "bull" if trend == "bullish" else "bear"
                return {
                    "detected": True,
                    "probability": trap_probability,
                    "type": trap_type,
                    "timeframe": timeframe,
                    "trend": trend,
                    "change": price_change
                }
            return None
        except Exception as e:
            self.logger.log_error(f"Error detecting MM trap: {str(e)}")
            return None

    def get_price_history(self, limit: int = 100) -> List[float]:
        """Get BTC price history."""
        try:
            history = self.get_btc_price_history(limit=limit)
            if not history:
                return []
            return [float(p["price"]) for p in history]
        except Exception as e:
            self.logger.log_error(f"Error getting BTC price history: {e}")
            return []

    def get_current_price(self) -> float:
        """Get current BTC price."""
        try:
            price = self.redis_manager.get_current_price()
            return float(price) if price else 0.0
        except Exception as e:
            self.logger.log_error(f"Error getting current price: {e}")
            return 0.0

    def calculate_fibonacci_levels(self, prices: List[float]) -> FibonacciLevels:
        """Calculate Fibonacci retracement levels."""
        return self._calculate_fibonacci_levels(prices)
        
    def _detect_mm_trap(self, prices: List[float]) -> Optional[Dict[str, Any]]:
        """Detect market maker trap patterns."""
        if not prices or len(prices) < 5:
            return None
            
        # Calculate price changes
        changes = np.diff(prices)
        
        # Detect sudden reversals
        mean_change = np.mean(changes)
        std_change = np.std(changes)
        
        # Look for significant deviations
        significant_moves = [abs(c) > 2 * std_change for c in changes]
        
        if any(significant_moves):
            return {
                "detected": True,
                "confidence": 0.8,
                "pattern": "sudden_reversal"
            }
            
        return None
        
    def analyze_market_trend(self, price_data: Optional[List[float]] = None) -> MarketAnalysisResult:
        """Analyze market trend using price data."""
        try:
            if not price_data:
                price_data = self._get_price_history()
                
            if not price_data:
                raise ValueError("Redis connection failed")
                
            # Update quantum states
            self.trinity_matrix.update_states(price_data)
            
            # Calculate Fibonacci levels
            fib_levels = self._calculate_fibonacci_levels(price_data)
            
            # Get latest price
            current_price = price_data[-1] if price_data else 0.0
            
            # Calculate trend metrics
            trend_direction = "bullish" if self.trinity_matrix.quantum_state > 0 else "bearish"
            energy_level = abs(self.trinity_matrix.energy_shift)
            alignment = self.trinity_matrix.alignment_score
            
            # Detect MM trap
            mm_trap = self._detect_mm_trap(price_data)
            
            return {
                "trend": trend_direction,
                "energy": energy_level,
                "alignment": alignment,
                "current_price": current_price,
                "fibonacci_levels": fib_levels,
                "quantum_state": self.trinity_matrix.quantum_state,
                "mm_trap": mm_trap
            }
            
        except ValueError as e:
            if str(e) == "Redis connection failed":
                return {"error": "Redis connection failed"}
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)} 