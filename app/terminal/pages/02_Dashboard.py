import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from mercury_ai.brain.scanner import Scanner

st.title("Dashboard Institucional")
analyses = Scanner().scan()
if analyses:
    analysis = analyses[0]
    st.metric("Viés", analysis.decision.decision)
    st.metric("Confiança", f"{analysis.decision.confidence*100:.1f}%")
