from typing import Dict, Any
from mercury_ai.analysis.performance_analytics import PerformanceAnalytics
from mercury_ai.analysis.performance_statistics import PerformanceStatistics
from mercury_ai.analysis.engine_performance_auditor import EnginePerformanceAuditor
from mercury_ai.analysis.confidence_calibration_auditor import ConfidenceCalibrationAuditor

class InstitutionalReportGenerator:
    def __init__(self):
        self.performance = PerformanceAnalytics()
        self.stats = PerformanceStatistics()
        self.engine_auditor = EnginePerformanceAuditor()
        self.calibration = ConfidenceCalibrationAuditor()

    def generate(self) -> Dict[str, Any]:
        perf_data = self.performance.analyze_performance()
        stats_data = self.stats.calculate()
        engine_data = self.engine_auditor.audit_engines()
        calib_data = self.calibration.audit()
        
        # Aggregate data into a single institutional report structure
        return {
            "resumo_executivo": {
                "total_trades": len(perf_data),
                "status": "Estabilizado e Auditado"
            },
            "performance": stats_data,
            "engine_ranking": engine_data,
            "calibracao": calib_data
        }
