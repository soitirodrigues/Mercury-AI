from mercury_ai.analysis.data_exporter import DataExporter
from pathlib import Path
import shutil

def test_data_exporter():
    test_dir = Path("tests/exports")
    if test_dir.exists():
        shutil.rmtree(test_dir)
        
    exporter = DataExporter(export_dir="tests/exports")
    exporter.export_all()
    
    assert (test_dir / "history.json").exists()
    assert (test_dir / "history.csv").exists()
    assert (test_dir / "snapshots.json").exists()
    assert (test_dir / "history.zip").exists()
    
    # Cleanup
    shutil.rmtree(test_dir)
