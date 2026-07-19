from mercury_ai.analysis.institutional_report_generator import InstitutionalReportGenerator

def test_institutional_report_generator():
    generator = InstitutionalReportGenerator()
    report = generator.generate()
    
    assert isinstance(report, dict)
    assert 'resumo_executivo' in report
    assert 'performance' in report
    assert 'engine_ranking' in report
    assert 'calibracao' in report
    
    assert report['resumo_executivo']['status'] == "Estabilizado e Auditado"
