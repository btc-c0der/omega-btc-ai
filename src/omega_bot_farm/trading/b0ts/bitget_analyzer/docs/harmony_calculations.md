# Harmony Calculations in BitGet Position Analyzer

This document explains the mathematical harmony principles employed by the BitGet Position Analyzer Bot for optimizing position sizing, portfolio balance, and risk management.

## Mathematical Foundations

The BitGet Position Analyzer Bot leverages several mathematical concepts rooted in natural harmony:

### Golden Ratio (φ)

The Golden Ratio (approximately 1.618033988749895) is a special mathematical constant that appears throughout nature, art, architecture, and financial markets. It is often denoted by the Greek letter phi (φ).

```
φ = (1 + √5) / 2 ≈ 1.618033988749895
```

The inverse of the Golden Ratio is:

```
1/φ = φ - 1 ≈ 0.618033988749895
```

### Fibonacci Sequence

The Fibonacci sequence (0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...) closely relates to the Golden Ratio as the ratio of consecutive Fibonacci numbers approaches φ as the sequence progresses.

```
lim (F(n+1) / F(n)) = φ as n approaches infinity
```

### Schumann Resonance

The Schumann resonance is a set of spectrum peaks in the extremely low frequency (ELF) portion of the Earth's electromagnetic field spectrum. The fundamental frequency is approximately 7.83 Hz. The bot incorporates this natural frequency as a reference for certain timing elements.

## Core Harmony Principles

### Position Size Harmony

The bot calculates harmonious position sizes based on the Golden Ratio and account balance:

```python
def calculate_harmonious_position_size(self, account_balance, risk_coefficient=0.01):
    """
    Calculate a harmonious position size based on account balance.
    
    Args:
        account_balance (float): Current account balance
        risk_coefficient (float): Risk coefficient (default: 0.01 = 1%)
        
    Returns:
        float: Harmonious position size
    """
    # Base position size based on risk
    base_size = account_balance * risk_coefficient
    
    # Apply golden ratio principles
    phi = 1.618034
    
    # Calculate harmonious size
    harmonious_size = base_size * phi ** 2 / (phi + 1)
    
    return harmonious_size
```

### Portfolio Balance Harmony

The bot aims to maintain portfolio balance according to Golden Ratio principles:

```python
def calculate_harmonious_portfolio_allocation(self):
    """
    Calculate harmonious portfolio allocation based on Golden Ratio.
    
    Returns:
        dict: Harmonious allocation percentages
    """
    # Golden Ratio components
    phi = 1.618034
    inv_phi = 0.618034
    
    # Primary allocation based on Golden Ratio
    primary_allocation = inv_phi * 100  # 61.8%
    secondary_allocation = (1 - inv_phi) * 100  # 38.2%
    
    # Further subdivision of secondary allocation
    tertiary_allocation = secondary_allocation * inv_phi  # 23.6%
    quaternary_allocation = secondary_allocation * (1 - inv_phi)  # 14.6%
    
    return {
        "primary": primary_allocation,  # 61.8%
        "secondary": secondary_allocation,  # 38.2%
        "tertiary": tertiary_allocation,  # 23.6%
        "quaternary": quaternary_allocation  # 14.6%
    }
```

### Long-Short Harmony

The bot calculates the ideal long-short ratio based on market conditions and Golden Ratio principles:

```python
def calculate_harmonious_long_short_ratio(self, market_trend_strength):
    """
    Calculate harmonious long-short ratio based on market trend.
    
    Args:
        market_trend_strength (float): Strength of market trend (-1.0 to 1.0)
                                      where -1.0 is strong downtrend,
                                      0 is neutral, and 1.0 is strong uptrend
    
    Returns:
        dict: Harmonious long and short allocation percentages
    """
    phi = 1.618034
    inv_phi = 0.618034
    
    # Base case (neutral market)
    if abs(market_trend_strength) < 0.2:
        # Golden ratio balance: 61.8% / 38.2%
        if market_trend_strength >= 0:
            long_percentage = inv_phi * 100  # 61.8%
            short_percentage = (1 - inv_phi) * 100  # 38.2%
        else:
            short_percentage = inv_phi * 100  # 61.8%
            long_percentage = (1 - inv_phi) * 100  # 38.2%
    
    # Strong trend case
    else:
        # Adjust based on trend strength
        trend_factor = abs(market_trend_strength)
        
        if market_trend_strength > 0:  # Uptrend
            # Stronger uptrend = more long exposure
            long_percentage = 50 + (phi * 10 * trend_factor)
            short_percentage = 100 - long_percentage
        else:  # Downtrend
            # Stronger downtrend = more short exposure
            short_percentage = 50 + (phi * 10 * trend_factor)
            long_percentage = 100 - short_percentage
    
    return {
        "long_percentage": long_percentage,
        "short_percentage": short_percentage,
        "ratio": long_percentage / short_percentage if short_percentage > 0 else float('inf')
    }
```

