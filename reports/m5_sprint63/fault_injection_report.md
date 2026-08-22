# Fault Injection Report — m5s63-3f15e368

Mode: full  Baseline: m5s62-41db6545  Created: 2026-09-05T00:37:12.745115+00:00

## Incidents

| # | incident_id | fault_type | cycle_id | target_candle | affected_asset | final_state | recovery_s |
|---|---|---|---|---|---|---|---|
| 0 | inc-add16e23 | DATA_PROVIDER_FAILURE | m5s63-provider-d316 | 2026-09-04T23:30:00+00:00 | EURUSD=X | ERROR | 43.985 |
| 1 | inc-825f56f9 | WORKER_CRASH | m5s63-crash-8215 | 2026-09-04T23:30:00+00:00 | GBPUSD=X | ERROR | 39.84 |
| 2 | inc-815a2e87 | WORKER_TIMEOUT | m5s63-timeout-35ce | 2026-09-04T23:30:00+00:00 | EURUSD=X | TIMEOUT | 20.531 |
| 3 | inc-2f86e249 | PER_ASSET_EXCEPTION | m5s63-isolation-f3bb | 2026-09-04T23:30:00+00:00 | USDJPY=X | ERROR | 40.604 |
| 4 | inc-f22fc683 | QUEUE_PRESSURE | m5s63-queue-6da0 | 2026-09-04T23:30:00+00:00 | EURUSD=X | COMPLETED | 48.45 |
| 5 | inc-1f070070 | WATCHDOG_STALL | m5s63-wd-a992 | 2026-09-04T23:30:00+00:00 | WATCHDOG | STALL_DETECTED | 0.707 |
| 6 | inc-8d50e85b | GRACEFUL_SIGINT | m5s63-shutdown-sigint-d24a | 2026-09-04T23:30:00+00:00 | SIGINT | SHUTDOWN | 7.786 |
| 7 | inc-76c7d5c2 | GRACEFUL_SIGTERM | m5s63-shutdown-sigterm-cf66 | 2026-09-04T23:30:00+00:00 | SIGTERM | SHUTDOWN | 8.059 |
| 8 | inc-561bc3fd | RESTART_INTEGRITY | m5-test-202609042340-e781 | 2026-09-04T23:40:00+00:00 | RESTART | NO_DUPLICATE | 90.853 |

## Gate Summary
- ARCHITECTURE: PASS
- BASELINE_INTEGRITY: PASS
- DATA_INTEGRITY: PASS
- WORKER_CRASH: PASS
- WORKER_TIMEOUT: PASS
- ASSET_ISOLATION: PASS
- QUEUE_PRESSURE: PASS
- WATCHDOG: PASS
- GRACEFUL_SHUTDOWN: PASS
- RESTART_INTEGRITY: PASS
- FRESHNESS: PASS
- CONCURRENCY: PASS
- RECOVERY: PASS
- LIVE_RECOVERY: PASS
- PERFORMANCE: PASS
- RESOURCE_SOAK: PASS
- DETERMINISM: PASS
- REGRESSION: PASS
- OPERATIONAL: PASS

## Data Integrity
- stale_as_fresh_total: 0 (required 0)
- error_as_wait_total: 0 (required 0)
- orphan_workers: 0 (required 0)
- restart no_duplicate: True (required true)
- watchdog_ok: True