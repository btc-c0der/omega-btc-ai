
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


# BitGet Position Analyzer Bot Configuration Guide

This document provides detailed instructions for configuring the BitGet Position Analyzer Bot to suit your specific needs and trading strategy.

## Configuration Options

The BitGet Position Analyzer Bot can be configured through several methods:

1. Environment variables
2. Constructor parameters
3. Configuration files
4. Runtime configuration

## API Credentials

### Environment Variables

The simplest way to configure API credentials is through environment variables:

```bash
# BitGet API Credentials
export BITGET_API_KEY="your_api_key"
export BITGET_SECRET_KEY="your_api_secret"
export BITGET_PASSPHRASE="your_passphrase"

# Network Configuration
export USE_TESTNET="true"  # Use "true" or "false"
```

You can add these to your `.env` file or `.bashrc`/`.zshrc` file.

### Constructor Parameters

You can also provide credentials directly when initializing the bot:

```python
from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t

analyzer = BitgetPositionAnalyzerB0t(
    api_key="your_api_key",
    api_secret="your_api_secret",
    api_passphrase="your_passphrase",
    use_testnet=True
)
```

## Core Configuration Parameters

### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | None | BitGet API key. Uses BITGET_API_KEY env var if None. |
| `api_secret` | str | None | BitGet API secret. Uses BITGET_SECRET_KEY env var if None. |
| `api_passphrase` | str | None | BitGet API passphrase. Uses BITGET_PASSPHRASE env var if None. |
| `use_testnet` | bool | False | Whether to use BitGet testnet. |
| `position_history_length` | int | 10 | Number of position snapshots to keep in history. |

### Example

```python
analyzer = BitgetPositionAnalyzerB0t(
    api_key="your_api_key",
    api_secret="your_api_secret",
    api_passphrase="your_passphrase",
    use_testnet=True,
    position_history_length=15
)
```

## Advanced Configuration

For more advanced configuration, you can create a configuration file:

### YAML Configuration File

Create a file named `bitget_analyzer_config.yaml`:

```yaml
# BitGet API Configuration
api:
  key: "your_api_key"
  secret: "your_api_secret"
  passphrase: "your_passphrase"
  use_testnet: true

# History Configuration
history:
  position_history_length: 15
  store_history: true
  history_file: "position_history.json"

# Analysis Configuration
analysis:
  fibonacci:
    use_extended_levels: true
    default_price_range: "week"  # day, week, month
  harmony:
    min_harmony_score: 0.6
    optimal_exposure_ratio: 0.618
    long_short_tolerance: 0.2

# Notification Configuration
notifications:
  enabled: true
  notify_on_position_changes: true
  notify_on_harmony_changes: true
  harmony_threshold: 0.7

# Logging Configuration
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  log_to_file: true
  log_file: "bitget_analyzer.log"
  rotate_logs: true
  max_log_size: 10485760  # 10 MB
```

### Loading Configuration from File

```python
import yaml
from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t

# Load config from file
with open("bitget_analyzer_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Initialize with config
analyzer = BitgetPositionAnalyzerB0t(
    api_key=config["api"]["key"],
    api_secret=config["api"]["secret"],
    api_passphrase=config["api"]["passphrase"],
    use_testnet=config["api"]["use_testnet"],
    position_history_length=config["history"]["position_history_length"]
)

# Set additional configuration
analyzer.set_fibonacci_config(
    use_extended_levels=config["analysis"]["fibonacci"]["use_extended_levels"],
    default_price_range=config["analysis"]["fibonacci"]["default_price_range"]
)

analyzer.set_harmony_config(
    min_harmony_score=config["analysis"]["harmony"]["min_harmony_score"],
    optimal_exposure_ratio=config["analysis"]["harmony"]["optimal_exposure_ratio"],
    long_short_tolerance=config["analysis"]["harmony"]["long_short_tolerance"]
)
```

## Runtime Configuration

You can also modify configuration at runtime:

