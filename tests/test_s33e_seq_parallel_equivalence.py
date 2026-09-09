"""S33-E.3 — Equivalencia SEQUENTIAL x PARALLEL (pipeline Mercury real).

Escopo autorizado:
- SOMENTE este arquivo de teste e criado/alterado. Nenhum arquivo de
  producao e alterado.
- Pipeline Mercury REAL (AnalysisPipeline + Indicator/Trend/Structure/
  SmartMoney/Liquidity/Risk/Confluence/Consensus/Decision/Resolver/MTF/
  Ranking). Somente a aquisicao de dados e congelada no teste.
- FrozenProvider SOMENTE dentro deste teste: retorna copia do DataFrame,
  nunca acessa Yahoo, nunca altera o original, aceita
  symbol/interval/period/start/end/auto_adjust, registra hash servido.
- Sem MTF artificial: o mesmo DataFrame congelado e servido para qualquer
  interval/period (mesma entrada controlada); nao cria M1/M15/H1/H4 derivados.
- Memoria institucional isolada: sequential usa tempfile proprio;
  parallel usa o mecanismo existente _build_worker_pipeline() (cada worker
  com tempfile proprio). Sem merge. get_consistency_score() intacto.
- Sem clock congelado (preferencia da autorizacao): DeterministicClock nao e
  setado; snapshot()/restore() usados em finally apenas como guarda.
- Comparacao normalizada por symbol, tolerancia 1e-9, excluindo IDs/
  timestamps/duracao/paths/identidade de worker/ordem de futures/metadata.
- 3 ciclos independentes, dataset comprovadamente identico, memoria global
  intacta.

Veredito possivel: EQUIVALENCE_READY (zero divergencias) ou BLOCKED
(com symbol/campo/seq/par/diferenca/origem provavel).
"""
import copy
import hashlib
import json
import math
import os
import tempfile
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from mercury_ai.brain.scanner import MercuryScanner
from mercury_ai.core.asset_registry import AssetRegistry
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
from mercury_ai.utils.deterministic_clock import DeterministicClock


SYMBOLS = ["EURUSD=X", "GBPUSD=X", "BTC-USD", "ETH-USD"]
TOL = 1e-9
N_CANDLES = 80
FROZEN_START = pd.Timestamp("2025-06-01 00:00:00", tz="UTC")
FROZEN_FREQ = "5min"

GLOBAL_MEMORY_CANDIDATES = [
    Path("data/institutional_memory.json"),
    Path("mercury_ai/data/institutional_memory.json"),
]


# ---------------------------------------------------------------- dataset

def _resolve_global_memory_path():
    for p in GLOBAL_MEMORY_CANDIDATES:
        if p.exists():
            return p.resolve()
    # default canonico (pode nao existir em maquina limpa)
    return (Path.cwd() / "data" / "institutional_memory.json").resolve()


def _build_deterministic_dataset(symbol: str) -> pd.DataFrame:
    """Dataset OHLCV deterministico: indice UTC fixo, >=60 candles, imutavel.

    Derivacao por symbol via sha256 (conteudo fixo, sem dado futuro).
    Precos positivos, low<=high, sem NaN/duplicatas/gaps, sem outliers z>5.
    """
    seed = int(hashlib.sha256(symbol.encode()).hexdigest()[:8], 16)
    rs = np.random.RandomState(seed)
    n = N_CANDLES
    idx = pd.date_range(FROZEN_START, periods=n, freq=FROZEN_FREQ, tz="UTC")
    base = {"EURUSD=X": 1.0850, "GBPUSD=X": 1.2720, "BTC-USD": 67000.0, "ETH-USD": 3500.0}.get(symbol, 100.0)
    drift = (rs.randn(n) * base * 0.0008).cumsum()
    # oscilacao suave deterministica (suficiente p/ swings/indicadores)
    wave = np.sin(np.arange(n) * 0.35) * base * 0.0012
    closes = base + drift + wave
    closes = np.maximum(closes, base * 0.5)
    spreads = np.abs(rs.randn(n) * base * 0.0004) + base * 0.0002
    opens = closes + rs.randn(n) * base * 0.00015
    highs = np.maximum(opens, closes) + spreads * 0.6
    lows = np.minimum(opens, closes) - spreads * 0.6
    vols = np.abs(rs.randn(n) * 800 + 2500)
    df = pd.DataFrame(
        {"open": opens, "high": highs, "low": lows, "close": closes, "volume": vols},
        index=idx,
    )
    df.index.name = "timestamp"
    return df


