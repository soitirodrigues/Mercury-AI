import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from mercury_ai.brain.scan_service import run_dashboard_scan
from app.dashboard.scan_presentation import (
    present_scan,
    status_banner,
    counters_line,
)

st.title("Dashboard Institucional")
# S33-E.5: UMA execucao workers=4 + ScanReport real.
# S33-E.6: APENAS apresentacao do envelope (TOP3/status/contadores verbatim).
analyses, _scan_report = run_dashboard_scan()
_view = present_scan(_scan_report.to_dict())
st.caption(
    f"scan_id={_view.get('scan_id')} status={_view.get('status')} "
    f"completed={_view.get('progress_text')} "
    f"ranqueados={_view.get('ranked_count')} "
    f"workers={_view.get('workers')}"
)
st.caption(counters_line(_view))
st.caption(status_banner(_view))
st.subheader("TOP 3 — ScanReport (sem recálculo)")
if _view.get("has_top3"):
    st.dataframe(pd.DataFrame(_view.get("top3")), use_container_width=True)
else:
    st.info(
        "TOP 3 vazio neste ciclo — nenhum item inventado. "
        f"(status={_view.get('status')})"
    )
if analyses:
    analysis = analyses[0]
    st.metric("Viés", analysis.decision.decision)
    st.metric("Confiança", f"{analysis.decision.confidence*100:.1f}%")
