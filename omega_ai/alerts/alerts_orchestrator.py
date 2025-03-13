import smtplib
import json
import requests
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

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
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(telegram_url, data=payload)

        if response.status_code == 200:
            print("✅ Telegram Alert Sent!")
        else:
            print(f"❌ Telegram Alert Failed: {response.text}")
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

def send_alert(message):
    """Send an alert to all configured channels."""
    print(f"🔔 ALERT: {message}")

    # Send via all enabled channels
    send_email_alert("🚨 MM Trap Detected!", message)
    send_telegram_alert(message)
    send_discord_alert(message)

# ✅ Example Usage
if __name__ == "__main__":
    send_alert("⚠️ TEST ALERT: Market Maker Trap Detected at BTC $90235.45!")