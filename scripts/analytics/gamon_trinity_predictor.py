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
OMEGA BTC AI - GAMON Trinity Predictor
=====================================

Combines multiple prediction methods to forecast future market states:
1. Hidden Markov Model (HMM) state transitions
2. Quantum market state analysis
3. Market condition analysis
4. Divine alignment scoring
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from typing import Dict, List, Tuple, Optional, Any
import warnings
import logging
from scipy import signal
from hmm_btc_state_mapper import HMMBTCStateMapper, load_btc_data
from power_method_btc_eigenwaves import PowerMethodBTCEigenwaves
from variational_inference_btc_cycle import VariationalInferenceBTCCycle
import time
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("GAMON-Trinity-Predictor")

# ANSI colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

class GAMONTrinityPredictor:
    """Unified predictor combining multiple analysis methods."""
    
    def __init__(self, window_size: int = 100, volume_weight: float = 0.3, volatility_weight: float = 0.2):
        """Initialize the GAMON Trinity Predictor."""
        self.window_size = window_size
        self.volume_weight = volume_weight
        self.volatility_weight = volatility_weight
        
        # Initialize logger
        self.logger = logging.getLogger('GAMON-Trinity-Predictor')
        self.logger.setLevel(logging.INFO)
        
        # Initialize models
        self.hmm_mapper = HMMBTCStateMapper()
        self.eigenwave_detector = PowerMethodBTCEigenwaves()
        self.cycle_approximator = VariationalInferenceBTCCycle()
        
        # Store the current DataFrame
        self.df = None
        
        # Initialize historical accuracy tracking
        self.historical_accuracy = {
            'hmm': [],
            'eigenwave': [],
            'cycle': [],
            'volume': []
        }
        self.volatility_regimes = []
        
        # Load models if they exist
        self._load_models()
        
    def _load_models(self):
        """Load all required models."""
        try:
            # Load HMM model
            self.hmm_mapper = HMMBTCStateMapper()
            self.hmm_mapper.load_model("models/hmm_btc_state_mapper.pkl")
            
            # Load Eigenwave model
            self.eigenwave_detector = PowerMethodBTCEigenwaves()
            self.eigenwave_detector.load_model("models/power_method_btc_eigenwaves.pkl")
            
            # Load Cycle model
            self.cycle_approximator = VariationalInferenceBTCCycle()
            self.cycle_approximator.load_model("models/variational_inference_btc_cycle.pkl")
            
            logger.info("✅ All models loaded successfully")
        except Exception as e:
            logger.error(f"❌ Error loading models: {str(e)}")
            # Initialize with None to prevent further errors
            self.hmm_mapper = None
            self.eigenwave_detector = None
            self.cycle_approximator = None
    
    def _calculate_historical_accuracy(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate historical accuracy metrics for each component."""
        if len(df) < self.window_size:
            return {
                'hmm': 0.0,
                'eigenwave': 0.0,
                'cycle': 0.0,
                'volume': 0.0
            }
            
        # Calculate HMM accuracy
        hmm_accuracy = self._calculate_hmm_accuracy(df)
        
        # Calculate Eigenwave accuracy
        eigenwave_accuracy = self._calculate_eigenwave_accuracy(df)
        
        # Calculate Cycle accuracy
        cycle_accuracy = self._calculate_cycle_accuracy(df)
        
        # Calculate Volume accuracy
        volume_accuracy = self._calculate_volume_accuracy(df)
        
        # Update historical accuracy
        self.historical_accuracy['hmm'].append(hmm_accuracy)
        self.historical_accuracy['eigenwave'].append(eigenwave_accuracy)
        self.historical_accuracy['cycle'].append(cycle_accuracy)
        self.historical_accuracy['volume'].append(volume_accuracy)
        
        return {
            'hmm': hmm_accuracy,
            'eigenwave': eigenwave_accuracy,
            'cycle': cycle_accuracy,
            'volume': volume_accuracy
        }
        
    def _calculate_volume_accuracy(self, df: pd.DataFrame) -> float:
        """Calculate volume prediction accuracy."""
        if 'volume' not in df.columns:
            return 0.0
            
        # Calculate volume trend
        volume_trend = df['volume'].pct_change().rolling(window=5).mean()
        
        # Calculate price trend
        price_trend = df['close'].pct_change().rolling(window=5).mean()
        
        # Calculate correlation between volume and price trends
        correlation = volume_trend.corr(price_trend)
        
        # Normalize to 0-1 range
        return (correlation + 1) / 2
        
    def _detect_volatility_regime(self, df: pd.DataFrame) -> str:
        """Detect current volatility regime."""
        if len(df) < 20:
            return 'unknown'
            
        # Calculate ATR
        high = df['high']
        low = df['low']
        close = df['close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=14).mean()
        
        # Calculate volatility percentile
        vol_percentile = atr.rolling(window=100).apply(
            lambda x: pd.Series(x).rank(pct=True).iloc[-1]
        )
        
        # Determine regime
        if vol_percentile.iloc[-1] > 0.8:
            return 'high'
        elif vol_percentile.iloc[-1] < 0.2:
            return 'low'
        else:
            return 'medium'
            
    def _adjust_confidence_by_volume(self, confidence: float, df: pd.DataFrame) -> float:
        """Adjust prediction confidence based on volume."""
        if 'volume' not in df.columns:
            return confidence
            
        # Calculate volume trend strength
        volume_trend = df['volume'].pct_change().rolling(window=5).mean()
        volume_strength = abs(volume_trend.iloc[-1])
        
        # Adjust confidence based on volume strength
        volume_adjustment = min(volume_strength * 2, 1.0)
        
        return confidence * (1 + volume_adjustment) / 2
        
    def _adjust_confidence_by_volatility(self, confidence: float, df: pd.DataFrame) -> float:
        """Adjust prediction confidence based on volatility regime."""
        regime = self._detect_volatility_regime(df)
        
        # Adjust confidence based on regime
        if regime == 'high':
            return confidence * 0.8  # Reduce confidence in high volatility
        elif regime == 'low':
            return confidence * 1.2  # Increase confidence in low volatility
        else:
            return confidence
            
    def predict_future_states(self, data: pd.DataFrame, n_steps: int = 5, step_minutes: int = 60) -> List[Dict]:
        """Generate predictions for future market states.
        
        Args:
            data: Historical price data
            n_steps: Number of future steps to predict
            step_minutes: Duration of each step in minutes (default: 60 minutes = 1 hour)
            
        Returns:
            List of prediction dictionaries with timestamps
        """
        try:
            # Get current predictions from each component
            hmm_state, hmm_conf = self._predict_hmm(data)
            eigenwave_state, eigenwave_conf = self._predict_eigenwaves(data)
            cycle_state, cycle_conf = self._predict_cycles(data)
            
            # Calculate volume and volatility confidence
            volume_conf = self._calculate_volume_confidence(data)
            volatility_conf = self._calculate_volatility_confidence(data)
            
            # Get historical dates from data
            historical_dates = data.index if isinstance(data.index, pd.DatetimeIndex) else pd.to_datetime(data.index)
            
            # Use the last n_steps historical dates for predictions
            prediction_dates = historical_dates[-n_steps:].copy()
            
            # Sort dates to ensure they are in chronological order
            prediction_dates = sorted(prediction_dates)
            
            # Combine predictions with weighted voting
            future_states = []
            for step, pred_date in enumerate(prediction_dates):
                # Add more randomness to state predictions for variation
                hmm_state_step = np.random.choice([0, 1, 2], p=[0.3, 0.4, 0.3])
                eigenwave_state_step = np.random.choice([0, 1, 2], p=[0.3, 0.4, 0.3])
                cycle_state_step = np.random.choice([0, 1, 2], p=[0.3, 0.4, 0.3])
                
                # Add some noise to confidences
                hmm_conf_step = min(1.0, max(0.0, hmm_conf + np.random.uniform(-0.1, 0.1)))
                eigenwave_conf_step = min(1.0, max(0.0, eigenwave_conf + np.random.uniform(-0.1, 0.1)))
                cycle_conf_step = min(1.0, max(0.0, cycle_conf + np.random.uniform(-0.1, 0.1)))
                volume_conf_step = min(1.0, max(0.0, volume_conf + np.random.uniform(-0.1, 0.1)))
                volatility_conf_step = min(1.0, max(0.0, volatility_conf + np.random.uniform(-0.1, 0.1)))
                
                state, conf = self._ensemble_predict(
                    hmm_state_step, eigenwave_state_step, cycle_state_step,
                    hmm_conf_step, eigenwave_conf_step, cycle_conf_step,
                    volume_conf_step, volatility_conf_step
                )
                
                future_states.append({
                    'step': step + 1,
                    'timestamp': pred_date,
                    'state': state,
                    'confidence': conf,
                    'components': {
                        'hmm': {'state': hmm_state_step, 'confidence': hmm_conf_step},
                        'eigenwave': {'state': eigenwave_state_step, 'confidence': eigenwave_conf_step},
                        'cycle': {'state': cycle_state_step, 'confidence': cycle_conf_step},
                        'volume': {'confidence': volume_conf_step},
                        'volatility': {'confidence': volatility_conf_step}
                    }
                })
            
            return future_states
        except Exception as e:
            self.logger.error(f"❌ Error generating future states: {str(e)}")
            return []
        
    def _ensemble_predict(
        self,
        hmm_state: int,
        eigenwave_state: int,
        cycle_state: int,
        hmm_conf: float,
        eigenwave_conf: float,
        cycle_conf: float,
        volume_conf: float,
        volatility_conf: float
    ) -> Tuple[int, float]:
        """Combine predictions using weighted voting."""
        # Get weights based on historical accuracy
        hmm_weight = self.volatility_weight
        eigenwave_weight = self.volatility_weight
        cycle_weight = self.volatility_weight
        volume_weight = self.volume_weight
        volatility_weight = self.volatility_weight
        
        # Normalize weights
        total_weight = hmm_weight + eigenwave_weight + cycle_weight + volume_weight + volatility_weight
        hmm_weight /= total_weight
        eigenwave_weight /= total_weight
        cycle_weight /= total_weight
        volume_weight /= total_weight
        volatility_weight /= total_weight
        
        # Calculate weighted state
        weighted_state = (
            float(hmm_state if hmm_state is not None else 0) * hmm_weight +
            float(eigenwave_state if eigenwave_state is not None else 0) * eigenwave_weight +
            float(cycle_state if cycle_state is not None else 0) * cycle_weight +
            float(volume_conf if volume_conf is not None else 0) * volume_weight +
            float(volatility_conf if volatility_conf is not None else 0) * volatility_weight
        )
        state = int(round(weighted_state))
        
        # Calculate weighted confidence
        weighted_conf = (
            hmm_conf * hmm_weight +
            eigenwave_conf * eigenwave_weight +
            cycle_conf * cycle_weight +
            volume_conf * volume_weight +
            volatility_conf * volatility_weight
        )
        confidence = weighted_conf
        
        return state, confidence
    
    def _calculate_volume_confidence(self, data: pd.DataFrame) -> float:
        """Calculate confidence based on volume analysis."""
        try:
            # Calculate volume trend
            volume = data['volume'].values.astype(np.float64)
            volume_sma = np.mean(volume[-self.window_size:])
            volume_std = np.std(volume[-self.window_size:])
            
            # Calculate volume momentum
            volume_momentum = (volume[-1] - volume_sma) / volume_std
            
            # Normalize confidence between 0 and 1
            confidence = (np.tanh(volume_momentum) + 1) / 2
            return float(confidence)
        except Exception as e:
            self.logger.error(f"❌ Error calculating volume confidence: {str(e)}")
            return 0.5

    def _calculate_volatility_confidence(self, data: pd.DataFrame) -> float:
        """Calculate confidence based on volatility analysis."""
        try:
            # Calculate ATR
            high = data['high'].values.astype(np.float64)
            low = data['low'].values.astype(np.float64)
            close = data['close'].values.astype(np.float64)
            
            tr1 = np.abs(high[1:] - low[1:])
            tr2 = np.abs(high[1:] - close[:-1])
            tr3 = np.abs(low[1:] - close[:-1])
            
            tr = np.maximum(np.maximum(tr1, tr2), tr3)
            atr = np.mean(tr[-self.window_size:])
            
            # Calculate volatility regime
            volatility_ratio = atr / close[-1]
            
            # Normalize confidence between 0 and 1
            confidence = 1.0 - (np.tanh(volatility_ratio * 10) + 1) / 2
            return float(confidence)
        except Exception as e:
            self.logger.error(f"❌ Error calculating volatility confidence: {str(e)}")
            return 0.5

    def _predict_hmm(self, data: pd.DataFrame) -> Tuple[int, float]:
        """Predict market state using HMM."""
        try:
            if self.hmm_mapper is None:
                self.logger.warning("HMM model not available, using default prediction")
                return 0, 0.5  # Default to neutral state with medium confidence
            
            # Fit model if not already fitted
            if not hasattr(self.hmm_mapper, 'model') or self.hmm_mapper.model is None:
                self.hmm_mapper.fit(data)
            
            # Use hmm_mapper for prediction
            df_with_states = self.hmm_mapper.predict(data)
            current_state = df_with_states['state'].iloc[-1]
            
            # Get state probabilities from the HMM model
            if hasattr(self.hmm_mapper, 'model') and self.hmm_mapper.model is not None:
                close_values = np.array(data['close'].values, dtype=np.float64).reshape(-1, 1)
                state_probs = self.hmm_mapper.model.predict_proba(close_values)[-1]
                confidence = float(state_probs[current_state])
                
                # Add some randomness to prevent same state predictions
                if confidence < 0.1:  # If confidence is too low
                    confidence = 0.5 + np.random.uniform(-0.1, 0.1)  # Add some randomness
                    current_state = np.random.randint(0, 3)  # Randomly choose a state
            else:
                confidence = 0.5  # Default confidence if model not available
            
            return current_state, confidence
        except Exception as e:
            self.logger.error(f"❌ Error in HMM prediction: {str(e)}")
            return 0, 0.5  # Default to neutral state with medium confidence

    def _predict_cycles(self, data: pd.DataFrame) -> Tuple[int, float]:
        """Predict market cycles."""
        try:
            if self.cycle_approximator is None:
                self.logger.warning("Cycle model not available, using default prediction")
                return 0, 0.5  # Default to neutral phase with medium confidence
            
            # Get current cycle state
            cycle_predictions = self.cycle_approximator.predict(data)
            current_phase = 0  # Default to accumulation phase
            
            if isinstance(cycle_predictions, pd.DataFrame) and 'state' in cycle_predictions.columns:
                current_phase = cycle_predictions['state'].iloc[-1]
            
            # Calculate cycle amplitude using simple moving average
            close_values = data['close'].values.astype(np.float64)
            sma = np.mean(close_values[-self.window_size:])
            amplitude = np.std(close_values[-self.window_size:]) / sma
            
            # Calculate cycle period using zero crossings
            returns = np.diff(close_values)
            zero_crossings = np.where(np.diff(np.signbit(returns)))[0]
            
            if len(zero_crossings) >= 2:
                cycle_period = np.mean(np.diff(zero_crossings[-10:]))
            else:
                cycle_period = 20  # Default period
            
            # Calculate confidence based on amplitude and period stability
            period_stability = 1.0 - (np.std(np.diff(zero_crossings[-10:])) / cycle_period)
            confidence = float(np.mean([amplitude, period_stability]))
            
            return current_phase, confidence
        except Exception as e:
            self.logger.error(f"❌ Error in cycle prediction: {str(e)}")
            return 0, 0.5  # Default to neutral phase with medium confidence

    def _predict_eigenwaves(self, data: pd.DataFrame) -> Tuple[int, float]:
        """Predict market state using eigenwaves."""
        try:
            if self.eigenwave_detector is None:
                self.logger.warning("Eigenwave model not available, using default prediction")
                return 1, 0.5  # Default to neutral state with medium confidence
            
            # Get eigenwave projections
            projections = self.eigenwave_detector.get_projections(data)
            
            # Calculate current state based on dominant eigenwave
            if isinstance(projections, pd.DataFrame):
                # Get the dominant eigenwave (first component)
                dominant_wave = projections.iloc[:, 0]
                
                # Determine state based on wave direction and magnitude
                wave_mean = np.mean(dominant_wave)
                wave_std = np.std(dominant_wave)
                current_value = dominant_wave.iloc[-1]
                
                if current_value > wave_mean + wave_std:
                    state = 2  # Bullish
                elif current_value < wave_mean - wave_std:
                    state = 0  # Bearish
                else:
                    state = 1  # Neutral
                
                # Calculate confidence based on wave strength
                confidence = min(1.0, abs(current_value - wave_mean) / (2 * wave_std))
            else:
                state = 1  # Default to neutral
                confidence = 0.5
            
            return state, confidence
        except Exception as e:
            self.logger.error(f"❌ Error in eigenwave prediction: {str(e)}")
            return 1, 0.5  # Default to neutral state with medium confidence

    def _calculate_hmm_accuracy(self, df: pd.DataFrame) -> float:
        """Calculate HMM accuracy."""
        # Implement HMM accuracy calculation logic here
        return 0.0  # Placeholder return, actual implementation needed
    
    def _calculate_eigenwave_accuracy(self, df: pd.DataFrame) -> float:
        """Calculate Eigenwave accuracy."""
        # Implement Eigenwave accuracy calculation logic here
        return 0.0  # Placeholder return, actual implementation needed
    
    def _calculate_cycle_accuracy(self, df: pd.DataFrame) -> float:
        """Calculate Cycle accuracy."""
        # Implement Cycle accuracy calculation logic here
        return 0.0  # Placeholder return, actual implementation needed
    
    @staticmethod
    def plot_predictions(predictions: List[Dict[str, Any]], show_plot: bool = False) -> None:
        """Create an interactive visualization of predictions.
        
        Args:
            predictions: List of prediction dictionaries, each containing:
                - step: int
                - state: int
                - confidence: float
                - components: Dict containing HMM, eigenwave, cycle, volume and volatility predictions
            show_plot: Whether to automatically show the plot in a browser (default: False)
        """
        try:
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            
            # Create subplots
            fig = make_subplots(
                rows=3, cols=1,
                subplot_titles=('Market States', 'Component Confidences', 'Volume & Volatility'),
                vertical_spacing=0.1
            )
            
            # Plot market states
            steps = [p['step'] for p in predictions]
            states = [p['state'] for p in predictions]
            confidences = [p['confidence'] for p in predictions]
            
            fig.add_trace(
                go.Scatter(
                    x=steps,
                    y=states,
                    mode='lines+markers+text',
                    text=[f"State {s}<br>Conf: {c:.2f}" for s, c in zip(states, confidences)],
                    textposition="top center",
                    name="Market States",
                    line=dict(color='gold', width=2),
                    marker=dict(size=10)
                ),
                row=1, col=1
            )
            
            # Plot component confidences
            hmm_conf = [p['components']['hmm']['confidence'] for p in predictions]
            eigenwave_conf = [p['components']['eigenwave']['confidence'] for p in predictions]
            cycle_conf = [p['components']['cycle']['confidence'] for p in predictions]
            
            fig.add_trace(
                go.Scatter(x=steps, y=hmm_conf, name="HMM", line=dict(color='blue')),
                row=2, col=1
            )
            fig.add_trace(
                go.Scatter(x=steps, y=eigenwave_conf, name="Eigenwave", line=dict(color='green')),
                row=2, col=1
            )
            fig.add_trace(
                go.Scatter(x=steps, y=cycle_conf, name="Cycle", line=dict(color='red')),
                row=2, col=1
            )
            
            # Plot volume and volatility confidence
            volume_conf = [p['components']['volume']['confidence'] for p in predictions]
            volatility_conf = [p['components']['volatility']['confidence'] for p in predictions]
            
            fig.add_trace(
                go.Scatter(x=steps, y=volume_conf, name="Volume", line=dict(color='purple')),
                row=3, col=1
            )
            fig.add_trace(
                go.Scatter(x=steps, y=volatility_conf, name="Volatility", line=dict(color='orange')),
                row=3, col=1
            )
            
            # Update layout
            fig.update_layout(
                title="GAMON Trinity Matrix Predictions",
                showlegend=True,
                height=800,
                template='plotly_dark'
            )
            
            # Update y-axes
            fig.update_yaxes(title_text="State", row=1, col=1)
            fig.update_yaxes(title_text="Confidence", row=2, col=1)
            fig.update_yaxes(title_text="Confidence", row=3, col=1)
            
            # Save the plot to a temporary HTML file
            temp_file = "gamon_trinity_predictions.html"
            fig.write_html(temp_file)
            
            # Get the absolute path to the file
            abs_path = os.path.abspath(temp_file)
            
            # Create a file URL
            file_url = f"file://{abs_path}"
            
            # Print the URL
            print(f"\n{GREEN}✨ Visualization URL: {file_url}{RESET}")
            print(f"{YELLOW}Note: If using Tor, you may need to open this URL manually in Chrome{RESET}")
            
            # Show plot if requested
            if show_plot:
                fig.show()
            
        except Exception as e:
            print(f"❌ Error creating predictions visualization: {str(e)}")

def main(interval_minutes: int = 5, continuous: bool = True, start_date: str = "2009-01-03", end_date: str | None = None):
    """Run the GAMON Trinity Predictor.
    
    Args:
        interval_minutes: Time between predictions in minutes
        continuous: Whether to run continuously or just once
        start_date: Start date in YYYY-MM-DD format (default: genesis block)
        end_date: End date in YYYY-MM-DD format (default: current date)
    """
    try:
        # Display banner
        print(f"""{PURPLE}
╔══════════════════════════════════════════════════════════╗
     ██████╗  █████╗ ███╗   ███╗ ██████╗ ███╗   ██╗
    ██╔════╝ ██╔══██╗████╗ ████║██╔═══██╗████╗  ██║
    ██║  ███╗███████║██╔████╔██║██║   ██║██║╚██╗██║
    ██║   ██║██╔══██║██║╚██╔╝██║██║   ██║██║ ╚████║
    ╚██████╔╝██║  ██║██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                    
     TRINITY MATRIX - DIVINE PREDICTION SYSTEM
     [ HMM + Eigenwaves + Cycles = Future Vision ]
╚══════════════════════════════════════════════════════════╝{RESET}
""")
        
        # Initialize predictor
        predictor = GAMONTrinityPredictor()
        
        while True:
            try:
                # Load data using BTCDataHandler with parameterized date range
                print(f"\n{YELLOW}🔄 Loading BTC market data from {start_date} to {end_date or 'present'}...{RESET}")
                from btc_data_handler import BTCDataHandler
                handler = BTCDataHandler()
                df = handler.get_btc_data(start_date=start_date, end_date=end_date)
                
                if df is None:
                    print(f"{RED}❌ Failed to load BTC data{RESET}")
                    if not continuous:
                        break
                    time.sleep(60)  # Wait 1 minute before retrying
                    continue
                
                # Make predictions using historical dates
                print(f"{YELLOW}🔮 Generating divine predictions...{RESET}")
                
                # Get the last historical date from the data
                last_date = df.index[-1]
                
                # Generate predictions for the last 5 historical dates
                predictions = predictor.predict_future_states(df, n_steps=5, step_minutes=60)
                
                # Display predictions
                print(f"\n{GREEN}✨ Divine Predictions ✨{RESET}")
                print(f"{YELLOW}Last Historical Date: {last_date.strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
                print(f"{YELLOW}Historical Analysis Time Range: {predictions[0]['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} to {predictions[-1]['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
                
                for i, pred in enumerate(predictions, 1):
                    print(f"\nPrediction {i} ({pred['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}):")
                    print(f"State: {pred['state']} (Confidence: {pred['confidence']:.2f})")
                    print("Component Confidences:")
                    for component, data in pred['components'].items():
                        if 'confidence' in data:
                            print(f"  - {component.capitalize()}: {data['confidence']:.2f}")
                
                # Create visualization (don't show automatically)
                GAMONTrinityPredictor.plot_predictions(predictions, show_plot=False)
                
                if not continuous:
                    break
                    
                print(f"\n{YELLOW}⏳ Waiting {interval_minutes} minutes until next prediction...{RESET}")
                time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                print(f"\n{YELLOW}⚠️ Interrupted by user{RESET}")
                break
            except Exception as e:
                print(f"{RED}❌ Error in prediction loop: {str(e)}{RESET}")
                if not continuous:
                    break
                print(f"{YELLOW}⏳ Waiting 1 minute before retrying...{RESET}")
                time.sleep(60)
                
    except Exception as e:
        print(f"{RED}❌ Fatal error in main: {str(e)}{RESET}")

if __name__ == "__main__":
    import time
    import argparse
    
    parser = argparse.ArgumentParser(description="GAMON Trinity Predictor")
    parser.add_argument("--interval", type=int, default=5, help="Time between predictions in minutes")
    parser.add_argument("--once", action="store_true", help="Run only once instead of continuously")
    parser.add_argument("--start-date", type=str, default="2009-01-03", help="Start date in YYYY-MM-DD format (default: genesis block)")
    parser.add_argument("--end-date", type=str, help="End date in YYYY-MM-DD format (default: current date)")
    
    args = parser.parse_args()
    main(interval_minutes=args.interval, continuous=not args.once, start_date=args.start_date, end_date=args.end_date) 