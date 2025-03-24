#!/usr/bin/env python3
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
from typing import Dict, List, Tuple, Optional
import warnings
import logging
from scipy import signal

# Import our GAMON Trinity Matrix components
from hmm_btc_state_mapper import HMMBTCStateMapper, load_btc_data
from power_method_btc_eigenwaves import PowerMethodBTCEigenwaves
from variational_inference_btc_cycle import VariationalInferenceBTCCycle

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
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
    
    def __init__(self):
        """Initialize the GAMON Trinity Predictor."""
        self.hmm_mapper = HMMBTCStateMapper()
        self.eigenwave_detector = PowerMethodBTCEigenwaves()
        self.cycle_approximator = VariationalInferenceBTCCycle()
        self.df = None  # Store the current DataFrame
        
        # Load models if they exist
        self._load_models()
        
    def _load_models(self):
        """Load pre-trained models if they exist."""
        try:
            self.hmm_mapper.load_model("models/hmm_btc_state_mapper.pkl")
            logger.info(f"{GREEN}✅ Loaded HMM model{RESET}")
        except Exception as e:
            logger.warning(f"{YELLOW}⚠️ Could not load HMM model: {e}{RESET}")
            
        try:
            self.eigenwave_detector.load_model("models/power_method_btc_eigenwaves.pkl")
            logger.info(f"{GREEN}✅ Loaded Eigenwave model{RESET}")
        except Exception as e:
            logger.warning(f"{YELLOW}⚠️ Could not load Eigenwave model: {e}{RESET}")
            
        try:
            self.cycle_approximator.load_model("models/variational_inference_btc_cycle.pkl")
            logger.info(f"{GREEN}✅ Loaded Cycle model{RESET}")
        except Exception as e:
            logger.warning(f"{YELLOW}⚠️ Could not load Cycle model: {e}{RESET}")
    
    def _ensemble_predict(self, predictions: Dict, historical_metrics: Dict) -> Dict:
        """Combine predictions using ensemble methods with weighted voting."""
        try:
            # Get weights from historical accuracy
            hmm_weight = historical_metrics['hmm']['accuracy']
            cycle_weight = historical_metrics['cycles']['accuracy']
            eigenwave_weight = historical_metrics['eigenwaves']['coverage']
            
            # Normalize weights
            total_weight = hmm_weight + cycle_weight + eigenwave_weight
            hmm_weight /= total_weight
            cycle_weight /= total_weight
            eigenwave_weight /= total_weight
            
            # Initialize ensemble predictions
            ensemble_predictions = []
            
            # Combine predictions for each step
            for i in range(len(predictions['hmm'])):
                # Get individual predictions
                hmm_pred = predictions['hmm'][i]
                cycle_pred = predictions['cycles'][i]
                
                # Map HMM state to cycle phase (0-3)
                hmm_phase = hmm_pred['state'] % 4
                cycle_phase = cycle_pred['phase']
                
                # Calculate weighted phase prediction
                weighted_phase = int(round(
                    hmm_phase * hmm_weight +
                    cycle_phase * cycle_weight
                )) % 4
                
                # Get phase name
                phase_names = ['Accumulation', 'Markup', 'Distribution', 'Markdown']
                phase_name = phase_names[weighted_phase]
                
                # Calculate ensemble confidence
                hmm_conf = hmm_pred['probability']
                cycle_conf = 1.0 if cycle_pred['confidence'] == 'high' else 0.7
                
                # Weight confidences
                ensemble_conf = (
                    hmm_conf * hmm_weight +
                    cycle_conf * cycle_weight
                )
                
                # Determine confidence level
                if ensemble_conf > 0.8:
                    confidence = 'high'
                elif ensemble_conf > 0.6:
                    confidence = 'medium'
                else:
                    confidence = 'low'
                
                # Get eigenwave contribution
                eigenwave_data = predictions['eigenwaves'][i]['projections']
                wave_strength = np.mean([abs(data['value']) for data in eigenwave_data.values()])
                
                # Create ensemble prediction
                ensemble_pred = {
                    'step': i + 1,
                    'phase': weighted_phase,
                    'phase_name': phase_name,
                    'confidence': confidence,
                    'ensemble_confidence': float(ensemble_conf),
                    'wave_strength': float(wave_strength),
                    'contributions': {
                        'hmm': {
                            'phase': hmm_phase,
                            'weight': float(hmm_weight),
                            'confidence': float(hmm_conf)
                        },
                        'cycle': {
                            'phase': cycle_phase,
                            'weight': float(cycle_weight),
                            'confidence': float(cycle_conf)
                        },
                        'eigenwave': {
                            'strength': float(wave_strength),
                            'weight': float(eigenwave_weight)
                        }
                    }
                }
                
                ensemble_predictions.append(ensemble_pred)
            
            return {
                'ensemble': ensemble_predictions,
                'weights': {
                    'hmm': float(hmm_weight),
                    'cycle': float(cycle_weight),
                    'eigenwave': float(eigenwave_weight)
                }
            }
            
        except Exception as e:
            logger.error(f"{RED}❌ Error in ensemble prediction: {e}{RESET}")
            return {}

    def predict_future_states(self, df: pd.DataFrame, n_steps: int = 5) -> Dict:
        """Predict future market states using all three methods."""
        try:
            # Store the DataFrame
            if df is not None:
                self.df = df.copy()
            else:
                logger.error(f"{RED}❌ Input DataFrame is None{RESET}")
                return {}
            
            # Get individual predictions
            predictions = {
                'hmm': self._predict_hmm_states(df, n_steps),
                'eigenwaves': self._predict_eigenwaves(df, n_steps),
                'cycles': self._predict_cycles(df, n_steps),
                'timestamp': datetime.now().isoformat()
            }
            
            # Calculate historical accuracy
            historical_metrics = self._calculate_historical_accuracy(df)
            
            # Generate ensemble predictions
            ensemble_results = self._ensemble_predict(predictions, historical_metrics)
            
            # Add ensemble results to predictions
            predictions.update(ensemble_results)
            
            # Calculate divine alignment score
            predictions['divine_alignment'] = self._calculate_divine_alignment(predictions)
            
            return predictions
            
        except Exception as e:
            logger.error(f"{RED}❌ Error in prediction: {e}{RESET}")
            return {}
    
    def _predict_hmm_states(self, df: pd.DataFrame, n_steps: int) -> List[Dict]:
        """Predict future states using HMM with confidence intervals."""
        try:
            # Check if model is fitted
            if not hasattr(self.hmm_mapper.model, 'transmat_') or getattr(self.hmm_mapper.model, 'transmat_', None) is None:
                logger.info(f"{YELLOW}⚠️ HMM model not fitted. Fitting model first...{RESET}")
                self.hmm_mapper.fit(df)
            
            # Get current state and transition matrix
            df_with_states = self.hmm_mapper.predict(df)
            current_state = df_with_states['state'].iloc[-1]
            
            # Ensure transition matrix exists
            transition_matrix = getattr(self.hmm_mapper.model, 'transmat_', None)
            if transition_matrix is None:
                logger.error(f"{RED}❌ HMM model transition matrix not available{RESET}")
                return []
                
            # Predict next n states with confidence intervals
            future_states = []
            current_state_idx = current_state
            confidence_threshold = 0.6  # Minimum confidence to consider a prediction
            
            for step in range(n_steps):
                # Get transition probabilities
                probs = transition_matrix[current_state_idx]
                
                # Find top 2 most likely states
                top_states = np.argsort(probs)[-2:][::-1]
                top_probs = probs[top_states]
                
                # Only include predictions with sufficient confidence
                if top_probs[0] >= confidence_threshold:
                    future_states.append({
                        'state': int(top_states[0]),
                        'probability': float(top_probs[0]),
                        'state_name': self.hmm_mapper.interpret_states(df_with_states)[top_states[0]],
                        'confidence': 'high' if top_probs[0] > 0.8 else 'medium',
                        'alternative_state': int(top_states[1]) if top_probs[1] > confidence_threshold else None,
                        'alternative_probability': float(top_probs[1]) if top_probs[1] > confidence_threshold else None
                    })
                else:
                    future_states.append({
                        'state': int(top_states[0]),
                        'probability': float(top_probs[0]),
                        'state_name': self.hmm_mapper.interpret_states(df_with_states)[top_states[0]],
                        'confidence': 'low',
                        'alternative_state': None,
                        'alternative_probability': None
                    })
                
                current_state_idx = top_states[0]
            
            return future_states
            
        except Exception as e:
            logger.error(f"{RED}❌ Error in HMM prediction: {e}{RESET}")
            return []
    
    def _predict_eigenwaves(self, df: pd.DataFrame, n_steps: int) -> List[Dict]:
        """Predict future eigenwave projections using ARIMA."""
        try:
            from statsmodels.tsa.arima.model import ARIMA
            
            # Get current eigenwave projections
            projections = self.eigenwave_detector.get_projections(df)
            
            # Predict future projections using ARIMA
            future_projections = []
            for i in range(n_steps):
                wave_predictions = {}
                
                # Fit ARIMA model for each eigenwave
                for wave in projections.columns:
                    # Fit ARIMA(1,1,1) model
                    model = ARIMA(projections[wave], order=(1,1,1))
                    results = model.fit()
                    
                    # Get forecast with confidence intervals
                    forecast = results.forecast(steps=1)
                    conf_int = results.get_forecast(steps=1).conf_int()
                    
                    wave_predictions[wave] = {
                        'value': float(forecast.iloc[0]),
                        'lower_bound': float(conf_int.iloc[0, 0]),
                        'upper_bound': float(conf_int.iloc[0, 1])
                    }
                
                future_projections.append({
                    'step': i + 1,
                    'projections': wave_predictions
                })
            
            return future_projections
            
        except Exception as e:
            logger.error(f"{RED}❌ Error in Eigenwave prediction: {e}{RESET}")
            return []
    
    def _predict_cycles(self, df: pd.DataFrame, n_steps: int) -> List[Dict]:
        """Predict future market cycles with amplitude and phase."""
        try:
            # Get current cycle state
            cycle_state = self.cycle_approximator.predict(df)
            
            # Calculate cycle amplitude using Hilbert transform
            close_values = df['close'].values
            if not isinstance(close_values, np.ndarray):
                close_values = np.array(close_values, dtype=np.float64)
            else:
                close_values = close_values.astype(np.float64)
            
            # Apply Hilbert transform
            try:
                analytic_signal = signal.hilbert(close_values.reshape(-1))
                amplitude_envelope = np.abs(analytic_signal)
            except Exception as e:
                logger.error(f"{RED}❌ Error in Hilbert transform: {e}{RESET}")
                return []
            
            # Calculate cycle period using autocorrelation
            try:
                autocorr = signal.correlate(close_values.reshape(-1), close_values.reshape(-1))
                peaks = signal.find_peaks(autocorr)[0]
                cycle_period = peaks[0] if len(peaks) > 0 else 20  # Default period
            except Exception as e:
                logger.error(f"{RED}❌ Error in cycle period calculation: {e}{RESET}")
                cycle_period = 20  # Default period
            
            # Predict future cycles with amplitude
            future_cycles = []
            current_phase = cycle_state
            
            for i in range(n_steps):
                # Calculate phase progression
                phase_progress = (i / cycle_period) * 2 * np.pi
                next_phase = (current_phase + phase_progress) % 4
                
                # Estimate amplitude for this phase
                phase_amplitude = amplitude_envelope[-1] * (1 + 0.1 * np.sin(phase_progress))
                
                future_cycles.append({
                    'step': i + 1,
                    'phase': int(next_phase),
                    'phase_name': ['Accumulation', 'Markup', 'Distribution', 'Markdown'][int(next_phase)],
                    'amplitude': float(phase_amplitude),
                    'confidence': 'high' if phase_amplitude > amplitude_envelope.mean() else 'medium'
                })
            
            return future_cycles
            
        except Exception as e:
            logger.error(f"{RED}❌ Error in Cycle prediction: {e}{RESET}")
            return []
    
    def _calculate_historical_accuracy(self, df: pd.DataFrame, window_size: int = 30) -> Dict:
        """Calculate historical accuracy metrics for each prediction method."""
        try:
            # Ensure df is not None and has enough data
            if df is None or len(df) <= window_size:
                logger.warning(f"{YELLOW}⚠️ Not enough data for historical accuracy calculation{RESET}")
                return {
                    'hmm': {'accuracy': 0.5, 'avg_confidence': 0.5},
                    'eigenwaves': {'rmse': 0.5, 'coverage': 0.5},
                    'cycles': {'accuracy': 0.5, 'avg_amplitude_error': 0.5}
                }
            
            metrics = {
                'hmm': {'accuracy': [], 'confidence': []},
                'eigenwaves': {'rmse': [], 'coverage': []},
                'cycles': {'accuracy': [], 'amplitude_error': []}
            }
            
            # Use sliding window for historical accuracy
            for i in range(len(df) - window_size):
                train_data = df.iloc[i:i+window_size].copy()
                actual_data = df.iloc[i+window_size:i+window_size+1].copy()
                
                # Ensure data is properly formatted
                required_columns = ['close', 'high', 'low', 'open', 'volume']
                if not all(col in train_data.columns for col in required_columns):
                    logger.warning(f"{YELLOW}⚠️ Missing required columns in training data{RESET}")
                    continue
                    
                if not all(col in actual_data.columns for col in required_columns):
                    logger.warning(f"{YELLOW}⚠️ Missing required columns in actual data{RESET}")
                    continue
                
                train_data = train_data[required_columns]
                actual_data = actual_data[required_columns]
                
                # HMM accuracy
                transition_matrix = getattr(self.hmm_mapper.model, 'transmat_', None)
                if transition_matrix is not None:
                    try:
                        hmm_states = self.hmm_mapper.predict(train_data)
                        actual_state = self.hmm_mapper.predict(actual_data)['state'].iloc[0]
                        predicted_state = hmm_states['state'].iloc[-1]
                        metrics['hmm']['accuracy'].append(1 if actual_state == predicted_state else 0)
                        metrics['hmm']['confidence'].append(
                            float(transition_matrix[predicted_state][actual_state])
                        )
                    except Exception as e:
                        logger.warning(f"{YELLOW}⚠️ Error in HMM accuracy calculation: {e}{RESET}")
                
                # Eigenwave accuracy
                try:
                    train_proj = self.eigenwave_detector.get_projections(train_data)
                    actual_proj = self.eigenwave_detector.get_projections(actual_data)
                    
                    if train_proj is not None and actual_proj is not None:
                        for wave in train_proj.columns:
                            rmse = np.sqrt(np.mean((train_proj[wave].iloc[-1] - actual_proj[wave].iloc[0])**2))
                            metrics['eigenwaves']['rmse'].append(rmse)
                            # Check if actual value is within prediction bounds
                            bounds = self._predict_eigenwaves(train_data, 1)[0]['projections'][wave]
                            coverage = 1 if bounds['lower_bound'] <= actual_proj[wave].iloc[0] <= bounds['upper_bound'] else 0
                            metrics['eigenwaves']['coverage'].append(coverage)
                except Exception as e:
                    logger.warning(f"{YELLOW}⚠️ Error in eigenwave accuracy calculation: {e}{RESET}")
                
                # Cycle accuracy
                try:
                    train_phase = self.cycle_approximator.predict(train_data)
                    actual_phase = self.cycle_approximator.predict(actual_data)
                    
                    if train_phase is not None and actual_phase is not None:
                        metrics['cycles']['accuracy'].append(1 if train_phase == actual_phase else 0)
                        
                        # Calculate amplitude error
                        train_values = train_data['close'].values
                        actual_values = actual_data['close'].values
                        
                        if not isinstance(train_values, np.ndarray):
                            train_values = np.array(train_values)
                        if not isinstance(actual_values, np.ndarray):
                            actual_values = np.array(actual_values)
                            
                        train_values = train_values.astype(np.float64)
                        actual_values = actual_values.astype(np.float64)
                        
                        if len(train_values) > 0 and len(actual_values) > 0:
                            train_amp = np.abs(signal.hilbert(train_values))[-1]
                            actual_amp = np.abs(signal.hilbert(actual_values))[0]
                            metrics['cycles']['amplitude_error'].append(abs(train_amp - actual_amp))
                except Exception as e:
                    logger.warning(f"{YELLOW}⚠️ Error in cycle accuracy calculation: {e}{RESET}")
            
            # Calculate final metrics with fallbacks
            return {
                'hmm': {
                    'accuracy': float(np.mean(metrics['hmm']['accuracy'])) if metrics['hmm']['accuracy'] else 0.5,
                    'avg_confidence': float(np.mean(metrics['hmm']['confidence'])) if metrics['hmm']['confidence'] else 0.5
                },
                'eigenwaves': {
                    'rmse': float(np.mean(metrics['eigenwaves']['rmse'])) if metrics['eigenwaves']['rmse'] else 0.5,
                    'coverage': float(np.mean(metrics['eigenwaves']['coverage'])) if metrics['eigenwaves']['coverage'] else 0.5
                },
                'cycles': {
                    'accuracy': float(np.mean(metrics['cycles']['accuracy'])) if metrics['cycles']['accuracy'] else 0.5,
                    'avg_amplitude_error': float(np.mean(metrics['cycles']['amplitude_error'])) if metrics['cycles']['amplitude_error'] else 0.5
                }
            }
            
        except Exception as e:
            logger.error(f"{RED}❌ Error calculating historical accuracy: {e}{RESET}")
            return {
                'hmm': {'accuracy': 0.5, 'avg_confidence': 0.5},
                'eigenwaves': {'rmse': 0.5, 'coverage': 0.5},
                'cycles': {'accuracy': 0.5, 'avg_amplitude_error': 0.5}
            }
    
    def _calculate_divine_alignment(self, predictions: Dict) -> float:
        """Calculate the divine alignment score between predictions."""
        try:
            # Get historical accuracy metrics
            historical_metrics = self._calculate_historical_accuracy(self.df)
            
            # Get states from each method
            hmm_states = [p['state'] for p in predictions['hmm']]
            cycle_phases = [p['phase'] for p in predictions['cycles']]
            
            alignment_scores = []
            for i in range(len(hmm_states)):
                # Map HMM states to cycle phases (0-3)
                hmm_phase = hmm_states[i] % 4
                cycle_phase = cycle_phases[i]
                
                # Calculate phase alignment (0-1)
                phase_diff = abs(hmm_phase - cycle_phase)
                phase_alignment = 1 - (phase_diff / 4)
                
                # Weight by HMM prediction confidence and historical accuracy
                hmm_conf = predictions['hmm'][i]['probability']
                hmm_accuracy = historical_metrics.get('hmm', {}).get('accuracy', 0.5)
                cycle_accuracy = historical_metrics.get('cycles', {}).get('accuracy', 0.5)
                
                # Calculate weighted alignment score
                weighted_alignment = phase_alignment * hmm_conf * (hmm_accuracy + cycle_accuracy) / 2
                alignment_scores.append(weighted_alignment)
            
            # Add eigenwave contribution to alignment
            eigenwave_metrics = historical_metrics.get('eigenwaves', {})
            eigenwave_score = eigenwave_metrics.get('coverage', 0.5) * (1 - eigenwave_metrics.get('rmse', 0.5))
            
            # Combine all scores
            final_score = (np.mean(alignment_scores) + eigenwave_score) / 2
            return float(final_score)
            
        except Exception as e:
            logger.error(f"{RED}❌ Error calculating divine alignment: {e}{RESET}")
            return 0.0
    
    def plot_predictions(self, predictions: Dict, output_file: str = "plots/gamon_trinity_predictions.html"):
        """Create an interactive visualization of the predictions."""
        try:
            # Get historical accuracy metrics
            if self.df is not None:
                historical_metrics = self._calculate_historical_accuracy(self.df)
            else:
                historical_metrics = {
                    'hmm': {'accuracy': 0.5, 'avg_confidence': 0.5},
                    'eigenwaves': {'rmse': 0.5, 'coverage': 0.5},
                    'cycles': {'accuracy': 0.5, 'avg_amplitude_error': 0.5}
                }
            
            # Create figure with subplots
            fig = make_subplots(
                rows=5, cols=1,
                subplot_titles=[
                    "HMM State Predictions",
                    "Eigenwave Projections",
                    "Market Cycle Predictions",
                    "Historical Accuracy Metrics",
                    "Ensemble Predictions"
                ],
                vertical_spacing=0.1
            )
            
            # Plot HMM predictions with confidence
            if predictions['hmm']:
                states = [p['state'] for p in predictions['hmm']]
                probs = [p['probability'] for p in predictions['hmm']]
                names = [p['state_name'] for p in predictions['hmm']]
                confidences = [p['confidence'] for p in predictions['hmm']]
                
                # Add main state predictions
                fig.add_trace(
                    go.Scatter(
                        x=list(range(len(states))),
                        y=states,
                        mode='lines+markers+text',
                        text=[f"{name}<br>Conf: {conf}" for name, conf in zip(names, confidences)],
                        textposition="top center",
                        name="HMM States",
                        line=dict(color='gold', width=2),
                        marker=dict(size=10)
                    ),
                    row=1, col=1
                )
                
                # Add alternative states if available
                alt_states = [p['alternative_state'] for p in predictions['hmm'] if p['alternative_state'] is not None]
                if alt_states:
                    fig.add_trace(
                        go.Scatter(
                            x=list(range(len(alt_states))),
                            y=alt_states,
                            mode='markers',
                            name="Alternative States",
                            marker=dict(color='silver', size=8, symbol='diamond')
                        ),
                        row=1, col=1
                    )
            
            # Plot Eigenwave predictions with confidence intervals
            if predictions['eigenwaves']:
                for i, proj in enumerate(predictions['eigenwaves']):
                    for wave, data in proj['projections'].items():
                        # Add main prediction line
                        fig.add_trace(
                            go.Scatter(
                                x=[i],
                                y=[data['value']],
                                mode='lines+markers',
                                name=f"{wave} (Step {i+1})",
                                line=dict(color='blue', width=1)
                            ),
                            row=2, col=1
                        )
                        
                        # Add confidence interval
                        fig.add_trace(
                            go.Scatter(
                                x=[i, i],
                                y=[data['lower_bound'], data['upper_bound']],
                                mode='lines',
                                name=f"{wave} CI (Step {i+1})",
                                line=dict(color='rgba(0,0,255,0.2)', width=1),
                                showlegend=False
                            ),
                            row=2, col=1
                        )
            
            # Plot Cycle predictions with amplitude
            if predictions['cycles']:
                phases = [p['phase'] for p in predictions['cycles']]
                names = [p['phase_name'] for p in predictions['cycles']]
                amplitudes = [p['amplitude'] for p in predictions['cycles']]
                confidences = [p['confidence'] for p in predictions['cycles']]
                
                # Add phase predictions
                fig.add_trace(
                    go.Scatter(
                        x=list(range(len(phases))),
                        y=phases,
                        mode='lines+markers+text',
                        text=[f"{name}<br>Amp: {amp:.2f}<br>Conf: {conf}" 
                              for name, amp, conf in zip(names, amplitudes, confidences)],
                        textposition="top center",
                        name="Cycle Phases",
                        line=dict(color='green', width=2),
                        marker=dict(size=10)
                    ),
                    row=3, col=1
                )
                
                # Add amplitude as a secondary y-axis
                fig.add_trace(
                    go.Scatter(
                        x=list(range(len(amplitudes))),
                        y=amplitudes,
                        mode='lines',
                        name="Cycle Amplitude",
                        line=dict(color='red', width=1, dash='dot'),
                        yaxis='y3'
                    ),
                    row=3, col=1
                )
            
            # Plot Historical Accuracy Metrics
            if historical_metrics:
                metrics = [
                    ('HMM Accuracy', historical_metrics['hmm']['accuracy'], 'gold'),
                    ('Cycle Accuracy', historical_metrics['cycles']['accuracy'], 'green'),
                    ('Eigenwave Coverage', historical_metrics['eigenwaves']['coverage'], 'blue')
                ]
                
                for name, value, color in metrics:
                    fig.add_trace(
                        go.Bar(
                            x=[name],
                            y=[value],
                            name=name,
                            marker_color=color
                        ),
                        row=4, col=1
                    )
            
            # Plot Ensemble Predictions
            if 'ensemble' in predictions:
                ensemble = predictions['ensemble']
                phases = [p['phase'] for p in ensemble]
                names = [p['phase_name'] for p in ensemble]
                confidences = [p['ensemble_confidence'] for p in ensemble]
                wave_strengths = [p['wave_strength'] for p in ensemble]
                
                # Add ensemble phase predictions
                fig.add_trace(
                    go.Scatter(
                        x=list(range(len(phases))),
                        y=phases,
                        mode='lines+markers+text',
                        text=[f"{name}<br>Conf: {conf:.2f}<br>Wave: {wave:.2f}" 
                              for name, conf, wave in zip(names, confidences, wave_strengths)],
                        textposition="top center",
                        name="Ensemble Phases",
                        line=dict(color='purple', width=2),
                        marker=dict(size=10)
                    ),
                    row=5, col=1
                )
                
                # Add wave strength as secondary y-axis
                fig.add_trace(
                    go.Scatter(
                        x=list(range(len(wave_strengths))),
                        y=wave_strengths,
                        mode='lines',
                        name="Wave Strength",
                        line=dict(color='orange', width=1, dash='dot'),
                        yaxis='y4'
                    ),
                    row=5, col=1
                )
            
            # Update layout with secondary y-axes
            fig.update_layout(
                title=f"GAMON Trinity Predictions (Divine Alignment: {predictions['divine_alignment']:.2f})",
                template="plotly_dark",
                height=1500,
                showlegend=True,
                yaxis3=dict(
                    title="Cycle Amplitude",
                    overlaying="y",
                    side="right",
                    showgrid=False
                ),
                yaxis4=dict(
                    title="Wave Strength",
                    overlaying="y",
                    side="right",
                    showgrid=False
                )
            )
            
            # Save figure
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            fig.write_html(output_file)
            logger.info(f"{GREEN}✅ Saved predictions visualization to {output_file}{RESET}")
            
        except Exception as e:
            logger.error(f"{RED}❌ Error creating predictions visualization: {e}{RESET}")

