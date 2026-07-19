import pytest
from mercury_ai.utils.performance_collector import PerformanceCollector
import time

def test_performance_collector_integration():
    collector = PerformanceCollector("TestPipeline")
    
    with collector.stage("Stage1"):
        time.sleep(0.01)
        with collector.stage("NestedStage"):
            time.sleep(0.02)
            
    with collector.stage("Stage2"):
        time.sleep(0.03)
        
    pipeline_metric, hotspot_report = collector.collect()
    
    assert pipeline_metric.pipeline_name == "TestPipeline"
    assert len(pipeline_metric.stage_metrics) == 2
    assert pipeline_metric.stage_metrics[0].name == "Stage1"
    assert len(pipeline_metric.stage_metrics[0].nested_metrics) == 1
    assert pipeline_metric.stage_metrics[0].nested_metrics[0].name == "NestedStage"
    assert len(hotspot_report.hotspots) == 3
    assert hotspot_report.hotspots[0] in ["Stage1", "Stage2"] # Should be the longest
    assert pipeline_metric.total_duration > 0
    assert pipeline_metric.stage_metrics[0].percentage_total > 0
