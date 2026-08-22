#!/usr/bin/env python3
"""TOP-3 SCANNER — SPRINT MERCURY-AI V1
Ranking deterministico sobre sinais elegiveis do M5 full scan.
"""
import json, pathlib, sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SCAN_PATH = ROOT / "reports" / "asset_universe" / "m5_full_scan.json"
OUT_JSON = ROOT / "reports" / "asset_universe" / "top3_scanner.json"
OUT_TXT = ROOT / "reports" / "asset_universe" / "top3_scanner.txt"

scan = json.loads(SCAN_PATH.read_text(encoding="utf-8"))
records = scan["records"]

# Formula deterministica:
# eligibility: status==REAL_SIGNAL, decision in BUY/SELL, trade_allowed true, valid probabilities (sum 100), confidence not None, confluence not None
# ranking score deterministico: use campos que Mercury ja possui.
# Definição: ranking_score = confluence_weighted + confidence*0.5 + grade_bonus + probability_bonus
# grade_bonus: A=20,B=15,C=10,D=5,N/A=0 (escala)
# probabilidade dominante: buy_prob if BUY else sell_prob
# confluence já é weighted_score 0-100; confidence armazenado é 0-1? No scan confidence 0-1 (0.68). Converter para 0-100.
# Para determinismo, sort por ranking_score desc, depois internal_symbol asc como tiebreaker.

GRADE_BONUS = {"A+":25,"A":20,"B":15,"C":10,"D":5,"N/A":0,"N/A ":0, None:0}

def prob_dominant(r):
    if r["decision"]=="BUY": return float(r["buy_probability"] or 0)
    if r["decision"]=="SELL": return float(r["sell_probability"] or 0)
    return 0.0

def confidence_100(r):
    c=r.get("confidence")
    if c is None: return 0.0
    # if stored 0-1 convert to 0-100, if already 0-100 keep
    # threshold: if c <=1.0 and c>0 then it's 0-1
    if 0 < c <= 1.1:
        return c*100
    return c

FORMULA = (
    "ranking_score = confluence_weighted (0-100) + confidence_100*0.30 + grade_bonus(A+25/A20/B15/C10/D5) + dominant_prob*0.20 ; "
    "tie-breaker: internal_symbol ASC, audit_id ASC. "
    "Eligibility: status==REAL_SIGNAL AND decision in (BUY,SELL) AND trade_allowed==true AND prob_sum_ok==true AND confidence not None AND confluence not None"
)

eligible=[]
for r in records:
    if r.get("status")!="REAL_SIGNAL": continue
    if r.get("decision") not in ("BUY","SELL"): continue
    if not r.get("trade_allowed"): continue
    if not r.get("prob_sum_ok"): continue
    if r.get("confidence") is None: continue
    if r.get("confluence") is None: continue
    # valid confidence / confluence
    c100 = confidence_100(r)
    confl = float(r["confluence"] or 0)
    grade = r.get("grade")
    gbon = GRADE_BONUS.get(grade, 0)
    # also handle grade string upper
    if gbon==0 and grade:
        gbon = GRADE_BONUS.get(str(grade).upper(), 0)
    pdom = prob_dominant(r)
    score = confl + c100*0.30 + gbon + pdom*0.20
    eligible.append((score, r))

# sort deterministic
eligible.sort(key=lambda x: (-x[0], x[1]["internal_symbol"], x[1]["audit_id"]))

top3 = eligible[:3]

output={
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "formula": FORMULA,
    "eligibility_count": len(eligible),
    "total_records": len(records),
    "top3": [
        {
            "rank": i+1,
            "hezilex_input": r["hezilex_input"],
            "internal_symbol": r["internal_symbol"],
            "asset_class": r["asset_class"],
            "provider_symbol": r["provider_symbol"],
            "decision": r["decision"],
            "grade": r["grade"],
            "confidence": r["confidence"],
            "confidence_100": confidence_100(r),
            "confluence": r["confluence"],
            "buy_probability": r["buy_probability"],
            "sell_probability": r["sell_probability"],
            "wait_probability": r["wait_probability"],
            "dominant_probability": prob_dominant(r),
            "score": score,
            "audit_id": r["audit_id"],
            "execution_timestamp": r["execution_timestamp"],
            "trade_allowed": r["trade_allowed"],
            "trade_quality": r["trade_quality"],
            "source_record": r["internal_symbol"],
        }
        for i,(score,r) in enumerate(top3)
    ],
    "all_ranked": [
        {"rank": idx+1, "symbol": r["internal_symbol"], "decision": r["decision"], "score": sc}
        for idx,(sc,r) in enumerate(eligible)
    ]
}

OUT_JSON.write_text(json.dumps(output, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

lines=[]
lines.append("TOP 3 M5 SIGNALS — MERCURY-AI V1")
lines.append(f"Generated: {output['generated_at']}")
lines.append(f"Formula: {FORMULA}")
lines.append(f"Eligible REAL_SIGNAL: {output['eligibility_count']} / {output['total_records']}")
lines.append("")
if not top3:
    lines.append("NO ELIGIBLE SIGNALS")
else:
    for item in output["top3"]:
        lines.append(f"{item['rank']}. {item['hezilex_input']} ({item['internal_symbol']})")
        lines.append(f"   decision={item['decision']}")
        lines.append(f"   grade={item['grade']}")
        lines.append(f"   confidence={item['confidence']} (100={item['confidence_100']:.2f})")
        lines.append(f"   confluence={item['confluence']}")
        lines.append(f"   probability dominant={item['dominant_probability']} (buy={item['buy_probability']} sell={item['sell_probability']} wait={item['wait_probability']})")
        lines.append(f"   score={item['score']:.4f}")
        lines.append(f"   audit_id={item['audit_id']}")
        lines.append(f"   timestamp={item['execution_timestamp']}")
        lines.append(f"   source={item['source_record']}")
        lines.append("")

OUT_TXT.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
print(f"\nWrote {OUT_JSON} and {OUT_TXT}")
