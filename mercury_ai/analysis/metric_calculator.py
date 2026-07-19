from dataclasses import dataclass
from typing import List, Dict
import numpy as np

@dataclass(frozen=True)
class PerformanceMetrics:
    accuracy: float
    precision_buy: float
    precision_sell: float
    recall: float
    f1_score: float
    balanced_accuracy: float
    mcc: float
    profit_factor: float
    expectancy: float
    win_rate: float
    avg_win: float
    avg_loss: float
    max_drawdown: float
    sharpe_simplified: float
    score_distribution: Dict[str, float]

class MetricCalculator:
    @staticmethod
    def calculate(decisions: List[str], outcomes: List[float], scores: List[float]) -> PerformanceMetrics:
        # Assuming outcomes are % P/L
        
        # Classification
        tp = sum(1 for d, o in zip(decisions, outcomes) if d == "BUY" and o > 0)
        tn = sum(1 for d, o in zip(decisions, outcomes) if d == "SELL" and o < 0)
        fp = sum(1 for d, o in zip(decisions, outcomes) if d == "BUY" and o <= 0)
        fn = sum(1 for d, o in zip(decisions, outcomes) if d == "SELL" and o >= 0)
        
        accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0.0
        precision_buy = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        precision_sell = tn / (tn + fn) if (tn + fn) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        
        f1_score = 2 * (precision_buy * recall) / (precision_buy + recall) if (precision_buy + recall) > 0 else 0.0
        balanced_accuracy = ((tp / (tp + fn)) + (tn / (tn + fp))) / 2 if (tp + fn) > 0 and (tn + fp) > 0 else 0.0
        
        # MCC
        denom = np.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
        mcc = (tp*tn - fp*fn) / denom if denom > 0 else 0.0
        
        # Trading metrics
        wins = [o for o in outcomes if o > 0]
        losses = [o for o in outcomes if o < 0]
        
        total_win = sum(wins)
        total_loss = abs(sum(losses))
        
        profit_factor = total_win / total_loss if total_loss > 0 else float('inf')
        win_rate = len(wins) / len(outcomes) if len(outcomes) > 0 else 0.0
        
        avg_win = sum(wins) / len(wins) if len(wins) > 0 else 0.0
        avg_loss = abs(sum(losses)) / len(losses) if len(losses) > 0 else 0.0
        expectancy = (win_rate * avg_win) - ((1 - win_rate) * avg_loss)
        
        # Drawdown
        cumulative = np.cumsum(outcomes)
        peak = np.maximum.accumulate(cumulative)
        drawdown = peak - cumulative
        max_drawdown = np.max(drawdown) if len(drawdown) > 0 else 0.0
        
        # Sharpe
        sharpe = (np.mean(outcomes) / np.std(outcomes)) * np.sqrt(252) if np.std(outcomes) > 0 else 0.0
        
        # Distribution
        hist, bins = np.histogram(scores, bins=10)
        distribution = {f"{bins[i]:.2f}-{bins[i+1]:.2f}": float(hist[i]) for i in range(len(hist))}
        
        return PerformanceMetrics(
            accuracy=accuracy, precision_buy=precision_buy, precision_sell=precision_sell,
            recall=recall, f1_score=f1_score, balanced_accuracy=balanced_accuracy,
            mcc=mcc, profit_factor=profit_factor, expectancy=expectancy,
            win_rate=win_rate, avg_win=avg_win, avg_loss=avg_loss,
            max_drawdown=max_drawdown, sharpe_simplified=sharpe,
            score_distribution=distribution
        )