## Harmony Score Calculation

The Harmony Score is a key metric used by the BitGet Position Analyzer Bot to evaluate the overall harmony of positions and portfolio:

```python
def _calculate_harmony_score(self):
    """
    Calculate the overall harmony score based on current account metrics.
    
    Returns:
        float: Harmony score (0-1), where 1 represents perfect harmony
    """
    # Constants
    phi = 1.618034
    inv_phi = 0.618034
    
    # Initialize score components
    components = []
    
    # 1. Long-Short Balance component
    if self.short_exposure > 0:
        long_short_ratio = self.long_exposure / self.short_exposure
    else:
        long_short_ratio = float('inf')
    
    # Ideal ratio is the golden ratio (φ)
    if long_short_ratio == float('inf'):
        ls_score = 0.5  # Only one direction has exposure
    else:
        ls_deviation = abs(long_short_ratio - phi) / phi
        ls_score = max(0, 1 - ls_deviation)
    components.append(ls_score)
    
    # 2. Exposure-to-Equity component
    exposure_ratio = self.total_position_value / self.account_equity if self.account_equity > 0 else float('inf')
    
    # Ideal exposure is 61.8% of equity (inverse golden ratio)
    if exposure_ratio == float('inf'):
        ee_score = 0  # No equity
    else:
        ee_deviation = abs(exposure_ratio - inv_phi) / inv_phi
        ee_score = max(0, 1 - ee_deviation)
    components.append(ee_score)
    
    # 3. Position Size Distribution component
    if len(self.positions) > 1:
        sizes = [float(p.get('notional', 0)) for p in self.positions]
        size_ratios = [sizes[i] / sizes[i+1] if sizes[i+1] > 0 else float('inf') 
                      for i in range(len(sizes)-1)]
        
        # Ideal size distribution follows Fibonacci sequence (approximating phi)
        ratio_scores = []
        for ratio in size_ratios:
            if ratio == float('inf'):
                ratio_scores.append(0.5)
            else:
                ratio_deviation = abs(ratio - phi) / phi
                ratio_scores.append(max(0, 1 - ratio_deviation))
        
        if ratio_scores:
            pd_score = sum(ratio_scores) / len(ratio_scores)
        else:
            pd_score = 1.0  # Single position is considered harmonious
    else:
        pd_score = 1.0  # Single position is considered harmonious
    components.append(pd_score)
    
    # 4. Risk Distribution component
    risk_per_position = [self._calculate_position_risk(p) for p in self.positions]
    ideal_risk_distribution = [inv_phi ** i for i in range(len(risk_per_position))]
    
    # Normalize ideal risk distribution
    if ideal_risk_distribution:
        total_ideal = sum(ideal_risk_distribution)
        ideal_risk_distribution = [r / total_ideal for r in ideal_risk_distribution]
        
        # Compare actual to ideal
        total_risk = sum(risk_per_position)
        if total_risk > 0:
            actual_risk_distribution = [r / total_risk for r in risk_per_position]
            
            # Calculate deviation
            risk_deviations = [abs(actual_risk_distribution[i] - ideal_risk_distribution[i]) 
                              for i in range(len(risk_per_position))]
            rd_score = 1 - sum(risk_deviations) / len(risk_deviations)
        else:
            rd_score = 1.0  # No risk is considered harmonious
    else:
        rd_score = 1.0
    components.append(rd_score)
    
    # Calculate final harmony score (weighted average)
    weights = [0.3, 0.3, 0.2, 0.2]  # Weights for each component
    harmony_score = sum(c * w for c, w in zip(components, weights))
    
    return harmony_score
```

