## Replay exato do Alpha Code (2026-09-20)

A prioridade documentada da extensao foi reproduzida sem ordens e sem sinais sobrepostos: `Q5 -> LAST2 -> ALT`.

- Total: 36.645 sinais, 49,05%, -4.293,6 unidades.
- Treino/validacao: 29.316 sinais, 49,22%.
- Teste final: 7.329 sinais, **48,36%**, -949,8 unidades.

Conclusao: o pacote nao fornece uma estrategia vencedora verificavel. O feed M1, o mapeamento de ativos e o contrato de expiracao podem ser usados como fonte de dados; a logica Q5/ALT/LAST2 e a assertividade exibida nao devem ser integradas.
## Decisao de integracao incremental (2026-09-20)

### Integrado

- Guard no `DecisionResolverEngine`: `NaN`/`Inf` em confluencia agora resultam em `WAIT` seguro. Esta e uma correcao de integridade com teste, nao uma alegacao de assertividade.
- Identidade de replay, isolamento temporal, freshness, clock restoration, pairing por replay_id e CHoCH correto ja estavam implementados e certificados nos auditos anteriores.

### Nao integrado por falta de evidencia adequada

- RSI/ADX, EMA, trendline e filtros simples: teste fora da amostra nao superou baseline.
- N3: 44,4% de acerto binario; o profit factor positivo documentado usa payoff `R` e nao e transferivel para payout fixo.
- Sweep/reclaim intrabar: 39,32% em 10.132 sinais.
- Gate SMC recente: 53,85% e -0,4 unidades na entrada real pela abertura de T+1.

Regra adotada: melhoria de integridade entra imediatamente quando coberta por teste; filtro de entrada só entra depois de vencer o mesmo contrato binário em teste temporal independente.
# Mercury AI V1 - Plano de Assertividade M5

## Limite tecnico

98% nao pode ser tratado como requisito garantido sem definir amostra, payout, janela de expiracao, ativos, horario, custos e regra de entrada. O baseline existente do repositorio fica proximo de 49%, e filtros isolados ja auditados nao provaram 98%. O objetivo correto e encontrar um subconjunto com vantagem estatistica fora da amostra, mesmo que isso reduza drasticamente a cobertura.

## Implementacao inicial

`mercury_ai/signals/m5_institutional_filters.py` agora possui `smc_reversal_setup()`. O gate e opt-in e nao muda BUY/SELL/WAIT. Ele exige, na vela fechada:

- sweep de liquidez a favor;
- preco em discount para BUY ou premium para SELL;
- candle de reversao coerente;
- trigger alinhada;
- corpo minimo de 25% do range;
- range da trigger <= 2 ATR;
- FVG ou inducement confirmado.

A funcao retorna score de 0 a 100, `approved` e motivos de rejeicao. A aprovacao nao e uma afirmacao de probabilidade; e apenas uma classificacao de setup.

## Fases de validacao

### 1. Definir o contrato

Fixar antes de medir: M5 fechado, entrada na abertura da proxima vela, expiracao de uma vela, sem gale na metrica principal, payout e spread/slippage explicitos. Separar Forex e Crypto e estratificar por sessao/regime.

### 2. Dataset e integridade

Usar candles fechados com timestamp do provedor, remover duplicatas e gaps, registrar dataset hash e excluir qualquer dado posterior ao instante da decisao. O conjunto deve conter pelo menos 12 meses e 10.000 oportunidades candidatas antes de concluir.

### 3. Walk-forward

Dividir por tempo, nunca aleatoriamente: treino 60%, validação 20%, teste final 20%. Parâmetros são congelados no teste final. Repetir em janelas móveis e reportar cada janela, ativo e regime.

### 4. Métricas mínimas

Para cada variação: número de sinais, cobertura, acurácia, intervalo Wilson de 95%, pior janela, sequência máxima de perdas, expectativa líquida após payout/custos e estabilidade por ativo. Uma taxa de 98% com amostra pequena ou cobertura residual não passa.

Critério provisório de promoção: pelo menos 1.000 sinais no conjunto de teste, limite inferior do intervalo de 95% >= 90%, nenhuma janela abaixo de 85%, expectativa líquida positiva após custos e nenhuma degradação material entre treino, validação e teste. O alvo de 98% permanece uma hipótese a ser testada, não uma promessa.

### 5. Comparação obrigatoria

Comparar quatro braços congelados:

1. baseline atual;
2. sweep + reversao;
3. sweep + reversao + zona + FVG/IDM;
4. gate completo `smc_reversal_setup`.

Publicar também os sinais descartados. O ganho deve vir de seleção correta, nao de apagar perdas.

### 6. Ativacao segura

Somente depois dos gates estatisticos, integrar o `approved` como filtro de oportunidade, mantendo WAIT para dados insuficientes e preservando `audit_id`, candle de decisao e explicacao. Rodar paper trading por no minimo 30 dias e comparar ao backtest antes de qualquer uso financeiro.

## Ordem de execucao

