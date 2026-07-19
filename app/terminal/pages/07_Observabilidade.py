import streamlit as st
import pandas as pd
from mercury_ai.utils.system_monitor import SystemMonitor
from mercury_ai.analysis.performance_statistics import PerformanceStatistics
from mercury_ai.analysis.health_checker import HealthChecker
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
import time

st.set_page_config(page_title="Painel de Observabilidade", layout="wide")
st.title("📊 Painel de Observabilidade")

# Metrics
col1, col2, col3, col4 = st.columns(4)
metrics = SystemMonitor.get_metrics()
col1.metric("CPU", f"{metrics['cpu_percent']}%")
col2.metric("RAM", f"{metrics['ram_percent']}%")
col3.metric("Disco", f"{metrics['disk_usage']}%")

# Performance Stats
st.subheader("Performance de Execução")
stats = PerformanceStatistics().calculate()
col_p1, col_p2, col_p3 = st.columns(3)
col_p1.metric("Tempo Médio", f"{stats.get('avg_time', 0):.4f}s")
col_p2.metric("Tempo Máximo", f"{stats.get('max_time', 0):.4f}s")
col_p3.metric("Tempo Mínimo", f"{stats.get('min_time', 0):.4f}s")

# System State
st.subheader("Estado do Sistema")
col_s1, col_s2, col_s3 = st.columns(3)
col_s1.metric("Health", "🟢 OK" if HealthChecker().check().system_ready else "🔴 FALHA")
col_s2.metric("Snapshots", len(DecisionSnapshotLogger().list_snapshots()))
col_s3.metric("Providers", "Ativos")

if st.button("Atualizar"):
    st.rerun()
