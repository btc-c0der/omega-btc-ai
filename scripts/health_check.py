
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

import redis
import psutil
import time
import logging
import smtplib
import argparse
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Redis connection
redis_conn = redis.Redis(host="localhost", port=6379, db=0)

# Email configuration
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_username"
SMTP_PASSWORD = "your_password"
ALERT_EMAIL = "admin@example.com"

def send_alert(subject, message):
    """Send an email alert."""
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = SMTP_USERNAME
        msg['To'] = ALERT_EMAIL

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        logging.info(f"Alert email sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send alert email: {e}")

def check_btc_live_feed(test_mode=False):
    """Check if BTC live feed is running and updating Redis."""
    try:
        # Check if the process is running
        for proc in psutil.process_iter(['name', 'cmdline']):
            if 'python' in proc.info['name'] and 'btc_live_feed.py' in ' '.join(proc.info['cmdline']):
                logging.info("BTC live feed process is running.")
                break
        else:
            error_msg = "BTC live feed process is not running!"
            logging.error(error_msg)
            if not test_mode:
                send_alert("BTC Live Feed Process Down", error_msg)
            return False

        # Check if Redis is being updated
        last_price = redis_conn.get("last_btc_price")
        if not last_price and not test_mode:
            error_msg = "No BTC price data in Redis!"
            logging.error(error_msg)
            send_alert("BTC Price Data Missing", error_msg)
            return False

        last_update_time = redis_conn.get("last_btc_update_time")
        if not last_update_time and not test_mode:
            error_msg = "No last update time in Redis!"
            logging.error(error_msg)
            send_alert("BTC Update Time Missing", error_msg)
            return False

        if not test_mode:
            last_update_time = datetime.fromtimestamp(float(last_update_time))
            if datetime.now() - last_update_time > timedelta(minutes=5):
                error_msg = f"BTC price data is stale. Last update: {last_update_time}"
                logging.error(error_msg)
                send_alert("BTC Price Data Stale", error_msg)
                return False

            logging.info(f"BTC live feed is healthy. Last price: ${float(last_price):.2f}, Last update: {last_update_time}")
        else:
            logging.info("Test mode: Simulating a healthy BTC live feed.")
            send_alert("Test Alert", "This is a test alert from the BTC live feed health check system.")

        return True

    except Exception as e:
        error_msg = f"Error checking BTC live feed: {e}"
        logging.error(error_msg)
        if not test_mode:
            send_alert("BTC Live Feed Check Error", error_msg)
        return False

def main():
    parser = argparse.ArgumentParser(description="BTC Live Feed Health Check")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()

    if args.test:
        logging.info("Running in test mode")
        check_btc_live_feed(test_mode=True)
    else:
        while True:
            check_btc_live_feed()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()