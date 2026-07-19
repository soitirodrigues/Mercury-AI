# Guia Oficial de Operação - Mercury AI V1

Este guia define os procedimentos padrão para a operação diária, manutenção e gestão da plataforma Mercury AI V1.

---

## 1. Fluxos Operacionais

### 1.1 Fluxo Diário
1.  **Healthcheck:** Executar `healthcheck.bat` para validar a integridade do sistema.
2.  **Inicialização:** Executar `run.bat` para iniciar a operação.
3.  **Monitoramento:** Acompanhar o Dashboard (`Painel Institucional`) durante a sessão.
4.  **Encerramento:** Finalizar via terminal e executar `backup.bat` para salvar o estado dos dados.

### 1.2 Fluxo Semanal
1.  **Backup Completo:** Garantir que o backup da pasta `data/` esteja atualizado.
2.  **Limpeza:** Remover logs antigos da pasta `/logs` (manter últimos 7 dias).
3.  **Performance:** Revisar o relatório gerado pelo `PerformanceCenter`.

### 1.3 Fluxo Mensal
1.  **Atualização:** Executar `update.bat` para garantir que as dependências estão atualizadas.
2.  **Auditoria:** Revisar todo o histórico operacional e snapshots acumulados.
3.  **Planejamento:** Analisar métricas de performance de longo prazo para ajustes de estratégia (se necessário).

---

## 2. Tarefas de Manutenção (Scripts Automatizados)
- **Backup (`backup.bat`):** Copia dados para diretório com timestamp.
- **Restore (`restore.bat`):** Restaura os dados do diretório de backup mais recente.
- **Healthcheck (`healthcheck.bat`):** Valida a integridade via suíte de testes.
- **Atualização (`update.bat`):** Atualiza as dependências do ambiente virtual.

---

## 3. Gestão de Componentes
- **Scanner:** Motor de ingestão; monitore logs de dados em tempo real.
- **Dashboard:** Interface principal para tomada de decisão.
- **Replay:** Utilizado para reexecutar sessões históricas e validar teses.
- **Snapshots:** Capturas de estado do pipeline. Essenciais para depuração.
- **Demo:** Ambiente de testes. Mantenha os dados de demo isolados dos dados de produção.

---

## 4. Boas Práticas e Falhas Comuns

### 4.1 Boas Práticas
- **Dados:** Nunca manipule manualmente os arquivos dentro de `data/` sem realizar um backup prévio.
- **Pipeline:** Não interrompa processos de gravação de snapshot.
- **Logs:** Verifique logs diariamente; eles são a principal ferramenta de diagnóstico.

### 4.2 Falhas Comuns e Recuperação
| Falha | Ação de Recuperação |
| :--- | :--- |
| **Inconsistência de Dados** | Executar `restore.bat`. |
| **Erro de Dependência** | Executar `update.bat`. |
| **Comportamento Inesperado** | Reiniciar a aplicação via `run.bat`. |
| **Dados Ausentes (API)** | Verificar conexão internet e logs de erro do provider. |

---

## 5. Checklist Operacional Consolidado

- [ ] **Diário:** Healthcheck, Monitoramento (Dashboard), Encerramento, Backup.
- [ ] **Semanal:** Limpeza de Logs, Auditoria de Integridade de Dados.
- [ ] **Mensal:** Atualização de dependências, Análise de Performance Institucional.

---
*Guia oficial emitido em 14 de julho de 2026. Este guia é o padrão para operação.*
