import datetime
from typing import List, Dict, Tuple
from omega_ai.trading.btc_futures_trader import BtcFuturesTrader, Position
import logging

logger = logging.getLogger(__name__)

class OmegaSuggestionsModule:
    def __init__(self, trader: BtcFuturesTrader):
        self.trader = trader

    def get_open_positions(self) -> List[Dict]:
        """
        Retrieve information about all currently open positions.
        Returns a list of dictionaries, where each dictionary represents an open position.
        """
        try:
            positions = []
            for pos in self.trader.open_positions:
                positions.append({
                    "direction": pos.direction,
                    "entry_price": pos.entry_price,
                    "size": pos.size,
                    "leverage": pos.leverage,
                    "entry_time": pos.entry_time.isoformat(),
                    "take_profits": [tp for tp in pos.take_profits],
                    "stop_loss": pos.stop_loss,
                    "unrealized_pnl": pos.calculate_unrealized_pnl(self.trader.current_price)[0]
                })
            return positions
        except Exception as e:
            logger.error(f"Error getting open positions: {e}")
            return []

    def get_closed_trades(self) -> List[Dict]:
        """
        Retrieve information about all closed trades.
        Returns a list of dictionaries, where each dictionary represents a closed trade.
        """
        try:
            trades = []
            for trade in self.trader.trade_history.trades:
                trades.append({
                    "direction": trade.direction,
                    "entry_price": trade.entry_price,
                    "exit_price": trade.exit_price,
                    "size": trade.size,
                    "leverage": trade.leverage,
                    "entry_time": trade.entry_time.isoformat(),
                    "exit_time": trade.exit_time.isoformat() if trade.exit_time else None,
                    "realized_pnl": trade.realized_pnl
                })
            return trades
        except Exception as e:
            logger.error(f"Error getting closed trades: {e}")
            return []

    def get_trading_performance(self) -> Dict:
        """
        Retrieve the overall trading performance statistics.
        Returns a dictionary containing the performance metrics.
        """
        try:
            return {
                "total_trades": self.trader.trade_history.total_trades,
                "winning_trades": self.trader.trade_history.winning_trades,
                "losing_trades": self.trader.trade_history.losing_trades,
                "total_pnl": self.trader.trade_history.total_pnl,
                "win_rate": self.trader.trade_history.win_rate,
                "average_win": self.trader.trade_history.average_win,
                "average_loss": self.trader.trade_history.average_loss,
                "largest_win": self.trader.trade_history.largest_win,
                "largest_loss": self.trader.trade_history.largest_loss
            }
        except Exception as e:
            logger.error(f"Error getting trading performance: {e}")
            return {}

    def execute(self) -> Dict:
        """
        Execute the OmegaSuggestionsModule and return the consolidated trading position information.
        """
        return {
            "open_positions": self.get_open_positions(),
            "closed_trades": self.get_closed_trades(),
            "trading_performance": self.get_trading_performance()
        }