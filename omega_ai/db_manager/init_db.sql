-- Create the Market Maker (MM) Traps Table
CREATE TABLE IF NOT EXISTS mm_traps (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    btc_price DECIMAL(12,2),
    price_change DECIMAL(6,4),
    trap_type TEXT
);

-- Create the BTC Prices Table
CREATE TABLE IF NOT EXISTS btc_prices (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    btc_price DECIMAL(12,2),
    volume DECIMAL(18,4)
);

-- Create the Schumann Resonance Table
CREATE TABLE IF NOT EXISTS schumann_resonance (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    schumann_value DECIMAL(6,2)
);

-- Create the Alerts Log Table
CREATE TABLE IF NOT EXISTS alerts_log (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    alert_message TEXT
);

-- Create the AI Predictions Table
CREATE TABLE IF NOT EXISTS ai_predictions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    predicted_btc_price DECIMAL(12,2),
    actual_btc_price DECIMAL(12,2),
    confidence_score DECIMAL(5,2)
);
