"""Teste REAL 39 ativos + Top-3 assertividade (observavel, sem alterar motor)."""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from mercury_ai.brain.scanner import MercuryScanner
from mercury_ai.signals.top3_selector import select_top3, setup_label

t0 = time.perf_counter()
sc = MercuryScanner()
ranked = sc.scan(workers=4, cycle_timeout_s=290.0)
rep = sc.last_scan_report
d = rep.to_dict()
dur = round(time.perf_counter() - t0, 1)
print(f"SCAN status={d['status']} completed={d['symbols_completed']}/{d['symbols_total']} ranked={len(d['ranked'])} top3raw={len(d['top3'])} dur={dur}s workers={d['workers']}")

top3 = select_top3(d)
print(f"TOP3_FILTRADO={len(top3)}")
for e in top3:
    sig = e.get("signal", {}) if isinstance(e, dict) else {}
    print(json.dumps({
        "symbol": e.get("symbol"), "decision": e.get("decision"),
        "score": e.get("score"), "confidence": sig.get("confidence"),
        "confluence": sig.get("confluence"), "rr": sig.get("risk_reward"),
        "grade": sig.get("grade"), "forward": sig.get("forward_state"),
        "next_struct": sig.get("next_structure"), "next_dir": sig.get("next_direction"),
        "next_agrees": sig.get("next_agrees"),
        "lta": sig.get("lta_exists"), "ltb": sig.get("ltb_exists"),
        "tl_bias": sig.get("trendline_bias"), "tl_aligned": sig.get("trendline_aligned"),
        "sweep": sig.get("has_liquidity_sweep"), "fvg": sig.get("has_fvg"),
        "idm": sig.get("has_inducement"), "zona": sig.get("in_premium_discount_zone"),
        "news": sig.get("news_risk"), "news_ev": sig.get("news_event"),
        "label": setup_label(e),
    }, ensure_ascii=False))

# consistencia: conta outcomes
from collections import Counter
c = Counter(r.get("outcome") for r in d["per_asset"])
print("OUTCOMES:", dict(c))
# top3raw detalhe
for e in d["top3"]:
    sig = e.get("signal", {}) if isinstance(e, dict) else {}
    print("RAW_TOP3:", e.get("symbol"), e.get("decision"), e.get("score"), sig.get("forward_state"), sig.get("risk_reward"))

Path("reports").mkdir(exist_ok=True)
Path("reports/top3_assertividade_real.json").write_text(json.dumps({"scan": d, "top3": top3, "dur_s": dur}, default=str, ensure_ascii=False, indent=2), encoding="utf-8")
print("saved reports/top3_assertividade_real.json")
