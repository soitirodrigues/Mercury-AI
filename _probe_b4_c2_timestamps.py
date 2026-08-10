"""
B4-C2 PROBE — Timestamp Contract & 1-Candle Outcome Forensics.
INVESTIGAÇÃO FORENSE APENAS. Não modifica produção.
Executa fora da produção, coleta evidências e será removido ao final.
"""
import sys
import os
import json
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest import mock

import numpy as np
import pandas as pd

from mercury_ai.utils.deterministic_clock import DeterministicClock
from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine
from mercury_ai.analysis.benchmark_framework import MercuryBenchmarkFramework

RESULT = {}


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
class FakePipeline:
    """Pipeline falso que retorna snapshot stub — isola o teste do motor de
    replay (P/L/outcome) sem rodar os ~20 engines pesados."""
    def __init__(self, **kwargs):
        pass

    def analyze(self, *args, **kwargs):
        snap = SimpleNamespace(
            decision_result=SimpleNamespace(
                decision="BUY", audit_id="b4c2probe", confidence=0.5,
            ),
            timestamp="2024-01-01T00:00:00",
        )
        self.last_snapshot = snap
        return snap


def make_mono_df(n=70, start=100.0):
    """close[i] = start + i => cada vela tem close distinto e crescente."""
    dates = pd.date_range("2024-01-01", periods=n, freq="5min")
    close = np.array([start + i for i in range(n)], dtype=float)
    return pd.DataFrame({
        "open": close - 0.5,
        "high": close + 1.0,
        "low": close - 1.0,
        "close": close,
        "volume": np.full(n, 1000.0),
    }, index=dates)


class FakeYahoo:
    """Provider falso que retorna um df controlado (mesma interface Yahoo).
    Classe no-arg (YahooFinanceProvider() é instanciada sem args no código).
    O df é armazenado em _df (variável de classe) antes do patch."""
    _df = None

    def __init__(self, *a, **k):
        pass

    def get_data(self, symbol, interval="5m", period="5d"):
        return FakeYahoo._df.copy()

    def is_available(self):
        return True

    def supports_symbol(self, s):
        return True

    def supports_market(self, m):
        return True

    def supports_timeframe(self, t):
        return True

    def max_history(self):
        return "10y"

    def source_name(self):
        return "YahooFinance"


# ---------------------------------------------------------------------------
# A) CONVENÇÕES DE TIMESTAMP
# ---------------------------------------------------------------------------
def part_a():
    print("=" * 70)
    print("PARTE A - CONVENÇÕES DE TIMESTAMP (valores reais)")
    print("=" * 70)
    DeterministicClock.reset()
    d_clock = DeterministicClock.utcnow()       # Conv A: naive UTC
    d_now = datetime.now()                       # Conv B: naive local
    d_utc = datetime.now(timezone.utc)           # Conv C: tz-aware UTC
    print(f"A) DeterministicClock.utcnow(): {d_clock}  tzinfo={d_clock.tzinfo!r}")
    print(f"B) datetime.now()            : {d_now}  tzinfo={d_now.tzinfo!r}")
    print(f"C) datetime.now(timezone.utc): {d_utc}  tzinfo={d_utc.tzinfo!r}")
    if d_clock.tzinfo is None and d_now.tzinfo is None:
        # A e B são naive; a diferença de wall-clock entre eles = offset local.
        wall = (d_clock - d_now).total_seconds()
        print(f"Wall-clock A - B = {wall:.0f}s -> A(UTC) e B(local) divergem "
              f"em {wall/3600:.1f}h (offset local da máquina).")
        print("  -> Mesma representação (naive, sem tzinfo) MAS valores semânticos")
        print("     diferentes: se A for consumido como B (ou vice-versa), erro de ~3h.")
    RESULT['A'] = {
        'clock_utcnow': str(d_clock), 'clock_tz': repr(d_clock.tzinfo),
        'local_now': str(d_now), 'local_tz': repr(d_now.tzinfo),
        'utc_aware': str(d_utc), 'utc_tz': repr(d_utc.tzinfo),
    }


