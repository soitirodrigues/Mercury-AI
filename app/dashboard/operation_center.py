import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from mercury_ai.brain.scan_service import run_dashboard_scan
from app.dashboard.scan_presentation import (
    present_scan,
    status_banner,
    counters_line,
)
from mercury_ai.analysis.operational_history import OperationalHistory
from mercury_ai.analysis.performance_statistics import PerformanceStatistics
from mercury_ai.analysis.integrity_checker import IntegrityChecker
from mercury_ai.analysis.health_checker import HealthChecker
from mercury_ai.config import settings

st.set_page_config(page_title="Mercury Operation Center", layout="wide")

st.title("🛡️ Mercury AI | Operation Center")

# Sidebar - Demo Mode Status
st.sidebar.subheader("Modo de Operação")
st.sidebar.write(f"**Demo Mode:** {'ATIVO' if settings.READ_ONLY else 'DESATIVADO'}")
st.sidebar.write(f"**Versão:** {settings.VERSION}")

# 1. Scanner & Market — S33-E.5: UMA execucao workers=4 + ScanReport real.
# S33-E.6: APENAS apresentacao do envelope (TOP3/status/contadores verbatim).
st.header("1. Scanner & Mercado")
analyses, _scan_report = run_dashboard_scan()
_view = present_scan(_scan_report.to_dict())
st.caption(
    f"scan_id={_view.get('scan_id')} status={_view.get('status')} "
    f"completed={_view.get('progress_text')} "
    f"ranqueados={_view.get('ranked_count')} "
    f"workers={_view.get('workers')} duration={_view.get('duration_s')}s"
)
st.caption(counters_line(_view))
st.caption(status_banner(_view))
if _view.get("has_top3"):
    st.dataframe(pd.DataFrame(_view.get("top3")), use_container_width=True)
else:
    st.info(
        "TOP 3 vazio neste ciclo — nenhum item inventado. "
        f"(status={_view.get('status')})"
    )
if analyses:
    analysis = analyses[0] # Mostrando o primeiro por conveniência
    st.metric("Ativo", analysis.market.symbol)
    st.metric("Regime", str(analysis.market_regime.regime) if analysis.market_regime else "N/A")
else:
    st.warning("Scanner vazio.")

# 2. Última Decisão & Snapshot
st.header("2. Última Decisão")
if analyses:
    st.write(f"**Decisão:** {analysis.decision.decision}")
    st.write(f"**Confidence:** {analysis.decision.confidence*100:.1f}%")
    st.write(f"**Timestamp:** {analysis.timestamp[:19]}")

# 3. Histórico e Replay
st.header("3. Histórico e Replay")
history = OperationalHistory().query()
st.dataframe(pd.DataFrame(history))

# 4. Performance e Estatísticas
st.header("4. Performance e Estatísticas")
stats = PerformanceStatistics().calculate()
st.json(stats)

# 5. Auditoria e Logs
st.header("5. Auditoria e Logs")
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Integridade")
    st.write(IntegrityChecker().check_all())
with col_b:
    st.subheader("Logs")
    log_path = Path("logs")
    if list(log_path.glob("*.log")):
        st.write("Logs disponíveis.")
    else:
        st.write("Nenhum log disponível.")

# 6. Monitoramento
st.header("6. Monitoramento")
st.json(HealthChecker().check().components)
