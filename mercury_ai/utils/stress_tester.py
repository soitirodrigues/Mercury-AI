import time
import tracemalloc
import random
from typing import Callable, Any, Dict, List
from mercury_ai.models.stress_test import StressTestResult

class StressTester:
    def __init__(self, engine_callable: Callable[[Any], Any]):
        self.engine = engine_callable
        self.generators: Dict[str, Callable[[int], Any]] = {}

    def register_generator(self, scenario: str, generator_func: Callable[[int], Any]):
        self.generators[scenario] = generator_func

    def run(self, scenario: str, dataset_size: int, repetitions: int) -> StressTestResult:
        if scenario not in self.generators:
            raise ValueError(f"Scenario {scenario} not registered.")
            
        generator = self.generators[scenario]
        runtimes = []
        peak_memories = []
        exceptions = []
        results = []
        failure_count = 0

        # Run once to establish expected output for determinism
        input_data = generator(dataset_size)
        
        for _ in range(repetitions):
            tracemalloc.start()
            start_time = time.perf_counter()
            try:
                result = self.engine(input_data)
                results.append(result)
            except Exception as e:
                exceptions.append(e)
                failure_count += 1
            finally:
                end_time = time.perf_counter()
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
            runtimes.append(end_time - start_time)
            peak_memories.append(peak)

        is_deterministic = all(r == results[0] for r in results[1:]) if results else True
        
        return StressTestResult(
            pipeline_name=self.engine.__name__,
            scenario=scenario,
            dataset_size=dataset_size,
            repetitions=repetitions,
            runtimes=runtimes,
            peak_memory=peak_memories,
            exceptions=exceptions,
            is_deterministic=is_deterministic,
            failure_count=failure_count
        )
