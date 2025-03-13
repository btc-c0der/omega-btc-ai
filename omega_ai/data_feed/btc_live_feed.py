import asyncio
import json
import psycopg2
import redis
import time
import websocket
import websockets
import logging
from datetime import datetime, UTC

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Binance WebSocket API
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"

# MM WebSocket Server URL
MM_WS_URL = "ws://localhost:8765"

# PostgreSQL Database Connection
DB_CONFIG = {
    "dbname": "omega_db",
    "user": "omega_user",
    "password": "omega_pass",
    "host": "localhost",
    "port": "5432"
}

# Redis Connection
redis_conn = redis.Redis(host="localhost", port=6379, db=0)

def check_redis_health():
    """Perform a health check on Redis connection and data integrity."""
    try:
        # Check Redis connection
        redis_conn.ping()
        logging.info("Redis connection: OK")

        # Check if essential keys exist
        essential_keys = ["last_btc_price", "prev_btc_price", "btc_movement_history"]
        for key in essential_keys:
            if not redis_conn.exists(key):
                logging.warning(f"Essential key missing: {key}")
            else:
                logging.info(f"Essential key present: {key}")

        # Check data integrity
        btc_movement_history = redis_conn.llen("btc_movement_history")
        logging.info(f"BTC movement history length: {btc_movement_history}")

        return True
    except redis.RedisError as e:
        logging.error(f"Redis health check failed: {e}")
        return False

async def send_to_mm_websocket(price):
    """Send BTC price update to MM Trap WebSocket."""
    while True:
        try:
            async with websockets.connect(
                MM_WS_URL,
                max_size=2**20,
                ping_interval=30,
                ping_timeout=10
            ) as ws:
                logging.info(f"Connected to MM WebSocket")
                await ws.send(json.dumps({"btc_price": price}))
                logging.info(f"BTC Price Sent: ${price:.2f}")
                return  # Exit loop on success
        except websockets.exceptions.ConnectionClosedOK:
            logging.info(f"WebSocket Closed Normally, reconnecting...")
        except websockets.exceptions.ConnectionClosedError as e:
            logging.error(f"WebSocket Disconnected (Error {e.code}), retrying...")
        except Exception as e:
            logging.error(f"WebSocket Error: {e}, retrying...")
        
        await asyncio.sleep(5)  # Persistent retry mechanism

def save_btc_price_to_db(price, volume):
    """Store BTC price in PostgreSQL for historical tracking."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO btc_prices (timestamp, btc_price, volume) VALUES (%s, %s, %s)",
            (datetime.now(UTC), price, volume)
        )
        conn.commit()
        cursor.close()
        conn.close()
        logging.info(f"Saved BTC price to DB: ${price:.2f}")
    except Exception as e:
        logging.error(f"Failed to save BTC price to DB: {e}")

def update_redis(price, volume):
    """Save BTC price & volume to Redis for MM Trap Processor with error handling."""
    try:
        if price <= 0:
            logging.warning(f"Skipping Redis update, invalid BTC price: {price}")
            return

        prev_price = redis_conn.get("prev_btc_price")
        prev_price = float(prev_price) if prev_price else None  

        if prev_price is None or price != prev_price:
            pipeline = redis_conn.pipeline()
            pipeline.set("last_btc_price", price)
            pipeline.set("last_btc_volume", volume if volume else 0)
            pipeline.rpush("btc_movement_history", price)
            pipeline.rpush("btc_volume_history", volume)
            pipeline.ltrim("btc_movement_history", -100, -1)
            pipeline.ltrim("btc_volume_history", -100, -1)
            
            abs_change = abs(price - prev_price) if prev_price is not None else 0
            abs_change_scaled = abs_change * 100
            pipeline.rpush("abs_price_change_history", abs_change_scaled)
            pipeline.ltrim("abs_price_change_history", -100, -1)
            pipeline.set("prev_btc_price", price)
            
            # Add last update time
            pipeline.set("last_btc_update_time", time.time())
            
            pipeline.execute()
            
            logging.info(f"Redis Updated: BTC Price = {price:.2f}, Volume = {volume}, Abs Change = {abs_change_scaled:.2f}")
        else:
            logging.debug(f"Price Unchanged, Skipping Redis Update: {price}")

    except redis.RedisError as e:
        logging.error(f"Redis Update Failed: {e}")
        # Attempt to reconnect
        try:
            redis_conn.ping()
        except:
            logging.error("Redis reconnection failed. Attempting to recreate connection.")
            global redis_conn
            redis_conn = redis.Redis(host="localhost", port=6379, db=0)

def on_message(ws, message):
    """Process incoming Binance BTC price data."""
    data = json.loads(message)
    price = float(data["p"])
    volume = float(data["q"])

    logging.info(f"LIVE BTC PRICE UPDATE: ${price:.2f}")

    save_btc_price_to_db(price, volume)
    update_redis(price, volume)
    asyncio.run(send_to_mm_websocket(price))

def on_error(ws, error):
    logging.error(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    logging.warning(f"WebSocket Closed: {close_status_code} - {close_msg}")
    time.sleep(5)
    start_btc_websocket()

def on_open(ws):
    logging.info("Connected to Binance WebSocket - Streaming BTC Prices...")

def start_btc_websocket():
    """Start WebSocket connection to Binance BTC Live Feed."""
    while True:
        try:
            if not check_redis_health():
                logging.error("Redis health check failed. Retrying in 60 seconds...")
                time.sleep(60)
                continue

            ws = websocket.WebSocketApp(
                BINANCE_WS_URL,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open
            )
            ws.run_forever()
        except Exception as e:
            logging.error(f"Error in WebSocket connection: {e}")
            time.sleep(5)

if __name__ == "__main__":
    start_btc_websocket()