# ---------------------------------------------------------------------------
# B) SEMÂNTICA P/L DO REPLAY (outcome window)
# ---------------------------------------------------------------------------
def part_b():
    print("=" * 70)
    print("PARTE B - SEMÂNTICA P/L DO REPLAY (outcome window)")
    print("=" * 70)
    df = make_mono_df(n=70, start=100.0)
    n_candles = 3
    with mock.patch("mercury_ai.analysis.historical_replay_engine.AnalysisPipeline", FakePipeline):
        engine = HistoricalReplayEngine()
        metrics = engine.run_replay("B4C2TEST", df, n_candles=n_candles, silent=True)
    start_idx = 60
    ok_all = True
    print(f"Total candles processados: {len(metrics)}")
    for k, m in enumerate(metrics):
        i = start_idx + k
        entry = float(df['close'].iloc[i])
        expected_pl = (float(df['close'].iloc[i + n_candles]) - entry) / entry
        match = abs(m.pl - expected_pl) < 1e-12
        ok_all = ok_all and match
        if k < 3:
            print(f"  i={i} T_DECISION={df.index[i]} ENTRY=close[{i}]={entry:.2f} "
                  f"EXIT=close[{i+n_candles}]={df['close'].iloc[i+n_candles]:.2f} "
                  f"PL={m.pl:.6f} esperado={expected_pl:.6f} match={match}")
    i0 = start_idx
    print(f"Ex.: i={i0} ENTRY_TIME={df.index[i0]} (close={df['close'].iloc[i0]}) -> "
          f"EXIT_TIME={df.index[i0+n_candles]} (close={df['close'].iloc[i0+n_candles]})")
    print(f"OUTCOME window = candles [{i0+1}..{i0+n_candles}] (EXCLUSIVO da vela de decisão {i0})")
    print(f"TODAS as {len(metrics)} P/L batem com (close[i+n]-close[i])/close[i]: {ok_all}")
    RESULT['B'] = {'all_match': ok_all, 'n_candles': n_candles, 'count': len(metrics)}


# ---------------------------------------------------------------------------
# C) BENCHMARK FRAMEWORK: OUTCOME 1-CANDLE (overlap)
# ---------------------------------------------------------------------------
def part_c():
    print("=" * 70)
    print("PARTE C - BENCHMARK FRAMEWORK: OUTCOME 1-CANDLE (overlap)")
    print("=" * 70)
    n = 50
    dates = pd.date_range("2024-01-01", periods=n, freq="5min")
    close = np.linspace(100.0, 103.0, n)
    close[-2] = 100.0    # candle de referência do outcome
    close[-1] = 105.0    # candle T0 = DECISION candle = endpoint do outcome
    df = pd.DataFrame({
        "Open": close - 0.1, "High": close + 1.0, "Low": close - 1.0,
        "Close": close, "Volume": np.full(n, 1000.0),
    }, index=dates)

    # 1) Outcome via _get_real_outcome (sem rodar __init__ do framework)
    fw = object.__new__(MercuryBenchmarkFramework)
    FakeYahoo._df = df
    with mock.patch("mercury_ai.analysis.benchmark_framework.YahooFinanceProvider", FakeYahoo):
        outcome = fw._get_real_outcome("X", "BUY")
    close_cur = float(df['Close'].iloc[-2])
    close_next = float(df['Close'].iloc[-1])
    expected = (close_next - close_cur) / close_cur
    print(f"df.iloc[-2] close (referencia)  = {close_cur}")
    print(f"df.iloc[-1] close (outcome end) = {close_next}  <- ULTIMA vela do df")
    print(f"outcome BUY = (close[-1]-close[-2])/close[-2] = {expected:.6f}")
    print(f"_get_real_outcome retornou: {outcome}  match={abs(outcome-expected)<1e-12}")

    # 2) Decisão usa a última vela (rodar pipeline real com o mesmo df)
    try:
        from mercury_ai.core.analysis_pipeline import AnalysisPipeline
        from mercury_ai.data.market_data import MarketDataService
        pipe = AnalysisPipeline(
            market_service=MarketDataService(providers=[FakeYahoo()]),
            providers=[FakeYahoo()],
        )
        res = pipe.analyze("X", silent=True)
        dec = res.decision.decision
        mc = getattr(res.market, 'close', None)
        print(f"Decisão (pipeline real, mesmo df): {dec}")
        print(f"  market.close (preço observado) = {mc}")
        if mc is not None:
            same = abs(float(mc) - close_next) < 1e-6
            print(f"  market.close == close[-1] ({close_next})? -> {same}")
        # altera SÓ a última vela (usar .loc/.iat p/ evitar chained-assignment)
        df2 = df.copy()
        df2.loc[df2.index[-1], 'Close'] = 110.0
        FakeYahoo._df = df2
        with mock.patch("mercury_ai.analysis.benchmark_framework.YahooFinanceProvider", FakeYahoo):
            outcome2 = fw._get_real_outcome("X", "BUY")
        exp2 = (110.0 - close_cur) / close_cur
        print(f"Alterando SÓ a última vela close->110: outcome2={outcome2:.6f} (esperado {exp2:.6f})")
        print("=> outcome responde à ÚLTIMA vela = a MESMA vela usada na decisão -> SOBREPOSIÇÃO.")
        RESULT['C'] = {
            'outcome': outcome, 'expected': expected, 'close_ref': close_cur,
            'close_next': close_next, 'decision': dec, 'market_close': mc,
            'market_close_matches': (abs(float(mc) - close_next) < 1e-6) if mc is not None else None,
            'outcome2': outcome2,
        }
    except Exception as e:
        print(f"(pipeline real falhou, evidência estrutural mantida): {type(e).__name__}: {e}")
        RESULT['C'] = {
            'outcome': outcome, 'expected': expected, 'close_ref': close_cur,
            'close_next': close_next, 'pipeline_error': str(e),
        }


