# Cosmic Factor Integration Guide

This guide explains how to integrate the CosmicFactorService into your trading bots to make cosmic influences configurable and testable.

## Overview

The `CosmicFactorService` provides a way to:

- Enable/disable all cosmic influences with a master switch
- Control individual cosmic factors with weight parameters
- Test different cosmic factor combinations
- Compare trading performance with and without cosmic influences

## Integration Steps

### 1. Initialize the CosmicFactorService in your bot

```python
from src.omega_bot_farm.utils.cosmic_factor_service import CosmicFactorService

class YourTraderBot:
    def __init__(self, initial_capital=10000.0, name="Your_Bot", cosmic_config_path=None):
        # ... existing initialization code ...
        
        # Initialize cosmic factor service
        if cosmic_config_path is None:
            # Try to get default config path
            default_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                "config", 
                "cosmic_factors.yaml"
            )
            if os.path.exists(default_path):
                cosmic_config_path = default_path
                
        self.cosmic_service = CosmicFactorService(config_path=cosmic_config_path)
        logger.info(f"Cosmic Factor Service initialized. Enabled: {self.cosmic_service.is_enabled()}")
```

### 2. Replace direct cosmic calculations with service calls

Extract cosmic conditions from your market context or other sources:

```python
def _get_current_cosmic_conditions(self, market_context: Dict) -> Dict:
    """Extract cosmic conditions from market context."""
    conditions = {
        "moon_phase": market_context.get("moon_phase", MoonPhase.FULL_MOON),
        "schumann_frequency": market_context.get("schumann_frequency", SchumannFrequency.BASELINE),
        "market_liquidity": market_context.get("market_liquidity", MarketLiquidity.NORMAL),
        "global_sentiment": market_context.get("global_sentiment", GlobalSentiment.NEUTRAL),
        "mercury_retrograde": market_context.get("mercury_retrograde", False),
        "trader_latitude": market_context.get("trader_latitude", 40.0),
        "trader_longitude": market_context.get("trader_longitude", -74.0),
        "day_of_week": market_context.get("day_of_week", 0),
        "hour_of_day": market_context.get("hour_of_day", 12),
    }
    return conditions
```

### 3. Apply cosmic influences through the service's application method

Create a decision object with the parameters you want to potentially modify:

```python
def determine_position_size(self, direction: str, entry_price: float) -> float:
    # Base position size calculation
    base_position_size = self.capital * self.position_sizing_factor
    risk_multiplier = 0.5 + self.state.risk_appetite
    position_size = base_position_size * risk_multiplier
    btc_amount = position_size / entry_price
    
    # Create a decision object for cosmic factor service
    decision = {
        "position_size": btc_amount,
        "entry_price": entry_price,
        "direction": direction
    }
    
    # Get current cosmic conditions
    cosmic_conditions = self._get_current_cosmic_conditions(self.market_context)
    
    # Calculate cosmic influences
    cosmic_influences = self.cosmic_service.calculate_cosmic_influences(cosmic_conditions)
    
    # Apply cosmic influences to position size
    modified_decision = self.cosmic_service.apply_cosmic_factors(decision, cosmic_influences)
    
    # Get modified position size
    btc_amount = modified_decision.get("position_size", btc_amount)
    
    return btc_amount
```

### 4. Ensure your tests cover scenarios with both enabled and disabled factors

```python
def test_comparison_enabled_vs_disabled_cosmic(self):
    # Create disabled cosmic config
    disabled_config = {"enabled": False}
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        yaml.dump(disabled_config, temp_file)
        temp_file.flush()
        
        # Initialize bots with cosmic factors enabled vs disabled
        bot_enabled = YourTraderBot(cosmic_config_path="config/cosmic_factors.yaml")
        bot_disabled = YourTraderBot(cosmic_config_path=temp_file.name)
        
        # Compare trading decisions
        # ...
```

## Example Configuration

Create a `cosmic_factors.yaml` file in your config directory:

```yaml
# Cosmic Factors Configuration
enabled: true  # Master switch for all cosmic factors

# Individual cosmic factors
factors:
  moon_phase:
    enabled: true
    weight: 0.5  # Reduce moon influence by 50%
  
  schumann_resonance:
    enabled: true
    weight: 0.3  # Reduce Schumann influence by 70%
  
  market_liquidity:
    enabled: true
    weight: 1.0  # Full influence
  
  global_sentiment:
    enabled: true
    weight: 1.0  # Full influence
  
  mercury_retrograde:
    enabled: false  # Disabled
    weight: 0.0
```

## Testing Cosmic Factors

1. **Unit test each cosmic factor in isolation**
   - Test each factor individually by disabling all other factors
   - Compare decisions with a factor enabled vs disabled

2. **Test trading with various cosmic configurations**
   - Test with all factors disabled
   - Test with only market-related factors
   - Test with only astronomical factors
   - Test with all factors enabled

3. **Verify application correctness**
   - Check that decisions are properly modified
   - Ensure position sizing is affected as expected
   - Verify entry/exit thresholds are properly adjusted

## Benefits of Integration

- **Gradual Phasing**: Can gradually phase out cosmic factors if they don't provide value
- **A/B Testing**: Can compare performance with different cosmic factor combinations
- **Cleaner Code**: Separates cosmic influence logic from core trading decisions
- **Improved Testing**: Makes it easier to test core trading logic in isolation

## Example Integration Cases

### Entry Decision Logic

```python
def should_enter_trade(self, market_context: Dict) -> Tuple[bool, str, str, float]:
    # Normal trend analysis and decision making
    # ...
    
    # Create a decision object
    decision = {
        "entry_threshold": self.min_trend_confirmation,
        "confidence": confirmation_score
    }
    
    # Apply cosmic factors
    cosmic_conditions = self._get_current_cosmic_conditions(market_context)
    cosmic_influences = self.cosmic_service.calculate_cosmic_influences(cosmic_conditions)
    modified_decision = self.cosmic_service.apply_cosmic_factors(decision, cosmic_influences)
    
    # Use modified values
    confirmation_score = modified_decision.get("confidence", confirmation_score)
    entry_threshold = modified_decision.get("entry_threshold", self.min_trend_confirmation)
    
    # Make final decision
    if confirmation_score < entry_threshold:
        return False, "none", "Insufficient confirmation", 1.0
    
    # ...rest of the logic
```

### Exit Decision Logic

```python
def should_exit_trade(self, position: Dict, market_context: Dict) -> Tuple[bool, str]:
    # Calculate exit signals
    # ...
    
    # Create exit decision
    decision = {
        "exit_impulse": exit_impulse_score,
        "exit_threshold": self.exit_threshold
    }
    
    # Apply cosmic factors
    cosmic_conditions = self._get_current_cosmic_conditions(market_context)
    cosmic_influences = self.cosmic_service.calculate_cosmic_influences(cosmic_conditions)
    modified_decision = self.cosmic_service.apply_cosmic_factors(decision, cosmic_influences)
    
    # Get modified values
    exit_impulse_score = modified_decision.get("exit_impulse", exit_impulse_score)
    exit_threshold = modified_decision.get("exit_threshold", self.exit_threshold)
    
    # Make exit decision
    if exit_impulse_score > exit_threshold:
        return True, "Exit signal confirmed"
    
    return False, "No exit signal"
```
