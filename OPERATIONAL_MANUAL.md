# Manual Operacional - Mercury AI V1

Este documento detalha o fluxo operacional e as diretrizes de manutenção para a Mercury AI V1.

---

## 1. Fluxo Completo de Operação

O fluxo oficial da plataforma é:
`main.py` → `MercuryScanner` → `AnalysisPipeline` → `AnalysisResult`

## 2. Componentes

### 2.1 Inicialização
Utilize o script `run.bat` na raiz do projeto para ativar o ambiente virtual e iniciar a execução principal (`main.py`).

### 2.2 Scanner
O `MercuryScanner` é o motor de ingestão. Ele monitora ativos configurados e alimenta o pipeline de análise.

### 2.3 Dashboard
Interface de visualização (Streamlit) para monitoramento em tempo real. Acessível via navegador após a inicialização.

### 2.4 Replay e Demo
Ferramentas de simulação e backtesting institucional.
- **Replay:** Execução determinística de dados históricos para auditoria.
- **Demo:** Ambiente de testes de estratégias em condições controladas.

### 2.5 Snapshots e Histórico
- **Snapshots:** Capturas de estado do pipeline.
- **Histórico:** Registro de todas as análises realizadas para auditoria institucional.

### 2.6 Monitoramento
Acompanhe os logs na pasta `/logs` e os relatórios gerados (`runtime_report_*.json`). Utilize `healthcheck.bat` para verificar a integridade da suíte de testes.

---

## 3. Boas Práticas
- Nunca crie múltiplos pipelines de análise.
- Reutilize componentes existentes.
- Mantenha a pasta `/data` sincronizada e faça backups periódicos com `backup.bat`.
- Sempre verifique os logs antes de iniciar novas sessões de trading.

---

## 4. Troubleshooting
- **Falha na execução:** Verifique `requirements.txt` e execute `update.bat`.
- **Inconsistência de dados:** Utilize `restore.bat` para reverter para o último backup conhecido.
- **Pipeline travado:** Reinicie a aplicação via `run.bat`.

---

## 5. Checklists de Manutenção

### 5.1 Diário
- [ ] Executar `healthcheck.bat`.
- [ ] Verificar logs de erro na pasta `/logs`.
- [ ] Validar se os relatórios de runtime estão sendo gerados.

### 5.2 Semanal
- [ ] Executar `backup.bat`.
- [ ] Limpar logs antigos.
- [ ] Verificar integridade dos dados históricos.

### 5.3 Mensal
- [ ] Atualizar dependências (`update.bat`).
- [ ] Revisar histórico de trading/análise para ajustes de performance.
- [ ] Auditoria completa de snapshots.