# ---------------------------------------------------------------------------
# D) TESTE DE FUTURO (decisão em i não vê candles > i)
# ---------------------------------------------------------------------------
def part_d():
    print("=" * 70)
    print("PARTE D - TESTE DE FUTURO (decisão em i só vê 0..i)")
    print("=" * 70)
    from mercury_ai.core.analysis_pipeline import AnalysisPipeline
    from mercury_ai.data.market_data import MarketDataService
    from mercury_ai.providers.historical_replay_provider import HistoricalReplayProvider

    df = make_mono_df(n=80, start=100.0)   # lowercase, index naive
    i = 65

    def run_at(df_in, idx):
        p = HistoricalReplayProvider()
        p.set_data(df_in)
        p.set_index(idx)
        pl = AnalysisPipeline(market_service=MarketDataService(providers=[p]), providers=[p])
        r = pl.analyze("B4C2TEST", silent=True)
        return r.decision.decision, getattr(r.market, 'close', None)

    d1, c1 = run_at(df, i)
    df2 = df.copy()
    df2.iloc[i + 1:] = df2.iloc[i + 1:] * 1000.0   # futuras drasticamente alteradas
    d2, c2 = run_at(df2, i)
    df3 = df.copy()
    df3.iloc[i] = df3.iloc[i] * 0.5                 # a própria vela i alterada
    d3, c3 = run_at(df3, i)

    # verificação do slice
    pchk = HistoricalReplayProvider()
    pchk.set_data(df)
    pchk.set_index(i)
    sliced = pchk.get_data("X")
    print(f"provider.get_data() em i={i} retorna {len(sliced)} linhas (esperado {i+1}) -> inclusivo 0..i")
    print(f"DECISION em i={i} (original)               : {d1} (close obs={c1})")
    print(f"DECISION com velas i+1..end *1000          : {d2} (close obs={c2})")
    print(f"  futuro alterado -> decisão inalterada?   : {d1==d2} ; preço observado igual? {c1==c2}")
    print(f"DECISION com vela i alterada (*0.5)        : {d3} (close obs={c3})")
    print(f"  contrato permite mudança quando altera a própria vela i? preço observado mudou: {c1!=c3}")
    RESULT['D'] = {
        'd1': d1, 'c1': c1, 'd2': d2, 'c2': c2, 'd3': d3, 'c3': c3,
        'future_unchanged': d1 == d2, 'price_unchanged': c1 == c2,
        'slice_len': len(sliced),
    }


# ---------------------------------------------------------------------------
# E) OFF-BY-ONE (N=1,2,3: qual vela é o exit)
# ---------------------------------------------------------------------------
def part_e():
    print("=" * 70)
    print("PARTE E - OFF-BY-ONE (N=1,2,3: qual vela é o exit)")
    print("=" * 70)
    df = make_mono_df(n=70, start=100.0)
    table = []
    for n in [1, 2, 3]:
        with mock.patch("mercury_ai.analysis.historical_replay_engine.AnalysisPipeline", FakePipeline):
            engine = HistoricalReplayEngine()
            metrics = engine.run_replay("B4C2TEST", df, n_candles=n, silent=True)
        i0 = 60
        m = metrics[0]
        entry = float(df['close'].iloc[i0])
        exit_ = float(df['close'].iloc[i0 + n])
        expected = (exit_ - entry) / entry
        match = abs(m.pl - expected) < 1e-12
        print(f"N={n}: i={i0} ENTRY=close[{i0}]={entry:.2f} EXIT=close[{i0+n}]={exit_:.2f} "
              f"PL={m.pl:.6f} esperado={expected:.6f} match={match}")
        table.append({'n': n, 'exit_index': i0 + n, 'exit_ts': str(df.index[i0 + n]), 'pl': m.pl, 'match': match})
    RESULT['E'] = table


