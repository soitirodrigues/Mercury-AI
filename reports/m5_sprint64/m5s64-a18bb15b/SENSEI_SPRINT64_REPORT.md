# SENSEI SPRINT 6.4 — AUDITABILITY, OBSERVABILITY & REPLAY INTEGRITY — m5s64-a18bb15b

**Data:** 2026-09-05T05:06:13.651103+00:00
**Session:** m5s64-a18bb15b  mode LIVE_CLOCK  baseline m5s62-41db6545 wall 114.4 min (1.91 h)
**Comando:** `python scripts/m5_sprint64_gate_runner.py --universe 64 --executor process --cycles 6 --mode live_clock`
**Quick:** True

## 1. Regra Zero
- Nenhuma alteracao em DecisionResolverEngine/DecisionResult/BUY/SELL/WAIT/probabilities/confidence/confluence/ranking/pesos/Top3/trade_allowed/DQ/MTF/universe/AnalysisPipeline/ranking.py
- Formula: `ranking_score = confluence_weighted (0-100) + confidence_100*0.30 + grade_bonus(A+25/A20/B15/C10/D5) + dominant_prob*0.20 ; tie-breaker: internal_symbol ASC, audit_id ASC. Eligibility: status==REAL_SIGNAL AND decision in (BUY,SELL) AND trade_allowed==true AND prob_sum_ok==true AND confidence not None AND confluence not None`

## 2. Baseline
- frozen determinism: SKIP

## 3. Live Audit
- cycles 2/2 qual 2/2
- stale_as_fresh 0 orphan 0 no_dup True
- audit_records 2 missing 0 integrity True
- replay 2/2 div 0
- events 34 loss 0 dup 0 order_viol 0

## 4. Replay/Tamper
- tamper_detected: True
- cross_executor_audit: PASS
- crash_recovery: True corrupt_accepted False

## 5. Gates §24
- ARCHITECTURE: PASS
- BASELINE_INTEGRITY: PASS
- AUDIT_IDENTITY: PASS
- AUDIT_IMMUTABILITY: PASS
- ARTIFACT_INTEGRITY: PASS
- TAMPER_DETECTION: PASS
- EVENT_OBSERVABILITY: PASS
- EVENT_ORDERING: PASS
- EVENT_COMPLETENESS: PASS
- DECISION_PROVENANCE: PASS
- REPLAY_INTEGRITY: PASS
- DETERMINISTIC_REPLAY: PASS
- FAULT_REPLAY: PASS
- FRESHNESS_REPLAY: PASS
- CROSS_EXECUTOR_AUDIT: PASS
- ARTIFACT_WRITE_RECOVERY: PASS
- AUDIT_CONTINUITY: PASS
- QUEUE_OBSERVABILITY: PASS
- LIVE_AUDIT: PASS
- PERFORMANCE: PASS
- RESOURCE_SOAK: PASS
- DETERMINISM: PASS
- REGRESSION: PASS
- OPERATIONAL: PASS

## 6. Certificacao §25
- baseline_determinism: PASS
- regression: PASS
- artifact_integrity_pass: PASS
- artifact_hash_mismatch_total==0: PASS
- missing_artifact_total==0: PASS
- corrupt_artifact_accepted==false: PASS
- replay_divergence_total==0: PASS
- deterministic_replay: PASS
- fault_replay_integrity: PASS
- event_loss_total==0: PASS
- duplicate_event_total==0: PASS
- event_order_violation_total==0: PASS
- decision_without_provenance_total==0: PASS
- replay_stale_as_fresh_total==0: PASS
- replay_error_as_wait_total==0: PASS
- orphan_workers==0: PASS
- no_duplicate_target_candle: PASS
- tamper_detection: PASS
- artifact_write_recovery: PASS
- audit_continuity: PASS
- cross_executor_audit: PASS
- live_audit: PASS

## 7. Status Final
**SPRINT 6.4 = AUDIT & REPLAY CERTIFIED**