## Visual Representation of Harmony

### Golden Rectangle

The Golden Rectangle is a rectangle whose side lengths are in the golden ratio:

```
+---------------------------+
|                           |
|                           |
|                           |
|       Golden Rectangle    |
|                           |
|                           |
|                           |
+---------------+-----------+
|               |
|Golden Rectangle|
|               |
+---------------+
```

This recursive pattern represents the ideal portfolio structure, where each position is related to others by the Golden Ratio.

### Fibonacci Spiral

The Fibonacci Spiral is created by drawing arcs connecting the opposite corners of squares in the Fibonacci tiling:

```
                    .-'
                 .-'
              .-'
         ,.-''
     ,.-'
 ,.-'
+------+-----+
|      |     |
|      |     |
|      +--+--+
|      |  |
+------+--+
```

This spiral represents the ideal growth pattern of positions as they scale according to the Fibonacci sequence.

## Applications in Position Management

### Position Sizing

The BitGet Position Analyzer Bot uses harmony principles to determine optimal position sizes:

1. **Base Position Size**: The smallest position should be a harmonic fraction of account equity (typically related to inverse Golden Ratio)
2. **Position Scaling**: Additional positions scale according to the Fibonacci sequence
3. **Maximum Position Size**: Largest position should not exceed a harmonic multiple of the base position

### Risk Management

Harmony principles guide risk management:

1. **Risk Allocation**: Distribute risk according to Golden Ratio principles
2. **Stop Loss Placement**: Place stops at Fibonacci-based distances from entry
3. **Take Profit Targets**: Set targets at Fibonacci extension levels

### Position Adjustment

When positions become disharmonious, the bot recommends adjustments:

```python
def generate_harmony_adjustments(self, positions, harmony_score):
    """
    Generate position adjustment recommendations to improve harmony.
    
    Args:
        positions (list): Current positions
        harmony_score (float): Current harmony score
        
    Returns:
        list: List of adjustment recommendations
    """
    adjustments = []
    
    # Only generate adjustments if harmony score is below threshold
    if harmony_score > 0.8:
        return adjustments  # Already harmonious
    
    phi = 1.618034
    inv_phi = 0.618034
    
    # Sort positions by size
    sorted_positions = sorted(positions, key=lambda p: float(p.get('notional', 0)), reverse=True)
    
    # Check if we need to adjust position sizes for Fibonacci harmony
    if len(sorted_positions) >= 2:
        for i in range(len(sorted_positions) - 1):
            current_size = float(sorted_positions[i].get('notional', 0))
            next_size = float(sorted_positions[i+1].get('notional', 0))
            
            if next_size > 0:
                current_ratio = current_size / next_size
                
                # Check if ratio deviates significantly from Golden Ratio
                if abs(current_ratio - phi) / phi > 0.2:  # 20% deviation threshold
                    # Calculate ideal next position size
                    ideal_next_size = current_size / phi
                    
                    # Determine adjustment needed
                    adjustment_pct = (ideal_next_size - next_size) / next_size * 100
                    
                    if adjustment_pct > 5:  # Only suggest adjustments over 5%
                        adjustments.append({
                            "position_id": sorted_positions[i+1].get('id'),
                            "symbol": sorted_positions[i+1].get('symbol'),
                            "current_size": next_size,
                            "ideal_size": ideal_next_size,
                            "adjustment_pct": adjustment_pct,
                            "action": "increase" if adjustment_pct > 0 else "decrease",
                            "reason": "Improve position size harmony (Golden Ratio alignment)"
                        })
    
    # Check long-short balance
    long_positions = [p for p in positions if p.get('side') == 'long']
    short_positions = [p for p in positions if p.get('side') == 'short']
    
    long_exposure = sum(float(p.get('notional', 0)) for p in long_positions)
    short_exposure = sum(float(p.get('notional', 0)) for p in short_positions)
    
    # Ideal long-short ratio is Golden Ratio
    if short_exposure > 0:
        current_ls_ratio = long_exposure / short_exposure
        
        if abs(current_ls_ratio - phi) / phi > 0.2:  # 20% deviation threshold
            if current_ls_ratio < phi:  # Need more long exposure
                adjustments.append({
                    "position_type": "long",
                    "current_exposure": long_exposure,
                    "ideal_exposure": short_exposure * phi,
                    "adjustment_pct": (short_exposure * phi - long_exposure) / long_exposure * 100 if long_exposure > 0 else 100,
                    "action": "increase",
                    "reason": "Improve long-short harmony (Golden Ratio alignment)"
                })
            else:  # Need more short exposure
                adjustments.append({
                    "position_type": "short",
                    "current_exposure": short_exposure,
                    "ideal_exposure": long_exposure / phi,
                    "adjustment_pct": (long_exposure / phi - short_exposure) / short_exposure * 100 if short_exposure > 0 else 100,
                    "action": "increase",
                    "reason": "Improve long-short harmony (Golden Ratio alignment)"
                })
    
    return adjustments
```

