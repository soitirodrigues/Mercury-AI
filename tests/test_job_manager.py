import time
from mercury_ai.core.job_manager import JobManager

def test_job_manager():
    manager = JobManager(interval_seconds=1)
    
    manager.start()
    time.sleep(1.5) # Wait for a cycle
    assert manager.running is True
    
    manager.pause()
    assert manager.paused is True
    
    manager.resume()
    assert manager.paused is False
    
    manager.stop()
    assert manager.running is False
