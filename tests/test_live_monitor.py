import pytest


def test_live_monitor_import():
    """Verifica se o módulo LiveMonitor pode ser importado."""
    from mercury_ai.analysis.live_monitor import LiveMonitor
    assert LiveMonitor is not None


def test_live_monitor_instantiation():
    """Verifica se o LiveMonitor pode ser instanciado."""
    from mercury_ai.analysis.live_monitor import LiveMonitor
    monitor = LiveMonitor()
    assert monitor is not None
