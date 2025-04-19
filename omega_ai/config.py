
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

"""Configuration settings for the OMEGA AI project."""

# Redis Configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# InfluxDB Configuration
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "your-token"  # Replace with your actual token
INFLUXDB_ORG = "your-org"     # Replace with your actual org
INFLUXDB_BUCKET = "omega_ai"  # Default bucket name

# Monitoring Intervals
MONITORING_INTERVAL = 5  # seconds
ERROR_RETRY_INTERVAL = 10  # seconds

# Price Thresholds
PRICE_PUMP_THRESHOLD = 0.02  # 2%
PRICE_DROP_THRESHOLD = -0.02  # -2%

# Market Analysis Settings
ROLLING_WINDOW = 50  # Number of data points for rolling calculations
VOLATILITY_WINDOW = 24  # Hours for volatility calculation
DIRECTIONAL_STRENGTH_WINDOW = 12  # Hours for directional strength calculation

# High-Frequency Mode Settings
HF_MODE_THRESHOLD = 0.01  # 1% price movement threshold
HF_MODE_WINDOW = 60  # seconds

# Trap Detection Settings
BASE_TRAP_THRESHOLD = 250.0  # Base threshold for trap detection
TRAP_CONFIDENCE_THRESHOLD = 0.7  # Minimum confidence for trap detection

# Database Settings
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "omega_ai"
DB_USER = "postgres"
DB_PASSWORD = "your-password"  # Replace with your actual password

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "omega_ai.log"

# Alert Settings
ALERT_ENABLED = True
ALERT_CHANNEL = "telegram"  # or "email", "slack", etc.
ALERT_THRESHOLD = 0.05  # 5% price movement threshold

# Visualization Settings
DASHBOARD_PORT = 8050
DASHBOARD_HOST = "localhost"
DASHBOARD_DEBUG = False 