# ---------------------------------------------------------------------------
# F) DETERMINISMO (RUN A vs RUN B)
# ---------------------------------------------------------------------------
def part_f():
    print("=" * 70)
    print("PARTE F - DETERMINISMO (RUN A vs RUN B)")
    print("=" * 70)
    df = make_mono_df(n=70, start=100.0)
    with mock.patch("mercury_ai.analysis.historical_replay_engine.AnalysisPipeline", FakePipeline):
        ea = HistoricalReplayEngine()
        ma = ea.run_replay("B4C2TEST", df, n_candles=2, silent=True)
        eb = HistoricalReplayEngine()
        mb = eb.run_replay("B4C2TEST", df, n_candles=2, silent=True)
    pa = [m.pl for m in ma]
    pb = [m.pl for m in mb]
    same = pa == pb and len(ma) == len(mb)
    print(f"RUN A: {len(ma)} metrics | RUN B: {len(mb)} metrics")
    print(f"P/L idênticos (A==B)? {same}")
    print(f"P/L A[:3]: {[round(x, 6) for x in pa[:3]]}")
    print(f"P/L B[:3]: {[round(x, 6) for x in pb[:3]]}")
    RESULT['F'] = {'same': same, 'nA': len(ma), 'nB': len(mb)}


# ---------------------------------------------------------------------------
# G) CLOCK ISOLATION (NORMAL -> REPLAY -> NORMAL)
# ---------------------------------------------------------------------------
def part_g():
    print("=" * 70)
    print("PARTE G - CLOCK ISOLATION (NORMAL -> REPLAY -> NORMAL)")
    print("=" * 70)
    DeterministicClock.reset()
    t1 = DeterministicClock.utcnow()
    print(f"NORMAL antes: utcnow={t1}")
    df = make_mono_df(n=70, start=100.0)
    with mock.patch("mercury_ai.analysis.historical_replay_engine.AnalysisPipeline", FakePipeline):
        engine = HistoricalReplayEngine()
        engine.run_replay("B4C2TEST", df, n_candles=2, silent=True)
    t2 = DeterministicClock.utcnow()
    print(f"NORMAL depois: utcnow={t2}")
    frozen = (t2 - t1).total_seconds() > 3600
    print(f"Clock congelado em histórico? {frozen}  (False = correto, B4-C1 mantido)")
    RESULT['G'] = {'before': str(t1), 'after': str(t2), 'frozen': frozen}
    DeterministicClock.reset()


# ---------------------------------------------------------------------------
# H) TZ DO ÍNDICE DE DADOS REAIS (Yahoo) — opcional/rede
# ---------------------------------------------------------------------------
def part_h():
    print("=" * 70)
    print("PARTE H - TZ DO ÍNDICE DE DADOS (Yahoo real, se rede disponível)")
    print("=" * 70)
    try:
        import yfinance as yf
        t = yf.Ticker("BTC-USD")
        df = t.history(period="2d", interval="5m")
        print(f"Yahoo index type : {type(df.index).__name__}")
        print(f"Yahoo index tz   : {df.index.tz!r}")
        print(f"Yahoo index[0]   : {df.index[0]!r}")
        print(f"Yahoo index[-1]  : {df.index[-1]!r}")
        RESULT['H'] = {
            'index_type': type(df.index).__name__, 'tz': repr(df.index.tz),
            'first': str(df.index[0]), 'last': str(df.index[-1]),
        }
    except Exception as e:
        print(f"(rede indisponível / Yahoo falhou): {type(e).__name__}: {e}")
        RESULT['H'] = {'error': f"{type(e).__name__}: {e}"}


