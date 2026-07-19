from typing import Dict, Any
from mercury_ai.analysis.performance_analytics import PerformanceAnalytics

class PerformanceStatistics:
    def __init__(self):
        self.analytics = PerformanceAnalytics()

    def calculate(self) -> Dict[str, Any]:
        report = self.analytics.analyze_performance()
        closed_trades = [t for t in report if t['result'] in ['GAIN', 'LOSS']]
        
        if not closed_trades:
            return {'status': 'No closed trades'}
        
        wins = [t['diff_pct'] for t in closed_trades if t['result'] == 'GAIN']
        losses = [t['diff_pct'] for t in closed_trades if t['result'] == 'LOSS']
        
        num_wins = len(wins)
        num_losses = len(losses)
        total_trades = num_wins + num_losses
        
        avg_winner = sum(wins) / num_wins if num_wins > 0 else 0
        avg_loser = sum(losses) / num_losses if num_losses > 0 else 0
        
        return {
            'win_rate': (num_wins / total_trades) * 100,
            'loss_rate': (num_losses / total_trades) * 100,
            'profit_factor': sum(wins) / abs(sum(losses)) if abs(sum(losses)) > 0 else float('inf'),
            'expectancy': ((num_wins / total_trades) * avg_winner) - ((num_losses / total_trades) * abs(avg_loser)),
            'avg_winner': avg_winner,
            'avg_loser': avg_loser,
            'largest_winner': max(wins) if wins else 0,
            'largest_loser': min(losses) if losses else 0,
            'avg_holding_time': sum(t['duration_hours'] for t in report) / len(report)
        }
