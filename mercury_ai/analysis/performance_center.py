from typing import Dict, Any
import pandas as pd
from mercury_ai.analysis.performance_analytics import PerformanceAnalytics
from mercury_ai.analysis.performance_statistics import PerformanceStatistics
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
from collections import Counter

class PerformanceCenter:
    """
    Centro de auditoria de performance institucional.
    Consome apenas snapshots e resultados históricos persistidos.
    """
    def __init__(self):
        self.analytics = PerformanceAnalytics()
        self.stats_engine = PerformanceStatistics()
        self.logger = DecisionSnapshotLogger()

    def get_report(self) -> Dict[str, Any]:
        # Dados de trading (Ganhos/Perdas)
        perf_data = self.analytics.analyze_performance()
        stats = self.stats_engine.calculate()
        
        # Dados de decisões (Snapshot)
        snapshots = self.logger.list_snapshots()
        decisions = []
        confidences = []
        buy_probs = []
        sell_probs = []
        wait_probs = []
        
        for path in snapshots:
            data = self.logger.load_snapshot(path)
            res = data['decision_result']
            decisions.append(res['decision'])
            confidences.append(res['confidence'])
            buy_probs.append(res['buy_probability'])
            sell_probs.append(res['sell_probability'])
            wait_probs.append(res['wait_probability'])
            
        # Distribuição
        total = len(decisions)
        counts = Counter(decisions)
        
        # Drawdown simples baseado em diff_pct acumulado
        df_perf = pd.DataFrame(perf_data)
        if 'diff_pct' in df_perf.columns:
            cum_pnl = df_perf['diff_pct'].cumsum()
            running_max = cum_pnl.cummax()
            drawdown = (cum_pnl - running_max).min()
        else:
            drawdown = 0.0
            
        return {
            "Win Rate": f"{stats.get('win_rate', 0):.2f}%",
            "Loss Rate": f"{stats.get('loss_rate', 0):.2f}%",
            "Profit Factor": f"{stats.get('profit_factor', 0):.2f}",
            "Expectancy": f"{stats.get('expectancy', 0):.2f}",
            "Drawdown": f"{drawdown:.2f}%",
            "Média Confidence": f"{sum(confidences)/total if total else 0:.2f}",
            "Média Probability": f"{(sum(buy_probs)+sum(sell_probs)+sum(wait_probs))/(total*3) if total else 0:.2f}",
            "Distribuição BUY": f"{(counts['BUY']/total)*100 if total else 0:.1f}%",
            "Distribuição SELL": f"{(counts['SELL']/total)*100 if total else 0:.1f}%",
            "Distribuição WAIT": f"{(counts['WAIT']/total)*100 if total else 0:.1f}%"
        }
