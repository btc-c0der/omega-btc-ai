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
AIXBT Correlation Analyzer
=========================

Analyzes the correlation between AIXBT and BTC prices using advanced statistical methods.
Identifies patterns, lag effects, and causal relationships between the two assets.

Features:
- Multi-timeframe correlation analysis
- Dynamic time warping for lag detection
- Non-linear correlation measurement
- Harmonic pattern recognition
- Quantum correlation scoring
"""

import os
import json
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timezone, timedelta
from scipy.stats import pearsonr, spearmanr, kendalltau
from statsmodels.tsa.stattools import grangercausalitytests, ccf
from tslearn.metrics import dtw

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("aixbt-correlation-analyzer")

# Constants
LOG_PREFIX = "🔄 AIXBT CORRELATION ANALYZER"
CORRELATION_THRESHOLDS = {
    "STRONG_POSITIVE": 0.7,
    "MODERATE_POSITIVE": 0.4,
    "WEAK_POSITIVE": 0.2,
    "NEUTRAL": 0.0,
    "WEAK_NEGATIVE": -0.2,
    "MODERATE_NEGATIVE": -0.4,
    "STRONG_NEGATIVE": -0.7
}

# Golden ratio-based harmonic constants
PHI = 1.618033988749895
INV_PHI = 0.618033988749895
FIBONACCI_LEVELS = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618, 4.236]

class CorrelationAnalyzer:
    """Advanced correlation analyzer for AIXBT and BTC."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the correlation analyzer.
        
        Args:
            config: Configuration dictionary (optional)
        """
        self.config = config or {}
        self.max_lag = self.config.get("max_lag", 10)
        self.timeframes = self.config.get("timeframes", ["1h", "4h", "1d"])
        self.correlation_history = {}
        self.causal_history = {}
        
        # Initialize with empty data
        self.data = pd.DataFrame()
        self.aixbt_prices = np.array([])
        self.btc_prices = np.array([])
        
        # Store latest analysis results
        self.latest_results = {
            "pearson": 0.0,
            "spearman": 0.0,
            "kendall": 0.0,
            "nonlinear": 0.0,
            "optimal_lag": 0,
            "dtw_distance": float('inf'),
            "granger_causality": {
                "btc_causes_aixbt": False,
                "aixbt_causes_btc": False,
                "causality_score": 0.0
            },
            "harmonic_alignment": 0.0,
            "quantum_correlation": 0.0,
            "correlation_phase": "NEUTRAL",
            "convergence_probability": 0.5
        }
        
        logger.info(f"{LOG_PREFIX} - Correlation analyzer initialized with max lag {self.max_lag}")
    
    def load_data(self, data: pd.DataFrame) -> None:
        """
        Load data for correlation analysis.
        
        Args:
            data: DataFrame with AIXBT and BTC price data
        """
        if data.empty:
            logger.warning(f"{LOG_PREFIX} - Empty DataFrame provided for analysis")
            return
            
        required_columns = ["timestamp", "aixbt_price", "btc_price"]
        if not all(col in data.columns for col in required_columns):
            logger.error(f"{LOG_PREFIX} - Missing required columns in data. Required: {required_columns}")
            return
        
        # Store data
        self.data = data.copy()
        
        # Extract price arrays for analysis
        self.aixbt_prices = np.array(self.data["aixbt_price"])
        self.btc_prices = np.array(self.data["btc_price"])
        
        logger.info(f"{LOG_PREFIX} - Loaded {len(data)} data points for analysis")
    
    def analyze_correlation(self, window_size: int = 0) -> Dict[str, Any]:
        """
        Analyze correlation between AIXBT and BTC prices.
        
        Args:
            window_size: Size of the rolling window (0 for entire dataset)
            
        Returns:
            Dictionary with correlation analysis results
        """
        if self.data.empty or len(self.aixbt_prices) == 0 or len(self.btc_prices) == 0:
            logger.warning(f"{LOG_PREFIX} - No data available for correlation analysis")
            return self.latest_results
        
        # Determine data window
        if window_size > 0 and window_size < len(self.aixbt_prices):
            aixbt = self.aixbt_prices[-window_size:]
            btc = self.btc_prices[-window_size:]
        else:
            aixbt = self.aixbt_prices
            btc = self.btc_prices
        
        # Linear correlation (Pearson)
        pearson, _ = pearsonr(aixbt, btc)
        
        # Rank correlation (Spearman)
        spearman, _ = spearmanr(aixbt, btc)
        
        # Kendall's Tau (another rank correlation)
        kendall, _ = kendalltau(aixbt, btc)
        
        # Non-linear correlation score (using mutual information)
        nonlinear = self._calculate_nonlinear_correlation(aixbt, btc)
        
        # Find optimal lag between BTC and AIXBT
        optimal_lag, lag_corr = self._find_optimal_lag(aixbt, btc)
        
        # Dynamic Time Warping distance
        dtw_distance = dtw(aixbt.reshape(-1, 1), btc.reshape(-1, 1))
        
        # Granger causality testing
        granger_results = self._test_granger_causality()
        
        # Harmonic pattern alignment
        harmonic_alignment = self._calculate_harmonic_alignment(aixbt, btc)
        
        # Generate quantum correlation score
        quantum_correlation = self._calculate_quantum_correlation(
            pearson, spearman, kendall, nonlinear, 
            optimal_lag, lag_corr, dtw_distance, 
            granger_results, harmonic_alignment
        )
        
        # Determine correlation phase
        correlation_phase = self._determine_correlation_phase(pearson, quantum_correlation)
        
        # Estimate convergence probability
        convergence_probability = self._estimate_convergence_probability(
            pearson, quantum_correlation, optimal_lag, harmonic_alignment
        )
        
        # Store results
        results = {
            "pearson": pearson,
            "spearman": spearman,
            "kendall": kendall,
            "nonlinear": nonlinear,
            "optimal_lag": optimal_lag,
            "lag_correlation": lag_corr,
            "dtw_distance": dtw_distance,
            "granger_causality": granger_results,
            "harmonic_alignment": harmonic_alignment,
            "quantum_correlation": quantum_correlation,
            "correlation_phase": correlation_phase,
            "convergence_probability": convergence_probability,
            "analysis_time": datetime.now(timezone.utc).isoformat()
        }
        
        # Update latest results
        self.latest_results = results
        
        # Update correlation history
        timeframe = self.config.get("current_timeframe", "1h")
        if timeframe not in self.correlation_history:
            self.correlation_history[timeframe] = []
        
        self.correlation_history[timeframe].append(results)
        
        logger.info(f"{LOG_PREFIX} - Correlation analysis completed: pearson={pearson:.4f}, quantum={quantum_correlation:.4f}")
        return results
    
    def _calculate_nonlinear_correlation(self, x: np.ndarray, y: np.ndarray) -> float:
        """Calculate non-linear correlation between two arrays."""
        try:
            # Calculate distance correlation (works for non-linear relationships)
            # Simplified implementation
            n = len(x)
            if n <= 3:
                return 0.0
            
            # Center the variables
            x_centered = x - np.mean(x)
            y_centered = y - np.mean(y)
            
            # Calculate correlation based on signs of deviations
            sign_agreement = np.sum(np.sign(x_centered) == np.sign(y_centered))
            nonlinear_corr = (sign_agreement / n) * 2 - 1  # Scale to [-1, 1]
            
            return nonlinear_corr
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error calculating non-linear correlation: {e}")
            return 0.0
    
    def _find_optimal_lag(self, x: np.ndarray, y: np.ndarray) -> Tuple[int, float]:
        """Find the optimal lag between two time series."""
        try:
            # Calculate cross-correlation function
            max_lag = min(self.max_lag, len(x) // 5)  # Limit max lag to 20% of series length
            
            # Calculate correlations for different lags
            correlations = []
            for lag in range(-max_lag, max_lag + 1):
                if lag < 0:
                    # Negative lag: y leads x
                    corr, _ = pearsonr(x[:lag], y[-lag:])
                elif lag > 0:
                    # Positive lag: x leads y
                    corr, _ = pearsonr(x[lag:], y[:-lag])
                else:
                    # No lag
                    corr, _ = pearsonr(x, y)
                
                correlations.append((lag, corr))
            
            # Find lag with maximum absolute correlation
            optimal_lag, max_corr = max(correlations, key=lambda x: abs(x[1]))
            
            return optimal_lag, max_corr
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error finding optimal lag: {e}")
            return 0, 0.0
    
    def _test_granger_causality(self) -> Dict[str, Any]:
        """Test Granger causality between BTC and AIXBT prices."""
        results = {
            "btc_causes_aixbt": False,
            "aixbt_causes_btc": False,
            "btc_causes_aixbt_p": 1.0,
            "aixbt_causes_btc_p": 1.0,
            "causality_score": 0.0
        }
        
        if self.data.empty or len(self.data) < 30:
            logger.warning(f"{LOG_PREFIX} - Not enough data for Granger causality test")
            return results
        
        try:
            # Prepare data
            data = self.data[["aixbt_price", "btc_price"]].copy()
            
            # Make data stationary (calculate returns)
            data["aixbt_returns"] = data["aixbt_price"].pct_change().fillna(0)
            data["btc_returns"] = data["btc_price"].pct_change().fillna(0)
            
            # Test BTC -> AIXBT causality
            test_result_btc = grangercausalitytests(
                data[["aixbt_returns", "btc_returns"]].values, 
                maxlag=min(self.max_lag, len(data) // 10),
                verbose=False
            )
            
            # Test AIXBT -> BTC causality
            test_result_aixbt = grangercausalitytests(
                data[["btc_returns", "aixbt_returns"]].values, 
                maxlag=min(self.max_lag, len(data) // 10),
                verbose=False
            )
            
            # Extract p-values for optimal lag
            optimal_lag = min(self.latest_results.get("optimal_lag", 1), len(test_result_btc))
            if optimal_lag < 1:
                optimal_lag = 1
                
            btc_p_value = test_result_btc[optimal_lag][0]["ssr_chi2test"][1]
            aixbt_p_value = test_result_aixbt[optimal_lag][0]["ssr_chi2test"][1]
            
            # Determine causality (95% confidence)
            btc_causes_aixbt = btc_p_value < 0.05
            aixbt_causes_btc = aixbt_p_value < 0.05
            
            # Calculate causality score (inverse of minimum p-value)
            causality_score = 1.0 - min(btc_p_value, aixbt_p_value)
            
            # Update results
            results = {
                "btc_causes_aixbt": btc_causes_aixbt,
                "aixbt_causes_btc": aixbt_causes_btc,
                "btc_causes_aixbt_p": btc_p_value,
                "aixbt_causes_btc_p": aixbt_p_value,
                "causality_score": causality_score
            }
            
            # Store in history
            self.causal_history[datetime.now(timezone.utc).isoformat()] = results
            
            return results
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error testing Granger causality: {e}")
            return results
    
    def _calculate_harmonic_alignment(self, x: np.ndarray, y: np.ndarray) -> float:
        """Calculate how well the price movements align with Fibonacci harmonics."""
        try:
            if len(x) < 3 or len(y) < 3:
                return 0.0
                
            # Calculate percentage changes
            x_pct = np.diff(x) / x[:-1]
            y_pct = np.diff(y) / y[:-1]
            
            # Calculate typical movement sizes
            x_typical = np.median(np.abs(x_pct))
            y_typical = np.median(np.abs(y_pct))
            
            # Check how many movements align with golden ratio and Fibonacci ratios
            fib_alignment_score = 0.0
            
            # Check each ratio
            for ratio in FIBONACCI_LEVELS:
                # Calculate how many x movements are close to this ratio of y movements
                x_target = y_typical * ratio
                x_alignment = np.mean(np.exp(-5 * np.abs(np.abs(x_pct) - x_target) / x_typical))
                
                # Calculate how many y movements are close to this ratio of x movements
                y_target = x_typical * ratio
                y_alignment = np.mean(np.exp(-5 * np.abs(np.abs(y_pct) - y_target) / y_typical))
                
                # Take maximum alignment for this ratio
                fib_alignment_score = max(fib_alignment_score, x_alignment, y_alignment)
            
            # Additional golden ratio specific check (price ratio)
            price_ratio = np.median(x / y)
            golden_price_alignment = np.exp(-2 * min(
                abs(price_ratio - PHI) / PHI,
                abs(price_ratio - INV_PHI) / INV_PHI,
                abs(price_ratio - (PHI*2)) / (PHI*2),
                abs(price_ratio - (INV_PHI/2)) / (INV_PHI/2)
            ))
            
            # Combine scores
            harmonic_score = 0.7 * fib_alignment_score + 0.3 * golden_price_alignment
            
            return harmonic_score
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error calculating harmonic alignment: {e}")
            return 0.0
    
    def _calculate_quantum_correlation(
        self, pearson: float, spearman: float, kendall: float, 
        nonlinear: float, lag: int, lag_corr: float, dtw_distance: float,
        granger_results: Dict[str, Any], harmonic_alignment: float
    ) -> float:
        """Calculate quantum correlation score that integrates multiple metrics."""
        try:
            # Normalize DTW distance to [0, 1] range for easier integration
            max_dtw = len(self.aixbt_prices) * 10  # Arbitrary large number based on data size
            dtw_norm = max(0, 1 - dtw_distance / max_dtw)
            
            # Causality component
            causality_score = granger_results.get("causality_score", 0.0)
            
            # Base correlation (weighted average of different correlation metrics)
            base_correlation = (
                0.4 * abs(pearson) + 
                0.3 * abs(spearman) + 
                0.2 * abs(kendall) + 
                0.1 * abs(nonlinear)
            )
            
            # Lag effect (penalize large lags)
            lag_factor = np.exp(-0.1 * abs(lag)) * abs(lag_corr)
            
            # Combine all components with golden ratio-inspired weighting
            quantum_correlation = (
                (base_correlation * PHI) + 
                (dtw_norm * INV_PHI) + 
                (harmonic_alignment * PHI) + 
                (causality_score * INV_PHI) + 
                (lag_factor * INV_PHI)
            ) / (PHI + INV_PHI + PHI + INV_PHI + INV_PHI)
            
            # Ensure result is in [0, 1] range
            quantum_correlation = max(0, min(1, quantum_correlation))
            
            # Add sign from pearson correlation
            quantum_correlation *= np.sign(pearson)
            
            return quantum_correlation
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error calculating quantum correlation: {e}")
            return 0.0
    
    def _determine_correlation_phase(self, pearson: float, quantum: float) -> str:
        """Determine the correlation phase based on correlation coefficients."""
        # Quantum correlation has primacy, but pearson provides direction
        correlation = quantum * np.sign(pearson)
        
        if correlation > CORRELATION_THRESHOLDS["STRONG_POSITIVE"]:
            return "STRONG_POSITIVE"
        elif correlation > CORRELATION_THRESHOLDS["MODERATE_POSITIVE"]:
            return "MODERATE_POSITIVE"
        elif correlation > CORRELATION_THRESHOLDS["WEAK_POSITIVE"]:
            return "WEAK_POSITIVE"
        elif correlation > CORRELATION_THRESHOLDS["NEUTRAL"]:
            return "NEUTRAL_POSITIVE"
        elif correlation > CORRELATION_THRESHOLDS["WEAK_NEGATIVE"]:
            return "NEUTRAL_NEGATIVE"
        elif correlation > CORRELATION_THRESHOLDS["MODERATE_NEGATIVE"]:
            return "WEAK_NEGATIVE"
        elif correlation > CORRELATION_THRESHOLDS["STRONG_NEGATIVE"]:
            return "MODERATE_NEGATIVE"
        else:
            return "STRONG_NEGATIVE"
    
    def _estimate_convergence_probability(
        self, pearson: float, quantum_correlation: float, 
        optimal_lag: int, harmonic_alignment: float
    ) -> float:
        """Estimate the probability of price convergence based on correlation metrics."""
        try:
            # Start with base probability derived from correlation strength
            base_probability = 0.5 + (quantum_correlation * 0.5)
            
            # Adjust based on lag (closer to zero lag is better for convergence)
            lag_factor = np.exp(-0.2 * abs(optimal_lag))
            
            # Harmonic alignment increases convergence probability
            harmonic_factor = harmonic_alignment
            
            # Combine factors using golden ratio-inspired weighting
            convergence_probability = (
                (base_probability * PHI) + 
                (lag_factor * INV_PHI) + 
                (harmonic_factor * 1.0)
            ) / (PHI + INV_PHI + 1.0)
            
            # Ensure result is in [0, 1] range
            convergence_probability = max(0, min(1, convergence_probability))
            
            return convergence_probability
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error estimating convergence probability: {e}")
            return 0.5
    
    def analyze_multi_timeframe(self, data_dict: Dict[str, pd.DataFrame]) -> Dict[str, Dict[str, Any]]:
        """
        Analyze correlation across multiple timeframes.
        
        Args:
            data_dict: Dictionary mapping timeframes to DataFrames
            
        Returns:
            Dictionary with analysis results for each timeframe
        """
        results = {}
        
        for timeframe, data in data_dict.items():
            if data.empty:
                logger.warning(f"{LOG_PREFIX} - Empty data for timeframe {timeframe}")
                continue
                
            # Set current timeframe in config
            self.config["current_timeframe"] = timeframe
            
            # Load data and analyze
            self.load_data(data)
            timeframe_results = self.analyze_correlation()
            
            # Store results
            results[timeframe] = timeframe_results
            
            logger.info(f"{LOG_PREFIX} - Completed analysis for timeframe {timeframe}")
        
        return results
    
    def generate_correlation_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive correlation report across all timeframes.
        
        Returns:
            Dictionary with correlation report data
        """
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "timeframes": {},
            "overall": {
                "correlation_strength": 0.0,
                "correlation_direction": "NEUTRAL",
                "optimal_lag": 0,
                "causality": "UNKNOWN",
                "convergence_probability": 0.5,
                "harmonic_alignment": 0.0,
                "insights": []
            }
        }
        
        # Process each timeframe
        overall_quantum = 0.0
        timeframe_count = 0
        
        for timeframe, history in self.correlation_history.items():
            if not history:
                continue
                
            # Get latest result for this timeframe
            latest = history[-1]
            
            # Add to report
            report["timeframes"][timeframe] = {
                "pearson": latest.get("pearson", 0.0),
                "quantum_correlation": latest.get("quantum_correlation", 0.0),
                "optimal_lag": latest.get("optimal_lag", 0),
                "correlation_phase": latest.get("correlation_phase", "NEUTRAL"),
                "convergence_probability": latest.get("convergence_probability", 0.5),
                "harmonic_alignment": latest.get("harmonic_alignment", 0.0)
            }
            
            # Accumulate for overall metrics
            overall_quantum += latest.get("quantum_correlation", 0.0)
            timeframe_count += 1
        
        # Calculate overall metrics
        if timeframe_count > 0:
            avg_quantum = overall_quantum / timeframe_count
            
            # Update overall section
            report["overall"]["correlation_strength"] = abs(avg_quantum)
            report["overall"]["correlation_direction"] = "POSITIVE" if avg_quantum >= 0 else "NEGATIVE"
            
            # Generate insights
            insights = self._generate_insights()
            report["overall"]["insights"] = insights
            
            # Extract additional overall metrics from short timeframe (if available)
            short_timeframe = min(self.correlation_history.keys()) if self.correlation_history else None
            if short_timeframe and self.correlation_history[short_timeframe]:
                latest_short = self.correlation_history[short_timeframe][-1]
                report["overall"]["optimal_lag"] = latest_short.get("optimal_lag", 0)
                report["overall"]["convergence_probability"] = latest_short.get("convergence_probability", 0.5)
                report["overall"]["harmonic_alignment"] = latest_short.get("harmonic_alignment", 0.0)
                
                # Determine causality
                granger = latest_short.get("granger_causality", {})
                if granger.get("btc_causes_aixbt") and not granger.get("aixbt_causes_btc"):
                    report["overall"]["causality"] = "BTC_LEADS"
                elif not granger.get("btc_causes_aixbt") and granger.get("aixbt_causes_btc"):
                    report["overall"]["causality"] = "AIXBT_LEADS"
                elif granger.get("btc_causes_aixbt") and granger.get("aixbt_causes_btc"):
                    report["overall"]["causality"] = "BIDIRECTIONAL"
                else:
                    report["overall"]["causality"] = "INDEPENDENT"
        
        return report
    
    def _generate_insights(self) -> List[str]:
        """Generate actionable insights based on correlation analysis."""
        insights = []
        
        # Check if we have correlation data
        if not self.correlation_history:
            return ["Insufficient data for insights"]
        
        # Get shortest timeframe data (e.g., "1h")
        short_timeframe = min(self.correlation_history.keys())
        short_history = self.correlation_history[short_timeframe]
        
        if not short_history:
            return ["Insufficient data for insights"]
        
        # Get most recent and previous correlation data
        latest = short_history[-1]
        previous = short_history[-2] if len(short_history) > 1 else latest
        
        # Check correlation trend
        if latest["quantum_correlation"] > previous["quantum_correlation"] + 0.1:
            insights.append("Correlation strength is rapidly increasing, suggesting stronger BTC influence")
        elif latest["quantum_correlation"] < previous["quantum_correlation"] - 0.1:
            insights.append("Correlation strength is rapidly decreasing, suggesting AIXBT price independence")
        
        # Check lag changes
        if abs(latest["optimal_lag"]) < abs(previous["optimal_lag"]):
            insights.append(f"Price reaction time decreasing from {abs(previous['optimal_lag'])} to {abs(latest['optimal_lag'])} periods")
        elif abs(latest["optimal_lag"]) > abs(previous["optimal_lag"]):
            insights.append(f"Price reaction time increasing from {abs(previous['optimal_lag'])} to {abs(latest['optimal_lag'])} periods")
        
        # Check for causality insights
        latest_granger = latest.get("granger_causality", {})
        if latest_granger.get("btc_causes_aixbt") and not latest_granger.get("aixbt_causes_btc"):
            insights.append("BTC movements are driving AIXBT price changes")
        elif not latest_granger.get("btc_causes_aixbt") and latest_granger.get("aixbt_causes_btc"):
            insights.append("AIXBT is moving independently and potentially influencing BTC")
        
        # Check for harmonic alignment
        if latest["harmonic_alignment"] > 0.7:
            insights.append("Strong harmonic alignment detected, suggesting natural market equilibrium")
        
        # Check for convergence probability
        if latest["convergence_probability"] > 0.7:
            insights.append("High probability of price convergence in the near term")
        elif latest["convergence_probability"] < 0.3:
            insights.append("Low probability of price convergence, potential for continued divergence")
        
        return insights

def main():
    """Run correlation analyzer as a standalone script."""
    import sys
    import argparse
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="AIXBT Correlation Analyzer")
    parser.add_argument("--data", type=str, help="Path to CSV file with price data")
    parser.add_argument("--timeframe", type=str, default="1h", help="Timeframe for analysis")
    args = parser.parse_args()
    
    # Check if data file is provided
    if not args.data:
        logger.error("No data file provided. Use --data to specify a CSV file.")
        sys.exit(1)
    
    # Load data
    try:
        data = pd.read_csv(args.data)
        logger.info(f"Loaded {len(data)} rows from {args.data}")
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        sys.exit(1)
    
    # Create analyzer
    analyzer = CorrelationAnalyzer({"current_timeframe": args.timeframe})
    
    # Load data and analyze
    analyzer.load_data(data)
    results = analyzer.analyze_correlation()
    
    # Print results
    print(json.dumps(results, indent=2))
    
    # Generate report
    report = analyzer.generate_correlation_report()
    print("\nCorrelation Report:")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main() 