```python
# Initialize with basic configuration
analyzer = BitgetPositionAnalyzerB0t(use_testnet=True)

# Update configuration at runtime
analyzer.update_config({
    "fibonacci_extended_levels": True,
    "min_harmony_score": 0.7,
    "position_history_length": 20,
    "logging_level": "DEBUG"
})
```

## Fibonacci Analysis Configuration

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `use_extended_levels` | bool | False | Whether to include extended Fibonacci levels. |
| `default_price_range` | str | "day" | Default timeframe for price range (day, week, month). |
| `custom_levels` | list | None | List of custom Fibonacci levels to include. |
| `detect_patterns` | bool | True | Whether to detect harmonic patterns. |
| `pattern_strength_threshold` | float | 0.7 | Minimum strength for pattern detection (0-1). |

### Example

```python
analyzer.set_fibonacci_config(
    use_extended_levels=True,
    default_price_range="week",
    custom_levels=[0.5, 0.707, 1.414, 2.0],
    detect_patterns=True,
    pattern_strength_threshold=0.8
)
```

## Harmony Calculation Configuration

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `min_harmony_score` | float | 0.6 | Minimum harmony score for recommendations. |
| `optimal_exposure_ratio` | float | 0.618 | Optimal exposure to equity ratio. |
| `long_short_tolerance` | float | 0.2 | Tolerance for long/short ratio deviation. |
| `position_size_tolerance` | float | 0.2 | Tolerance for position size ratio deviation. |
| `risk_distribution_method` | str | "fibonacci" | Method for risk distribution ("fibonacci", "equal", "custom"). |

### Example

```python
analyzer.set_harmony_config(
    min_harmony_score=0.7,
    optimal_exposure_ratio=0.618,
    long_short_tolerance=0.15,
    position_size_tolerance=0.15,
    risk_distribution_method="fibonacci"
)
```

## Notification Configuration

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `notify_on_position_changes` | bool | True | Whether to notify on position changes. |
| `notify_on_harmony_changes` | bool | True | Whether to notify on harmony score changes. |
| `harmony_threshold` | float | 0.7 | Threshold for harmony score notifications. |
| `notification_channels` | list | ["log"] | Channels for notifications (log, email, webhook). |
| `webhook_url` | str | None | Webhook URL for notifications. |

### Example

```python
analyzer.set_notification_config(
    notify_on_position_changes=True,
    notify_on_harmony_changes=True,
    harmony_threshold=0.75,
    notification_channels=["log", "webhook"],
    webhook_url="https://your-webhook-url.com/notify"
)
```

## Logging Configuration

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `logging_level` | str | "INFO" | Logging level (DEBUG, INFO, WARNING, ERROR). |
| `log_to_file` | bool | False | Whether to log to a file. |
| `log_file` | str | "bitget_analyzer.log" | Log file path. |
| `rotate_logs` | bool | False | Whether to rotate logs. |
| `max_log_size` | int | 10485760 | Maximum log size in bytes (10 MB default). |

### Example

```python
analyzer.set_logging_config(
    logging_level="DEBUG",
    log_to_file=True,
    log_file="logs/bitget_analyzer.log",
    rotate_logs=True,
    max_log_size=5242880  # 5 MB
)
```

## Redis Integration Configuration

If you want to use Redis for data persistence and messaging:

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `redis_host` | str | "localhost" | Redis server host. |
| `redis_port` | int | 6379 | Redis server port. |
| `redis_db` | int | 0 | Redis database number. |
| `redis_password` | str | None | Redis password. |
| `redis_prefix` | str | "bitget_analyzer:" | Prefix for Redis keys. |

### Example

```python
analyzer.set_redis_config(
    redis_host="redis.example.com",
    redis_port=6379,
    redis_db=1,
    redis_password="your_redis_password",
    redis_prefix="production:bitget_analyzer:"
)
```

## Environment-Specific Configuration

You can create different configuration files for different environments:

### Development Configuration

```yaml
# dev_config.yaml
api:
  use_testnet: true
logging:
  level: "DEBUG"
```

### Production Configuration

```yaml
# prod_config.yaml
api:
  use_testnet: false
logging:
  level: "WARNING"
  log_to_file: true
```

### Loading Environment-Specific Configuration

