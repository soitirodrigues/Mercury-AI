import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from mercury_ai.analysis.operational_history import OperationalHistory
from mercury_ai.analysis.performance_statistics import PerformanceStatistics
from mercury_ai.brain.scan_service import SCAN_REPORTS_DIR, load_latest_scan_report
from app.dashboard.scan_presentation import (
    present_scan,
    status_banner,
    counters_line,
)

st.title("Histórico e Estatísticas")

# S33-E.6 Fase 9 — historico do ScanReport persistido (status real verbatim).
st.subheader("Último Scan persistido (status real)")
_latest = load_latest_scan_report()
if _latest is None:
    st.info(
        "Nenhum ScanReport persistido ainda "
        f"({SCAN_REPORTS_DIR}/latest.json ausente). "
        "Execute um scan para gerar histórico."
    )
else:
    _hv = present_scan(_latest)
    st.caption(f"scan_id={_hv.get('scan_id')}")
    _hs = _hv.get("status")
    if _hs == "COMPLETE":
        st.success(status_banner(_hv))
    elif _hs == "PARTIAL":
        st.warning(status_banner(_hv))
    elif _hs in ("TIMEOUT", "ERROR"):
        st.error(
            f"{status_banner(_hv)}"
            + (f" — {_hv.get('error')}" if _hv.get("error") else "")
        )
    else:
        st.warning(status_banner(_hv))
    st.caption(counters_line(_hv))
    st.caption(
        f"Progresso: {_hv.get('progress_text')} "
        f"| ranqueados={_hv.get('ranked_count')} "
        f"| top3={_hv.get('top3_symbols')}"
    )
    if _hv.get("has_top3"):
        st.dataframe(pd.DataFrame(_hv.get("top3")), use_container_width=True)
    else:
        st.info("TOP 3 vazio no relatório persistido — nenhum item inventado.")

st.subheader("Trading Journal")
history = OperationalHistory().query()
st.dataframe(pd.DataFrame(history))

st.subheader("Performance Estatística")
st.json(PerformanceStatistics().calculate())
