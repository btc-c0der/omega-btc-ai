import redis
import json

# Connect to Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Check BTC price
btc_price = r.get('last_btc_price')
print(f'BTC Price: {btc_price}')

# Check BTC movement history
movement_history = r.lrange('btc_movement_history', 0, 5)
print(f'BTC Movement History (first 5 entries): {movement_history}')

# Check candle data for different timeframes
for tf in ['1min', '5min', '15min', '30min', '60min', '240min']:
    candle_data = r.get(f'btc_candle_{tf}')
    print(f'Candle data for {tf}: {candle_data}')

# Check Fibonacci levels
fib_levels = r.get('fibonacci:current_levels')
if fib_levels:
    try:
        levels = json.loads(fib_levels)
        print(f'Fibonacci Levels: {len(levels)} levels available')
        for key, value in list(levels.items())[:5]:
            print(f'  {key}: ${value}')
        if len(levels) > 5:
            print(f'  ... and {len(levels) - 5} more levels')
    except:
        print(f'Fibonacci Levels: Unable to parse JSON')
else:
    print('Fibonacci Levels: None')

# Check trends data
for tf in ['1min', '5min', '15min', '30min', '60min', '240min']:
    trend_data = r.get(f'btc_trend_{tf}')
    if trend_data:
        try:
            trend = json.loads(trend_data)
            print(f'Trend data for {tf}: {trend.get("trend", "Unknown")}, Change: {trend.get("change", 0)}%')
        except:
            print(f'Trend data for {tf}: Unable to parse JSON')
    else:
        print(f'Trend data for {tf}: None')

# Check AI predictions
ai_predictions = r.get('ai_predictions')
if ai_predictions:
    try:
        predictions = json.loads(ai_predictions)
        print(f'AI Predictions available')
        print(f'  Trend: {predictions.get("trend", {}).get("trend", "Unknown")}')
        print(f'  Price: ${predictions.get("price", {}).get("price", 0)}')
        trap_data = predictions.get("trap", {})
        trap_detected = trap_data.get("trap_detected", False)
        trap_type = trap_data.get("trap_type", "Unknown")
        print(f'  Trap: {"Detected - " + trap_type if trap_detected else "None detected"}')
    except:
        print(f'AI Predictions: Unable to parse JSON')
else:
    print('AI Predictions: None') 