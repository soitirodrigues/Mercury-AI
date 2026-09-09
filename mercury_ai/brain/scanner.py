import logging
import time
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.core.asset_registry import AssetRegistry
from mercury_ai.config.configuration_center import MercuryConfigCenter

from mercury_ai.providers.mercury_data_provider import MercuryDataProvider

from mercury_ai.analysis.ranking_engine import RankingEngine
from mercury_ai.brain.institutional_brain import InstitutionalBrain
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.analysis.notification_center import NotificationCenter
from mercury_ai.core.exceptions import (
    MarketClosedException,
    DataValidationError,
    InvalidSymbolError,
    ProviderError,
)
from mercury_ai.sessions.market_sessions import MarketSessions
from mercury_ai.utils.deterministic_clock import DeterministicClock

logger = logging.getLogger(__name__)

# Estados terminais observáveis emitidos pelo pipeline via decision.audit_id.
# Um WAIT legítimo carrega audit_id = hash sha256 (64 hex) gerado pelo
# DecisionResultBuilder — nunca coincide com estes estados reservados.
# Erros de pipeline/provider: NÃO entram no ranking, NÃO sobrescrevem stats.
PIPELINE_ERROR_STATES = frozenset({
    "PIPELINE_ERROR",
    "DATA_PROVIDER_UNAVAILABLE",
})
# Estados de análise descartada (não são oportunidades nem erros fatais):
# registrados de forma observável, fora do ranking e das estatísticas do ativo.
PIPELINE_SKIP_STATES = frozenset({
    "DATA_QUALITY_FAIL",
    "INSUFFICIENT_DATA",
    "MARKET_CLOSED",
})

# S33-E — status explícitos de ciclo de scan (Fase 3: TOP3 parcial honesto).
# COMPLETE: universo elegível inteiro processado dentro do cycle_timeout.
# PARTIAL: cycle_timeout atingido mas >=1 ativo concluído (TOP3 parcial válido).
# TIMEOUT: cycle_timeout atingido sem nenhum ativo concluído.
# ERROR: falha antes/depois do loop (ex: universo vazio por erro, ranking).
SCAN_COMPLETE = "COMPLETE"
SCAN_PARTIAL = "PARTIAL"
SCAN_TIMEOUT = "TIMEOUT"
SCAN_ERROR = "ERROR"

# S33-E: default operacional — workers e timeouts alinhados à janela M5.
# cycle_timeout_s=290s (janela M5 300s com margem); worker_timeout não é
# enforceado por ativo no ThreadPool (fut.result sem timeout individual para
# não abortar pipeline no meio de persistência) — o deadline global do ciclo
# é que decide PARTIAL vs COMPLETE.
SCAN_DEFAULT_WORKERS = 4
SCAN_DEFAULT_CYCLE_TIMEOUT_S = 290.0


@dataclass
class ScanReport:
    """Envelope observável de um ciclo de scan (S33-E Fase 3).

    NUNCA mistura execuções: cada scan gera um scan_id (uuid4) registrado em
    todas as linhas per_asset. ranked/top3 preservam a semântica do caminho
    sequencial (mesma ordenação do RankingEngine). status distingue
    COMPLETE/PARTIAL/TIMEOUT/ERROR — parcial nunca é declarado completo.
    """

    scan_id: str
    status: str
    ranked: List[Any] = field(default_factory=list)
    top3: List[Any] = field(default_factory=list)
    symbols_total: int = 0
    symbols_completed: int = 0
    symbols_timeout: int = 0
    symbols_error: int = 0
    per_asset: List[Dict[str, Any]] = field(default_factory=list)
    duration_s: float = 0.0
    cycle_timeout_s: float = SCAN_DEFAULT_CYCLE_TIMEOUT_S
    workers: int = 1
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        def _summarize(a: Any) -> Dict[str, Any]:
            try:
                dec = getattr(a, "decision", None)
                mkt = getattr(a, "market", None)
                reg = getattr(a, "market_regime", None)
                return {
                    "symbol": getattr(mkt, "symbol", "?"),
                    "decision": getattr(dec, "decision", "?"),
                    "score": getattr(dec, "score", None),
                    "confidence": getattr(dec, "confidence", None),
                    "grade": getattr(dec, "grade", None),
                    "audit_id": getattr(dec, "audit_id", None),
                    "regime": getattr(reg, "regime", None) if reg else None,
                }
            except Exception:
                return {"symbol": "?", "error": "summarize-failed"}

        return {
            "scan_id": self.scan_id,
            "status": self.status,
            "symbols_total": self.symbols_total,
            "symbols_completed": self.symbols_completed,
            "symbols_timeout": self.symbols_timeout,
            "symbols_error": self.symbols_error,
            "duration_s": round(self.duration_s, 2),
            "cycle_timeout_s": self.cycle_timeout_s,
            "workers": self.workers,
            "ranked": [_summarize(a) for a in self.ranked],
            "top3": [_summarize(a) for a in self.top3],
            "per_asset": self.per_asset,
            "error": self.error,
        }


