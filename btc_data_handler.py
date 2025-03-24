#!/usr/bin/env python3
"""
OMEGA BTC AI - BTC Data Handler
==============================

Handles BTC data retrieval with Redis as primary source and yfinance as backup.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import redis
import json
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("BTC-Data-Handler")

class BTCDataHandler:
    """Handles BTC data retrieval and storage."""
    
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379, redis_db: int = 0):
        """Initialize the BTC Data Handler."""
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.logger = logging.getLogger("BTC-Data-Handler")
        
    def get_btc_data(self, start_date: str = "2020-01-01", end_date: str | None = None) -> Optional[pd.DataFrame]:
        """
        Get BTC data from Redis or download from yfinance if not available.
        
        Args:
            start_date: Start date for data in YYYY-MM-DD format
            end_date: End date for data in YYYY-MM-DD format
            
        Returns:
            DataFrame with BTC price data or None if loading fails
        """
        try:
            # Try to get data from Redis first
            redis_data = self._get_from_redis(start_date, end_date)
            if redis_data is not None:
                self.logger.info("✅ Successfully retrieved BTC data from Redis")
                return redis_data
            
            # If Redis fails, download from yfinance
            self.logger.info("⚠️ Redis data not available, downloading from yfinance...")
            yf_data = self._download_from_yfinance(start_date, end_date)
            
            if yf_data is not None:
                # Store in Redis for future use
                self._store_in_redis(yf_data)
                return yf_data
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error getting BTC data: {str(e)}")
            return None
    
    def _get_from_redis(self, start_date: str, end_date: str | None = None) -> Optional[pd.DataFrame]:
        """Get BTC data from Redis."""
        try:
            # Get all BTC keys
            btc_keys = self.redis_client.keys("btc:*")
            if not btc_keys:
                return None
            
            # Convert keys to dates and filter by date range
            dates = []
            for key in btc_keys:
                date_str = key.decode().split(":")[1]
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    if start_date and date < datetime.strptime(start_date, "%Y-%m-%d"):
                        continue
                    if end_date and date > datetime.strptime(end_date, "%Y-%m-%d"):
                        continue
                    dates.append(date)
                except ValueError:
                    continue
            
            if not dates:
                return None
            
            # Get data for each date
            data_list = []
            for date in sorted(dates):
                key = f"btc:{date.strftime('%Y-%m-%d')}"
                data = self.redis_client.get(key)
                if data:
                    data_list.append(json.loads(data))
            
            if not data_list:
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(data_list)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            return df
            
        except Exception as e:
            self.logger.error(f"❌ Error getting data from Redis: {str(e)}")
            return None
    
    def _download_from_yfinance(self, start_date: str, end_date: str | None = None) -> Optional[pd.DataFrame]:
        """Download BTC data from yfinance.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: Optional end date in YYYY-MM-DD format
            
        Returns:
            DataFrame with BTC price data or None if loading fails
        """
        try:
            # Ensure start date is not before Bitcoin's genesis (2009-01-03)
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            bitcoin_genesis = datetime.strptime("2009-01-03", "%Y-%m-%d")
            
            # If start date is before 2017, use 2017-01-01 as earliest reliable date
            earliest_available = datetime.strptime("2017-01-01", "%Y-%m-%d")
            if start_dt < earliest_available:
                self.logger.warning(f"⚠️ Start date {start_date} is before earliest reliable data (2017-01-01). Using earliest available date.")
                start_date = "2017-01-01"
            
            # Use provided end_date or current date if not specified
            if end_date is None:
                end_date = datetime.now().strftime("%Y-%m-%d")
            
            # Download data using BTC-USD symbol
            btc = yf.download("BTC-USD", start=start_date, end=end_date, auto_adjust=True)
            
            # Check if data is retrieved
            if btc is None or btc.empty:
                self.logger.warning("No data retrieved from yfinance")
                return None
            
            # Extract columns
            if isinstance(btc.columns, pd.MultiIndex):
                btc.columns = [col[0].lower() for col in btc.columns]
            else:
                btc.columns = [col.lower() for col in btc.columns]
            
            # Ensure index is DatetimeIndex
            if not isinstance(btc.index, pd.DatetimeIndex):
                btc.index = pd.to_datetime(btc.index)
            
            # Sort by date to ensure most recent data is last
            btc = btc.sort_index()
            
            # Filter out any future dates
            current_date = datetime.now()
            btc = btc[btc.index <= current_date]
            
            return btc
            
        except Exception as e:
            self.logger.error(f"❌ Error downloading from yfinance: {str(e)}")
            return None
    
    def _store_in_redis(self, df: pd.DataFrame) -> None:
        """Store DataFrame in Redis.
        
        Args:
            df: DataFrame with BTC data
        """
        try:
            # Ensure DataFrame has a datetime index
            if not isinstance(df.index, pd.DatetimeIndex):
                df.index = pd.to_datetime(df.index)
            
            # Store each row in Redis
            for date, row in df.iterrows():
                # Create key with date
                ts = pd.Timestamp(str(date))  # Convert to Timestamp explicitly
                date_str = ts.strftime('%Y-%m-%d')
                key = f"btc:{date_str}"
                
                # Create data dictionary with date from index
                data = {
                    'date': date_str,
                    'open': float(row['open']),
                    'high': float(row['high']),
                    'low': float(row['low']),
                    'close': float(row['close']),
                    'volume': float(row['volume'])
                }
                
                # Store in Redis
                self.redis_client.set(key, json.dumps(data))
                
        except Exception as e:
            self.logger.error(f"❌ Error storing data in Redis: {str(e)}")
            raise

def main():
    """Test the BTC Data Handler."""
    handler = BTCDataHandler()
    df = handler.get_btc_data()
    
    if df is not None:
        print("Successfully retrieved BTC data:")
        print(df.head())
    else:
        print("Failed to retrieve BTC data")

if __name__ == "__main__":
    main() 