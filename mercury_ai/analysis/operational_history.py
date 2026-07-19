from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
from mercury_ai.analysis.performance_analytics import PerformanceAnalytics
from typing import List, Dict, Any

class OperationalHistory:
    """
    Camada de consulta para histórico operacional baseado em snapshots.
    """
    def __init__(self):
        self.logger = DecisionSnapshotLogger()
        self.analytics = PerformanceAnalytics()
        
    def query(self) -> List[Dict[str, Any]]:
        history = []
        # Get outcomes from performance analytics
        outcomes = { (t['timestamp'], t['asset']): t['result'] for t in self.analytics.analyze_performance() }
        
        for path in self.logger.list_snapshots():
            data = self.logger.load_snapshot(path)
            decision = data['decision_result']
            
            explanation = decision.get('explanation', {})
            if isinstance(explanation, str):
                narrative = explanation
            else:
                narrative = explanation.get('exec_summary', 'N/A')
            
            # Match outcome using timestamp and asset
            key = (data.get('timestamp'), data.get('asset'))
            result = outcomes.get(key, 'OPEN')

            history.append({
                'timestamp': data.get('timestamp'),
                'asset': data.get('asset'),
                'timeframe': data.get('timeframe'),
                'decision': decision.get('decision'),
                'confidence': decision.get('confidence'),
                'probability': {
                    'buy': decision.get('buy_probability'),
                    'sell': decision.get('sell_probability'),
                    'wait': decision.get('wait_probability')
                },
                'narrative': narrative,
                'result': result
            })
        return history
