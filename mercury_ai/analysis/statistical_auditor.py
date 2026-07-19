from typing import List, Dict, Any
from collections import Counter
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger

class StatisticalAuditor:
    def __init__(self):
        self.logger = DecisionSnapshotLogger()

    def audit(self) -> Dict[str, Any]:
        snapshots = self.logger.list_snapshots()
        if not snapshots:
            return {}

        decisions = []
        confidences = []
        probs = {'buy': [], 'sell': [], 'wait': []}
        risks = []
        regimes = []

        for path in snapshots:
            data = self.logger.load_snapshot(path)
            
            # Decision
            decisions.append(data['decision_result']['decision'])
            
            # Confidence
            confidences.append(data['decision_result']['confidence'])
            
            # Probability
            probs['buy'].append(data['decision_result']['buy_probability'])
            probs['sell'].append(data['decision_result']['sell_probability'])
            probs['wait'].append(data['decision_result']['wait_probability'])
            
            # Risk
            risks.append(data['decision_result']['expected_risk'])
            
            # Regime
            if data['context'] and 'market_regime' in data['context'] and data['context']['market_regime']:
                regimes.append(data['context']['market_regime']['regime'])

        total = len(decisions)
        counts = Counter(decisions)
        
        return {
            'buy_pct': (counts['BUY'] / total) * 100,
            'sell_pct': (counts['SELL'] / total) * 100,
            'wait_pct': (counts['WAIT'] / total) * 100,
            'avg_confidence': sum(confidences) / total,
            'avg_buy_prob': sum(probs['buy']) / total,
            'avg_sell_prob': sum(probs['sell']) / total,
            'avg_wait_prob': sum(probs['wait']) / total,
            'avg_risk': sum(risks) / total,
            'frequent_regimes': Counter(regimes).most_common(3)
        }
