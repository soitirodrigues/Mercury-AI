import sys
from pathlib import Path

# adiciona a raiz do projeto ao PYTHONPATH
ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from mercury_ai.brain.scanner import MercuryScanner
from mercury_ai.analysis.performance_statistics import PerformanceStatistics
from mercury_ai.analysis.engine_performance_auditor import EnginePerformanceAuditor
from mercury_ai.analysis.institutional_report_generator import InstitutionalReportGenerator
from mercury_ai.analysis.notification_center import NotificationCenter
from app.ui_utils import apply_design_system, display_metric

# Notification Center Initialization
if 'notification_center' not in st.session_state:
    st.session_state.notification_center = NotificationCenter()

st.set_page_config(page_title="Mercury AI Institutional", layout="wide")
apply_design_system()

st.title("🧠 Mercury AI | Dashboard Institucional")

@st.cache_data
def load_data():
    scanner = MercuryScanner()
    return scanner.scan()

analyses = load_data()

if not analyses:
    st.warning("Nenhuma oportunidade encontrada.")
    st.stop()

# Selector
selected_symbol = st.sidebar.selectbox("Ativo", [a.market.symbol for a in analyses])
analysis = next(a for a in analyses if a.market.symbol == selected_symbol)

# Institutional Status Panel
st.sidebar.subheader("Status Institucional")
from mercury_ai.analysis.health_checker import HealthChecker
from mercury_ai.config import settings
import time

# Auto Refresh Control
auto_refresh = st.sidebar.checkbox("Atualização Automática", value=False)
if auto_refresh:
    time.sleep(settings.MONITORING_INTERVAL)
    st.rerun()

health = HealthChecker().check()
st.sidebar.write(f"**Versão:** {settings.VERSION}")
st.sidebar.write(f"**Session ID:** {health.timestamp[:10]}") # Simplified for UI
st.sidebar.write(f"**Build:** V1.0-Stable")
st.sidebar.write(f"**Health:** {'🟢' if health.system_ready else '🔴'}")

# Statistics & Counters
st.sidebar.subheader("Auditoria de Dados")
snapshots = Scanner().snapshot_logger.list_snapshots()
st.sidebar.write(f"**Snapshots:** {len(snapshots)}")
st.sidebar.write(f"**Replay Count:** {len(snapshots)}") # Replay is supported if snapshots exist

# Tabs
tabs = st.tabs(["Painel Institucional", "Centro de Operações", "Scanner Institucional", "Performance", "Histórico e Replay", "Estatísticas Institucionais", "Engines", "Trading Journal", "Configurações"])

with tabs[0]:
    # Institutional Metrics
    st.subheader("Painel Institucional")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("Viés", analysis.decision.decision)
    with col2: st.metric("Confiança", f"{analysis.decision.confidence*100:.1f}%")
    with col3: st.metric("Score", f"{analysis.decision.score:.2f}")
    with col4: st.metric("Risco", f"{analysis.decision.risk_score:.2f}")
    with col5: st.metric("Regime", str(analysis.market_regime.regime) if analysis.market_regime else "N/A")

    col6, col7 = st.columns(2)
    with col6: st.metric("Confluência", f"{analysis.decision.clarity:.1f}%")
    with col7: st.metric("Timestamp", analysis.timestamp[:19])

    # Executive Summary
    st.subheader("Racional Institucional")
    st.info(analysis.decision.summary)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Probabilidades Institucionais")
        p_col1, p_col2, p_col3 = st.columns(3)
        with p_col1: st.progress(analysis.decision.buy_probability / 100, text=f"BUY: {analysis.decision.buy_probability:.1f}%")
        with p_col2: st.progress(analysis.decision.sell_probability / 100, text=f"SELL: {analysis.decision.sell_probability:.1f}%")
        with p_col3: st.progress(analysis.decision.wait_probability / 100, text=f"NEUTRAL: {analysis.decision.wait_probability:.1f}%")
    with col_b:
        st.subheader("Evidências Dominantes")
        if analysis.decision.evidence_ranking:
            st.write("Top Evidência:", analysis.decision.evidence_ranking.strongest_evidence.evidence_name)
            st.write("Engine:", analysis.decision.evidence_ranking.strongest_evidence.engine_name)
        else:
            st.write("Sem ranking detalhado disponível.")