class MercuryScanner:

    def __init__(self, min_quality_score=40.0):

        # Provider central V1
        self.provider = MercuryDataProvider()
        self.provider_manager = self.provider  # alias para compatibilidade com testes

        # Pipeline institucional
        self.pipeline = AnalysisPipeline(
            market_service=MarketDataService(
                provider=self.provider
            ),
            providers=[
                self.provider
            ]
        )

        self.ranking_engine = RankingEngine()
        self.brain = InstitutionalBrain()

        self.min_quality_score = min_quality_score

        self.asset_registry = AssetRegistry()

        self.config = MercuryConfigCenter()

        self.notification_center = NotificationCenter()

        # S33-E: envelope observável do último ciclo (None antes do 1º scan).
        self.last_scan_report: Optional[ScanReport] = None

    def scan(self, workers: int = 1, cycle_timeout_s: float = SCAN_DEFAULT_CYCLE_TIMEOUT_S):
        """Executa o scan do universo operacional.

        S33-E: path sequencial (workers<=1, default) preserva byte-a-byte o
        comportamento legado — mesma ordem, mesmos logs, mesmo retorno
        (lista ranked). Path paralelo opt-in (workers>1) usa pipelines
        isoladas por ativo + deadline global do ciclo + ScanReport com status
        COMPLETE/PARTIAL/TIMEOUT/ERROR. Replay (clock congelado) SEMPRE usa o
        path sequencial para preservar determinismo (thread-local clock não
        herdado por workers).
        """

        symbols, replay_isolated, filtered_by_session = self._resolve_scan_symbols()

        # Observabilidade: quando tudo foi filtrado por sessao, registrar vazio
        if not symbols and filtered_by_session:
            logger.info("SESSION_FILTER: nenhum ativo elegivel para este ciclo (weekend Forex)")

        if not symbols:
            ranked: List[Any] = []
            self.last_scan_report = ScanReport(
                scan_id=str(uuid.uuid4()),
                status=SCAN_COMPLETE,
                ranked=ranked,
                top3=[],
                symbols_total=0,
                symbols_completed=0,
                symbols_timeout=0,
                symbols_error=0,
                per_asset=[],
                duration_s=0.0,
                cycle_timeout_s=cycle_timeout_s,
                workers=workers,
            )
            return ranked

        # Replay determinístico nunca paraleliza (clock thread-local).
        if replay_isolated or workers is None or workers <= 1 or len(symbols) <= 1:
            return self._scan_sequential(symbols, filtered_by_session, workers=1, cycle_timeout_s=cycle_timeout_s)

        return self._scan_parallel(symbols, workers=workers, cycle_timeout_s=cycle_timeout_s)

    def _resolve_scan_symbols(self):
        """Pré-ambulo compartilhado: perfil, broker, registry, session gate.

        Retorna (symbols, replay_isolated, filtered_by_session).
        Não executa pipeline — sem efeito colateral além de logs.
        """

        logger.info("=" * 60)
        logger.info("MERCURY AI SCANNER")
        logger.info("=" * 60)

        active_profile = self.config.get(
            "OPERATIONAL_PROFILE",
            "active",
            "Demo"
        )

        active_broker = self.config.get(
            "OPERATIONAL_PROFILE",
            "broker",
            "XP"
        )

        authorized_symbols = (
            self.asset_registry
            .get_assets_for_broker(active_broker)
        )

        if not authorized_symbols:
            logger.warning(
                "Nenhum ativo autorizado para o broker '%s'. "
                "Verifique data/brokers/%s.json "
                "(perfil ativo: %s). Ranking vazio.",
                active_broker,
                active_broker,
                active_profile,
            )

        enabled_assets = [
            a
            for a in self.asset_registry.assets.values()
            if (
                a.enabled
                and a.profile == active_profile
                and a.symbol in authorized_symbols
            )
        ]

        enabled_assets.sort(
            key=lambda a: (
                -a.favorite,
                -a.last_operated,
                -a.previous_score,
                -a.priority,
                -a.liquidity,
                a.spread
            )
        )

        # F2 — Session eligibility gate (antes de pipeline).
        # Replay: quando DeterministicClock estiver congelado, o scanner esta
        # sendo usado dentro de HistoricalReplayEngine; nesse caso NAO aplicar
        # gate de sessao live (replay deve ser deterministico por indice, nao
        # por calendario real). Bypass observavel via replay_isolated flag.
        replay_isolated = DeterministicClock.is_frozen()
        filtered_by_session: list = []
        if not replay_isolated:
            gate = MarketSessions()
            kept = []
            for a in enabled_assets:
                # resolve market via universe (FOREX/CRYPTO) — fallback via Asset.category
                try:
                    from mercury_ai.config.universe import get_asset
                    ua = get_asset(a.symbol)
                    market = ua.market if ua is not None else (a.market or a.category or "")
                except Exception:
                    market = a.market or a.category or ""
                if gate.is_market_eligible(market):
                    kept.append(a)
                else:
                    filtered_by_session.append(a.symbol)
                    logger.info(
                        "SESSION_FILTER: %s (%s) -> NOT ELIGIBLE (weekend, %s)",
                        a.symbol, market, gate.eligibility_reason(market),
                    )
            if filtered_by_session:
                logger.info(
                    "SESSION_FILTER: %s ativos filtrados (Forex weekend), %s seguem para analise",
                    len(filtered_by_session), len(kept),
                )
            enabled_assets = kept

        symbols = [
            a.symbol
            for a in enabled_assets
        ]

        return symbols, replay_isolated, filtered_by_session

    def _scan_sequential(self, symbols, filtered_by_session, workers=1, cycle_timeout_s=SCAN_DEFAULT_CYCLE_TIMEOUT_S):
        """Path legado verbatim: loop sequencial com o pipeline compartilhado."""

        scan_id = str(uuid.uuid4())
        t_start = time.perf_counter()
        analyses = []
        per_asset: List[Dict[str, Any]] = []
        n_timeout = 0
        n_error = 0
        # S33-E.2 P3 — envelope de correlação do ciclo (transitório, nunca
        # persistido no snapshot; identidades audit/replay/run/session intactas).
        try:
            self.pipeline.scan_id_context = scan_id
        except Exception:
            pass

        for symbol in symbols:

            try:

                logger.info("Analisando %s...", symbol)
                t0 = time.perf_counter()

                # Analise pelo provider V1
                analysis = self.pipeline.analyze(symbol)

                # Transparência (ACHADO 1/2/5): distingue estados de erro/
                # indisponibilidade de um WAIT legítimo (audit_id = hash sha256).
                # Erros NÃO entram no ranking e NÃO sobrescrevem as estatísticas
                # do ativo (evita corromper previous_score com score 0).
                audit_id = analysis.decision.audit_id
                if audit_id in PIPELINE_ERROR_STATES:
                    logger.error(
                        ">>> ERRO DE PIPELINE em %s: audit_id=%s | %s | score=%.2f",
                        symbol,
                        audit_id,
                        analysis.decision.summary,
                        analysis.decision.score,
                    )
                    self._trigger_failover(
                        symbol,
                        f"{audit_id}: {analysis.decision.summary}",
                    )
                    n_error += 1
                    per_asset.append(self._row(scan_id, symbol, "ERROR", analysis, time.perf_counter() - t0, None))
                    continue

                if audit_id in PIPELINE_SKIP_STATES:
                    logger.warning(
                        ">>> ANÁLISE DESCARTADA em %s (estado observável): audit_id=%s | %s | score=%.2f",
                        symbol,
                        audit_id,
                        analysis.decision.summary,
                        analysis.decision.score,
                    )
                    per_asset.append(self._row(scan_id, symbol, f"SKIPPED_{audit_id}", analysis, time.perf_counter() - t0, None))
                    continue

                logger.debug("=" * 80)
                logger.debug("DEBUG ANALYSIS")
                logger.debug("=" * 80)

                logger.debug("Decision : %s", analysis.decision.decision)
                logger.debug("Score    : %s", analysis.decision.score)
                logger.debug("Confidence: %s", analysis.decision.confidence)
                logger.debug("BUY      : %s", analysis.decision.buy_probability)
                logger.debug("SELL     : %s", analysis.decision.sell_probability)
                logger.debug("WAIT     : %s", analysis.decision.wait_probability)

                logger.debug("=" * 80)

                score = analysis.decision.score
                

                self.asset_registry.update_asset_stats(
                    symbol,
                    score
                )

                logger.info("Scanner Score........: %.2f", score)
                logger.info("Score mínimo.........: %.2f", self.min_quality_score)

                if score < self.min_quality_score:
                    logger.info(">>> DESCARTADO PELO SCANNER <<<")
                    per_asset.append(self._row(scan_id, symbol, "DISCARDED_SCORE", analysis, time.perf_counter() - t0, None))
                    continue

                logger.info(">>> ADICIONADO AO RANKING <<<")

                analyses.append(
                    analysis
                )
                per_asset.append(self._row(scan_id, symbol, "RANKED", analysis, time.perf_counter() - t0, None))

                self._print_report(
                    analysis
                )

            except (MarketClosedException, DataValidationError, InvalidSymbolError, ProviderError, ConnectionError, TimeoutError, OSError, ValueError, KeyError) as e:

                logger.error("=" * 80)
                logger.error("ERRO DURANTE A ANÁLISE DE %s", symbol)
                logger.error("=" * 80)

                traceback.print_exc()

                logger.error("Mensagem: %s", e)

                logger.error("=" * 80)

                n_error += 1
                per_asset.append(self._row(scan_id, symbol, "EXCEPTION", None, time.perf_counter() - t0, e))

                # Trigger provider failover on failure
                if hasattr(self, 'provider_manager') and self.provider_manager is not None:
                    try:
                        self.provider_manager.trigger_failover()
                        self.notification_center.send(
                            "scanner_failover",
                            {"symbol": symbol, "error": str(e)}
                        )
                    except (RuntimeError, ConnectionError, OSError, AttributeError) as failover_error:
                        logger.error("Falha no failover: %s", failover_error)

        # Observabilidade (ACHADO 6): expõe eventos de falha capturados pelo
        # audit_sink do pipeline. O sink é o mesmo objeto usado pelo pipeline,
        # então acumula as falhas de todos os símbolos deste ciclo de scan.
        failed_events = self.pipeline.get_failed_events()
        if failed_events:
            logger.error("=" * 60)
            logger.error(
                "EVENTOS DE FALHA DO PIPELINE (audit_sink): %d",
                len(failed_events),
            )
            for ev in failed_events:
                logger.error(
                    "  [%s] stage=%s tipo=%s erro=%s",
                    ev.symbol or "?",
                    ev.stage_name,
                    ev.error_type,
                    ev.error_message,
                )
            logger.error("=" * 60)

        ranked = self.ranking_engine.rank(
            analyses
        )

        self._print_ranking(
            ranked
        )

        logger.info("=" * 60)

        duration_s = time.perf_counter() - t_start
        self.last_scan_report = ScanReport(
            scan_id=scan_id,
            status=SCAN_COMPLETE,
            ranked=ranked,
            top3=list(ranked[:3]),
            symbols_total=len(symbols),
            symbols_completed=len([r for r in per_asset if r["outcome"] not in ("TIMEOUT",)]),
            symbols_timeout=0,
            symbols_error=n_error,
            per_asset=per_asset,
            duration_s=duration_s,
            cycle_timeout_s=cycle_timeout_s,
            workers=workers,
        )
        # S33-E.2 P3 — envelope transitório nunca vaza para o próximo ciclo.
        try:
            self.pipeline.scan_id_context = None
        except Exception:
            pass

        return ranked

    @staticmethod
    def _row(scan_id, symbol, outcome, analysis, duration_s, error):
        """Linha per_asset do ScanReport (S33-E Fase 3: identidade da execução)."""
        row = {
            "scan_id": scan_id,
            "symbol": symbol,
            "outcome": outcome,
            "duration_ms": round(duration_s * 1000, 1),
            "error": str(error) if error is not None else None,
        }
        try:
            if analysis is not None:
                dec = analysis.decision
                mkt = analysis.market
                reg = analysis.market_regime
                row.update({
                    "decision": getattr(dec, "decision", None),
                    "score": getattr(dec, "score", None),
                    "confidence": getattr(dec, "confidence", None),
                    "grade": getattr(dec, "grade", None),
                    "audit_id": getattr(dec, "audit_id", None),
                    "regime": getattr(reg, "regime", None) if reg else None,
                    "market_symbol": getattr(mkt, "symbol", symbol),
                })
        except Exception:
            pass
        return row

    def _build_worker_pipeline(self, scan_id=None):
        """Pipeline isolada por ativo (S33-E.2): provider+service+pipeline próprios.

        Espelha a construção do __init__ para equivalência seq×paralelo.
        Profiler desligado por worker (tracemalloc global não é thread-safe
        para uso concorrente).

        S33-E.2 P1 — isolamento de InstitutionalMemory (reusa o mecanismo
        existente `institutional_memory_path` de AnalysisPipeline, o mesmo
        usado por M5OperationalRunner via M5_WORKER_ISOLATED_MEMORY):
        cada worker recebe um tempfile JSON próprio (`m5_worker_mem_*`);
        NENHUM worker escreve em `data/institutional_memory.json`.
        Scoring/get_consistency_score intactos; sem merge com a global.
        S33-E.2 P3 — scan_id propaga só como envelope transitório
        (`pipeline.scan_id_context`); nunca entra no snapshot.
        """
        import tempfile as _tf
        import threading as _th
        from mercury_ai.providers.mercury_data_provider import MercuryDataProvider as _MDP
        from mercury_ai.data.market_data import MarketDataService as _MDS

        provider = _MDP()
        _tmp = _tf.NamedTemporaryFile(delete=False, prefix="m5_worker_mem_", suffix=".json")
        try:
            _tmp.write(b"[]")
            _tmp.close()
        except Exception:
            try:
                _tmp.close()
            except Exception:
                pass
        pipeline = AnalysisPipeline(
            market_service=_MDS(provider=provider),
            providers=[provider],
            institutional_memory_path=_tmp.name,
        )
        try:
            pipeline.profiler.active = False
        except Exception:
            pass
        try:
            # Lock privado por worker: nenhum estado compartilhado entre workers.
            pipeline.memory._lock = _th.Lock()
        except Exception:
            pass
        try:
            pipeline._worker_mem_tmp = _tmp.name
        except Exception:
            pass
        if scan_id is not None:
            try:
                pipeline.scan_id_context = scan_id
            except Exception:
                pass
        return pipeline

    def _analyze_symbol_isolated(self, symbol, scan_id=None):
        """Executa pipeline.analyze(symbol) em pipeline própria. Nunca levanta.

        Retorna (symbol, analysis, exc, dur, failed, worker_scan_id) — o
        worker ecoa o scan_id recebido para a parent amarrar resultado↔ciclo
        (P3); divergência = quarentena como órfão.
        """
        import os as _os
        t0 = time.perf_counter()
        try:
            pipeline = self._build_worker_pipeline(scan_id=scan_id)
            try:
                analysis = pipeline.analyze(symbol)
            finally:
                try:
                    _tmp = getattr(pipeline, "_worker_mem_tmp", None)
                    if _tmp:
                        _os.unlink(_tmp)
                except Exception:
                    pass
            try:
                failed = pipeline.get_failed_events()
            except Exception:
                failed = []
            return (symbol, analysis, None, time.perf_counter() - t0, failed, scan_id)
        except Exception as e:  # noqa: BLE001 — isolamento por ativo
            return (symbol, None, e, time.perf_counter() - t0, [], scan_id)

    def _scan_parallel(self, symbols, workers, cycle_timeout_s, worker_timeout_s=None):
        """Path paralelo opt-in (S33-E.2): ThreadPool bounded + deadline global.

        Classificação, registry updates, failover e logs acontecem na thread
        PARENT em ordem determinística de `symbols` — workers só executam
        pipeline.analyze. Resultado lógico idêntico ao sequencial; status
        COMPLETE/PARTIAL/TIMEOUT conforme deadline.

        S33-E.2 P4 — política reutilizada do M5OperationalRunner.run_cycle:
        worker_timeout (quando informado) conta SOMENTE a partir do momento
        em que o worker está RUNNING (`fut.running()`); workers na fila não
        consomem deadline. cycle_timeout global prevalece. Não há thread-kill:
        futuros estourados recebem `cancel()` (best-effort) e o resultado —
        mesmo que termine depois — é quarentenado como TIMEOUT/ORPHAN:
        fora de ranked/top3/registry/estado do ciclo. Efeitos persistentes do
        worker tardio permanecem isolados (P1: tempfile próprio + snapshot
        com nome único), e a amarração por scan_id (P3) impede que um
        resultado tardio seja atribuído ao scan seguinte.
        """
        scan_id = str(uuid.uuid4())
        t_start = time.perf_counter()
        deadline = t_start + cycle_timeout_s
        max_workers = max(1, min(int(workers), len(symbols)))
        logger.info(
            "S33-E parallel scan: %d ativos workers=%d cycle_timeout=%.0fs scan_id=%s",
            len(symbols), max_workers, cycle_timeout_s, scan_id,
        )

        analyses: List[Any] = []
        per_asset: List[Dict[str, Any]] = []
        n_error = 0

        ex = ThreadPoolExecutor(max_workers=max_workers)
        try:
            fut_to_sym = {ex.submit(self._analyze_symbol_isolated, s, scan_id): s for s in symbols}
            pending = set(fut_to_sym)
            done: Dict[str, Any] = {}
            fut_deadlines: Dict[Any, float] = {}
            worker_timed_out: Dict[str, Any] = {}

            def _refresh_deadlines():
                if worker_timeout_s is None:
                    return
                now_t = time.perf_counter()
                for fut in list(pending):
                    if fut in done or fut in worker_timed_out.values():
                        continue
                    try:
                        is_running = fut.running()
                    except Exception:
                        is_running = False
                    if is_running and fut not in fut_deadlines:
                        fut_deadlines[fut] = now_t + float(worker_timeout_s)

            while pending:
                remaining = deadline - time.perf_counter()
                if remaining <= 0:
                    break
                _refresh_deadlines()
                if fut_deadlines:
                    try:
                        nearest = min(fut_deadlines[f] for f in fut_deadlines if f in pending)
                    except ValueError:
                        nearest = None
                    if nearest is not None:
                        wait_timeout = min(nearest - time.perf_counter(), remaining, 1.0)
                    else:
                        wait_timeout = min(remaining, 1.0)
                else:
                    wait_timeout = min(remaining, 1.0)
                if wait_timeout < 0:
                    wait_timeout = 0
                finished, pending = wait(pending, timeout=max(wait_timeout, 0.05), return_when=FIRST_COMPLETED)
                for f in finished:
                    done[fut_to_sym[f]] = f
                    fut_deadlines.pop(f, None)
                # Timeouts por worker: só entre RUNNING com deadline atribuído.
                if worker_timeout_s is not None:
                    now2 = time.perf_counter()
                    for f in list(pending):
                        dl = fut_deadlines.get(f)
                        if dl is not None and now2 >= dl and f not in finished:
                            sym = fut_to_sym[f]
                            worker_timed_out[sym] = f
                            fut_deadlines.pop(f, None)
                            try:
                                f.cancel()
                            except Exception:
                                pass
                            logger.warning(
                                ">>> WORKER TIMEOUT em %s (worker %.0fs, ciclo %s)",
                                sym, float(worker_timeout_s), scan_id,
                            )
                    if worker_timed_out:
                        pending -= set(worker_timed_out.values())
            timed_out = {fut_to_sym[f] for f in pending}
            timed_out |= set(worker_timed_out.keys())

            for symbol in symbols:
                if symbol in timed_out:
                    logger.warning(">>> TIMEOUT DE CICLO em %s (deadline %.0fs)", symbol, cycle_timeout_s)
                    per_asset.append({
                        "scan_id": scan_id, "symbol": symbol, "outcome": "TIMEOUT",
                        "duration_ms": round(cycle_timeout_s * 1000, 1),
                        "error": f"cycle deadline {cycle_timeout_s}s exceeded",
                    })
                    continue
                fut = done.get(symbol)
                if fut is None:
                    n_error += 1
                    per_asset.append({
                        "scan_id": scan_id, "symbol": symbol, "outcome": "EXCEPTION",
                        "duration_ms": 0.0, "error": "future missing",
                    })
                    continue
                try:
                    _res = fut.result()
                except Exception as e:  # noqa: BLE001 — nunca deveria acontecer
                    n_error += 1
                    per_asset.append(self._row(scan_id, symbol, "EXCEPTION", None, 0.0, e))
                    continue
                try:
                    (_sym, analysis, exc, dur, failed, worker_scan_id) = _res
                except ValueError:
                    # Compat: doubles legados retornam tupla de 5 sem scan_id.
                    (_sym, analysis, exc, dur, failed) = _res
                    worker_scan_id = scan_id
                if worker_scan_id != scan_id:
                    # P3/P4 — resultado órfão de outro ciclo: quarentena total.
                    logger.warning(
                        ">>> ORFÃO QUARENTENADO em %s (scan %s != ciclo %s)",
                        symbol, worker_scan_id, scan_id,
                    )
                    per_asset.append({
                        "scan_id": scan_id, "symbol": symbol, "outcome": "TIMEOUT",
                        "duration_ms": round(dur * 1000, 1),
                        "error": f"orphan quarantined (worker scan {worker_scan_id})",
                    })
                    continue

                for ev in failed or []:
                    logger.error(
                        "  [%s] stage=%s tipo=%s erro=%s",
                        getattr(ev, "symbol", None) or symbol,
                        getattr(ev, "stage_name", "?"),
                        getattr(ev, "error_type", "?"),
                        getattr(ev, "error_message", "?"),
                    )

                if exc is not None or analysis is None:
                    logger.error("ERRO DURANTE A ANÁLISE DE %s: %s", symbol, exc)
                    n_error += 1
                    per_asset.append(self._row(scan_id, symbol, "EXCEPTION", None, dur, exc))
                    self._trigger_failover(symbol, str(exc) if exc else "unknown")
                    continue

                audit_id = analysis.decision.audit_id
                if audit_id in PIPELINE_ERROR_STATES:
                    logger.error(
                        ">>> ERRO DE PIPELINE em %s: audit_id=%s | %s | score=%.2f",
                        symbol, audit_id, analysis.decision.summary, analysis.decision.score,
                    )
                    n_error += 1
                    per_asset.append(self._row(scan_id, symbol, "ERROR", analysis, dur, None))
                    self._trigger_failover(symbol, f"{audit_id}: {analysis.decision.summary}")
                    continue

                if audit_id in PIPELINE_SKIP_STATES:
                    logger.warning(
                        ">>> ANÁLISE DESCARTADA em %s (estado observável): audit_id=%s | %s | score=%.2f",
                        symbol, audit_id, analysis.decision.summary, analysis.decision.score,
                    )
                    per_asset.append(self._row(scan_id, symbol, f"SKIPPED_{audit_id}", analysis, dur, None))
                    continue

                score = analysis.decision.score
                self.asset_registry.update_asset_stats(symbol, score)
                logger.info("Scanner Score........: %.2f", score)
                if score < self.min_quality_score:
                    logger.info(">>> DESCARTADO PELO SCANNER <<<")
                    per_asset.append(self._row(scan_id, symbol, "DISCARDED_SCORE", analysis, dur, None))
                    continue

                logger.info(">>> ADICIONADO AO RANKING <<<")
                analyses.append(analysis)
                per_asset.append(self._row(scan_id, symbol, "RANKED", analysis, dur, None))
        finally:
            # Não bloquear no deadline: cancela pendentes; órfãs quarentenadas
            # via scan_id (P3) + memória isolada por worker (P1: tempfile
            # próprio, apagado ao fim de _analyze_symbol_isolated) — nenhum
            # efeito persistente de worker tardio alcança ranked/top3/registry
            # (P4, política M5OperationalRunner: cancel best-effort, sem thread-kill).
            try:
                ex.shutdown(wait=False, cancel_futures=True)
            except TypeError:
                ex.shutdown(wait=False)

        ranked = self.ranking_engine.rank(analyses)
        self._print_ranking(ranked)
        logger.info("=" * 60)

        n_timeout = len([r for r in per_asset if r["outcome"] == "TIMEOUT"])
        n_completed = len([r for r in per_asset if r["outcome"] != "TIMEOUT"])
        if n_timeout == 0:
            status = SCAN_COMPLETE
        elif n_completed > 0:
            status = SCAN_PARTIAL
        else:
            status = SCAN_TIMEOUT

        duration_s = time.perf_counter() - t_start
        self.last_scan_report = ScanReport(
            scan_id=scan_id,
            status=status,
            ranked=ranked,
            top3=list(ranked[:3]),
            symbols_total=len(symbols),
            symbols_completed=n_completed,
            symbols_timeout=n_timeout,
            symbols_error=n_error,
            per_asset=per_asset,
            duration_s=duration_s,
            cycle_timeout_s=cycle_timeout_s,
            workers=max_workers,
        )
        logger.info(
            "S33-E scan %s status=%s completed=%d timeout=%d errors=%d wall=%.1fs",
            scan_id, status, n_completed, n_timeout, n_error, duration_s,
        )
        return ranked

    def get_download_stats(self) -> Dict[str, Any]:
        """Agrega contadores do YahooAdapter (downloads reais, hits, misses)."""
        try:
            yahoo = self.provider._providers.get("Yahoo")
            if yahoo is not None and hasattr(yahoo, "get_cache_stats"):
                return yahoo.get_cache_stats()
        except Exception:
            pass
        return {"downloads": None, "hits": None, "misses": None, "entries": None}

    def _trigger_failover(self, symbol, reason):
        """Failover honesto (ACHADO 5): tenta alternar de provider e reporta
        com verdade se existe ou não provider funcional de contingência.

        Com a correção do ACHADO 4, adapters stub não são 'healthy', portanto
        trigger_failover retorna False quando não há provider secundário real —
        e isso é registrado como erro, em vez de falhar silenciosamente para
        um stub que devolveria um DataFrame vazio.
        """
        if self.provider_manager is None:
            return

        try:
            failover_ok = self.provider_manager.trigger_failover(reason=reason)
            if not failover_ok:
                logger.error(
                    "Sem provider funcional de contingência para %s (%s)",
                    symbol,
                    reason,
                )
            self.notification_center.send(
                "scanner_failover",
                {
                    "symbol": symbol,
                    "error": reason,
                    "failover": bool(failover_ok),
                },
            )
        except (RuntimeError, ConnectionError, OSError, AttributeError) as e:
            logger.error("Falha no failover: %s", e)

    def _print_ranking(self, ranked):

        logger.info("=" * 60)
        logger.info("RANKING INSTITUCIONAL DE OPORTUNIDADES")
        logger.info("=" * 60)

        for index, analysis in enumerate(ranked):

            score = analysis.decision.score

            logger.info(
                "%d. %-10s | Score: %.2f | %s",
                index + 1,
                analysis.market.symbol,
                score,
                analysis.decision.decision,
            )

            logger.info(
                "%s",
                self.brain
                .explain(analysis)
                .replace("\n", " "),
            )

        logger.info("=" * 60)

    def _print_report(self, analysis):

        market = analysis.market
        decision = analysis.decision
        regime = analysis.market_regime

        logger.info("=" * 60)
        logger.info("RELATÓRIO MERCURY AI | %s", market.symbol)
        logger.info("=" * 60)

        self._print_line(
            "Ativo",
            market.symbol
        )

        self._print_line(
            "Decisão",
            decision.decision
        )

        self._print_line(
            "Confiança",
            f"{decision.confidence*100:.1f}%"
        )

        self._print_line(
            "Probabilidades",
            (
                f"BUY {decision.buy_probability:.1f}% | "
                f"SELL {decision.sell_probability:.1f}% | "
                f"WAIT {decision.wait_probability:.1f}%"
            )
        )

        self._print_line(
            "Regime",
            regime.regime if regime else "N/A"
        )

        self._print_line(
            "Score",
            decision.score
        )

        # =====================================================
        # DECISION EXPLAINABILITY
        # =====================================================
        if decision.explainability:
            exp = decision.explainability
            logger.info("-" * 40)
            logger.info("DECISION EXPLAINABILITY")
            logger.info("-" * 40)
            self._print_line("Decisão", exp.decision)
            self._print_line("Razão", exp.reason)
            self._print_line("Direção Dominante", exp.dominant_direction)
            self._print_line("Nota Oportunidade", exp.opportunity_grade)
            self._print_line("Sinais Conflitantes", str(exp.conflicting_signals))
            self._print_line("Score Institucional", f"{exp.institutional_score:.2f}")
            self._print_line("Confiança", f"{exp.confidence:.1f}%")
            self._print_line("Regra Disparada", exp.triggered_rule)
            if exp.contributions:
                logger.info("Contribuições por Engine:")
                for contrib in exp.contributions:
                    self._print_line(
                        f"  {contrib.engine_name}",
                        f"peso={contrib.weight} raw={contrib.raw_score:.2f} "
                        f"weighted={contrib.weighted_score:.2f} dir={contrib.direction} "
                        f"conf={contrib.confidence:.1f}%"
                    )
            if exp.decision_chain:
                logger.info("Cadeia de Decisão:")
                for i, step in enumerate(exp.decision_chain, 1):
                    logger.info("  %d. %s", i, step)

        logger.info("=" * 60)

    def _print_line(self, label, value):

        logger.info("%-20s: %s", label, self._value(value))

    def _value(self, value):

        if value is None:
            return "N/A"

        if isinstance(value, float):
            return f"{value:.2f}"

        return value