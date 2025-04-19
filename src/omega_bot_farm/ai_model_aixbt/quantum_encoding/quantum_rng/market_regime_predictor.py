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
Market Regime Predictor
======================

A predictor module that uses quantum RNG outputs to predict market regime changes.
"""

import numpy as np
import pandas as pd
import logging
from typing import List, Dict, Union, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass

from .quantum_rng import QuantumRNG

logger = logging.getLogger("quantum-rng")

class MarketRegime(Enum):
    """Enum representing different market regimes."""
    
    TRENDING_BULL = "trending_bull"  # Strong upward trend
    TRENDING_BEAR = "trending_bear"  # Strong downward trend
    RANGING = "ranging"  # Sideways/consolidation
    VOLATILE = "volatile"  # High volatility, no clear direction
    BREAKDOWN = "breakdown"  # Breaking through support
    BREAKOUT = "breakout"  # Breaking through resistance
    REVERSAL = "reversal"  # Change in trend direction


@dataclass
class RegimePredictionConfig:
    """Configuration for market regime prediction."""
    
    historical_window: int = 30  # Window size for historical data
    quantum_samples: int = 1000  # Number of quantum samples per prediction
    confidence_threshold: float = 0.7  # Confidence threshold for predictions
    simulate_quantum_ensembles: bool = True  # Use quantum ensembles
    volatility_weight: float = 0.4  # Weight for volatility in prediction
    trend_weight: float = 0.3  # Weight for trend in prediction
    volume_weight: float = 0.2  # Weight for volume in prediction
    sentiment_weight: float = 0.1  # Weight for sentiment in prediction
    price_key: str = "close"  # Column name for price data


class MarketRegimePredictor:
    """
    Predicts market regime changes using quantum random number generation.
    
    This class uses quantum RNG outputs to feed stochastic models for
    predicting changes in market regimes.
    """
    
    def __init__(
        self,
        config: Optional[RegimePredictionConfig] = None,
        quantum_rng: Optional[QuantumRNG] = None
    ):
        """
        Initialize the Market Regime Predictor.
        
        Args:
            config: Configuration for regime prediction
            quantum_rng: Quantum random number generator to use
        """
        self.config = config or RegimePredictionConfig()
        self.quantum_rng = quantum_rng or QuantumRNG()
        
        # Initialize state
        self.current_regime = None
        self.regime_probabilities = self._initialize_regime_probabilities()
        self.regime_history = []
        self.prediction_history = []
        
        logger.info("Initialized Market Regime Predictor")
    
    def _initialize_regime_probabilities(self) -> Dict[MarketRegime, float]:
        """Initialize the probability of each market regime."""
        # Start with equal probabilities for all regimes
        regimes = list(MarketRegime)
        equal_prob = 1.0 / len(regimes)
        
        return {regime: equal_prob for regime in regimes}
    
    def _calculate_technical_features(self, price_data: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate technical features from price data.
        
        Args:
            price_data: DataFrame with OHLCV data
            
        Returns:
            Dictionary of technical features
        """
        features = {}
        
        # Basic price features
        price_series = price_data[self.config.price_key].values
        
        # Calculate log returns
        log_returns = np.diff(np.log(price_series))
        
        # Trend features
        features["trend_direction"] = 1 if log_returns[-1] > 0 else -1
        features["trend_strength"] = abs(np.mean(log_returns) / np.std(log_returns))
        
        # Volatility features
        features["volatility"] = np.std(log_returns) * np.sqrt(252)  # Annualized
        features["volatility_change"] = features["volatility"] / np.std(log_returns[:-5])
        
        # Volume features (if available)
        if "volume" in price_data.columns:
            volume = price_data["volume"].values
            features["volume_change"] = volume[-1] / np.mean(volume[-10:])
            features["relative_volume"] = volume[-1] / np.mean(volume)
        else:
            features["volume_change"] = 1.0
            features["relative_volume"] = 1.0
        
        # Range features
        highs = price_data["high"].values if "high" in price_data.columns else price_series
        lows = price_data["low"].values if "low" in price_data.columns else price_series
        
        features["range_width"] = (highs[-1] - lows[-1]) / price_series[-1]
        features["avg_range_width"] = np.mean((highs - lows) / price_series)
        
        # Normalize some features
        features["normalized_volatility"] = min(1.0, features["volatility"] / 0.5)  # Cap at 100%
        
        return features
    
    def _generate_stochastic_parameters(self) -> Dict[str, float]:
        """
        Generate stochastic parameters using quantum RNG.
        
        Returns:
            Dictionary of stochastic parameters
        """
        params = {}
        
        # Generate noise factors for the model
        params["volatility_noise"] = self.quantum_rng.generate_random_float(0.8, 1.2)
        params["trend_noise"] = self.quantum_rng.generate_random_float(0.8, 1.2)
        params["volume_noise"] = self.quantum_rng.generate_random_float(0.8, 1.2)
        
        # Generate probabilistic thresholds
        params["regime_change_threshold"] = self.quantum_rng.generate_random_float(0.15, 0.35)
        
        # Generate random weights for feature combination
        weight_sum = 0.0
        raw_weights = {}
        
        for feature in ["trend", "volatility", "range", "volume"]:
            raw_weights[feature] = self.quantum_rng.generate_random_float(0.5, 1.5)
            weight_sum += raw_weights[feature]
        
        # Normalize weights
        params["feature_weights"] = {
            feature: weight / weight_sum for feature, weight in raw_weights.items()
        }
        
        return params
    
    def _run_stochastic_simulation(
        self,
        features: Dict[str, float],
        num_samples: int
    ) -> Dict[MarketRegime, float]:
        """
        Run stochastic simulation to predict regime probabilities.
        
        Args:
            features: Dictionary of technical features
            num_samples: Number of simulation samples
            
        Returns:
            Dictionary of regime probabilities
        """
        # Initialize regime counts
        regime_counts = {regime: 0 for regime in MarketRegime}
        
        # Run stochastic simulations
        for _ in range(num_samples):
            # Generate stochastic parameters
            params = self._generate_stochastic_parameters()
            
            # Calculate regime scores
            regime_scores = self._calculate_regime_scores(features, params)
            
            # Determine most likely regime based on scores
            most_likely_regime = max(regime_scores.items(), key=lambda x: x[1])[0]
            regime_counts[most_likely_regime] += 1
        
        # Convert counts to probabilities
        regime_probs = {
            regime: count / num_samples for regime, count in regime_counts.items()
        }
        
        return regime_probs
    
    def _calculate_regime_scores(
        self,
        features: Dict[str, float],
        params: Dict[str, float]
    ) -> Dict[MarketRegime, float]:
        """
        Calculate scores for each market regime.
        
        Args:
            features: Dictionary of technical features
            params: Dictionary of stochastic parameters
            
        Returns:
            Dictionary of regime scores
        """
        # Initialize scores
        scores = {regime: 0.0 for regime in MarketRegime}
        
        # Calculate score for TRENDING_BULL
        trend_score = features["trend_direction"] * features["trend_strength"] * params["trend_noise"]
        vol_score = (1 - features["normalized_volatility"]) * params["volatility_noise"]
        
        scores[MarketRegime.TRENDING_BULL] = (
            2.0 * (trend_score > 0) * trend_score + 
            0.5 * vol_score + 
            0.5 * (features["volume_change"] > 1.0) * features["volume_change"] * params["volume_noise"]
        )
        
        # Calculate score for TRENDING_BEAR
        scores[MarketRegime.TRENDING_BEAR] = (
            2.0 * (trend_score < 0) * (-trend_score) + 
            0.5 * vol_score + 
            0.5 * (features["volume_change"] > 1.0) * features["volume_change"] * params["volume_noise"]
        )
        
        # Calculate score for RANGING
        range_score = 1.0 - abs(features["range_width"] / features["avg_range_width"] - 1.0)
        scores[MarketRegime.RANGING] = (
            2.0 * range_score + 
            1.0 * (1 - features["normalized_volatility"]) + 
            0.5 * (1 - features["trend_strength"] / 2.0)
        )
        
        # Calculate score for VOLATILE
        scores[MarketRegime.VOLATILE] = (
            3.0 * features["normalized_volatility"] * params["volatility_noise"] + 
            0.5 * features["range_width"] / features["avg_range_width"]
        )
        
        # Calculate score for BREAKDOWN
        breakdown_score = (features["trend_direction"] < 0) * features["trend_strength"]
        scores[MarketRegime.BREAKDOWN] = (
            2.0 * breakdown_score + 
            1.0 * (features["volume_change"] > 1.2) * features["volume_change"] * params["volume_noise"] +
            1.0 * features["normalized_volatility"] * params["volatility_noise"]
        )
        
        # Calculate score for BREAKOUT
        breakout_score = (features["trend_direction"] > 0) * features["trend_strength"]
        scores[MarketRegime.BREAKOUT] = (
            2.0 * breakout_score + 
            1.0 * (features["volume_change"] > 1.2) * features["volume_change"] * params["volume_noise"] +
            1.0 * features["normalized_volatility"] * params["volatility_noise"]
        )
        
        # Calculate score for REVERSAL
        # A reversal is characterized by a change in trend direction
        # We proxy this by looking at difference between short and long term trends
        # Since we don't have those directly, we use a random factor with weight based on
        # high volatility and volume change
        reversal_potential = features["normalized_volatility"] * features["volume_change"] / 2.0
        reversal_factor = self.quantum_rng.generate_random_float(0, 1) * params["trend_noise"]
        scores[MarketRegime.REVERSAL] = reversal_potential * reversal_factor
        
        return scores
    
    def predict_regime(
        self,
        price_data: pd.DataFrame
    ) -> Tuple[MarketRegime, Dict[MarketRegime, float]]:
        """
        Predict the current market regime based on price data.
        
        Args:
            price_data: DataFrame with OHLCV data
            
        Returns:
            Predicted market regime and probability distribution
        """
        # Calculate technical features
        features = self._calculate_technical_features(price_data)
        
        # Run stochastic simulation
        regime_probs = self._run_stochastic_simulation(
            features, 
            self.config.quantum_samples
        )
        
        # Find most likely regime
        predicted_regime = max(regime_probs.items(), key=lambda x: x[1])[0]
        
        # Store state
        self.current_regime = predicted_regime
        self.regime_probabilities = regime_probs
        self.regime_history.append(predicted_regime)
        
        # Record prediction
        prediction = {
            "regime": predicted_regime,
            "probabilities": regime_probs,
            "features": features,
            "confidence": regime_probs[predicted_regime]
        }
        self.prediction_history.append(prediction)
        
        logger.info(f"Predicted market regime: {predicted_regime.value} with confidence {regime_probs[predicted_regime]:.2f}")
        
        return predicted_regime, regime_probs
    
    def is_regime_change_likely(self) -> Tuple[bool, Optional[MarketRegime]]:
        """
        Determine if a regime change is likely based on recent predictions.
        
        Returns:
            Tuple of (is_change_likely, new_regime)
        """
        if not self.prediction_history or not self.current_regime:
            return False, None
        
        # Get latest prediction
        latest = self.prediction_history[-1]
        
        # Find the regime with highest probability that is not the current regime
        alternative_regimes = {
            regime: prob for regime, prob in latest["probabilities"].items()
            if regime != self.current_regime
        }
        
        next_likely_regime, next_likely_prob = max(
            alternative_regimes.items(), 
            key=lambda x: x[1]
        )
        
        # Check if there's a potential regime change
        current_prob = latest["probabilities"][self.current_regime]
        prob_difference = abs(current_prob - next_likely_prob)
        
        # Determine if change is likely
        is_change_likely = (
            next_likely_prob > self.config.confidence_threshold / 1.5 and
            prob_difference < 0.15
        )
        
        return is_change_likely, next_likely_regime if is_change_likely else None
    
    def generate_regime_transition_matrix(self) -> pd.DataFrame:
        """
        Generate a transition matrix between market regimes.
        
        Returns:
            DataFrame representing the transition matrix
        """
        if len(self.regime_history) < 2:
            return pd.DataFrame()
        
        # Initialize transition counts
        regimes = list(MarketRegime)
        transition_counts = {r1: {r2: 0 for r2 in regimes} for r1 in regimes}
        
        # Count transitions
        for i in range(1, len(self.regime_history)):
            prev_regime = self.regime_history[i-1]
            curr_regime = self.regime_history[i]
            transition_counts[prev_regime][curr_regime] += 1
        
        # Convert to probabilities
        transition_probs = {}
        for prev_regime, counts in transition_counts.items():
            total = sum(counts.values())
            if total > 0:
                transition_probs[prev_regime] = {
                    curr_regime: count / total for curr_regime, count in counts.items()
                }
            else:
                transition_probs[prev_regime] = {curr_regime: 0 for curr_regime in regimes}
        
        # Convert to DataFrame
        regime_values = [r.value for r in regimes]
        df = pd.DataFrame(index=regime_values, columns=regime_values)
        
        for prev_regime in regimes:
            for curr_regime in regimes:
                df.loc[prev_regime.value, curr_regime.value] = transition_probs[prev_regime][curr_regime]
        
        return df
    
    def get_typical_regime_duration(self) -> Dict[MarketRegime, float]:
        """
        Calculate the typical duration of each market regime.
        
        Returns:
            Dictionary mapping regimes to their typical duration in periods
        """
        if len(self.regime_history) < 2:
            return {regime: float('nan') for regime in MarketRegime}
        
        durations = {regime: [] for regime in MarketRegime}
        
        # Calculate durations
        current_regime = self.regime_history[0]
        current_duration = 1
        
        for i in range(1, len(self.regime_history)):
            regime = self.regime_history[i]
            
            if regime == current_regime:
                current_duration += 1
            else:
                durations[current_regime].append(current_duration)
                current_regime = regime
                current_duration = 1
        
        # Add the last regime duration
        durations[current_regime].append(current_duration)
        
        # Calculate average durations
        avg_durations = {}
        for regime, regime_durations in durations.items():
            if regime_durations:
                avg_durations[regime] = np.mean(regime_durations)
            else:
                avg_durations[regime] = float('nan')
        
        return avg_durations

if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Create synthetic price data
    import numpy as np
    
    # Generate synthetic price data
    n_days = 100
    np.random.seed(42)
    
    # Generate random returns
    returns = np.random.normal(0.0005, 0.01, n_days)
    
    # Convert to price series
    price = 100 * np.exp(np.cumsum(returns))
    volume = np.random.lognormal(10, 1, n_days)
    
    # Create DataFrame
    dates = pd.date_range("2023-01-01", periods=n_days)
    df = pd.DataFrame({
        "open": price * (1 - 0.002),
        "high": price * (1 + 0.005),
        "low": price * (1 - 0.005),
        "close": price,
        "volume": volume
    }, index=dates)
    
    # Create predictor
    predictor = MarketRegimePredictor()
    
    # Predict regime
    regime, probs = predictor.predict_regime(df)
    
    print(f"Predicted regime: {regime.value}")
    for r, p in probs.items():
        print(f"  {r.value}: {p:.2f}")
    
    # Check if regime change is likely
    is_change_likely, next_regime = predictor.is_regime_change_likely()
    print(f"Regime change likely: {is_change_likely}")
    if next_regime:
        print(f"Potential next regime: {next_regime.value}")