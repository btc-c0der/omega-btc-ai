#!/bin/bash

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

# OMEGA BTC AI - PostgreSQL Setup & Initialization
# Copyright (c) 2024 OMEGA BTC AI Team
# Licensed under MIT License

set -e

# Color constants
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🔱 OMEGA BTC AI - PostgreSQL Setup${NC}"
echo -e "${GREEN}================================${NC}"

# Check PostgreSQL connection
echo -e "${YELLOW}Checking PostgreSQL connection...${NC}"
if pg_isready -h ${POSTGRES_HOST:-localhost} -p ${POSTGRES_PORT:-5432}; then
    echo -e "${GREEN}✓ PostgreSQL is running${NC}"
else
    echo -e "${RED}❌ PostgreSQL is not running${NC}"
    exit 1
fi

# Create database tables
echo -e "${YELLOW}Creating database tables...${NC}"

PSQL="psql -h ${POSTGRES_HOST:-localhost} -p ${POSTGRES_PORT:-5432} -U ${POSTGRES_USER:-omega_user} -d ${POSTGRES_DB:-omega_db}"

$PSQL << EOF
-- BTC price history
CREATE TABLE IF NOT EXISTS btc_prices (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    btc_price DECIMAL(18,8) NOT NULL,
    volume DECIMAL(18,8) NOT NULL
);

-- Create index on timestamp
CREATE INDEX IF NOT EXISTS idx_btc_prices_timestamp ON btc_prices(timestamp);

-- Subtle price movements
CREATE TABLE IF NOT EXISTS subtle_movements (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    btc_price DECIMAL(18,8) NOT NULL,
    prev_price DECIMAL(18,8) NOT NULL,
    absolute_change DECIMAL(18,8) NOT NULL,
    price_change_percentage DECIMAL(18,8) NOT NULL,
    movement_tag VARCHAR(50) NOT NULL,
    volume DECIMAL(18,8) NOT NULL
);

-- Create index on timestamp and movement_tag
CREATE INDEX IF NOT EXISTS idx_subtle_movements_timestamp ON subtle_movements(timestamp);
CREATE INDEX IF NOT EXISTS idx_subtle_movements_tag ON subtle_movements(movement_tag);

-- Market maker traps
CREATE TABLE IF NOT EXISTS mm_traps (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    trap_type VARCHAR(50) NOT NULL,
    confidence DECIMAL(5,4) NOT NULL,
    price DECIMAL(18,8) NOT NULL,
    price_change DECIMAL(18,8) NOT NULL,
    volume DECIMAL(18,8),
    metadata JSONB
);

-- Create indexes for trap analysis
CREATE INDEX IF NOT EXISTS idx_mm_traps_timestamp ON mm_traps(timestamp);
CREATE INDEX IF NOT EXISTS idx_mm_traps_type ON mm_traps(trap_type);
CREATE INDEX IF NOT EXISTS idx_mm_traps_confidence ON mm_traps(confidence);

-- Performance metrics
CREATE TABLE IF NOT EXISTS performance_metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    metric_name VARCHAR(50) NOT NULL,
    metric_value DECIMAL(18,8) NOT NULL,
    metadata JSONB
);

-- Create indexes for metrics
CREATE INDEX IF NOT EXISTS idx_performance_metrics_timestamp ON performance_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_name ON performance_metrics(metric_name);
EOF

echo -e "${GREEN}✓ Database tables created${NC}"

# Verify tables
echo -e "${YELLOW}Verifying database tables...${NC}"
$PSQL -c "\dt"

echo -e "${GREEN}🚀 PostgreSQL is ready for OMEGA BTC AI${NC}" 