```python
import os
import yaml

# Determine environment
env = os.getenv("ENV", "development")

# Load base configuration
with open("base_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Load environment-specific configuration
env_config_file = f"{env}_config.yaml"
if os.path.exists(env_config_file):
    with open(env_config_file, "r") as f:
        env_config = yaml.safe_load(f)
        # Update base config with environment-specific values
        for key, section in env_config.items():
            if key in config:
                config[key].update(section)
            else:
                config[key] = section

# Initialize with merged configuration
analyzer = BitgetPositionAnalyzerB0t(
    api_key=config["api"]["key"],
    api_secret=config["api"]["secret"],
    api_passphrase=config["api"]["passphrase"],
    use_testnet=config["api"]["use_testnet"]
)
```

## Command Line Configuration

When running from the command line, you can specify configuration options:

```bash
python -m src.omega_bot_farm.trading.b0ts --bot bitget_analyzer --config path/to/config.yaml --log-level DEBUG --testnet
```

## Configuration Best Practices

1. **Never Commit API Keys**: Store sensitive information in environment variables or secure vaults, not in code.
2. **Use Configuration Files**: For complex configurations, use YAML or JSON files rather than hardcoding values.
3. **Environment-Specific Configs**: Maintain separate configurations for development, testing, and production.
4. **Validate Configuration**: Always validate configuration values to prevent errors.
5. **Sensible Defaults**: Provide sensible defaults for all configuration options.
6. **Document Configuration**: Clearly document all configuration options and their effects.
7. **Centralize Configuration**: Keep all configuration in one place for easier management.
8. **Version Configuration**: Version control your configuration files alongside your code.

## Troubleshooting Configuration Issues

### API Connection Issues

If you encounter API connection issues:

1. Verify your API credentials are correct
2. Check if you're using the correct network (testnet vs. mainnet)
3. Ensure your IP is whitelisted in BitGet settings
4. Verify the API key has the necessary permissions

### Configuration Loading Issues

If configuration doesn't load properly:

1. Verify the configuration file exists and is accessible
2. Check the YAML/JSON syntax for errors
3. Ensure environment variables are set correctly
4. Check for typos in configuration keys

## Example: Complete Configuration Setup

```python
import os
import yaml
import logging
from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("bitget_analyzer_config")

# Determine environment
env = os.getenv("ENV", "development")
logger.info(f"Loading configuration for environment: {env}")

# Load configuration
config_file = os.getenv("CONFIG_FILE", f"config/{env}_config.yaml")
try:
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    logger.info(f"Loaded configuration from {config_file}")
except Exception as e:
    logger.error(f"Failed to load configuration: {e}")
    config = {}

# Initialize analyzer with configuration
try:
    analyzer = BitgetPositionAnalyzerB0t(
        api_key=config.get("api", {}).get("key") or os.getenv("BITGET_API_KEY"),
        api_secret=config.get("api", {}).get("secret") or os.getenv("BITGET_SECRET_KEY"),
        api_passphrase=config.get("api", {}).get("passphrase") or os.getenv("BITGET_PASSPHRASE"),
        use_testnet=config.get("api", {}).get("use_testnet", True)
    )
    
    # Apply additional configuration
    if "fibonacci" in config:
        analyzer.set_fibonacci_config(**config["fibonacci"])
    
    if "harmony" in config:
        analyzer.set_harmony_config(**config["harmony"])
    
    if "notifications" in config:
        analyzer.set_notification_config(**config["notifications"])
    
    if "logging" in config:
        analyzer.set_logging_config(**config["logging"])
    
    if "redis" in config:
        analyzer.set_redis_config(**config["redis"])
    
    logger.info("BitGet Position Analyzer Bot configured successfully")
except Exception as e:
    logger.error(f"Failed to initialize analyzer: {e}")
    raise

# Test configuration
positions = await analyzer.get_positions()
logger.info(f"Successfully fetched {len(positions.get('positions', []))} positions")
```

This concludes the configuration guide for the BitGet Position Analyzer Bot. For additional assistance, refer to the API Reference documentation or contact support.
