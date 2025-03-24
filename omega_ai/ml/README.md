# Market Trends AI Model

This module contains an AI model that learns from historical market trends data to predict future market behavior. The model integrates with the existing OMEGA BTC AI system, using Redis as the data store.

## Features

- Predict market trends (bullish, bearish, neutral) with confidence scores
- Predict future BTC prices based on historical patterns
- Detect potential market maker traps
- Calculate Fibonacci-inspired harmony scores for overall market assessment
- Store and track prediction accuracy over time
- Beautiful console output with divine wisdom

## Components

- `market_trends_model.py` - Main AI model class implementation
- `generate_dummy_data.py` - Tool to generate dummy data for testing
- `run_market_ai.py` - Runner script to generate data, train, and make predictions

## Prerequisites

- Redis server running on localhost (or specified in `.env` file)
- Python 3.8 or higher
- Required Python packages: redis, numpy, pandas, scikit-learn, joblib

## Usage

### Generating Test Data

To generate dummy historical data for training and testing:

```bash
python -m omega_ai.ml.generate_dummy_data
```

This will generate 30 days of price and trend data in your Redis instance.

### Running the Model

The main runner script provides several options:

```bash
python -m omega_ai.ml.run_market_ai --help
```

#### Basic Usage

```bash
# Generate data, train and predict
python -m omega_ai.ml.run_market_ai --generate-data --train --predict

# Train on existing data and make predictions
python -m omega_ai.ml.run_market_ai --train

# Just make predictions using previously trained model
python -m omega_ai.ml.run_market_ai --predict

# Run in continuous monitoring mode
python -m omega_ai.ml.run_market_ai --monitor --interval 60
```

### Integration with Other OMEGA Components

The AI model stores its predictions in Redis, making them available to other components in the OMEGA system:

- `ai_trend_prediction` - Latest trend prediction
- `ai_price_prediction` - Latest price prediction
- `ai_trap_prediction` - Latest market maker trap prediction
- `ai_predictions` - Combined prediction data
- `ai_prediction_history_*` - Historical prediction data for accuracy tracking

## Development

### Adding New Features

To extend the model with new capabilities:

1. Add new methods to the `MarketTrendsModel` class
2. Create appropriate Redis storage keys for your data
3. Update the test cases in `tests/test_market_trends_model.py`

### Model Persistence

Models are automatically saved to `omega_ai/ml/models/` directory. You can load these models later without retraining.

## Divine Fibonacci Integration

The model incorporates sacred Fibonacci mathematics for:

- Feature engineering with Fibonacci-inspired windows (8, 13, 21, 34, 55)
- Harmony scoring based on the Golden Ratio
- Trap detection using Fibonacci alignment principles
- Divine wisdom generation based on market conditions

## Example Output

```
🧠 AI MODEL PREDICTIONS 🧠
══════════════════════════════════════

📈 TREND PREDICTION:
  Direction: Bullish
  Confidence: 0.85

💰 PRICE PREDICTION:
  Current: $75,321.45
  Predicted: $77,982.34 (+3.53%)
  Confidence: 0.76

⚠️ TRAP PREDICTION:
  No trap detected
  Confidence: 0.89

🌟 FIBONACCI HARMONY SCORE:
  8.42/10

🔮 DIVINE WISDOM:
  The divine Fibonacci patterns reveal strong bullish momentum. The market is in harmony with upward forces.

Timestamp: 2023-10-25T12:34:56.789012+00:00
══════════════════════════════════════
```

## License

This module is licensed under the terms of the GPU license, as described in `BOOK/divine_chronicles/GPU_LICENSE.md`.