1. Implementar backtest sem lookahead e bootstrap/Wilson.
2. Rodar baseline e quatro braços em dados congelados.
3. Diagnosticar por ativo, sessao, regime e tipo de setup.
4. Ajustar apenas no treino e repetir walk-forward.
5. Integrar somente se o teste final passar.

Execucao local:

```powershell
python scripts/m5_walk_forward_report.py caminho\dados_m5.csv --timestamp-column timestamp --out reports\m5_walk_forward.json
```

O CSV deve conter `Open`, `High`, `Low` e `Close`; `Volume` e timestamp sao recomendados. O relatorio grava as observacoes individuais, os cortes temporais e o intervalo Wilson.

## Regra de parada

Se o limite inferior, a expectativa liquida ou a estabilidade falhar, o gate nao entra em producao. A resposta correta e WAIT, nao gale e nao relaxamento de criterios para fabricar oportunidades.

## Primeira medicao real (2026-09-20)

Coleta Yahoo M5: manifesto `data/validation_m5/manifest.json`, 38 ativos validos, ate 60 dias, CSVs com SHA-256. O primeiro lote controlado usou os 300 candles mais recentes por ativo, `horizon=1`, payout 0,80 e custo 0.

Resultado agregado: 178 sinais, 89 wins, **50,0%**, retorno liquido **-17,8 unidades**. Houve grande dispersao por ativo e varios ativos tiveram menos de 10 sinais. Este resultado **reprova** a ativacao do gate para capital real e nao sustenta a alegacao de 98%. O relatorio esta em `reports/m5_validation_batch_300.json`.

Observacao: o lote de 2.000 candles foi interrompido por custo computacional excessivo dos detectores recalculados a cada candle; o limite de 300 esta registrado no relatorio. A proxima melhoria deve otimizar calculos incrementalmente antes de ampliar a janela, sem mudar o contrato temporal.

## Otimizacao segura (2026-09-20)

Foi criado o caminho `smc_reversal_flags()`, que calcula somente as oito flags consumidas pelo gate, em vez de calcular tambem EMA200, RSI/ADX, Bollinger, S/R e trendlines de painel. Em benchmark de 100 candles reais, o resultado do gate foi identico e o tempo caiu de 0,071s para 0,038s (**1,87x**).

Tambem foi aplicado pre-calculo vetorial do corpo/range, sem alterar o criterio de aprovacao. O pre-filtro ATR vetorizado foi removido porque nao reproduziu bit a bit a implementacao historica; nao foi mantido nenhum ganho que alterasse sinais.

O lote otimizado atual esta em `reports/m5_validation_batch_300_optimized_equivalent.json`: 177 sinais, 89 wins, 50,28% e -16,8 unidades. O relatorio anterior tinha 178 sinais; a divergencia ficou isolada em AVAX e nao sera tratada como equivalencia certificada sem uma fixture versionada. O caminho lean foi comparado diretamente no mesmo frame normalizado e nao apresentou divergencias por candle.

## Correcao de falso positivo temporal (2026-09-20)

O gate anterior aceitava um sweep historico e um FVG antigo como confirmacao da vela atual. O detector de sweep tambem retornava a primeira ocorrencia da serie. Foi adicionada idade do evento e limite de 3 candles para sweep, FVG e inducement, com busca do sweep na janela recente correta.

No mesmo lote de 38 ativos e 300 candles recentes: **13 sinais, 9 wins, 69,23%, +3,2 unidades**. O intervalo Wilson de 95% e apenas **42,37% a 87,32%**. Portanto a correcao e tecnicamente promissora, mas ainda nao prova consistencia; 13 sinais sao insuficientes e o limite inferior esta muito abaixo de qualquer criterio de producao.

Relatorio: `reports/m5_validation_batch_300_recent_events_v2.json`. O gate continua fora do pipeline oficial e bloqueado para capital real.

## Correcao da semantica de entrada binaria (2026-09-20)

O avaliador inicialmente comparava `close(T+1)` com `close(T)`. Isso nao representa uma entrada binaria apos o fechamento de T: a entrada real e a abertura de T+1 e a expiracao e o fechamento de T+1. O contrato foi corrigido para `open_of_outcome_candle`.

Revalidacao da mesma amostra: **13 sinais, 7 wins, 53,85%, -0,4 unidades**. Relatorio: `reports/m5_validation_batch_300_binary_open.json`. Este e o resultado valido; a leitura de 69,23% foi invalidada por lookahead/entrada incorreta e nao deve ser usada como evidencia de melhoria.

## Probe intrabar da entrada no pavio (2026-09-20)

Foi coletada uma amostra M1 recente para 38 ativos e testado o contrato descrito pelo operador: sweep do max/min de 20 candles M5, reclaim no primeiro minuto e entrada ate o fechamento da mesma M5. Resultado: **10.132 sinais, 3.984 wins, 39,32%, -2.960,8 unidades** com payout 0,80.

Conclusao: sweep/reclaim puro e perdedor e nao sera integrado. A vantagem alegada pelo produto comercial nao pode ser atribuida apenas a pavio; deve envolver selecao contextual, horario, ativo, expiracao, feed ou outra regra ainda nao identificada. Relatorio: `reports/m5_intrabar_probe.json`.
