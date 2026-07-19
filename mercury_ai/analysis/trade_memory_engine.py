import pandas as pd
import os
from typing import Dict, Any
from mercury_ai.models.trade_memory import TradeMemory

class TradeMemoryEngine:
    """
    Motor institucional de memória estatística de trades.
    """
    
    FILE_PATH = "trade_history.csv"

    def save_trade(self, trade: TradeMemory):
        # Salva trade em arquivo CSV para persistência
        file_exists = os.path.isfile(self.FILE_PATH)
        df = pd.DataFrame([trade.__dict__])
        df.to_csv(self.FILE_PATH, mode='a', index=False, header=not file_exists)

    def find_similar_trades(self, current_regime: str, current_bias: str) -> Dict[str, Any]:
        if not os.path.isfile(self.FILE_PATH):
            return {"count": 0, "win_rate": 0, "expectancy": 0}
            
        df = pd.read_csv(self.FILE_PATH)
        similar = df[(df['regime'] == current_regime)]
        
        if len(similar) == 0:
            return {"count": 0, "win_rate": 0, "expectancy": 0}
            
        total = len(similar)
        wins = len(similar[similar['result'].str.endswith('_CORRETO')])
        win_rate = wins / total
        expectancy = similar['profit'].mean()
        
        return {
            "count": total,
            "win_rate": win_rate * 100,
            "expectancy": expectancy,
            "avg_mae": similar['mae'].mean(),
            "avg_mfe": similar['mfe'].mean()
        }
