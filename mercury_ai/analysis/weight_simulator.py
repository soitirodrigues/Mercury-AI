from typing import Dict, Any
from mercury_ai.analysis.engine_performance_auditor import EnginePerformanceAuditor

class WeightSimulator:
    def __init__(self):
        self.auditor = EnginePerformanceAuditor()
        # Default weights from MercuryDecisionEngine
        self.current_weights = {
            "Trend": 0.4, 
            "Structure": 0.3, 
            "Liquidity": 0.2, 
            "Volatility": 0.1
        }

    def simulate(self) -> Dict[str, Any]:
        perf_data = self.auditor.audit_engines()
        report = {}
        
        # System average win rate to determine benchmark
        total_wins = sum(d['wins'] for d in perf_data.values())
        total_trades = sum(d['wins'] + d['losses'] for d in perf_data.values())
        avg_win_rate = (total_wins / total_trades * 100) if total_trades > 0 else 50.0

        for engine, stats in perf_data.items():
            current = self.current_weights.get(engine, 0.05)
            
            # Simple adaptive logic: adjust based on performance relative to average
            win_rate_diff = stats['win_rate'] - avg_win_rate
            adjustment = 1.0 + (win_rate_diff / 100.0)
            suggested = current * adjustment
            
            # Confidence based on number of activations
            conf = min(stats['activations'] / 50.0, 1.0)
            
            report[engine] = {
                'current_weight': current,
                'suggested_weight': round(suggested, 2),
                'reason': f"Win rate {'above' if win_rate_diff > 0 else 'below'} average" if abs(win_rate_diff) > 5 else "Performance neutral",
                'statistical_confidence': round(conf, 2)
            }
            
        return report