def _dataframe_hash(df: pd.DataFrame) -> str:
    h = pd.util.hash_pandas_object(df, index=True)
    return hashlib.sha256(h.values.tobytes()).hexdigest()


def _build_frozen_datasets():
    return {s: _build_deterministic_dataset(s) for s in SYMBOLS}


# ------------------------------------------------------- FrozenProvider

class FrozenProvider:
    """Provider congelado SOMENTE p/ este teste (nunca Yahoo, copia sempre).

    Aceita symbol/interval/period/start/end/auto_adjust. Registra hash do
    dataset servido por (symbol, interval, period) p/ prova de identidade.
    """

    name = "FrozenTest"
    priority = -100
    is_implemented = True
    supported_assets = list(SYMBOLS)

    def __init__(self, datasets):
        self._datasets = datasets  # symbol -> DataFrame imutavel (nunca mutar)
        self._expected = {s: _dataframe_hash(df) for s, df in datasets.items()}
        self.served_hashes = {}  # (symbol, interval, period) -> hash
        self.served_per_symbol = {}  # symbol -> hash (ultimo servido)
        import threading as _th
        self._lock = _th.Lock()

    # compat MarketDataService(provider_manager=...) e providers=[...]
    def check_health(self):
        return True

    def is_available(self):
        return True

    def supports_symbol(self, symbol):
        return symbol in self._datasets

    def best_provider(self, symbol):
        return self

    def get_data(self, symbol, interval="5m", period="5d", start=None, end=None, auto_adjust=None):
        if symbol not in self._datasets:
            return pd.DataFrame()
        src = self._datasets[symbol]
        out = src.copy(deep=True)
        h = _dataframe_hash(out)
        with self._lock:
            self.served_hashes[(symbol, str(interval), str(period))] = h
            self.served_per_symbol[symbol] = h
        return out


# ------------------------------------------------------- comparacao semantica

EXCLUDED_EXACT = frozenset({
    "scan_id", "session_id", "replay_id", "audit_id", "run_id",
    "timestamp", "timestamps",
    "duration", "duration_s", "duration_ms",
    "execution_time", "start_time", "end_time",
    "wall_clock", "wallclock",
    "worker_scan_id", "scan_id_context",
    "version", "engine_version", "pipeline_version",
    "context_version", "weights_version", "version_metadata",
    "dataset_hash", "config_hash", "audit_events",
    "filename", "filepath", "file_path", "tmp_path", "temp_path",
    "snapshot_path", "memory_path", "registry_file", "base_path",
    "worker", "worker_id", "thread", "thread_id",
})


def _is_excluded_key(k: str) -> bool:
    if not isinstance(k, str):
        return False
    if k in EXCLUDED_EXACT:
        return True
    if k.startswith("_"):
        return True
    lk = k.lower()
    if lk in EXCLUDED_EXACT:
        return True
    if lk.endswith(("_path", "_file", "_dir", "_tmp", "_tmp_path")):
        return True
    if lk in ("filename", "filepath", "worker", "worker_id", "thread", "thread_id"):
        return True
    return False


