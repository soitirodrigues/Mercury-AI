import pytest
import os
from mercury_ai.analysis.notification_center import NotificationCenter

def test_notification_center_features():
    nc = NotificationCenter()
    nc.send("Scanner", "Scanner started")
    nc.send("Error", "Provider down")
    nc.send("Health", "Health OK")
    
    # Test History
    assert len(nc.get_history()) == 3
    
    # Test Filter
    assert len(nc.get_history(filter_type="Scanner")) == 1
    
    # Test Search
    assert len(nc.get_history(search_text="down")) == 1
    
    # Test Export
    json_file = "test_export.json"
    csv_file = "test_export.csv"
    nc.export_to_json(json_file)
    nc.export_to_csv(csv_file)
    
    assert os.path.exists(json_file)
    assert os.path.exists(csv_file)
    
    # Cleanup
    os.remove(json_file)
    os.remove(csv_file)
