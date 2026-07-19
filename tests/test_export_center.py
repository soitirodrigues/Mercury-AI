import pytest
import os
import json
import pandas as pd
from mercury_ai.core.export_center import ExportCenter

def test_export_center_functionality(tmp_path):
    export_dir = tmp_path / "exports"
    ec = ExportCenter(export_dir=str(export_dir))
    
    data = [
        {"id": 1, "value": 10},
        {"id": 2, "value": 20},
        {"id": 3, "value": 30}
    ]
    
    # Test partial export
    ec.export_data(data, "test_partial", ["json"], partial=True)
    assert (export_dir / "test_partial.json").exists()
    
    # Test filtering
    ec.export_data(data, "test_filter", ["csv"], filter_func=lambda x: x["value"] > 15)
    df = pd.read_csv(export_dir / "test_filter.csv")
    assert len(df) == 2
    
    # Test format existence
    ec.export_data(data, "test_formats", ["csv", "json", "zip"])
    assert (export_dir / "test_formats.csv").exists()
    assert (export_dir / "test_formats.json").exists()
    assert (export_dir / "test_formats.zip").exists()