def _to_comparable(o):
    if o is None:
        return None
    if isinstance(o, bool):
        return o
    if isinstance(o, int):
        return o
    if isinstance(o, float):
        return float(o)
    if isinstance(o, Enum):
        return o.value
    if isinstance(o, datetime):
        return "EXCLUDED_DATETIME"
    if isinstance(o, pd.Timestamp):
        return "EXCLUDED_DATETIME"
    try:
        import numpy as _np  # local p/ evitar custo global
        if isinstance(o, _np.floating):
            return float(o)
        if isinstance(o, _np.integer):
            return int(o)
        if isinstance(o, _np.bool_):
            return bool(o)
        if isinstance(o, _np.ndarray):
            return [_to_comparable(x) for x in o.tolist()]
    except Exception:
        pass
    if isinstance(o, pd.DataFrame):
        return {"dataframe_hash": _dataframe_hash(o)}
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            if _is_excluded_key(k):
                continue
            out[k] = _to_comparable(v)
        return out
    if isinstance(o, (list, tuple)):
        return [_to_comparable(x) for x in o]
    if is_dataclass(o):
        try:
            return _to_comparable(asdict(o))
        except Exception:
            pass
    if hasattr(o, "__dict__"):
        try:
            d = {k: v for k, v in vars(o).items() if not k.startswith("_")}
            return _to_comparable(d)
        except Exception:
            pass
    if isinstance(o, str):
        return o
    # fallback deterministico: repr estavel p/ objetos simples
    try:
        return str(o)
    except Exception:
        return "UNREPRESENTABLE"


def _collect_semantic(result) -> dict:
    """Extrai somente campos semanticos reais existentes (nunca inventa)."""
    return _to_comparable(result)


def _compare_vals(a, b, path, divs):
    # bool antes de int (bool e subclass de int)
    if isinstance(a, bool) or isinstance(b, bool):
        if a is not b and a != b:
            divs.append((path, a, b, abs(1) if True else 0, "bool mismatch"))
        return
    if isinstance(a, float) or isinstance(b, float):
        try:
            af, bf = float(a), float(b)
        except Exception:
            if a != b:
                divs.append((path, a, b, None, "float coerce mismatch"))
            return
        if math.isnan(af) and math.isnan(bf):
            return
        if math.isnan(af) or math.isnan(bf):
            divs.append((path, a, b, float("inf"), "NaN unilateral"))
            return
        diff = abs(af - bf)
        if diff > TOL:
            divs.append((path, a, b, diff, "float fora da tolerancia 1e-9"))
        return
    if isinstance(a, int) and isinstance(b, int):
        if a != b:
            divs.append((path, a, b, abs(a - b), "int mismatch"))
        return
    if isinstance(a, str) or isinstance(b, str):
        if a != b:
            divs.append((path, a, b, None, "str mismatch"))
        return
    if a is None or b is None:
        if a is not b:
            divs.append((path, a, b, None, "None unilateral"))
        return
    if isinstance(a, dict) and isinstance(b, dict):
        ka, kb = set(a.keys()), set(b.keys())
        for k in sorted(ka - kb):
            divs.append((f"{path}.{k}", a[k], "<MISSING>", None, "chave ausente no parallel"))
        for k in sorted(kb - ka):
            divs.append((f"{path}.{k}", "<MISSING>", b[k], None, "chave ausente no sequential"))
        for k in sorted(ka & kb):
            _compare_vals(a[k], b[k], f"{path}.{k}" if path else str(k), divs)
        return
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            divs.append((path, f"len={len(a)}", f"len={len(b)}", abs(len(a) - len(b)), "list len mismatch"))
            return
        for i, (x, y) in enumerate(zip(a, b)):
            _compare_vals(x, y, f"{path}[{i}]", divs)
        return
    if a != b:
        divs.append((path, a, b, None, f"type/value mismatch ({type(a).__name__} vs {type(b).__name__})"))


def _assert_no_yahoo(monkeypatch):
    import mercury_ai.providers.data_adapters as _da
    calls = {"n": 0}

    def _boom(*a, **k):
        calls["n"] += 1
        raise AssertionError("Yahoo nao pode ser fonte de dados do teste S33-E.3")

    monkeypatch.setattr(_da.yf, "download", _boom)
    return calls