# ---------------------------------------------------------------------------
# I) TESTE DE FUTURO DO OUTCOME DO REPLAY (alterar velas além do horizonte)
# ---------------------------------------------------------------------------
def part_i():
    print("=" * 70)
    print("PARTE I - OUTCOME DO REPLAY: velas além do horizonte NÃO mudam P/L(i)")
    print("=" * 70)
    df = make_mono_df(n=80, start=100.0)
    n_candles = 3
    with mock.patch("mercury_ai.analysis.historical_replay_engine.AnalysisPipeline", FakePipeline):
        e1 = HistoricalReplayEngine()
        m1 = e1.run_replay("B4C2TEST", df, n_candles=n_candles, silent=True)
    # altera drasticamente TODAS as velas a partir de i+4 (fora do horizonte i+1..i+3)
    df2 = df.copy()
    df2.loc[df2.index[64]:, ['open', 'high', 'low', 'close']] *= 1000.0
    with mock.patch("mercury_ai.analysis.historical_replay_engine.AnalysisPipeline", FakePipeline):
        e2 = HistoricalReplayEngine()
        m2 = e2.run_replay("B4C2TEST", df2, n_candles=n_candles, silent=True)
    i0 = 60
    p1 = [m.pl for m in m1]
    p2 = [m.pl for m in m2]
    # candle 60: horizonte usa close[63]; alterar a partir de 64 não deve afetar
    same60 = abs(m1[0].pl - m2[0].pl) < 1e-12
    same_all = all(abs(a - b) < 1e-12 for a, b in zip(p1, p2))
    print(f"i={i0} P/L original={m1[0].pl:.6f}  P/L com velas>63*1000={m2[0].pl:.6f}  igual? {same60}")
    print(f"Todos os P/L inalterados (velas fora do horizonte): {same_all}")
    print("  -> outcome(i) usa apenas close[i..i+n]; velas após i+n não afetam.")
    RESULT['I'] = {'same60': same60, 'same_all': same_all, 'count': len(m1)}


# ---------------------------------------------------------------------------
# J) BOUNDARY: decisão em T_i usa close[i] (T+0), NÃO close[i+1] (T+1)
# ---------------------------------------------------------------------------
def part_j():
    print("=" * 70)
    print("PARTE J - BOUNDARY: decisão em T_i observa close[i] (T+0), não T+1")
    print("=" * 70)
    from mercury_ai.core.analysis_pipeline import AnalysisPipeline
    from mercury_ai.data.market_data import MarketDataService
    from mercury_ai.providers.historical_replay_provider import HistoricalReplayProvider
    # grid 5min começando 09:30 (exemplo conceitual da missão)
    n = 70
    dates = pd.date_range("2024-01-01 09:30", periods=n, freq="5min")
    close = 100.0 + np.arange(n, dtype=float)
    df = pd.DataFrame({
        "open": close - 0.1, "high": close + 0.2, "low": close - 0.2,
        "close": close, "volume": np.full(n, 1000.0),
    }, index=dates)
    # decisão em i=65 (slice 0..65 com 66 linhas >= 11 -> pipeline real roda)
    i = 65
    p = HistoricalReplayProvider(); p.set_data(df); p.set_index(i)
    pipe = AnalysisPipeline(market_service=MarketDataService(providers=[p]), providers=[p])
    r = pipe.analyze("B4C2TEST", silent=True)
    mc = float(getattr(r.market, 'close', -1))
    print(f"Grid 5min de {dates[0]} a {dates[-1]}")
    print(f"Decisão em i={i} (T_DECISION/clock = {df.index[i]}): close observado = {mc}")
    print(f"  close[i]={close[i]} ; close[i+1]={close[i+1]}")
    uses_t0 = abs(mc - close[i]) < 1e-6
    uses_t1 = abs(mc - close[i + 1]) < 1e-6
    print(f"  Observa close[i] (T+0)? {uses_t0}  | Usa close[i+1] (T+1)? {uses_t1}")
    print(f"  SEMÂNTICA: timestamp armazenado = OPEN da vela i ({df.index[i]});")
    print(f"  close[i] é realizado ao FECHAMENTO da vela i (T_i + 5min). Decisão pós-close.")
    RESULT['J'] = {'i': i, 't_decision': str(df.index[i]), 'close_obs': mc,
                   'close_i': close[i], 'close_i1': close[i + 1],
                   'uses_T0': bool(uses_t0), 'uses_T1': bool(uses_t1)}


if __name__ == "__main__":
    part_a()
    part_b()
    part_c()
    part_d()
    part_e()
    part_f()
    part_g()
    part_h()
    part_i()
    part_j()
    print("=" * 70)
    print("RESULTADO JSON:")
    print(json.dumps(RESULT, indent=2, default=str))