def main():
    """Run the GAMON Trinity Predictor."""
    try:
        # Display banner
        print(f"""{PURPLE}
╔══════════════════════════════════════════════════════════╗
     ██████╗  █████╗ ███╗   ███╗ ██████╗ ███╗   ██╗
    ██╔════╝ ██╔══██╗████╗ ████║██╔═══██╗████╗  ██║
    ██║  ███╗███████║██╔████╔██║██║   ██║██╔██╗ ██║
    ██║   ██║██╔══██║██║╚██╔╝██║██║   ██║██║╚██╗██║
    ╚██████╔╝██║  ██║██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                    
     TRINITY MATRIX - DIVINE PREDICTION SYSTEM
     [ HMM + Eigenwaves + Cycles = Future Vision ]
╚══════════════════════════════════════════════════════════╝{RESET}
""")
        
        # Load data
        print(f"{YELLOW}🔄 Loading BTC market data...{RESET}")
        df = load_btc_data(start_date="2020-01-01")
        
        # Initialize predictor
        predictor = GAMONTrinityPredictor()
        
        # Make predictions
        print(f"{YELLOW}🔮 Generating divine predictions...{RESET}")
        predictions = predictor.predict_future_states(df)
        
        # Display predictions
        print(f"\n{GREEN}✨ Divine Predictions ✨{RESET}")
        print(f"Timestamp: {predictions['timestamp']}")
        print(f"Divine Alignment Score: {predictions['divine_alignment']:.2f}")
        
        print("\nHMM State Predictions:")
        for i, pred in enumerate(predictions['hmm'], 1):
            print(f"Step {i}: {pred['state_name']} (Probability: {pred['probability']:.2f})")
        
        print("\nMarket Cycle Predictions:")
        for i, pred in enumerate(predictions['cycles'], 1):
            print(f"Step {i}: {pred['phase_name']}")
        
        # Create visualization
        predictor.plot_predictions(predictions)
        
    except KeyboardInterrupt:
        print(f"{YELLOW}⚠️ Interrupted by user{RESET}")
    except Exception as e:
        print(f"{RED}❌ Error in main: {e}{RESET}")

if __name__ == "__main__":
    main() 