def _capture_global_memory():
    p = _resolve_global_memory_path()
    if not p.exists():
        return {"path": str(p), "exists": False, "hash": "ABSENT", "mtime_ns": -1, "bytes": b""}
    data = p.read_bytes()
    st = p.stat()
    return {
        "path": str(p),
        "exists": True,
        "hash": hashlib.sha256(data).hexdigest(),
        "mtime_ns": st.st_mtime_ns,
        "bytes": data,
    }


def _redirect_runtime_reports(monkeypatch, dest_dir: Path):
    dest_dir.mkdir(parents=True, exist_ok=True)
    import mercury_ai.core.analysis_pipeline as _ap

    orig = _ap.atomic_json_write

    def _redir(path, payload, *a, **k):
        name = os.path.basename(str(path))
        if name.startswith("runtime_report_"):
            return orig(str(dest_dir / name), payload, *a, **k)
        # reports/replay/runtime_report_* tambem isola
        if "runtime_report_" in str(path):
            return orig(str(dest_dir / name), payload, *a, **k)
        return orig(path, payload, *a, **k)

    monkeypatch.setattr(_ap, "atomic_json_write", _redir)
    return orig


def _new_temp_json_with_empty_list(path: Path) -> str:
    path.write_text("[]", encoding="utf-8")
    return str(path)


