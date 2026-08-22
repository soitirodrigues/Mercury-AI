#!/usr/bin/env python3
"""
ASSET UNIVERSE DISCOVERY — SPRINT MERCURY-AI V1
Descobre a configuracao real do Mercury e gera mapeamento Hezilex -> Mercury.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.config.universe import OPERATIONAL_UNIVERSE, FOREX_UNIVERSE, CRYPTO_UNIVERSE, STOCK_UNIVERSE, COMMODITY_UNIVERSE

# Hezilex inputs exactly as sprint spec
HEZILEX_FOREX = [
 "EUR/USD","EUR/GBP","AUD/JPY","EUR/JPY","GBP/USD","AUD/CAD","USD/CAD","NZD/USD",
 "USD/JPY","CAD/JPY","CHF/JPY","AUD/CHF","EUR/AUD","GBP/CHF","GBP/AUD","GBP/JPY",
 "USD/CHF","NZD/JPY","EUR/CHF","CAD/CHF","EUR/CAD","BTC/USD","AUD/NZD","AUD/USD",
 "NZD/CHF","GBP/CAD","GBP/NZD","NZD/CAD",
]
HEZILEX_CRYPTO = ["BITCOIN","LITECOIN","BNB","XRP","ETHEREUM","SOLANA","AVAX","DOGE","SUI","STELLAR","CARDANO","LINK"]
HEZILEX_STOCKS = ["APPLE","NETFLIX","META","TESLA","MICROSOFT","MCDONALDS","AMAZON","PAYPAL","STARBUCKS","NVIDIA","DISNEY","INTEL","VISA","IBM","FORD","COCA-COLA","NIKE","MASTERCARD","SPOTFY","SPACEX","JPMORGAN","BANK OF AMERICA","CITIGROUP","WELLS FARGO STANLEY"]
HEZILEX_COMMODITIES = ["PETRÓLEO","PRATA","OURO"]

# Mapping table: hezilex input -> mercury
# For explicit handling we define a dict with manual mappings

MANUAL_MAP = {
    # FOREX
    "EUR/USD": ("FOREX","EURUSD","EURUSD=X","EURUSD=X"),
    "EUR/GBP": ("FOREX","EURGBP","EURGBP=X","EURGBP=X"),
    "AUD/JPY": ("FOREX","AUDJPY","AUDJPY=X","AUDJPY=X"),
    "EUR/JPY": ("FOREX","EURJPY","EURJPY=X","EURJPY=X"),
    "GBP/USD": ("FOREX","GBPUSD","GBPUSD=X","GBPUSD=X"),
    "AUD/CAD": ("FOREX","AUDCAD","AUDCAD=X","AUDCAD=X"),
    "USD/CAD": ("FOREX","USDCAD","USDCAD=X","USDCAD=X"),
    "NZD/USD": ("FOREX","NZDUSD","NZDUSD=X","NZDUSD=X"),
    "USD/JPY": ("FOREX","USDJPY","USDJPY=X","USDJPY=X"),
    "CAD/JPY": ("FOREX","CADJPY","CADJPY=X","CADJPY=X"),
    "CHF/JPY": ("FOREX","CHFJPY","CHFJPY=X","CHFJPY=X"),
    "AUD/CHF": ("FOREX","AUDCHF","AUDCHF=X","AUDCHF=X"),
    "EUR/AUD": ("FOREX","EURAUD","EURAUD=X","EURAUD=X"),
    "GBP/CHF": ("FOREX","GBPCHF","GBPCHF=X","GBPCHF=X"),
    "GBP/AUD": ("FOREX","GBPAUD","GBPAUD=X","GBPAUD=X"),
    "GBP/JPY": ("FOREX","GBPJPY","GBPJPY=X","GBPJPY=X"),
    "USD/CHF": ("FOREX","USDCHF","USDCHF=X","USDCHF=X"),
    "NZD/JPY": ("FOREX","NZDJPY","NZDJPY=X","NZDJPY=X"),
    "EUR/CHF": ("FOREX","EURCHF","EURCHF=X","EURCHF=X"),
    "CAD/CHF": ("FOREX","CADCHF","CADCHF=X","CADCHF=X"),
    "EUR/CAD": ("FOREX","EURCAD","EURCAD=X","EURCAD=X"),
    "BTC/USD": ("FOREX","BTCUSD","BTC-USD","BTC-USD"),  # maps to crypto
    "AUD/NZD": ("FOREX","AUDNZD","AUDNZD=X","AUDNZD=X"),
    "AUD/USD": ("FOREX","AUDUSD","AUDUSD=X","AUDUSD=X"),
    "NZD/CHF": ("FOREX","NZDCHF","NZDCHF=X","NZDCHF=X"),
    "GBP/CAD": ("FOREX","GBPCAD","GBPCAD=X","GBPCAD=X"),
    "GBP/NZD": ("FOREX","GBPNZD","GBPNZD=X","GBPNZD=X"),
    "NZD/CAD": ("FOREX","NZDCAD","NZDCAD=X","NZDCAD=X"),
    # CRYPTO
    "BITCOIN": ("CRYPTO","BTC","BTC-USD","BTC-USD"),
    "LITECOIN": ("CRYPTO","LTC","LTC-USD","LTC-USD"),
    "BNB": ("CRYPTO","BNB","BNB-USD","BNB-USD"),
    "XRP": ("CRYPTO","XRP","XRP-USD","XRP-USD"),
    "ETHEREUM": ("CRYPTO","ETH","ETH-USD","ETH-USD"),
    "SOLANA": ("CRYPTO","SOL","SOL-USD","SOL-USD"),
    "AVAX": ("CRYPTO","AVAX","AVAX-USD","AVAX-USD"),
    "DOGE": ("CRYPTO","DOGE","DOGE-USD","DOGE-USD"),
    "SUI": ("CRYPTO","SUI","SUI-USD","SUI-USD"),
    "STELLAR": ("CRYPTO","XLM","XLM-USD","XLM-USD"),
    "CARDANO": ("CRYPTO","ADA","ADA-USD","ADA-USD"),
    "LINK": ("CRYPTO","LINK","LINK-USD","LINK-USD"),
    # STOCKS
    "APPLE": ("STOCK","AAPL","AAPL","AAPL"),
    "NETFLIX": ("STOCK","NFLX","NFLX","NFLX"),
    "META": ("STOCK","META","META","META"),
    "TESLA": ("STOCK","TSLA","TSLA","TSLA"),
    "MICROSOFT": ("STOCK","MSFT","MSFT","MSFT"),
    "MCDONALDS": ("STOCK","MCD","MCD","MCD"),
    "AMAZON": ("STOCK","AMZN","AMZN","AMZN"),
    "PAYPAL": ("STOCK","PYPL","PYPL","PYPL"),
    "STARBUCKS": ("STOCK","SBUX","SBUX","SBUX"),
    "NVIDIA": ("STOCK","NVDA","NVDA","NVDA"),
    "DISNEY": ("STOCK","DIS","DIS","DIS"),
    "INTEL": ("STOCK","INTC","INTC","INTC"),
    "VISA": ("STOCK","V","V","V"),
    "IBM": ("STOCK","IBM","IBM","IBM"),
    "FORD": ("STOCK","F","F","F"),
    "COCA-COLA": ("STOCK","KO","KO","KO"),
    "NIKE": ("STOCK","NKE","NKE","NKE"),
    "MASTERCARD": ("STOCK","MA","MA","MA"),
    "SPOTFY": ("STOCK","SPOT","SPOT","SPOT"),  # typo corrected
    "SPACEX": ("STOCK","SPACEX",None,None),
    "JPMORGAN": ("STOCK","JPM","JPM","JPM"),
    "BANK OF AMERICA": ("STOCK","BAC","BAC","BAC"),
    "CITIGROUP": ("STOCK","C","C","C"),
    # WELLS FARGO STANLEY will be split
    # COMMODITIES
    "PETRÓLEO": ("COMMODITY","CL","CL=F","CL=F"),
    "PRATA": ("COMMODITY","SI","SI=F","SI=F"),
    "OURO": ("COMMODITY","GC","GC=F","GC=F"),
}

OUT_DIR = ROOT / "reports" / "asset_universe"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def check_configured(internal_symbol):
    if internal_symbol is None:
        return False
    return internal_symbol in OPERATIONAL_UNIVERSE and OPERATIONAL_UNIVERSE[internal_symbol].enabled

def build_entry(input_name, asset_class, normalized, internal, provider, reason=None, split_note=None):
    configured = check_configured(internal) if internal else False
    supported = configured  # Yahoo supports all universe assets
    if internal is None:
        mapping_status = "UNSUPPORTED"
        reason = reason or "NO_SUPPORTED_PUBLIC_INSTRUMENT"
        supported = False
        configured = False
    elif not supported:
        mapping_status = "UNSUPPORTED"
        reason = reason or "NO_SUPPORTED_PUBLIC_INSTRUMENT"
    else:
        mapping_status = "PASS"
        reason = reason or "MAPPED_TO_UNIVERSE"
    # Additional mapping_reason handling
    mapping_reason = reason
    if input_name == "SPOTFY":
        mapping_reason = "TYPO_CORRECTED_SPOTFY->SPOT"
    if input_name == "WELLS FARGO STANLEY":
        mapping_reason = split_note or reason
    if input_name == "BTC/USD":
        mapping_reason = "FOREX_LIST_CONTAINS_CRYPTO_MAPPED_TO_BTC-USD"
    if input_name in ("CARDANO","LINK","LITECOIN"):
        mapping_reason = "NO_SUPPORTED_PUBLIC_INSTRUMENT_NOT_IN_MERCURY_UNIVERSE"
    if input_name == "SPACEX":
        mapping_reason = "PRIVATE_COMPANY_NO_PUBLIC_TICKER"
    if input_name == "STANLEY":
        mapping_reason = "MORGAN_STANLEY_MS_NOT_IN_MERCURY_UNIVERSE_23_STOCKS"

    entry = {
        "source": "hezilex",
        "asset": input_name,
        "input_name": input_name,
        "asset_class": asset_class,
        "normalized_name": normalized,
        "internal_symbol": internal,
        "provider_symbol": provider,
        "configured": configured,
        "supported": supported,
        "mapping_status": mapping_status,
        "reason": reason,
        "mapping_reason": mapping_reason,
    }
    # minimal format required by sprint section 4
    return entry

def main():
    all_entries = []
    # FOREX
    for a in HEZILEX_FOREX:
        ac, norm, internal, provider = MANUAL_MAP[a]
        e = build_entry(a, ac, norm, internal, provider)
        all_entries.append(e)
    # CRYPTO
    for a in HEZILEX_CRYPTO:
        ac, norm, internal, provider = MANUAL_MAP[a]
        # mark unsupported correctly
        reason = None
        if a in ("LITECOIN","CARDANO","LINK"):
            reason = "NO_SUPPORTED_PUBLIC_INSTRUMENT"
        e = build_entry(a, ac, norm, internal, provider, reason=reason)
        all_entries.append(e)
    # STOCKS
    for a in HEZILEX_STOCKS:
        if a == "WELLS FARGO STANLEY":
            # split into two effective assets
            # Entry 1: WELLS FARGO -> WFC
            e1 = build_entry("WELLS FARGO", "STOCK", "WFC", "WFC", "WFC", reason="MAPPED_TO_UNIVERSE_SPLIT_FROM_WELLS_FARGO_STANLEY")
            e1["input_name"] = "WELLS FARGO STANLEY -> WELLS FARGO"
            e1["asset"] = "WELLS FARGO"
            e1["mapping_reason"] = "SPLIT_WELLS_FARGO_STANLEY_INTO_WFC_AND_MS"
            all_entries.append(e1)
            # Entry 2: MORGAN STANLEY -> MS (unsupported)
            e2 = build_entry("STANLEY", "STOCK", "MS", "MS", "MS", reason="NO_SUPPORTED_PUBLIC_INSTRUMENT")
            e2["input_name"] = "WELLS FARGO STANLEY -> MORGAN STANLEY"
            e2["asset"] = "MORGAN STANLEY"
            e2["asset_class"] = "STOCK"
            e2["normalized_name"] = "MS"
            e2["mapping_reason"] = "SPLIT_WELLS_FARGO_STANLEY_MS_NOT_IN_UNIVERSE"
            e2["mapping_status"] = "UNSUPPORTED"
            e2["supported"] = False
            e2["configured"] = False
            all_entries.append(e2)
            continue
        ac, norm, internal, provider = MANUAL_MAP[a]
        reason = None
        if a == "SPACEX":
            reason = "NO_SUPPORTED_PUBLIC_INSTRUMENT"
        e = build_entry(a, ac, norm, internal, provider, reason=reason)
        all_entries.append(e)
    # COMMODITIES
    for a in HEZILEX_COMMODITIES:
        ac, norm, internal, provider = MANUAL_MAP[a]
        e = build_entry(a, ac, norm, internal, provider)
        all_entries.append(e)

    # Write mapping json
    out_path = OUT_DIR / "hezilex_asset_mapping.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(all_entries)} entries to {out_path}")

    # Also produce normalization table for attention items
    norm_table = []
    for e in all_entries:
        norm_table.append({
            "input_name": e["input_name"],
            "normalized_name": e["normalized_name"],
            "asset_class": e["asset_class"],
            "internal_symbol": e["internal_symbol"],
            "provider_symbol": e["provider_symbol"],
            "mapping_status": e["mapping_status"],
            "mapping_reason": e["mapping_reason"]
        })
    # Print summary
    supported = sum(1 for e in all_entries if e["supported"])
    unsupported = sum(1 for e in all_entries if not e["supported"])
    print(f"HEZILEX EFFECTIVE ASSETS: {len(all_entries)} (raw 67 +1 split)")
    print(f"SUPPORTED: {supported}")
    print(f"UNSUPPORTED: {unsupported}")

    # Source of truth discovery
    sot = {
        "SOURCE_OF_TRUTH": "mercury_ai/config/universe.py :: OPERATIONAL_UNIVERSE",
        "config_file": "mercury_ai/config/universe.py",
        "config_path": str(ROOT / "mercury_ai" / "config" / "universe.py"),
        "registry_module": "mercury_ai.config.universe",
        "asset_count": len(OPERATIONAL_UNIVERSE),
        "breakdown": {
            "FOREX": len(FOREX_UNIVERSE),
            "CRYPTO": len(CRYPTO_UNIVERSE),
            "STOCK": len(STOCK_UNIVERSE),
            "COMMODITY": len(COMMODITY_UNIVERSE),
        },
        "broker_config": str(ROOT / "data" / "brokers" / "XP.json"),
        "asset_registry": str(ROOT / "data" / "asset_registry.json"),
        "broker_count_current": len(json.load(open(ROOT/"data/brokers/XP.json")) if (ROOT/"data/brokers/XP.json").exists() else []),
        "registry_count_current": len(json.load(open(ROOT/"data/asset_registry.json")) if (ROOT/"data/asset_registry.json").exists() else {}),
        "secondary_source_warning": "data/brokers/XP.json and data/asset_registry.json are SECONDARY - they must be synced from universe.py (only 3 assets currently -> GAP).",
    }
    with open(OUT_DIR / "source_of_truth.json", "w", encoding="utf-8") as f:
        json.dump(sot, f, indent=2, ensure_ascii=False)
    print(f"SOURCE_OF_TRUTH: {sot['SOURCE_OF_TRUTH']} count={sot['asset_count']}")

if __name__ == "__main__":
    main()
