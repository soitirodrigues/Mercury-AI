from typing import Dict, Any, List
import numpy as np
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
from mercury_ai.analysis.trade_outcome_engine import TradeOutcomeEngine
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider

class ConfidenceCalibrationAuditor:
    def __init__(self):
        self.logger = DecisionSnapshotLogger()
        self.market_service = MarketDataService(providers=[YahooFinanceProvider()])
        self.outcome_engine = TradeOutcomeEngine()

    def audit(self) -> Dict[str, Any]:
        snapshots = self.logger.list_snapshots()
        if not snapshots:
            return {'status': 'No snapshots'}

        predicted_confidences = []
        outcomes = [] # 1 for WIN, 0 for LOSS

        for path in snapshots:
            data = self.logger.load_snapshot(path)
            
            # Skip if decision was WAIT
            if data['decision_result']['decision'] == 'WAIT':
                continue
            
            # Get current price to evaluate outcome
            try:
                df = self.market_service.get_data(data['asset'])
                current_price = df.iloc[-1]['Close']
            except Exception:
                continue
                
            outcome = self.outcome_engine.determine_outcome(data, current_price)
            if outcome not in ["WIN", "LOSS"]:
                continue
            
            predicted_confidences.append(data['decision_result']['confidence'])
            outcomes.append(1 if outcome == "WIN" else 0)

        if not predicted_confidences:
            return {'status': 'No valid closed trades for calibration'}

        predicted_confidences = np.array(predicted_confidences)
        outcomes = np.array(outcomes)

        # Metrics
        mean_confidence = np.mean(predicted_confidences)
        mean_real_confidence = np.mean(outcomes)
        mean_error = np.mean(np.abs(predicted_confidences - outcomes))
        brier_score = np.mean((predicted_confidences - outcomes) ** 2)

        # Calibration Curve (Binning)
        bins = np.linspace(0, 1, 6) # 0.0, 0.2, 0.4, 0.6, 0.8, 1.0
        calibration_curve = {}
        for i in range(len(bins) - 1):
            mask = (predicted_confidences >= bins[i]) & (predicted_confidences < bins[i+1])
            if np.any(mask):
                calibration_curve[f"{bins[i]:.1f}-{bins[i+1]:.1f}"] = {
                    'mean_confidence': np.mean(predicted_confidences[mask]),
                    'win_rate': np.mean(outcomes[mask])
                }

        return {
            'mean_confidence': mean_confidence,
            'mean_real_confidence': mean_real_confidence,
            'mean_error': mean_error,
            'brier_score': brier_score,
            'calibration_curve': calibration_curve
        }
