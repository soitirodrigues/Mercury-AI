import pytest
import pandas as pd
import numpy as np
from mercury_ai.analysis.data_quality_engine import DataQualityEngine

def test_data_quality_engine_perfect_data():
    engine = DataQualityEngine()
    index = pd.date_range(start="2025-01-01", periods=5, freq="1min")
    df = pd.DataFrame({
        'Open': [10, 11, 12, 13, 14],
        'High': [12, 13, 14, 15, 16],
        'Low': [9, 10, 11, 12, 13],
        'Close': [11, 12, 13, 14, 15],
        'Volume': [100, 100, 100, 100, 100]
    }, index=index)
    
    report = engine.generate_report(df)
    assert report.quality_score == 1.0
    assert report.missing_candles == 0

def test_data_quality_engine_issues():
    engine = DataQualityEngine()
    # Data with gap, duplicity, NaN, and high < low
    index = pd.to_datetime(["2025-01-01 00:00:00", "2025-01-01 00:05:00", "2025-01-01 00:05:00"])
    df = pd.DataFrame({
        'Open': [10, 11, 11],
        'High': [12, 10, 10], # High < Low (10 < 13 later)
        'Low': [9, 13, 13],
        'Close': [11, 12, np.nan], # NaN
        'Volume': [100, 0, 100] # Volume <= 0
    }, index=index)
    
    report = engine.generate_report(df)
    assert report.quality_score < 1.0
    assert report.missing_candles > 0
    assert report.duplicity_issues == 1
    assert report.integrity_issues == 1
    assert report.volume_issues == 1
    assert report.consistency_issues == 2
