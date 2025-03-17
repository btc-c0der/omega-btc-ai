import smtplib
import json
import requests
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from omega_ai.alerts.rasta_vibes import RastaVibes

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
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7769786963:AAGVAi2VO5BCNGOqeyN2ha4fdzXGhpGjKtk")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ✅ Discord Webhook
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "your-discord-webhook-url")

def send_email_alert(subject, message):
    """Send an email alert about MM Trap Detection."""
    if not EMAIL_ALERTS_ENABLED:
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECIPIENT
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())

        print(f"✅ Email Alert Sent: {subject}")
    except Exception as e:
        print(f"❌ Email Alert Failed: {e}")

def send_telegram_alert(message):
    """Send a Telegram alert about MM Trap Detection."""
    if not TELEGRAM_ALERTS_ENABLED:
        return

    try:
        # 1. Add debug logging
        print(f"🔔 Attempting to send Telegram alert to chat ID: {TELEGRAM_CHAT_ID}")
        
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        # 2. Fix potential formatting issues
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,  # Keep as string from .env
            "text": message,
            "parse_mode": "Markdown"  # Add markdown support
        }
        
        # 3. Add headers and proper content type
        headers = {"Content-Type": "application/json"}
        
        # 4. Use json parameter instead of data for proper JSON encoding
        response = requests.post(telegram_url, json=payload, headers=headers)

        if response.status_code == 200:
            print("✅ Telegram Alert Sent!")
        else:
            # 5. Better error logging
            print(f"❌ Telegram Alert Failed: Status {response.status_code}")
            print(f"❌ Response: {response.text}")
            print(f"❌ Request Payload: {payload}")
    except Exception as e:
        print(f"❌ Telegram Alert Failed: {e}")

def send_discord_alert(message):
    """Send a Discord alert about MM Trap Detection."""
    if not DISCORD_ALERTS_ENABLED:
        return

    try:
        payload = {"content": message}
        response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})

        if response.status_code == 204:
            print("✅ Discord Alert Sent!")
        else:
            print(f"❌ Discord Alert Failed: {response.text}")
    except Exception as e:
        print(f"❌ Discord Alert Failed: {e}")

def send_alert(message, alert_type="OMEGA ALERT"):
    """Send an alert to all configured channels with Rasta vibes."""
    print(f"🔔 ALERT: {message}")
    
    # Enhance message with Rastafarian wisdom
    enhanced_message = RastaVibes.enhance_alert(alert_type, message)
    
    # Send via all enabled channels
    send_email_alert(f"🚨 {alert_type}", enhanced_message)
    send_telegram_alert(enhanced_message)
    send_discord_alert(enhanced_message)

# ✅ Example Usage
if __name__ == "__main__":
    send_alert("⚠️ TEST ALERT: Market Maker Trap Detected at BTC $90235.45!")