def _run_one_cycle(monkeypatch, tmp_root: Path, cycle_idx: int, global_before, yahoo_calls):
    """Executa 1 ciclo seq->par isolado. Retorna dict com provas."""
    import mercury_ai.core.analysis_pipeline as _ap

    cdir = tmp_root / f"cycle{int(cycle_idx)}"
    (cdir / "snaps_seq").mkdir(parents=True, exist_ok=True)
    (cdir / "snaps_par").mkdir(parents=True, exist_ok=True)
    (cdir / "reports").mkdir(parents=True, exist_ok=True)
    seq_mem = _new_temp_json_with_empty_list(cdir / "seq_mem.json")
    reg_seq = cdir / "registry_seq.json"
    reg_par = cdir / "registry_par.json"
    reg_seq.write_text("{}", encoding="utf-8")
    reg_par.write_text("{}", encoding="utf-8")

    datasets = _build_frozen_datasets()
    expected_hashes = {s: _dataframe_hash(df) for s, df in datasets.items()}
    # imutabilidade: snapshot dos bytes antes
    frozen_before = {s: datasets[s].copy(deep=True) for s in SYMBOLS}

    seq_frozen = FrozenProvider(datasets)
    par_frozen = FrozenProvider(datasets)

    global_mem_path = _resolve_global_memory_path()

    state = DeterministicClock.snapshot()
    prev_env = os.environ.get("FROZEN_EQUIVALENCE_ISOLATED")
    try:
        # ---------------- sequential real ----------------
        sc_seq = MercuryScanner()
        sc_seq.asset_registry = AssetRegistry(registry_file=str(reg_seq))
        sc_seq.min_quality_score = 40.0
        seq_pipe = AnalysisPipeline(
            market_service=MarketDataService(provider=seq_frozen),
            providers=[seq_frozen],
            institutional_memory_path=seq_mem,
        )
        # MTF usa a mesma fonte congelada (mesma entrada controlada)
        seq_pipe.mtf_engine.market_service = MarketDataService(provider=seq_frozen)
        seq_pipe.snapshot_logger = DecisionSnapshotLogger(base_path=str(cdir / "snaps_seq"))
        try:
            seq_pipe.profiler.active = False
        except Exception:
            pass
        sc_seq.pipeline = seq_pipe
        sc_seq._print_report = lambda *a, **k: None
        sc_seq._print_ranking = lambda *a, **k: None

        seq_captured = {}
        _orig_seq_analyze = seq_pipe.analyze

        def _cap_seq(symbol, *a, **k):
            r = _orig_seq_analyze(symbol, *a, **k)
            seq_captured[symbol] = r
            return r

        seq_pipe.analyze = _cap_seq  # captura sem mockar engines
        ranked_seq = sc_seq._scan_sequential(list(SYMBOLS), [], workers=1)
        assert len(seq_captured) == 4, f"sequential deve analisar 4 symbols, obteve {sorted(seq_captured)}"
        assert set(seq_captured.keys()) == set(SYMBOLS)
        assert sc_seq.last_scan_report is not None
        assert sc_seq.last_scan_report.symbols_total == 4

        # ---------------- parallel real (workers=4) ----------------
        sc_par = MercuryScanner()
        sc_par.asset_registry = AssetRegistry(registry_file=str(reg_par))
        sc_par.min_quality_score = 40.0
        sc_par._print_ranking = lambda *a, **k: None

        worker_mem_paths = []
        par_captured = {}
        _orig_build = MercuryScanner._build_worker_pipeline

        def _patched_build(self, scan_id=None):
            pipe = _orig_build(self, scan_id=scan_id)
            try:
                worker_mem_paths.append(pipe.memory.memory_path)
            except Exception:
                pass
            pipe.market_service = MarketDataService(provider=par_frozen)
            try:
                pipe.mtf_engine.market_service = MarketDataService(provider=par_frozen)
            except Exception:
                pass
            try:
                pipe.snapshot_logger = DecisionSnapshotLogger(base_path=str(cdir / "snaps_par"))
            except Exception:
                pass
            return pipe

        sc_par._build_worker_pipeline = _patched_build.__get__(sc_par, MercuryScanner)

        _orig_isolated = sc_par._analyze_symbol_isolated

        def _cap_isolated(symbol, scan_id=None):
            res = _orig_isolated(symbol, scan_id=scan_id)
            # res = (symbol, analysis, exc, dur, failed, worker_scan_id)
            try:
                _sym, _analysis, _exc = res[0], res[1], res[2]
                if _analysis is not None:
                    par_captured[_sym] = _analysis
            except Exception:
                pass
            return res

        sc_par._analyze_symbol_isolated = _cap_isolated
        ranked_par = sc_par._scan_parallel(list(SYMBOLS), workers=4, cycle_timeout_s=290.0)
        assert sc_par.last_scan_report is not None
        assert sc_par.last_scan_report.workers == 4
        assert sc_par.last_scan_report.symbols_total == 4
        assert len(par_captured) == 4, f"parallel deve analisar 4 symbols, obteve {sorted(par_captured)}"
        assert set(par_captured.keys()) == set(SYMBOLS)

        # imutabilidade do dataset
        for s in SYMBOLS:
            pd.testing.assert_frame_equal(datasets[s], frozen_before[s])

        # dataset identity: seq e par receberam o mesmo dataset
        hash_seq = {s: seq_frozen.served_per_symbol.get(s) for s in SYMBOLS}
        hash_par = {s: par_frozen.served_per_symbol.get(s) for s in SYMBOLS}
        for s in SYMBOLS:
            assert hash_seq.get(s) == expected_hashes[s], f"seq nao serviu dataset congelado p/ {s}"
            assert hash_par.get(s) == expected_hashes[s], f"par nao serviu dataset congelado p/ {s}"
            assert hash_seq[s] == hash_par[s], f"BLOCKED dataset divergente p/ {s}"

        # memoria: sequential isolada da global; workers isolados entre si e da global
        assert os.path.abspath(seq_mem) != os.path.abspath(str(global_mem_path))
        assert len(worker_mem_paths) == 4, f"esperado 4 workers isolados, obteve {worker_mem_paths}"
        assert len(set(worker_mem_paths)) == 4, "worker_A_memory_path != worker_B_memory_path"
        for p in worker_mem_paths:
            assert os.path.abspath(p) != os.path.abspath(str(global_mem_path))
            assert "institutional_memory.json" not in p.replace("\\", "/").split("/")[-1] or "m5_worker_mem_" in p

        # global intacta apos seq e par (verificado pelo chamador tambem)
        return {
            "cdir": cdir,
            "seq_mem": seq_mem,
            "worker_mem_paths": list(worker_mem_paths),
            "seq_captured": seq_captured,
            "par_captured": par_captured,
            "ranked_seq": ranked_seq,
            "ranked_par": ranked_par,
            "hash_seq": hash_seq,
            "hash_par": hash_par,
            "expected_hashes": expected_hashes,
            "rep_seq": sc_par.last_scan_report and sc_seq.last_scan_report,
            "last_seq": sc_seq.last_scan_report,
            "last_par": sc_par.last_scan_report,
        }
    finally:
        try:
            DeterministicClock.restore(state)
        except Exception:
            pass
        if prev_env is None:
            os.environ.pop("FROZEN_EQUIVALENCE_ISOLATED", None)
        else:
            os.environ["FROZEN_EQUIVALENCE_ISOLATED"] = prev_env


