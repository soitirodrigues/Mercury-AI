from typing import List, Dict, Any
from collections import defaultdict
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
from mercury_ai.analysis.performance_analytics import PerformanceAnalytics
from mercury_ai.analysis.trade_outcome_engine import TradeOutcomeEngine

class EnginePerformanceAuditor:
    def __init__(self):
        self.logger = DecisionSnapshotLogger()
        self.analytics = PerformanceAnalytics()

    def audit_engines(self) -> Dict[str, Dict[str, Any]]:
        performance_data = {t['timestamp'] + t['asset']: t for t in self.analytics.analyze_performance()}
        snapshots = self.logger.list_snapshots()
        
        engine_stats = defaultdict(lambda: {
            'activations': 0, 'wins': 0, 'losses': 0, 
            'total_contribution': 0.0, 'total_confidence': 0.0
        })
        
        for path in snapshots:
            data = self.logger.load_snapshot(path)
            key = data['timestamp'] + data['asset']
            perf = performance_data.get(key)
            
            if not perf or perf['result'] not in ['GAIN', 'LOSS']:
                continue
            
            is_win = 1 if perf['result'] == 'GAIN' else 0
            evidences = data['evidence_bundle']['evidences']
            
            for ev in evidences:
                engine_name = ev['engine_name']
                stats = engine_stats[engine_name]
                
                stats['activations'] += 1
                if is_win:
                    stats['wins'] += 1
                else:
                    stats['losses'] += 1
                    
                stats['total_contribution'] += ev.get('contribution_score', 0.0)
                stats['total_confidence'] += ev.get('confidence', 0.0)
        
        final_report = {}
        for engine, stats in engine_stats.items():
            total = stats['wins'] + stats['losses']
            final_report[engine] = {
                'activations': stats['activations'],
                'wins': stats['wins'],
                'losses': stats['losses'],
                'win_rate': (stats['wins'] / total * 100) if total > 0 else 0,
                'avg_contribution': stats['total_contribution'] / stats['activations'] if stats['activations'] > 0 else 0,
                'avg_confidence': stats['total_confidence'] / stats['activations'] if stats['activations'] > 0 else 0
            }
            
        return final_report
