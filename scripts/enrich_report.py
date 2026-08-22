import json, pathlib
p = pathlib.Path('reports/asset_universe/m5_continuous_scanner.json')
data = json.loads(p.read_text(encoding='utf-8'))
last = data['cycles'][-1] if data['cycles'] else {}
data['verdict'] = {
    'CONTINUOUS_SCANNER': 'PASS',
    'FRESHNESS_CONTROL': 'PASS',
    'INCREMENTAL_MODEL': 'PARTIAL',
    'MTF_INCREMENTAL': 'NOT_PROVEN',
    'CACHE': 'PARTIAL',
    'PARALLELIZATION': 'NEEDS_MORE_TEST',
    'TIME_TO_FIRST_DECISION': '21.9s (cycle2) / 27.8s (cycle1) — 12 assets seq',
    'TIME_TO_PARTIAL_TOP3': '70.2s (cycle2) / 84.9s (cycle1) — 12 assets seq',
    'TIME_TO_COMPLETE_TOP3': '296.2s (cycle2) / 285.1s (cycle1) — 12 assets seq; 82s com 2 workers',
    'RECOMMENDED_NEXT_STEP': 'E) combinacao: A) otimizar MTF (78% bottleneck) + B) paralelizacao controlada com emissao incremental + C) cache validado por candle + D) scanner continuo permanente com rolling queue',
    'details': {
        'continuous_scanner_reason': 'PASS: 2 ciclos completos, 24 decisoes, 0 erros, queue P1 detectou nova vela M5 (12/12 just closed), freshness FRESH/STALE/DATA_UNAVAILABLE explicito, Top-3 PARTIAL em ~70s e COMPLETE em ~285s sem esperar batch, audit rastreavel.',
        'freshness_reason': 'PASS: decision_candle == latest_available => FRESH; < latest => STALE; nunca convertido em REAL_SIGNAL; DataQuality UNavailable preservado; nova vela dispara P1.',
        'incremental_reason': 'PARTIAL: temporal/freshness/queue/cache/ranking SAFE; MTF compute e Trend/Liquidity/Volatility sao REQUIRES_FULL_RECALC ou UNKNOWN — nao otimizar silenciosamente.',
        'mtf_reason': 'NOT_PROVEN: 7 REQUIRES_FULL_RECALC (fetch + IndicatorEngine + Structure), 3 UNKNOWN (Trend/Liquidity/Volatility), 4 SAFE (Consensus/Normalize/Ranking). MTF 78% nao reduzido neste sprint.',
        'cache_reason': 'PARTIAL: SAFE (validado por candle, nao TTL cego; HIT so se cached==required, STALE se < required); medicao HIT 24 MISS 12 STALE 12 REFRESH 24 — correto mas fetch 2.6% do wall, economiza ~21s em 1026s, insuficiente.',
        'parallel_reason': 'NEEDS_MORE_TEST: 12 assets seq 285s vs par2 82s (3.4x) mas time_to_first degradou em batch par; DeterministicClock SAFE, SnapshotLogger SAFE, tracemalloc mitigado, yfinance rate limit UNKNOWN; precisa emissao incremental por worker + backoff/jitter + teste 64.',
    }
}
data['UNIVERSE_SIZE'] = data.get('universe_size')
data['CYCLES_TESTED'] = data.get('cycles_tested')
data['TIME_TO_FIRST_DECISION'] = last.get('time_to_first_decision_s')
data['TIME_TO_PARTIAL_TOP3'] = last.get('time_to_partial_top3_s')
data['TIME_TO_COMPLETE_TOP3'] = last.get('time_to_complete_top3_s')
data['FRESH_RESULTS'] = data['summary']['fresh_results']
data['STALE_RESULTS'] = data['summary']['stale_results']
data['DATA_UNAVAILABLE'] = data['summary']['data_unavailable']
data['PROVIDER_ERRORS'] = data['summary']['provider_errors']
data['CACHE_HIT'] = data['summary']['cache_hit']
data['CACHE_MISS'] = data['summary']['cache_miss']
data['CACHE_STALE'] = data['summary']['cache_stale']
data['CACHE_REFRESH'] = data['summary']['cache_refresh']
data['SEQUENTIAL_TIME'] = 285.182
data['CONTROLLED_PARALLEL_TIME'] = 81.968
data['MTF_REUSABLE_COMPONENTS'] = data['mtf_classification']['safe_incremental']
data['MTF_FULL_RECALC_COMPONENTS'] = data['mtf_classification']['requires_full_recalc']
data['MTF_UNKNOWN_COMPONENTS'] = data['mtf_classification']['unknown']
data['TOP3_PARTIAL'] = data['top3']['partial']
data['TOP3_COMPLETE'] = data['top3']['complete']
data['comparison'] = {
    'CURRENT_BATCH_64_seq_s': 1026.14,
    'CONTINUOUS_12_seq_s': 285.182,
    'CONTINUOUS_12_par2_s': 81.968,
    'batch_time_to_first_64': 'N/A (batch so entrega apos 64)',
    'continuous_time_to_first_12': '21-27s',
    'continuous_time_to_partial_12': '70-85s',
    'extrapolated_64_continuous_seq_projection_s': round(285.182/12*64,1),
    'extrapolated_64_continuous_par2_projection_s': round(81.968/12*64,1),
    'note': 'Projecao linear 12->64 e estimativa, nao medicao; MTF 78% domina, paralelizacao com 2 workers projeta ~437s ainda >300s para 64.',
    'encerramento_criterios': {
        '1_nova_vela_dispara_incremental': 'PASS — ciclo 2 P1=12 just closed (14:55->15:00)',
        '2_decisoes_antigas_nao_apresentadas_como_novas': 'PASS — freshness STALE explicito, audit_id diferente por vela',
        '3_nao_espera_64_para_primeiro_resultado': 'PASS — first 22s, partial Top3 70s vs complete 285s (12)',
        '4_top3_mesma_logica_oficial': 'PASS — mercury_ai.operations.ranking FORMULA identica',
        '5_DecisionResolver_intocado': 'PASS — git diff 0 alteracao',
        '6_rastreaveis': 'PASS — audit_id 64hex, decision_candle, data_latest, snapshot_file, timestamp',
        '7_medicao_REAL': 'PASS — wall clock medido por ciclo (perf_counter)',
    }
}
data['regression_gates'] = {
    'top3_scanner': 'PASS (57 eligible, 68 records)',
    'top3_determinism': 'PASS (hash run1==run2 f556e527)',
    'DECISION_INTEGRITY': 'PASS',
    'PROBABILITY_SUM': 'PASS (0 fails)',
    'RESOLVER_INTEGRITY': 'PASS (0 inconsistencias REAL_SIGNAL)',
    'POST_RESOLVER_INTEGRITY': 'PASS (5 fails sao DATA_UNAVAILABLE esperados)',
    'TOP3_TRACEABILITY': 'PASS',
    'NO_DECISION_FABRICATION': 'PASS',
    'FRESHNESS_GATE': 'PASS',
}
p.write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding='utf-8')
print('Enriched', p)
