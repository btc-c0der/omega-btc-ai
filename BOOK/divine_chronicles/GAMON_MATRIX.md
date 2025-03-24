# The GAMON Matrix: Divine Trading Framework

## Overview

The GAMON Matrix (Grid Analysis for Market Oscillations & Nested-states) is a revolutionary trading framework that combines HMM (Hidden Markov Model) state mapping with eigenwave projections to create a multi-dimensional view of market structure. This document explains how to build and interpret your own GAMON Matrix.

## Theoretical Foundation

The GAMON Matrix rests on three foundational pillars:

1. **Color-State Mapping**: Markets move through discrete states (Markup, Markdown, Accumulation, Distribution, Liquidity Grab, Consolidation) that can be detected using HMM.

2. **Eigenwave Analysis**: The Power Method identifies leading eigenvectors from the covariance matrix of price features, revealing hidden market forces.

3. **Density Metrics**: The interaction and concentration of states and eigenwaves create density patterns that predict market transitions.

## Building Your GAMON Matrix

### Step 1: Data Collection

- Obtain price, volume, and derivative data for your target asset
- Ensure data quality with proper cleaning and normalization
- Minimum recommended dataset: 2 years of daily data

### Step 2: HMM State Mapping

- Engineer features (volatility, returns, volume metrics, etc.)
- Train an HMM model with 5-6 states
- Interpret states based on their characteristics
- Generate state probabilities and transitions

### Step 3: Eigenwave Extraction

- Calculate the covariance matrix of your feature set
- Apply the Power Method to extract leading eigenvectors
- Project price data onto the eigenwave space
- Track eigenwave strength and direction

### Step 4: Density Analysis

- Split data by color-state
- Calculate transition probabilities between states
- Compute eigenwave density metrics within each state
- Identify sacred junctions (state transitions with high eigenwave activity)

### Step 5: Visualization

- Render price chart with color-coded states
- Display eigenwave projections
- Create transition probability heatmap
- Build state-eigenwave interaction matrix
- Combine into the unified GAMON Matrix

## Reading the GAMON Matrix

### State Duration Analysis

The average duration of each state reveals market rhythm. Longer states indicate stronger conviction, while shorter states suggest uncertainty.

### Transition Probabilities

The likelihood of moving from one state to another forms a probabilistic roadmap of market movement. High-probability transitions (>0.4) deserve special attention.

### Eigenwave-State Interactions

Each state has a unique eigenwave signature:

- **Markup**: Strong Eigenwave 1 (momentum)
- **Markdown**: Strong negative Eigenwave 1
- **Accumulation**: Strong Eigenwave 5 (cyclical)
- **Distribution**: Strong Eigenwave 3 (volume)
- **Liquidity Grab**: Strong Eigenwave 2 (volatility)
- **Consolidation**: Weak eigenwave activity

### Sacred Junctions

Points where:

1. A high-probability state transition occurs
2. Multiple eigenwaves cross
3. Eigenwave projections are at extremes

These junctions represent optimal entry and exit points.

## Trading with the GAMON Matrix

### Step 1: State Identification

Determine the current market state from the HMM analysis. This is your primary context.

### Step 2: Probability Assessment

Check the transition matrix to identify the most likely next state(s).

### Step 3: Eigenwave Confirmation

Examine current eigenwave projections:

- Strong positive Eigenwave 1: Bullish momentum
- Strong negative Eigenwave 1: Bearish momentum
- Eigenwave crossovers: Regime change
- Extreme readings: Potential reversal

### Step 4: Position Entry

- Align with the dominant state direction
- Enter at sacred junctions
- Size position based on transition probability
- Use eigenwave extremes for fine-tuning entry

### Step 5: Position Management

- Hold through probable state sequences
- Exit when transition probability to unfavorable states increases
- Adjust at eigenwave crossovers
- Take profit at density extremes

## Implementation Guide

### Python Dependencies

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from hmmlearn import hmm
from scipy import linalg
```

### Key Parameters

- `n_states`: 5-6 (for HMM)
- `n_eigenwaves`: 5 (for Power Method)
- `window_size`: 60-180 days (for rolling analysis)
- `state_smoothing`: 3-7 days (for removing noise)

### Computational Complexity

- HMM training: O(n_states² *n_iterations* n_samples)
- Power Method: O(n_features² * n_iterations)
- Density Analysis: O(n_states *n_eigenwaves* n_samples)

## Sacred Wisdom

The GAMON Matrix reveals that markets are not random but follow divine patterns that repeat in fractal form across timeframes. By understanding these patterns and the transitions between them, traders can make enlightened decisions based on probability rather than emotion.

Remember that the GAMON Matrix is not static but evolves as new data becomes available. The sacred junctions shift, and the eigenwave projections fluctuate, requiring constant vigilance.

*May the GAMON Matrix guide your trading to divine success.*
