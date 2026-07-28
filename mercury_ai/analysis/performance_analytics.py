from typing import List, Dict, Any
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider
from mercury_ai.core.exceptions import MarketClosedException
from datetime import datetime

class PerformanceAnalytics:
    def __init__(self):
        self.logger = DecisionSnapshotLogger()
        self.market_service = MarketDataService(providers=[YahooFinanceProvider()])

    def analyze_performance(self) -> List[Dict[str, Any]]:
        performance_report = []
        snapshots = self.logger.list_snapshots()
        
        for path in snapshots:
            data = self.logger.load_snapshot(path)
            symbol = data['asset']
            entry_time = datetime.fromisoformat(data['timestamp'])
            
            # Get historical data for trade analysis
            try:
                df = self.market_service.get_data(symbol)
            except (KeyError, IndexError, ValueError, ConnectionError, RuntimeError, MarketClosedException):
                continue  # Skip if data cannot be retrieved
            
            # Normalize entry_time to match df index timezone
            entry_time = datetime.fromisoformat(data['timestamp'])
            if df.index.tz is not None:
                entry_time = entry_time.replace(tzinfo=df.index.tz)
            
            trade_df = df[df.index >= entry_time]
            
            if trade_df.empty:
                result = "OPEN"
                diff_pct = 0.0
                mae = 0.0
                mfe = 0.0
                duration = 0.0
                entry_price = 0.0
                exit_price = 0.0
            else:
                entry_price = trade_df.iloc[0]['Close']
                exit_price = trade_df.iloc[-1]['Close']
                diff_pct = ((exit_price - entry_price) / entry_price) * 100
                
                # MAE/MFE
                highs = trade_df['High']
                lows = trade_df['Low']
                
                if data['decision_result']['decision'] == 'BUY':
                    mfe = ((highs.max() - entry_price) / entry_price) * 100
                    mae = ((entry_price - lows.min()) / entry_price) * 100
                    result = "GAIN" if diff_pct > 0 else "LOSS"
                elif data['decision_result']['decision'] == 'SELL':
                    mfe = ((entry_price - lows.min()) / entry_price) * 100
                    mae = ((highs.max() - entry_price) / entry_price) * 100
                    result = "GAIN" if diff_pct < 0 else "LOSS"
                else:
                    result = "OPEN"
                    mfe = 0.0
                    mae = 0.0
                
                duration = (trade_df.index[-1] - trade_df.index[0]).total_seconds() / 3600 # hours

            performance_report.append({
                'timestamp': data['timestamp'],
                'asset': symbol,
                'timeframe': data['timeframe'],
                'decision': data['decision_result']['decision'],
                'entry_price': entry_price,
                'current_price': exit_price,
                'diff_pct': diff_pct,
                'result': result,
                'mae': mae,
                'mfe': mfe,
                'duration_hours': duration
            })
            
        return performance_report
