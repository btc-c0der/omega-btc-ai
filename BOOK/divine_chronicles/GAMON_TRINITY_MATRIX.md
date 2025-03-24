# 🔮 GAMON Trinity Matrix - Divine Market Analysis System

## Overview

The GAMON Trinity Matrix is a sophisticated market analysis system that combines three powerful methods to forecast market states and cycles:

1. **Hidden Markov Model (HMM) State Mapper**
2. **Power Method Eigenwave Detector**
3. **Variational Inference Cycle Approximator**

## Divine Components

### 1. HMM State Mapper

- Identifies six market states:
  - Markup
  - Markdown
  - Accumulation
  - Distribution
  - Liquidity Grab
  - Consolidation
- Provides state transition probabilities
- Includes confidence intervals for predictions
- Historical accuracy tracking

### 2. Power Method Eigenwave Detector

- Extracts dominant market oscillations
- Uses ARIMA for future projections
- Provides confidence intervals
- Calculates wave strength metrics

### 3. Variational Inference Cycle Approximator

- Identifies market phases
- Calculates cycle amplitude
- Uses Hilbert transform for envelope detection
- Provides phase confidence levels

## Divine Alignment Score

The system calculates a Divine Alignment Score (0-1) that measures the harmony between predictions:

```python
divine_alignment = (phase_alignment * hmm_conf * (hmm_accuracy + cycle_accuracy) / 2 + eigenwave_score) / 2
```

Where:

- `phase_alignment`: Agreement between HMM and cycle predictions
- `hmm_conf`: Confidence in HMM state prediction
- `hmm_accuracy`: Historical accuracy of HMM
- `cycle_accuracy`: Historical accuracy of cycle predictions
- `eigenwave_score`: Quality of eigenwave predictions

## Visualization

The system generates an interactive visualization with five panels:

1. **HMM State Predictions**
   - Shows predicted states with confidence levels
   - Displays alternative states when available

2. **Eigenwave Projections**
   - Visualizes wave predictions with confidence intervals
   - Shows multiple eigenwave components

3. **Market Cycle Predictions**
   - Displays phase predictions with amplitude
   - Includes confidence levels for each phase

4. **Historical Accuracy Metrics**
   - Shows accuracy scores for each component
   - Visualizes confidence trends

5. **Ensemble Predictions**
   - Combines all predictions with weighted voting
   - Shows wave strength as secondary metric

## Performance Metrics

### Historical Accuracy Tracking

- **Sliding Window Analysis**
  - 30-day default window
  - Adaptive window size based on volatility
  - Exponential weighting for recent data

- **Component-Specific Metrics**
  - HMM: State prediction accuracy
  - Eigenwaves: Projection RMSE
  - Cycles: Phase detection accuracy
  - Volume: Prediction correlation

- **Cross-Validation**
  - Time-series split validation
  - Rolling window backtesting
  - Out-of-sample performance tracking

### Volume and Volatility Integration

- **Volume-Based Confidence**
  - Volume-weighted state probabilities
  - Volume trend alignment scoring
  - Liquidity impact assessment

- **Volatility-Adjusted Metrics**
  - ATR-based confidence scaling
  - Volatility regime detection
  - Risk-adjusted performance measures

- **Market Regime Analysis**
  - High/Low volatility state detection
  - Volume profile analysis
  - Market depth consideration

### Confidence Assessment

- High: > 0.8
- Medium: 0.6 - 0.8
- Low: < 0.6

## Usage

```python
# Initialize predictor with advanced metrics
predictor = GAMONTrinityPredictor(
    window_size=30,
    volume_weight=0.3,
    volatility_weight=0.2
)

# Load market data with volume
df = load_btc_data(
    start_date="2020-01-01",
    include_volume=True,
    include_volatility=True
)

# Generate predictions with confidence metrics
predictions = predictor.predict_future_states(
    df,
    include_volume=True,
    include_volatility=True
)

# Create visualization with enhanced metrics
predictor.plot_predictions(
    predictions,
    show_volume=True,
    show_volatility=True
)
```

## Future Enhancements

1. **Ensemble Methods**
   - Add more sophisticated aggregation techniques
   - Implement dynamic weight adjustment
   - Include volume-based confidence scaling

2. **Advanced Metrics**
   - Add cross-validation scores
   - Implement backtesting framework
   - Add risk-adjusted performance metrics

3. **Visualization Improvements**
   - Add 3D state-space visualization
   - Implement real-time updates
   - Add custom theme support

## References

1. Hidden Markov Models in Finance (Springer)
2. Power Method for Eigenvalue Computation (Numerical Linear Algebra)
3. Variational Inference in Financial Time Series (Journal of Financial Econometrics)

🔱 JAH JAH BLESS THE SACRED TRINITY 🔱
