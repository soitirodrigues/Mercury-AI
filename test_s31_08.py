"""
S31-08 — SIGNAL-ONLY Final Safety Gate Test

Confirm that the system operates in SIGNAL-ONLY mode by design:
- LIVE orders = 0
- No live broker configured
- No live credentials
- No real orders
- explicit_live_gate required
- This sprint does NOT release LIVE
"""

import sys
import os
import json

# Add workspace to path
sys.path.insert(0, r"C:\Projetos\Mercury-AI")