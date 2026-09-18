"""Edge Tracker — win rate histórico por ativo (observável, audit-only).

Lê reports/top3_assertividade_historico.jsonl (+ _fb.jsonl de backfill) e
expõe o desempenho medido por símbolo para o Signal. NUNCA bloqueia o motor:
classifica o ativo em EDGE / NEUTRO / ANTI_EDGE / INSUFICIENTE para o
operador decidir. Bloqueio automático só é honesto com n >= MIN_N_BLOCK.

Regra de classificação (dados reais, sem otimismo):
  n < MIN_N_CLASSIFY ........ INSUFICIENTE (amostra não sustenta conclusão)
  winrate >= 0.60 ........... EDGE
  winrate <= 0.35 e n >= MIN_N_BLOCK ... ANTI_EDGE (candidato a blacklist)
  caso contrário ............ NEUTRO

Determinístico: sem rede, sem clock, sem RNG. Cache em memória por mtime
do arquivo (releitura só quando o histórico muda).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

MIN_N_CLASSIFY = 5    # abaixo disso, qualquer % é ruído
MIN_N_BLOCK = 10      # abaixo disso, NUNCA bloquear
EDGE_MIN = 0.60
ANTI_EDGE_MAX = 0.35

_CACHE: Dict[str, Any] = {"mtime": None, "data": {}}


def _hist_paths() -> list:
    root = Path(__file__).resolve().parents[2]
    hist = root / "reports" / "top3_assertividade_historico.jsonl"
    return [hist, hist.with_name(hist.stem + "_fb.jsonl")]


def _load() -> Dict[str, Dict[str, int]]:
    """{symbol: {"win": w, "n": n}} — combinada (gales contam como win)."""
    paths = _hist_paths()
    try:
        mtime = max(p.stat().st_mtime for p in paths if p.exists())
    except OSError:
        return {}
    if _CACHE["mtime"] == mtime and _CACHE["data"]:
        return _CACHE["data"]
    seen = set()
    stats: Dict[str, Dict[str, int]] = {}
    for p in paths:
        if not p.exists():
            continue
        try:
            with open(p, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        r = json.loads(line)
                    except Exception:
                        continue
                    res = r.get("reentry_result")
                    sym = r.get("symbol")
                    if not res or not sym:
                        continue
                    key = (r.get("ts"), sym)  # dedup HIST vs _fb
                    if key in seen:
                        continue
                    seen.add(key)
                    s = stats.setdefault(sym, {"win": 0, "n": 0})
                    s["n"] += 1
                    if res != "LOSS_FINAL":
                        s["win"] += 1
        except OSError:
            continue
    _CACHE["mtime"] = mtime
    _CACHE["data"] = stats
    return stats


def symbol_edge(symbol: str) -> Dict[str, Any]:
    """Desempenho medido do ativo no histórico (combinada com gales)."""
    stats = _load()
    s = stats.get(symbol)
    if not s or s["n"] < MIN_N_CLASSIFY:
        return {"edge_n": s["n"] if s else 0, "edge_winrate": None,
                "edge_status": "INSUFICIENTE"}
    wr = s["win"] / s["n"]
    if wr >= EDGE_MIN:
        status = "EDGE"
    elif wr <= ANTI_EDGE_MAX and s["n"] >= MIN_N_BLOCK:
        status = "ANTI_EDGE"
    else:
        status = "NEUTRO"
    return {"edge_n": s["n"], "edge_winrate": round(wr, 4), "edge_status": status}


def global_edge() -> Dict[str, Any]:
    """Assertividade combinada global do histórico (todos os ativos)."""
    stats = _load()
    w = sum(s["win"] for s in stats.values())
    n = sum(s["n"] for s in stats.values())
    return {"edge_global_n": n,
            "edge_global_winrate": round(w / n, 4) if n else None}
