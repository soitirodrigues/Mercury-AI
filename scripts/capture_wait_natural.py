import json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
# Add GC=F naturally: expand XP.json and registry to 3 assets
xp_path=ROOT/"data/brokers/XP.json"
reg_path=ROOT/"data/asset_registry.json"
xp=json.loads(xp_path.read_text())
reg=json.loads(reg_path.read_text())
# Backup check not needed; we will add GC=F if missing
added=False
if "GC=F" not in xp:
    xp.append("GC=F")
    xp_path.write_text(json.dumps(xp, indent=2))
    print(f"XP.json now {xp}")
    added=True
else:
    print("GC=F already in XP.json")

if "GC=F" not in reg:
    reg["GC=F"]={
        "symbol":"GC=F",
        "category":"Commodities",
        "priority":3,
        "profile":"Demo",
        "enabled": True,
        "provider":"Yahoo",
        "fallback_provider":"Polygon",
        "market":"Commodities",
        "timeframe":"5m",
        "tick_size":0.1,
        "pip_size":0.01,
        "trading_session":"Standard",
        "liquidity":1.0,
        "spread":0.1,
        "favorite": False,
        "last_operated": 0,
        "previous_score": 0
    }
    reg_path.write_text(json.dumps(reg, indent=2))
    print("Registry added GC=F")
else:
    if not reg["GC=F"]["enabled"]:
        reg["GC=F"]["enabled"]=True
        reg_path.write_text(json.dumps(reg, indent=2))
        print("Enabled GC=F")
    else:
        print("GC=F already enabled")

# Now run proof
import subprocess, pathlib
print("Running v1 proof with GC=F ...")
proc = subprocess.run([sys.executable, str(ROOT/"scripts/v1_final_operational_proof_all_assets.py")], capture_output=False)
