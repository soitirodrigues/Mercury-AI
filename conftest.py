import pytest

pytestmark = pytest.mark.timeout(300)


def pytest_configure(config):
    """Registra marcadores customizados para evitar warnings."""
    config.addinivalue_line("markers", "slow: testes lentos (CPU-bound)")
