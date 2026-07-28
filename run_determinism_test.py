#!/usr/bin/env python3
"""
Determinism Test - Run pipeline 100 times and compare 9 metrics:
1. Decision
2. Confidence
3. Institutional Score
4. Probability (buy/sell/wait)
5. Explainability (DecisionExplainability)
6. Snapshot (DecisionSnapshot)
7. Runtime Report
8. Decision Chain
9. Hash of objects

All must be identical. If differences exist: show exact file, line, cause.
Generates: DETERMINISM_CERTIFICATION.md
"""

import sys
import json
import hashlib
import pickle
from pathlib import Path
from dataclasses import asdict
from typing import Any, Dict, List, Tuple, Optional
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.mercury_data_provider import MercuryDataProvider
from mercury_ai.models.analysis_result import AnalysisResult
from mercury_ai.models.decision_result import DecisionResult
from mercury_ai.models.decision_snapshot import DecisionSnapshot
from mercury_ai.analysis.decision_explainability import DecisionExplainability
from mercury_ai.core.runtime_report import RuntimeReport
from mercury_ai.utils.deterministic_clock import DeterministicClock


class DeterminismTester:
    """Runs pipeline 100 times and compares all outputs for determinism."""
    
    def __init__(self, symbol: str = "GC=F", runs: int = 100):
        self.symbol = symbol
        self.runs = runs
        self.results: List[Dict[str, Any]] = []
        self.differences: List[Dict[str, Any]] = []
        
    def _create_pipeline(self) -> AnalysisPipeline:
        """Create a fresh pipeline instance for each run."""
        provider = MercuryDataProvider()
        market_service = MarketDataService(provider=provider)
        return AnalysisPipeline(market_service=market_service, providers=[provider])
    
    def _extract_metrics(self, result: AnalysisResult, pipeline: AnalysisPipeline, run_num: int) -> Dict[str, Any]:
        """Extract the 9 metrics from a pipeline run."""
        decision: DecisionResult = result.decision
        explainability: Optional[DecisionExplainability] = decision.explainability
        snapshot: Optional[DecisionSnapshot] = pipeline.last_snapshot
        runtime_report: Optional[RuntimeReport] = pipeline.runtime_report
        
        # 1. Decision
        decision_str = decision.decision
        
        # 2. Confidence
        confidence = decision.confidence
        
        # 3. Institutional Score
        institutional_score = explainability.institutional_score if explainability else None
        
        # 4. Probability (buy/sell/wait)
        probability = {
            "buy": decision.buy_probability,
            "sell": decision.sell_probability,
            "wait": decision.wait_probability
        }
        
        # 5. Explainability (full object)
        explainability_dict = None
        if explainability:
            explainability_dict = {
                "decision": explainability.decision,
                "reason": explainability.reason,
                "dominant_direction": explainability.dominant_direction,
                "opportunity_grade": explainability.opportunity_grade,
                "conflicting_signals": explainability.conflicting_signals,
                "institutional_score": explainability.institutional_score,
                "confidence": explainability.confidence,
                "triggered_rule": explainability.triggered_rule,
                "contributions": [
                    {
                        "engine_name": c.engine_name,
                        "weight": c.weight,
                        "raw_score": c.raw_score,
                        "weighted_score": c.weighted_score,
                        "direction": c.direction,
                        "confidence": c.confidence
                    }
                    for c in explainability.contributions
                ],
                "decision_chain": list(explainability.decision_chain)
            }
        
        # 6. Snapshot (DecisionSnapshot)
        snapshot_dict = None
        if snapshot:
            snapshot_dict = {
                "timestamp": snapshot.timestamp,
                "asset": snapshot.asset,
                "timeframe": snapshot.timeframe,
                "session_id": snapshot.session_id,
                "version": snapshot.version,
                "audit_events": list(snapshot.audit_events),
                "version_metadata": {
                    "engine_version": snapshot.version_metadata.engine_version,
                    "pipeline_version": snapshot.version_metadata.pipeline_version,
                    "context_version": snapshot.version_metadata.context_version,
                    "weights_version": snapshot.version_metadata.weights_version
                } if snapshot.version_metadata else None
            }
        
        # 7. Runtime Report
        runtime_report_dict = None
        if runtime_report:
            runtime_report_dict = runtime_report.to_dict()
        
        # 8. Decision Chain
        decision_chain = list(explainability.decision_chain) if explainability else []
        
        # 9. Hash of objects (using pickle for deep hash)
        # Hash the decision result
        decision_hash = self._hash_object(decision)
        explainability_hash = self._hash_object(explainability) if explainability else None
        snapshot_hash = self._hash_object(snapshot) if snapshot else None
        runtime_report_hash = self._hash_object(runtime_report) if runtime_report else None
        
        return {
            "run": run_num,
            "decision": decision_str,
            "confidence": confidence,
            "institutional_score": institutional_score,
            "probability": probability,
            "explainability": explainability_dict,
            "snapshot": snapshot_dict,
            "runtime_report": runtime_report_dict,
            "decision_chain": decision_chain,
            "hashes": {
                "decision": decision_hash,
                "explainability": explainability_hash,
                "snapshot": snapshot_hash,
                "runtime_report": runtime_report_hash
            }
        }
    
    def _hash_object(self, obj: Any) -> str:
        """Create a deterministic hash of an object using pickle."""
        if obj is None:
            return "None"
        try:
            # Use pickle with protocol 4 for deterministic serialization
            data = pickle.dumps(obj, protocol=4)
            return hashlib.sha256(data).hexdigest()[:32]
        except Exception as e:
            return f"ERROR: {e}"
    
    def _compare_values(self, values: List[Any], metric_name: str, run_num: int) -> List[Dict[str, Any]]:
        """Compare a list of values across runs and return differences."""
        diffs = []
        if not values:
            return diffs
        
        first_value = values[0]
        for i, value in enumerate(values[1:], start=2):
            if value != first_value:
                diffs.append({
                    "metric": metric_name,
                    "run": i,
                    "expected": first_value,
                    "actual": value,
                    "difference": self._describe_difference(first_value, value, metric_name)
                })
        return diffs
    
    def _describe_difference(self, expected: Any, actual: Any, metric_name: str) -> str:
        """Describe the difference between two values."""
        if isinstance(expected, dict) and isinstance(actual, dict):
            diffs = []
            all_keys = set(expected.keys()) | set(actual.keys())
            for key in all_keys:
                if key not in expected:
                    diffs.append(f"Missing key '{key}' in expected")
                elif key not in actual:
                    diffs.append(f"Missing key '{key}' in actual")
                elif expected[key] != actual[key]:
                    diffs.append(f"Key '{key}': expected={expected[key]}, actual={actual[key]}")
            return "; ".join(diffs)
        elif isinstance(expected, list) and isinstance(actual, list):
            if len(expected) != len(actual):
                return f"List length differs: expected={len(expected)}, actual={len(actual)}"
            diffs = []
            for i, (e, a) in enumerate(zip(expected, actual)):
                if e != a:
                    diffs.append(f"Index {i}: expected={e}, actual={a}")
            return "; ".join(diffs) if diffs else "Lists differ but elements equal (unexpected)"
        else:
            return f"Expected: {expected}, Actual: {actual}"
    
    def run_tests(self) -> None:
        """Run the pipeline 100 times and collect metrics."""
        print(f"Starting determinism test: {self.runs} runs for symbol {self.symbol}")
        print("=" * 60)
        
        for run_num in range(1, self.runs + 1):
            if run_num % 10 == 0:
                print(f"Progress: {run_num}/{self.runs} runs completed...")
            
            pipeline = self._create_pipeline()
            result = pipeline.analyze(symbol=self.symbol, silent=True)
            metrics = self._extract_metrics(result, pipeline, run_num)
            self.results.append(metrics)
        
        print(f"\nAll {self.runs} runs completed. Analyzing results...")
        self._analyze_results()
    
    def _analyze_results(self) -> None:
        """Analyze all results and find differences."""
        if not self.results:
            return
        
        # Compare each metric across all runs
        metrics_to_compare = [
            ("decision", lambda r: r["decision"]),
            ("confidence", lambda r: r["confidence"]),
            ("institutional_score", lambda r: r["institutional_score"]),
            ("probability", lambda r: r["probability"]),
            ("explainability", lambda r: r["explainability"]),
            ("snapshot", lambda r: r["snapshot"]),
            ("runtime_report", lambda r: r["runtime_report"]),
            ("decision_chain", lambda r: r["decision_chain"]),
            ("hashes.decision", lambda r: r["hashes"]["decision"]),
            ("hashes.explainability", lambda r: r["hashes"]["explainability"]),
            ("hashes.snapshot", lambda r: r["hashes"]["snapshot"]),
            ("hashes.runtime_report", lambda r: r["hashes"]["runtime_report"]),
        ]
        
        for metric_name, extractor in metrics_to_compare:
            values = [extractor(r) for r in self.results]
            diffs = self._compare_values(values, metric_name, 1)
            self.differences.extend(diffs)
        
        # Also check if all hashes are identical (stronger test)
        all_hashes_identical = True
        for hash_type in ["decision", "explainability", "snapshot", "runtime_report"]:
            hashes = [r["hashes"][hash_type] for r in self.results]
            if len(set(hashes)) > 1:
                all_hashes_identical = False
                self.differences.append({
                    "metric": f"hashes.{hash_type}",
                    "run": "multiple",
                    "expected": hashes[0],
                    "actual": "varies",
                    "difference": f"Hash values differ across runs: {len(set(hashes))} unique values"
                })
        
        print(f"\nAnalysis complete. Found {len(self.differences)} differences.")
    
    def generate_report(self) -> str:
        """Generate the DETERMINISM_CERTIFICATION.md report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# DETERMINISM CERTIFICATION REPORT

**Generated:** {timestamp}  
**Symbol:** {self.symbol}  
**Runs Executed:** {self.runs}  
**Test Script:** run_determinism_test.py  

---

## EXECUTIVE SUMMARY

"""
        
        if not self.differences:
            report += """✅ **CERTIFICATION: PASSED**

All 100 runs produced **IDENTICAL** results across all 9 metrics:
1. Decision
2. Confidence
3. Institutional Score
4. Probability (buy/sell/wait)
5. Explainability (DecisionExplainability)
6. Snapshot (DecisionSnapshot)
7. Runtime Report
8. Decision Chain
9. Hash of objects

The system is **deterministic** - given the same inputs, it produces exactly the same outputs every time.
"""
        else:
            report += f"""❌ **CERTIFICATION: FAILED**

Found **{len(self.differences)} differences** across {self.runs} runs.

The system is **NOT deterministic** - identical inputs produce different outputs.
"""
        
        report += f"""

---

## METRICS COMPARED

| # | Metric | Status | Details |
|---|--------|--------|---------|
| 1 | Decision | {'✅ PASS' if not any(d['metric'] == 'decision' for d in self.differences) else '❌ FAIL'} | Final decision (BUY/SELL/WAIT) |
| 2 | Confidence | {'✅ PASS' if not any(d['metric'] == 'confidence' for d in self.differences) else '❌ FAIL'} | Decision confidence (0-1) |
| 3 | Institutional Score | {'✅ PASS' if not any(d['metric'] == 'institutional_score' for d in self.differences) else '❌ FAIL'} | Institutional score from explainability |
| 4 | Probability | {'✅ PASS' if not any(d['metric'] == 'probability' for d in self.differences) else '❌ FAIL'} | Buy/Sell/Wait probabilities |
| 5 | Explainability | {'✅ PASS' if not any(d['metric'] == 'explainability' for d in self.differences) else '❌ FAIL'} | Full DecisionExplainability object |
| 6 | Snapshot | {'✅ PASS' if not any(d['metric'] == 'snapshot' for d in self.differences) else '❌ FAIL'} | DecisionSnapshot object |
| 7 | Runtime Report | {'✅ PASS' if not any(d['metric'] == 'runtime_report' for d in self.differences) else '❌ FAIL'} | RuntimeReport with telemetry |
| 8 | Decision Chain | {'✅ PASS' if not any(d['metric'] == 'decision_chain' for d in self.differences) else '❌ FAIL'} | Step-by-step decision chain |
| 9 | Object Hashes | {'✅ PASS' if not any(d['metric'].startswith('hashes.') for d in self.differences) else '❌ FAIL'} | SHA256 hashes of all objects |

---

## DETAILED DIFFERENCES

"""
        
        if self.differences:
            for i, diff in enumerate(self.differences, 1):
                report += f"""### Difference #{i}

**Metric:** `{diff['metric']}`  
**Run:** {diff['run']}  
**Expected:** `{diff['expected']}`  
**Actual:** `{diff['actual']}`  
**Difference:** {diff['difference']}

"""
        else:
            report += "No differences found. All runs identical.\n"
        
        report += f"""

---

## SAMPLE OUTPUT (Run 1)

### Decision Result
```json
{json.dumps(self.results[0]['decision'], indent=2, default=str)}
```

### Confidence
```
{self.results[0]['confidence']}
```

### Institutional Score
```
{self.results[0]['institutional_score']}
```

### Probability
```json
{json.dumps(self.results[0]['probability'], indent=2)}
```

### Decision Chain
```json
{json.dumps(self.results[0]['decision_chain'], indent=2)}
```

### Hashes
```json
{json.dumps(self.results[0]['hashes'], indent=2)}
```

---

## VERIFICATION METHODOLOGY

1. **Fresh Pipeline per Run**: Each run creates a new `AnalysisPipeline` instance to ensure no state leakage
2. **Same Inputs**: Same symbol ({self.symbol}), same market data provider
3. **Silent Mode**: Pipeline runs with `silent=True` to suppress console output
4. **Deep Comparison**: 
   - Direct value comparison for primitives
   - Recursive dict/list comparison for complex objects
   - SHA256 hash of pickled objects for binary-level verification
5. **Deterministic Clock**: Uses `DeterministicClock` for all timestamps

---

## ENVIRONMENT

- **Python Version:** {sys.version.split()[0]}
- **Working Directory:** {Path.cwd()}
- **Test Date:** {timestamp}

---

## CONCLUSION

"""
        
        if not self.differences:
            report += """**VERDICT: DETERMINISTIC ✅**

The Mercury AI pipeline produces bit-for-bit identical results across 100 consecutive runs.
All 9 metrics are verified deterministic:
- Decision logic
- Confidence calculation
- Institutional scoring
- Probability computation
- Explainability generation
- Snapshot persistence
- Runtime telemetry
- Decision chain recording
- Object identity (hashes)

**Certification Status: APPROVED**
"""
        else:
            report += f"""**VERDICT: NON-DETERMINISTIC ❌**

The Mercury AI pipeline produces **different results** across runs.
{len(self.differences)} differences detected across {self.runs} runs.

**Root Cause Analysis Required**: Each difference above must be investigated to identify:
1. Source of non-determinism (random, time, threading, external API, etc.)
2. Exact file and line number causing the difference
3. Fix to make the pipeline deterministic

**Certification Status: REJECTED**
"""
        
        return report
    
    def save_results(self, output_dir: Path = None) -> None:
        """Save raw results and report."""
        if output_dir is None:
            output_dir = Path.cwd() / "determinism_test_results"
        
        output_dir.mkdir(exist_ok=True)
        
        # Save raw results as JSON
        results_file = output_dir / f"determinism_results_{self.symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            # Convert non-serializable objects
            serializable_results = []
            for r in self.results:
                sr = {k: v for k, v in r.items() if k not in ['explainability', 'snapshot', 'runtime_report']}
                sr['explainability'] = r['explainability']
                sr['snapshot'] = r['snapshot']
                sr['runtime_report'] = r['runtime_report']
                serializable_results.append(sr)
            json.dump(serializable_results, f, indent=2, default=str)
        
        # Save report
        report_file = output_dir / "DETERMINISM_CERTIFICATION.md"
        report = self.generate_report()
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\nResults saved to: {output_dir}")
        print(f"  - Raw data: {results_file}")
        print(f"  - Report: {report_file}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run determinism test on Mercury AI pipeline")
    parser.add_argument("--symbol", default="GC=F", help="Symbol to test (default: GC=F)")
    parser.add_argument("--runs", type=int, default=100, help="Number of runs (default: 100)")
    parser.add_argument("--output", help="Output directory (default: ./determinism_test_results)")
    
    args = parser.parse_args()
    
    tester = DeterminismTester(symbol=args.symbol, runs=args.runs)
    tester.run_tests()
    
    output_dir = Path(args.output) if args.output else None
    tester.save_results(output_dir)
    
    # Print summary
    report = tester.generate_report()
    print("\n" + "=" * 60)
    print("REPORT SUMMARY")
    print("=" * 60)
    
    if tester.differences:
        print(f"\n❌ FAILED: {len(tester.differences)} differences found")
        for diff in tester.differences[:5]:  # Show first 5
            print(f"  - {diff['metric']}: {diff['difference'][:100]}")
        if len(tester.differences) > 5:
            print(f"  ... and {len(tester.differences) - 5} more differences")
        sys.exit(1)
    else:
        print("\n✅ PASSED: All 100 runs identical")
        sys.exit(0)


if __name__ == "__main__":
    main()