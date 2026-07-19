from mercury_ai.analysis.live_monitor import LiveMonitor

def test_live_monitor_cycle():
    monitor = LiveMonitor(interval_seconds=1)
    # Executa um ciclo para validar a integridade da integração
    monitor.run_cycle()
    # Se não houver exceções, o monitoramento está integrado corretamente
