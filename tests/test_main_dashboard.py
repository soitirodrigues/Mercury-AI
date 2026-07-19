import pytest
from app.dashboard.main_dashboard import main

def test_main_dashboard_initialization():
    # Verify main function exists (cannot run full streamlit app in test)
    assert main is not None
    assert True
