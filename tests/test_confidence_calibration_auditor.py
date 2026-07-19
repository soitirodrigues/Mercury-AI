from mercury_ai.analysis.confidence_calibration_auditor import ConfidenceCalibrationAuditor

def test_confidence_calibration_auditor():
    auditor = ConfidenceCalibrationAuditor()
    results = auditor.audit()
    
    # Check if the result is either a valid dict or the 'no snapshots' status
    if 'status' in results:
        assert results['status'] in ['No snapshots', 'No valid closed trades for calibration']
    else:
        assert 'mean_confidence' in results
        assert 'mean_real_confidence' in results
        assert 'brier_score' in results
        assert 'calibration_curve' in results
        assert 0 <= results['brier_score'] <= 1