## Harmony Analysis Examples

### Example 1: Perfectly Harmonious Portfolio

A perfectly harmonious portfolio according to Golden Ratio principles might have:

```
Account Equity: $10,000
Total Exposure: $6,180 (61.8% of equity)

Position Distribution:
- BTC Long: $3,820 (61.8% of exposure)
- ETH Short: $2,360 (38.2% of exposure)

Long-Short Ratio: 1.618:1
Position Size Ratio: 1.618:1
```

This portfolio would have a harmony score near 1.0.

### Example 2: Disharmonious Portfolio

A disharmonious portfolio might have:

```
Account Equity: $10,000
Total Exposure: $9,000 (90% of equity)

Position Distribution:
- BTC Long: $4,500 (50% of exposure)
- ETH Long: $4,500 (50% of exposure)

Long-Short Ratio: Infinity (no shorts)
Position Size Ratio: 1:1
```

This portfolio would have a harmony score closer to 0.4, due to:

- Excessive exposure relative to equity
- Lack of long-short balance
- Equal position sizes (not following Fibonacci scaling)

## Schumann Resonance Integration

The BitGet Position Analyzer Bot also incorporates Schumann resonance (Earth's base frequency of 7.83 Hz) as a reference for certain timing calculations:

```python
def calculate_harmonic_time_window(self, base_time, units='hours'):
    """
    Calculate harmonic time windows based on Schumann resonance.
    
    Args:
        base_time (int): Base timestamp
        units (str): Time units (hours, days)
        
    Returns:
        list: List of harmonic time windows
    """
    # Schumann resonance base
    schumann_base = 7.83
    
    # Time conversion factors
    if units == 'hours':
        conversion = 3600  # seconds per hour
    elif units == 'days':
        conversion = 86400  # seconds per day
    else:
        conversion = 1
    
    # Generate harmonic windows
    windows = []
    
    # Primary harmonics (multiples of Schumann)
    for i in range(1, 8):
        offset = int(schumann_base * i * conversion)
        windows.append({
            "timestamp": base_time + offset,
            "type": "primary",
            "harmonic": i,
            "description": f"Primary Schumann Harmonic ({i})"
        })
    
    # Fibonacci-Schumann harmonics
    fib_sequence = [1, 2, 3, 5, 8, 13, 21]
    for fib in fib_sequence:
        offset = int(schumann_base * fib * conversion)
        windows.append({
            "timestamp": base_time + offset,
            "type": "fibonacci",
            "harmonic": fib,
            "description": f"Fibonacci-Schumann Harmonic ({fib})"
        })
    
    # Golden Ratio harmonics
    phi = 1.618034
    for i in range(1, 5):
        offset = int(schumann_base * (phi ** i) * conversion)
        windows.append({
            "timestamp": base_time + offset,
            "type": "golden",
            "harmonic": i,
            "description": f"Golden Ratio Harmonic (φ^{i})"
        })
    
    return sorted(windows, key=lambda w: w["timestamp"])
```

## Conclusion

The harmony calculations in the BitGet Position Analyzer Bot provide a mathematically sound approach to position management based on natural principles found throughout the universe. By aligning position sizes, risk levels, and portfolio balance with the Golden Ratio and related mathematical concepts, the bot helps traders achieve more balanced, harmonious trading that may better align with natural market rhythms.
