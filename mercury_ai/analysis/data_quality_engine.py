import pandas as pd
import numpy as np
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class QualityReport:
    missing_candles: int = 0
    price_gaps: int = 0
    delay_seconds: float = 0.0
    volume_issues: int = 0
    integrity_issues: int = 0
    consistency_issues: int = 0
    duplicity_issues: int = 0
    quality_score: float = 1.0

class DataQualityEngine:
    def calculate_score(self, df: pd.DataFrame) -> float:
        report = self.generate_report(df)
        return report.quality_score

    def generate_report(self, df: pd.DataFrame) -> QualityReport:
        if df.empty:
            return QualityReport(quality_score=0.0)

        # 1. Missing candles (assuming 1 minute frequency)
        missing_candles = (df.index.to_series().diff() > pd.Timedelta(minutes=1)).sum()
        
        # 2. Gaps (price jumps > 3 std devs)
        price_diff = df['Close'].diff().abs()
        price_std = df['Close'].std()
        price_gaps = (price_diff > (3 * price_std)).sum() if price_std > 0 else 0
        
        # 3. Delay
        delay = (datetime.now() - df.index.max()).total_seconds()
        
        # 4. Volume issues
        volume_issues = (df['Volume'] <= 0).sum()
        
        # 5. Integrity issues (NaNs)
        integrity_issues = df.isna().sum().sum()
        
        # 6. Consistency (High < Low)
        consistency_issues = (df['High'] < df['Low']).sum()
        
        # 7. Duplicity
        duplicity_issues = df.index.duplicated().sum()
        
        # Calculate score (normalized, simplified)
        total_issues = missing_candles + price_gaps + volume_issues + integrity_issues + consistency_issues + duplicity_issues
        quality_score = max(0.0, 1.0 - (total_issues / (len(df) + 1)))
        
        return QualityReport(
            missing_candles=int(missing_candles),
            price_gaps=int(price_gaps),
            delay_seconds=float(delay),
            volume_issues=int(volume_issues),
            integrity_issues=int(integrity_issues),
            consistency_issues=int(consistency_issues),
            duplicity_issues=int(duplicity_issues),
            quality_score=float(quality_score)
        )
