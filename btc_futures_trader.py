import pandas as pd
import logging
from binance.client import Client

logger = logging.getLogger(__name__)

class BtcFuturesTrader:
    def __init__(self, api_key: str, api_secret: str):
        """Initialize the BTC Futures Trader."""
        self.client = Client(api_key, api_secret)
        
    def get_historical_data(self, symbol: str, interval: str, limit: int = 100) -> pd.DataFrame:
        """Get historical klines/candlestick data for a symbol."""
        try:
            klines = self.client.futures_klines(
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            
            if not klines:
                return pd.DataFrame()
            
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_volume', 'trades', 'taker_buy_base',
                'taker_buy_quote', 'ignore'
            ])
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Convert string values to float
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting historical data: {str(e)}")
            return pd.DataFrame() 