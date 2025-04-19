
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

import smtplib
import json
import requests
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
import redis

# ✅ Load Environment Variables
load_dotenv()

# ✅ Alert Configurations
EMAIL_ALERTS_ENABLED = os.getenv("EMAIL_ALERTS_ENABLED", "false").lower() == "true"
TELEGRAM_ALERTS_ENABLED = os.getenv("TELEGRAM_ALERTS_ENABLED", "false").lower() == "true"
DISCORD_ALERTS_ENABLED = os.getenv("DISCORD_ALERTS_ENABLED", "false").lower() == "true"

# ✅ Email Settings
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your-email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-email-password")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "recipient-email@gmail.com")

# ✅ Telegram Bot Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your-telegram-bot-token")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "your-chat-id")

# ✅ Discord Webhook
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "your-discord-webhook-url")

# ✅ Redis Connection
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

def send_email_alert(subject, message, is_trap=False):
    """Send an email alert about MM Trap Detection."""
    if not EMAIL_ALERTS_ENABLED:
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECIPIENT
        
        # Special formatting for traps
        if is_trap:
            subject = f"🚨 URGENT: {subject}"
            
        msg["Subject"] = subject
        
        # HTML-formatted message for better visibility if it's a trap
        if is_trap:
            html_message = f"""
            <html>
            <head>
                <style>
                    .trap-alert {{
                        background-color: #ffebee;
                        border-left: 5px solid #f44336;
                        padding: 15px;
                        margin-bottom: 20px;
                    }}
                    .trap-details {{
                        font-family: monospace;
                        background-color: #f5f5f5;
                        padding: 10px;
                        border-radius: 4px;
                    }}
                    .trap-price {{
                        font-weight: bold;
                        color: #d32f2f;
                    }}
                    .trap-time {{
                        color: #757575;
                        font-size: 0.9em;
                    }}
                </style>
            </head>
            <body>
                <div class="trap-alert">
                    <h2>🚨 Market Maker Trap Detected!</h2>
                    <p>{message}</p>
                </div>
                <div class="trap-details">
                    <p>Detection Time: <span class="trap-time">{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</span></p>
                </div>
            </body>
            </html>
            """
            msg.attach(MIMEText(html_message, "html"))
        else:
            msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())

        print(f"✅ Email Alert Sent: {subject}")
    except Exception as e:
        print(f"❌ Email Alert Failed: {e}")

def send_telegram_alert(message, is_trap=False):
    """Send a Telegram alert about MM Trap Detection."""
    if not TELEGRAM_ALERTS_ENABLED:
        return

    try:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        # Format message with emojis and bold text for traps
        if is_trap:
            formatted_message = f"""
🚨 *MARKET MAKER TRAP DETECTED* 🚨

{message}

⏰ *Detection Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
            payload = {
                "chat_id": TELEGRAM_CHAT_ID, 
                "text": formatted_message,
                "parse_mode": "Markdown"
            }
        else:
            payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
            
        response = requests.post(telegram_url, data=payload)

        if response.status_code == 200:
            print("✅ Telegram Alert Sent!")
        else:
            print(f"❌ Telegram Alert Failed: {response.text}")
    except Exception as e:
        print(f"❌ Telegram Alert Failed: {e}")

def send_discord_alert(message, is_trap=False):
    """Send a Discord alert about MM Trap Detection."""
    if not DISCORD_ALERTS_ENABLED:
        return

    try:
        # Special formatting for traps in Discord with embeds
        if is_trap:
            payload = {
                "content": "🚨 **MARKET MAKER TRAP DETECTED** 🚨",
                "embeds": [
                    {
                        "title": "Market Maker Trap Alert",
                        "description": message,
                        "color": 16711680,  # Red color
                        "footer": {
                            "text": f"Detection Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
                        }
                    }
                ]
            }
        else:
            payload = {"content": message}
            
        response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})

        if response.status_code == 204:
            print("✅ Discord Alert Sent!")
        else:
            print(f"❌ Discord Alert Failed: {response.text}")
    except Exception as e:
        print(f"❌ Discord Alert Failed: {e}")

def send_alert(message):
    """Send a general alert to all configured channels."""
    print(f"🔔 ALERT: {message}")

    # Send via all enabled channels
    send_email_alert("OmegaBTC Alert", message)
    send_telegram_alert(message)
    send_discord_alert(message)

def send_mm_trap_alert(trap_data):
    """
    Send a specialized alert for Market Maker traps with enhanced formatting.
    
    Args:
        trap_data: Dictionary containing trap information
            - trap_type: Type of manipulation ('stop_hunt', 'liquidity_grab', etc.)
            - btc_price: Price at which trap occurred
            - price_change: Percentage price change that triggered the trap
            - confidence: Confidence score of the detection (0.0-1.0)
            - liquidity_grabbed: Amount of liquidity grabbed in the trap
    """
    trap_type = trap_data.get("trap_type", "Unknown")
    price = trap_data.get("btc_price", 0)
    confidence = trap_data.get("confidence", 0)
    price_change = trap_data.get("price_change", 0)
    liquidity = trap_data.get("liquidity_grabbed", 0)
    
    # Create a standardized message with all important details
    message = f"""
⚠️ MM TRAP DETECTED: {trap_type.upper()} ⚠️

• BTC Price: ${price:,.2f}
• Price Change: {price_change:.2%}
• Confidence: {confidence:.2f}
• Liquidity Grabbed: ${liquidity:,.2f}

This appears to be a Market Maker manipulation event.
Take caution with your trading decisions.
"""
    
    print(f"🚨 MM TRAP ALERT: {trap_type} at ${price:,.2f}")

    # Send specialized alerts with trap formatting
    send_email_alert(f"MM Trap: {trap_type} at ${price:,.2f}", message, is_trap=True)
    send_telegram_alert(message, is_trap=True)
    send_discord_alert(message, is_trap=True)
    
    # Store in Redis for tracking recent alerts
    alert_key = f"recent_mm_trap_alerts"
    trap_summary = json.dumps({
        "type": trap_type,
        "price": price,
        "confidence": confidence,
        "timestamp": datetime.now().isoformat()
    })
    
    # Use a sorted set with timestamp as score for chronological order
    timestamp = datetime.now().timestamp()
    redis_client.zadd(alert_key, {trap_summary: timestamp})
    
    # Keep only the most recent 50 alerts
    redis_client.zremrangebyrank(alert_key, 0, -51)

def get_recent_trap_alerts(limit=10):
    """
    Get most recent MM trap alerts from Redis.
    
    Args:
        limit: Maximum number of recent alerts to retrieve
        
    Returns:
        List of recent trap alert dictionaries
    """
    alert_key = "recent_mm_trap_alerts"
    recent_alerts_json = redis_client.zrevrange(alert_key, 0, limit-1)
    
    if not recent_alerts_json:
        return []
        
    try:
        return [json.loads(alert) for alert in recent_alerts_json]
    except Exception as e:
        print(f"Error parsing recent alerts: {e}")
        return []

# ✅ Example Usage
if __name__ == "__main__":
    # Example general alert
    send_alert("⚠️ TEST ALERT: Important system notification!")
    
    # Example MM trap alert
    example_trap = {
        "trap_type": "liquidity_grab",
        "btc_price": 90235.45,
        "price_change": 0.0325,
        "confidence": 0.92,
        "liquidity_grabbed": 15750.25
    }
    send_mm_trap_alert(example_trap)