def _semantic_of(captured: dict) -> dict:
    return {s: _collect_semantic(captured[s]) for s in SYMBOLS}


def _diff_semantic(seq_sem: dict, par_sem: dict):
    divs = []
    for s in SYMBOLS:
        a = seq_sem.get(s)
        b = par_sem.get(s)
        if a is None or b is None:
            divs.append({"symbol": s, "field": "<RESULT>", "seq": a, "par": b, "diff": None, "origin": "resultado ausente"})
            continue
        local = []
        _compare_vals(a, b, "", local)
        for (path, va, vb, diff, why) in local:
            divs.append({"symbol": s, "field": path or "<ROOT>", "seq": va, "par": vb, "diff": diff, "origin": why})
    return divs


# ------------------------------------------------------------------ testes

def test_s33e_seq_real_4_symbols(tmp_path, monkeypatch):
    yahoo_calls = _assert_no_yahoo(monkeypatch)
    _redirect_runtime_reports(monkeypatch, tmp_path / "reports")
    before = _capture_global_memory()
    out = _run_one_cycle(monkeypatch, tmp_path, 1, before, yahoo_calls)
    assert set(out["seq_captured"].keys()) == set(SYMBOLS)
    assert out["last_seq"].symbols_total == 4
    assert out["last_seq"].symbols_completed == 4
    assert yahoo_calls["n"] == 0, "cache Yahoo nao pode ser fonte de dados do teste"
    after = _capture_global_memory()
    assert after["hash"] == before["hash"], "memoria global alterada pelo sequential"
    assert after["mtime_ns"] == before["mtime_ns"] or not after["exists"]


def test_s33e_parallel_real_workers4(tmp_path, monkeypatch):
    yahoo_calls = _assert_no_yahoo(monkeypatch)
    _redirect_runtime_reports(monkeypatch, tmp_path / "reports")
    before = _capture_global_memory()
    out = _run_one_cycle(monkeypatch, tmp_path, 1, before, yahoo_calls)
    assert set(out["par_captured"].keys()) == set(SYMBOLS)
    assert out["last_par"].workers == 4
    assert out["last_par"].symbols_total == 4
    assert out["last_par"].symbols_completed == 4
    assert yahoo_calls["n"] == 0
    after = _capture_global_memory()
    assert after["hash"] == before["hash"]


def test_s33e_dataset_identical_and_normalized_by_symbol(tmp_path, monkeypatch):
    yahoo_calls = _assert_no_yahoo(monkeypatch)
    _redirect_runtime_reports(monkeypatch, tmp_path / "reports")
    before = _capture_global_memory()
    out = _run_one_cycle(monkeypatch, tmp_path, 1, before, yahoo_calls)
    # normalizacao por symbol: chaves sao symbols, nunca ordem de futures
    assert sorted(out["seq_captured"].keys()) == sorted(SYMBOLS)
    assert sorted(out["par_captured"].keys()) == sorted(SYMBOLS)
    for s in SYMBOLS:
        assert out["hash_seq"][s] == out["hash_par"][s] == out["expected_hashes"][s], f"BLOCKED dataset {s}"
    assert yahoo_calls["n"] == 0


