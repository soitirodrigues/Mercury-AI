import pytest
from mercury_ai.core.read_only import check_read_only, ReadOnlyViolation

def test_read_only_mode():
    with pytest.raises(ReadOnlyViolation):
        check_read_only(True)
    
    # Should not raise for False
    check_read_only(False)
