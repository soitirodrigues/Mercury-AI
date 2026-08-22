#!/usr/bin/env python3
"""Sprint 6 §25 — LIVE_CONTROLLED reproducible command wrapper.

Canonical (§25 alternativa):
  python scripts/m5_operational_runner.py --universe 64 --executor process --cycles 24
This wrapper aliases to the Sprint 6 gate runner for LIVE_CONTROLLED traceability.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import scripts.m5_sprint6_gate_runner as gate
if __name__ == "__main__":
    # forward args
    gate.main()
