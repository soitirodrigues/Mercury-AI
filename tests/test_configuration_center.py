import os
import pytest
from mercury_ai.config.configuration_center import MercuryConfigCenter

def test_configuration_center_new_structure():
    config_file = "test_config.json"
    cc = MercuryConfigCenter(config_file=config_file)
    
    # Test updating a category
    cc.save("SCANNER", {"auto_run": True, "interval": 30})
    
    # Reload from file
    cc2 = MercuryConfigCenter(config_file=config_file)
    assert cc2.get("SCANNER", "auto_run") is True
    assert cc2.get("SCANNER", "interval") == 30
    assert cc2.get("GENERAL", "read_only") is True
    
    # Cleanup
    if os.path.exists(config_file):
        os.remove(config_file)