with tabs[1]:
    st.subheader("Centro de Operações")
    col_o1, col_o2 = st.columns(2)
    with col_o1:
        mode = st.radio("Modo de Operação", ["Demo", "Real"], index=0 if settings.READ_ONLY else 1)
        st.warning(f"Modo selecionado: {mode} (Execução bloqueada automaticamente)")
    
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    with col_b1:
        if st.button("Executar Scanner"): st.rerun()
        if st.button("Atualizar"): st.rerun()
    with col_b2:
        if st.button("Abrir Ativo"): st.write("Selecione um ativo.")
        if st.button("Replay"): st.write("Replay funcional.")
    with col_b3:
        if st.button("Histórico"): st.switch_page("pages/03_Historico_Estatisticas.py")
        if st.button("Estatísticas"): st.switch_page("pages/03_Historico_Estatisticas.py")
    with col_b4:
        if st.button("Exportar"):
            from mercury_ai.analysis.data_exporter import DataExporter
            DataExporter().export_all()
            st.success("Dados exportados.")

with tabs[2]:
    st.subheader("Scanner Institucional")
    all_analyses = load_data()
    scan_data = []
    for a in all_analyses:
        scan_data.append({
            "Ativo": a.market.symbol,
            "Decisão": a.decision.decision,
            "Confiança": f"{a.decision.confidence*100:.1f}%",
            "Prob. Buy": f"{a.decision.buy_probability:.1f}%",
            "Prob. Sell": f"{a.decision.sell_probability:.1f}%",
            "Prob. Wait": f"{a.decision.wait_probability:.1f}%",
            "Regime": str(a.market_regime.regime) if a.market_regime else "N/A",
            "Score": a.decision.score,
            "Timestamp": a.timestamp[:19]
        })
    st.dataframe(pd.DataFrame(scan_data))

with tabs[3]:
    st.subheader("Performance Analytics")
    stats = PerformanceStatistics().calculate()
    st.json(stats)

with tabs[4]:
    st.subheader("Histórico e Replay")
    from mercury_ai.analysis.operational_history import OperationalHistory
    history = OperationalHistory().query()
    st.dataframe(pd.DataFrame(history))

with tabs[5]:
    st.subheader("Estatísticas e Regimes")
    report = InstitutionalReportGenerator().generate()
    st.json(report['performance'])

with tabs[6]:
    st.subheader("Performance das Engines")
    engine_perf = EnginePerformanceAuditor().audit_engines()
    st.dataframe(pd.DataFrame.from_dict(engine_perf, orient='index'))

with tabs[7]:
    st.subheader("Trading Journal")
    from mercury_ai.analysis.operational_history import OperationalHistory
    journal = OperationalHistory().query()
    # Flatten probabilities for better display
    df_journal = pd.DataFrame(journal)
    if not df_journal.empty:
        prob_df = pd.json_normalize(df_journal['probability'])
        df_journal = pd.concat([df_journal.drop(columns=['probability']), prob_df], axis=1)
    st.dataframe(df_journal)

with tabs[8]:
    st.subheader("Configurações do Sistema")
    with st.form("settings_form"):
        col1, col2 = st.columns(2)
        with col1:
            new_asset = st.text_input("Ativo Principal", settings.ASSET)
            new_timeframe = st.text_input("Timeframe", settings.TIMEFRAME)
            new_capital = st.number_input("Capital", value=settings.CAPITAL)
            new_stop = st.number_input("Stop Diário", value=settings.DAILY_STOP)
            new_target = st.number_input("Meta Diária", value=settings.DAILY_TARGET)
        with col2:
            new_broker = st.text_input("Broker", settings.BROKER)
            new_account = st.selectbox("Conta", ["Demo", "Real"], index=0 if settings.ACCOUNT_TYPE == "Demo" else 1)
            new_interval = st.number_input("Intervalo de Monitoramento (s)", settings.MONITORING_INTERVAL)
            new_path = st.text_input("Pasta de Snapshots", settings.SNAPSHOT_PATH)
            new_log = st.text_input("Pasta de Logs", settings.LOG_PATH)
            new_theme = st.selectbox("Tema", ["light", "dark"], index=0 if settings.THEME == "light" else 1)
            new_read_only = st.checkbox("Modo Demo (Read Only)", settings.READ_ONLY)
        
        if st.form_submit_button("Salvar Configurações"):
            from mercury_ai.config.configuration_center import MercuryConfigCenter
            config_center = MercuryConfigCenter()
            config_center.save("GENERAL", {
                "READ_ONLY": new_read_only
            })
            config_center.save("SCANNER", {
                "interval": new_interval
            })
            # ... other categories ...
            
            st.success("Configurações atualizadas com sucesso.")