def test_s33e_semantic_equivalence_and_ids_excluded(tmp_path, monkeypatch):
    yahoo_calls = _assert_no_yahoo(monkeypatch)
    _redirect_runtime_reports(monkeypatch, tmp_path / "reports")
    before = _capture_global_memory()
    out = _run_one_cycle(monkeypatch, tmp_path, 1, before, yahoo_calls)
    seq_sem = _semantic_of(out["seq_captured"])
    par_sem = _semantic_of(out["par_captured"])
    # prova que IDs/metadados diferem mas nao causam FAIL (foram excluidos)
    raw_seq_ids = {s: out["seq_captured"][s].decision.audit_id for s in SYMBOLS}
    raw_par_ids = {s: out["par_captured"][s].decision.audit_id for s in SYMBOLS}
    assert all(isinstance(v, str) and len(v) > 0 for v in list(raw_seq_ids.values()) + list(raw_par_ids.values()))
    # equivalencia semantica real
    divs = _diff_semantic(seq_sem, par_sem)
    if divs:
        d0 = divs[0]
        pytest.fail(
            "BLOCKED divergencia semantica "
            f"symbol={d0['symbol']} campo={d0['field']} seq={d0['seq']!r} "
            f"par={d0['par']!r} diff={d0['diff']!r} origem={d0['origin']}"
        )
    assert yahoo_calls["n"] == 0


def test_s33e_memory_isolation_and_global_intact(tmp_path, monkeypatch):
    yahoo_calls = _assert_no_yahoo(monkeypatch)
    _redirect_runtime_reports(monkeypatch, tmp_path / "reports")
    before = _capture_global_memory()
    out = _run_one_cycle(monkeypatch, tmp_path, 1, before, yahoo_calls)
    gpath = os.path.abspath(str(_resolve_global_memory_path()))
    assert os.path.abspath(out["seq_mem"]) != gpath
    assert len(out["worker_mem_paths"]) == 4 and len(set(out["worker_mem_paths"])) == 4
    for p in out["worker_mem_paths"]:
        assert os.path.abspath(p) != gpath
    mid = _capture_global_memory()
    assert mid["hash"] == before["hash"], "memoria global alterada"
    assert mid["mtime_ns"] == before["mtime_ns"] or not mid["exists"]
    assert yahoo_calls["n"] == 0


def test_s33e_three_cycles_zero_divergence(tmp_path, monkeypatch):
    yahoo_calls = _assert_no_yahoo(monkeypatch)
    _redirect_runtime_reports(monkeypatch, tmp_path / "reports")
    before = _capture_global_memory()
    all_divs = []
    for i in (1, 2, 3):
        out = _run_one_cycle(monkeypatch, tmp_path, i, before, yahoo_calls)
        # cada ciclo com isolamento proprio
        assert os.path.abspath(out["seq_mem"]) != os.path.abspath(str(_resolve_global_memory_path()))
        seq_sem = _semantic_of(out["seq_captured"])
        par_sem = _semantic_of(out["par_captured"])
        divs = _diff_semantic(seq_sem, par_sem)
        for d in divs:
            d["cycle"] = i
        all_divs.extend(divs)
        # dataset identico todo ciclo
        for s in SYMBOLS:
            assert out["hash_seq"][s] == out["hash_par"][s], f"BLOCKED ciclo {i} dataset {s}"
        mid = _capture_global_memory()
        assert mid["hash"] == before["hash"], f"memoria global alterada no ciclo {i}"
    if all_divs:
        d0 = all_divs[0]
        pytest.fail(
            f"BLOCKED ciclo={d0.get('cycle')} symbol={d0['symbol']} campo={d0['field']} "
            f"seq={d0['seq']!r} par={d0['par']!r} diff={d0['diff']!r} origem={d0['origin']}"
        )
    assert yahoo_calls["n"] == 0, "Yahoo nao pode ser fonte de dados"
