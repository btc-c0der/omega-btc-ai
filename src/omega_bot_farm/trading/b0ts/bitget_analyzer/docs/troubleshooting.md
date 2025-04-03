# BitGet Position Analyzer Bot: Troubleshooting Guide

This guide provides solutions for common issues you might encounter when using the BitGet Position Analyzer Bot.

## Table of Contents

1. [API Connection Issues](#api-connection-issues)
2. [Authentication Problems](#authentication-problems)
3. [Data Retrieval Issues](#data-retrieval-issues)
4. [Performance Concerns](#performance-concerns)
5. [Analysis Discrepancies](#analysis-discrepancies)
6. [Integration Issues](#integration-issues)
7. [Error Messages](#common-error-messages)
8. [Logging and Debugging](#logging-and-debugging)
9. [Environment Setup](#environment-setup)
10. [Advanced Troubleshooting](#advanced-troubleshooting)

## API Connection Issues

### Connection Timeouts

**Symptoms:**

- Requests to BitGet API time out
- `TimeoutError` or `ConnectionError` exceptions

**Solutions:**

1. Check your internet connection
2. Verify BitGet API status at <https://status.bitget.com/>
3. Increase timeout values:

   ```python
   analyzer = BitgetPositionAnalyzerB0t(
       use_testnet=True,
       request_timeout=30  # Increase timeout to 30 seconds
   )
   ```

4. Implement retry logic:

   ```python
   from src.omega_bot_farm.utils.retry import with_retry
   
   positions = await with_retry(analyzer.get_positions, max_retries=3, delay=2)
   ```

### Network Restrictions

**Symptoms:**

- IP restriction errors
- Connection refused errors

**Solutions:**

1. Verify your IP is whitelisted in BitGet settings
2. Check firewall settings to ensure outbound connections are allowed
3. If using a VPN, try connecting without it
4. For cloud deployments, ensure egress rules allow connections to BitGet API endpoints

## Authentication Problems

### Invalid API Credentials

**Symptoms:**

- Authentication errors
- `401 Unauthorized` responses

**Solutions:**

1. Double-check your API key, secret, and passphrase
2. Ensure environment variables are set correctly:

   ```bash
   echo $BITGET_API_KEY
   echo $BITGET_SECRET_KEY
   echo $BITGET_PASSPHRASE
   ```

3. Regenerate API keys in BitGet if necessary
4. Verify API keys have the correct permissions in BitGet settings

### Expired API Keys

**Symptoms:**

- Authentication was working but suddenly stops
- Expiration-related error messages

**Solutions:**

1. Check key expiration in BitGet account settings
2. Generate new API keys and update your configuration
3. Implement a credential rotation system for long-running applications

## Data Retrieval Issues

### Empty Position Data

**Symptoms:**

- Position list is empty
- Bot reports no positions but positions exist in BitGet

**Solutions:**

1. Verify the account has active positions
2. Check if you're connected to the correct network (testnet vs. mainnet)
3. Ensure API keys have read permissions for futures/swap positions
4. Try specifying the symbol explicitly:

   ```python
   positions = await analyzer.get_positions(symbol="BTCUSDT")
   ```

### Delayed or Stale Data

**Symptoms:**

- Position data is outdated
- Changes in BitGet aren't reflected in analyzer results

**Solutions:**

1. Decrease the polling interval:

   ```python
   await analyzer.start_monitoring(polling_interval=10)  # 10 seconds
   ```

2. Check if you're using cached data by mistake
3. Implement force refresh:

   ```python
   positions = await analyzer.get_positions(force_refresh=True)
   ```

## Performance Concerns

### Slow Response Times

**Symptoms:**

- Bot takes too long to analyze positions
- High CPU usage during analysis

**Solutions:**

1. Limit the number of positions analyzed:

   ```python
   positions = await analyzer.get_positions(limit=10)
   ```

2. Optimize Fibonacci calculations:

   ```python
   analyzer.set_fibonacci_config(
       use_extended_levels=False,  # Disable extended levels
       detect_patterns=False  # Disable pattern detection
   )
   ```

3. Enable caching:

   ```python
   analyzer.enable_caching(expiry=300)  # Cache results for 5 minutes
   ```

### Memory Leaks

**Symptoms:**

- Increasing memory usage over time
- Out of memory errors after extended operation

**Solutions:**

1. Limit position history size:

   ```python
   analyzer = BitgetPositionAnalyzerB0t(position_history_length=5)
   ```

2. Implement periodic garbage collection:

   ```python
   import gc
   
   # Run after extensive operations
   gc.collect()
   ```

3. Monitor memory usage with tools like `memory_profiler`

## Analysis Discrepancies

### Inconsistent Fibonacci Levels

**Symptoms:**

- Fibonacci levels don't match expected values
- Different results when analyzing the same position multiple times

**Solutions:**

1. Check if you're using the correct price range:

   ```python
   fib_levels = analyzer.generate_fibonacci_levels(
       high_price=50000,
       low_price=40000,
       current_price=45000,
       extended_levels=True
   )
   ```

2. Ensure the high and low prices are correctly identified
3. Use a standard timeframe for consistency:

   ```python
   analyzer.set_fibonacci_config(default_price_range="week")
   ```

### Unexpected Harmony Scores

**Symptoms:**

- Harmony scores seem incorrect
- Positions you expect to be harmonious have low scores

**Solutions:**

1. Review harmony calculation parameters:

   ```python
   analyzer.set_harmony_config(
       optimal_exposure_ratio=0.5,  # Adjust to your preference
       long_short_tolerance=0.3  # Increase tolerance
   )
   ```

2. Check if all required data is available for harmony calculations
3. Verify position sizes and ratios manually to identify discrepancies

## Integration Issues

### Redis Connection Problems

**Symptoms:**

- Redis connection errors
- Bot fails to store or retrieve data from Redis

**Solutions:**

1. Verify Redis server is running and accessible:

   ```bash
   redis-cli ping
   ```

2. Check Redis connection settings:

   ```python
   analyzer.set_redis_config(
       redis_host="localhost",
       redis_port=6379,
       redis_password="your_password"
   )
   ```

3. Ensure Redis has enough memory available
4. Test Redis connection separately:

   ```python
   from redis import Redis
   
   redis = Redis(host="localhost", port=6379)
   result = redis.ping()
   print(f"Redis connection test: {result}")
   ```

### Integration with Other Bots

**Symptoms:**

- Data not being shared between bots
- Other bots not recognizing analyzer output

**Solutions:**

1. Ensure compatible data formats:

   ```python
   # Standardize output format
   positions_data = analyzer.get_positions_standardized()
   ```

2. Use shared Redis channels:

   ```python
   analyzer.set_redis_config(
       redis_channel="shared_bot_channel",
       publish_results=True
   )
   ```

3. Implement a common messaging format:

   ```python
   import json
   
   # Publish analysis results in a standard format
   message = json.dumps({
       "bot": "bitget_analyzer",
       "timestamp": int(time.time()),
       "data": analyzer.get_last_analysis()
   })
   redis_client.publish("bot_channel", message)
   ```

## Common Error Messages

### "Invalid API Key"

**Cause:** The API key is incorrect or has been revoked.

**Solution:**

1. Regenerate API keys in BitGet account settings
2. Update your configuration with the new keys
3. Verify the keys are correctly formatted (no extra spaces or characters)

### "Request Frequency Exceeds the Limit"

**Cause:** You're sending too many requests and hitting rate limits.

**Solution:**

1. Decrease polling frequency:

   ```python
   await analyzer.start_monitoring(polling_interval=60)  # 60 seconds
   ```

2. Implement rate limiting:

   ```python
   from src.omega_bot_farm.utils.rate_limiter import RateLimiter
   
   rate_limiter = RateLimiter(max_calls=10, period=60)  # 10 calls per minute
   
   async def get_positions_rate_limited():
       async with rate_limiter:
           return await analyzer.get_positions()
   ```

3. Batch requests where possible
4. Implement caching to reduce API calls

### "Connection Refused"

**Cause:** Cannot establish connection to BitGet API.

**Solution:**

1. Check if BitGet API is accessible from your network
2. Verify firewall settings
3. Ensure the correct API endpoint is being used:

   ```python
   analyzer = BitgetPositionAnalyzerB0t(
       use_testnet=True,  # Or False for mainnet
       api_endpoint="https://api.bitget.com"  # Override default endpoint
   )
   ```

### "Position Not Found"

**Cause:** The specified position does not exist or is not accessible.

**Solution:**

1. Verify the position exists in BitGet UI
2. Check if the position ID is correct
3. Ensure the API key has permissions to access positions
4. Fetch all positions first to confirm they're accessible:

   ```python
   all_positions = await analyzer.get_positions()
   print(f"Available positions: {[p.get('id') for p in all_positions.get('positions', [])]}")
   ```

## Logging and Debugging

### Enable Debug Logging

To get more detailed information about what's happening:

```python
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Or configure via the bot
analyzer.set_logging_config(logging_level="DEBUG")
```

### Log to File

To keep a persistent record of operations:

```python
analyzer.set_logging_config(
    logging_level="DEBUG",
    log_to_file=True,
    log_file="logs/bitget_analyzer.log",
    rotate_logs=True
)
```

### Request/Response Logging

To see the exact API requests and responses:

```python
analyzer.set_logging_config(
    log_requests=True,  # Log API requests
    log_responses=True,  # Log API responses
    log_sensitive_data=False  # Don't log API keys
)
```

## Environment Setup

### Python Environment Issues

**Symptoms:**

- Import errors
- Missing module errors

**Solutions:**

1. Verify Python version (3.8+ recommended):

   ```bash
   python --version
   ```

2. Ensure dependencies are installed:

   ```bash
   pip install -r requirements.txt
   ```

3. Check for conflicting packages:

   ```bash
   pip list
   ```

4. Use a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Environment Variables

**Symptoms:**

- Configuration not loading
- Default values being used instead of configured ones

**Solutions:**

1. Verify environment variables are set:

   ```bash
   env | grep BITGET
   ```

2. Check .env file (if using):

   ```bash
   cat .env
   ```

3. Set environment variables in your script:

   ```python
   import os
   
   os.environ["BITGET_API_KEY"] = "your_key"
   os.environ["BITGET_SECRET_KEY"] = "your_secret"
   os.environ["BITGET_PASSPHRASE"] = "your_passphrase"
   ```

## Advanced Troubleshooting

### Creating a Diagnostic Report

To generate a comprehensive diagnostic report:

```python
diagnostics = await analyzer.run_diagnostics()
print(diagnostics["summary"])

# Save detailed report to file
with open("analyzer_diagnostics.json", "w") as f:
    import json
    json.dump(diagnostics, f, indent=2)
```

### Webhook Debug Mode

To debug webhook integrations:

```python
analyzer.set_notification_config(
    notification_channels=["webhook"],
    webhook_url="https://webhook.site/your-unique-url",  # Use a webhook debugging service
    webhook_debug_mode=True  # Add extra debugging info to webhook payloads
)
```

### Mock Mode

To test without making real API calls:

```python
analyzer = BitgetPositionAnalyzerB0t(
    use_mock=True,
    mock_data_file="tests/mock_data/bitget_positions.json"
)

# Or use built-in mock data
analyzer = BitgetPositionAnalyzerB0t(
    use_mock=True,
    mock_scenario="bullish"  # Available: bullish, bearish, mixed, empty
)
```

### Thread and Task Analysis

For asyncio and threading issues:

```python
import asyncio

# Print all running tasks
all_tasks = asyncio.all_tasks()
print(f"Number of running tasks: {len(all_tasks)}")
for task in all_tasks:
    print(f"Task: {task.get_name()}, Done: {task.done()}")

# Enable asyncio debug mode
import logging
logging.getLogger("asyncio").setLevel(logging.DEBUG)
```

## Common Issues by Feature

### Position History Tracking

**Issue:** Position history not updating

**Solution:**

1. Verify `position_history_length` is greater than 0
2. Ensure positions are fetched regularly:

   ```python
   # Set up periodic fetching
   import asyncio
   
   async def periodic_fetch():
       while True:
           await analyzer.get_positions()
           await asyncio.sleep(60)  # Fetch every 60 seconds
   
   # Start the task
   asyncio.create_task(periodic_fetch())
   ```

### Harmony Calculation

**Issue:** Harmony calculations return NaN or errors

**Solution:**

1. Check for division by zero in your position data
2. Ensure account has sufficient balance and positions
3. Initialize with default values to prevent NaN:

   ```python
   analyzer = BitgetPositionAnalyzerB0t(
       default_values={
           "account_balance": 10000,
           "min_position_size": 100
       }
   )
   ```

### Fibonacci Analysis

**Issue:** Fibonacci levels not calculated correctly

**Solution:**

1. Ensure high price is greater than low price
2. Verify price range is significant enough (not too small)
3. Use absolute values for calculations:

   ```python
   fib_levels = analyzer.generate_fibonacci_levels(
       high_price=max(high, low),
       low_price=min(high, low),
       use_absolute_values=True
   )
   ```

## Next Steps

If you've tried the solutions in this troubleshooting guide and still encounter issues:

1. Check the GitHub repository for known issues and updates
2. Review the API documentation for BitGet for any changes
3. Consult the Omega Bot Farm community forum for similar issues
4. Submit a detailed bug report with:
   - Exact error messages
   - Steps to reproduce
   - Environment details
   - Log files (with sensitive information redacted)
   - Configuration (with API keys redacted)

For urgent issues, contact support with diagnostic reports attached.
