"""Testes do Edge Tracker (puros, sem rede — usa jsonl temporário)."""
import json

import mercury_ai.signals.edge_tracker as et


def _write(tmp_path, rows):
    p = tmp_path / "top3_assertividade_historico.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    return p


def _patch_paths(monkeypatch, hist):
    fb = hist.with_name(hist.stem + "_fb.jsonl")
    monkeypatch.setattr(et, "_hist_paths", lambda: [hist, fb])
    monkeypatch.setattr(et, "_CACHE", {"mtime": None, "data": {}})


def test_insuficiente_sem_amostra(tmp_path, monkeypatch):
    hist = _write(tmp_path, [])
    _patch_paths(monkeypatch, hist)
    r = et.symbol_edge("XXX")
    assert r["edge_status"] == "INSUFICIENTE" and r["edge_n"] == 0


def test_edge_com_amostra(tmp_path, monkeypatch):
    rows = [{"ts": f"t{i}", "symbol": "AAA", "reentry_result": "WIN"} for i in range(4)]
    rows += [{"ts": "t9", "symbol": "AAA", "reentry_result": "LOSS_FINAL"}]
    hist = _write(tmp_path, rows)
    _patch_paths(monkeypatch, hist)
    r = et.symbol_edge("AAA")
    assert r["edge_status"] == "EDGE" and r["edge_n"] == 5 and r["edge_winrate"] == 0.8


def test_anti_edge_exige_n10(tmp_path, monkeypatch):
    # 0% com n=5: NEUTRO (não bloqueia sem amostra); n=10: ANTI_EDGE
    rows5 = [{"ts": f"t{i}", "symbol": "BAD", "reentry_result": "LOSS_FINAL"} for i in range(5)]
    hist = _write(tmp_path, rows5)
    _patch_paths(monkeypatch, hist)
    assert et.symbol_edge("BAD")["edge_status"] == "NEUTRO"
    rows10 = rows5 + [{"ts": f"x{i}", "symbol": "BAD", "reentry_result": "LOSS_FINAL"} for i in range(5)]
    hist = _write(tmp_path, rows10)
    _patch_paths(monkeypatch, hist)
    assert et.symbol_edge("BAD")["edge_status"] == "ANTI_EDGE"


def test_dedup_hist_vs_fb(tmp_path, monkeypatch):
    rows = [{"ts": "t0", "symbol": "AAA", "reentry_result": "WIN"}]
    hist = _write(tmp_path, rows)
    fb = hist.with_name(hist.stem + "_fb.jsonl")
    fb.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    _patch_paths(monkeypatch, hist)
    r = et.symbol_edge("AAA")
    assert r["edge_n"] == 1  # mesma linha nos dois arquivos conta 1x


def test_gale_conta_como_win(tmp_path, monkeypatch):
    rows = [{"ts": f"t{i}", "symbol": "AAA", "reentry_result": r}
            for i, r in enumerate(["WIN", "REENTRY_G1", "REENTRY_G2", "LOSS_FINAL", "LOSS_FINAL"])]
    hist = _write(tmp_path, rows)
    _patch_paths(monkeypatch, hist)
    r = et.symbol_edge("AAA")
    assert r["edge_winrate"] == 0.6 and r["edge_status"] == "EDGE"


def test_global(tmp_path, monkeypatch):
    rows = [{"ts": "t0", "symbol": "A", "reentry_result": "WIN"},
            {"ts": "t1", "symbol": "B", "reentry_result": "LOSS_FINAL"}]
    hist = _write(tmp_path, rows)
    _patch_paths(monkeypatch, hist)
    g = et.global_edge()
    assert g["edge_global_n"] == 2 and g["edge_global_winrate"] == 0.5
