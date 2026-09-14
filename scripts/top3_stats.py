"""Estatistica acumulada do Top-3 (leitura, sem alterar motor).

Le reports/top3_assertividade_historico.jsonl e imprime: n, taxa
direcional N+1, SL/TP (quando medidos), quebra por estrutura/LTA-LTB,
sweep/FVG/IDM, selo A/B e noticia. Uso: python scripts/top3_stats.py
"""
import json
import sys
from collections import Counter
from pathlib import Path

HIST = Path("reports/top3_assertividade_historico.jsonl")

if not HIST.exists():
    print("sem historico:", HIST)
    sys.exit(0)

rows = [json.loads(line) for line in HIST.read_text(encoding="utf-8").splitlines() if line.strip()]
print(f"sinais: {len(rows)}")
ok = [r for r in rows if r.get("n1_dir_ok") is True]
bad = [r for r in rows if r.get("n1_dir_ok") is False]
na = [r for r in rows if r.get("n1_dir_ok") is None]
val = ok + bad
print(f"forward valido: {len(val)} | dir_ok: {len(ok)} | miss: {len(bad)} | sem_dado: {len(na)}")
if val:
    print(f"taxa direcional N+1: {100.0 * len(ok) / len(val):.1f}% (n={len(val)}, sem significancia se n<30)")
print("por estrutura:", dict(Counter(str(r.get('next_structure')) for r in rows)))
print("por bias LTA/LTB:", dict(Counter(str(r.get('trendline_bias')) for r in rows)))
print("por noticia:", dict(Counter(str(r.get('news')) for r in rows)))
print("por forward:", dict(Counter(str(r.get('forward')) for r in rows)))
for r in rows:
    print(f"  {r.get('symbol')} {r.get('decision')} struct={r.get('next_structure')} "
          f"tl={r.get('trendline_bias')} news={r.get('news')} dir_ok={r.get('n1_dir_ok')}")
