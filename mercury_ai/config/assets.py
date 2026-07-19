ASSET_REGISTRY = {
    "EURUSD=X": {"symbol": "EURUSD=X", "display_name": "EUR/USD", "market": "FOREX", "enabled": True, "volatility": "MEDIUM", "precision": 5, "priority": 1},
    "BTC-USD": {"symbol": "BTC-USD", "display_name": "BTC/USD", "market": "CRYPTO", "enabled": True, "volatility": "HIGH", "precision": 2, "priority": 1},
    "ETH-USD": {"symbol": "ETH-USD", "display_name": "ETH/USD", "market": "CRYPTO", "enabled": True, "volatility": "HIGH", "precision": 2, "priority": 1},
    "GC=F": {"symbol": "GC=F", "display_name": "Gold", "market": "COMMODITIES", "enabled": True, "volatility": "MEDIUM", "precision": 2, "priority": 1},
    "SI=F": {"symbol": "SI=F", "display_name": "Silver", "market": "COMMODITIES", "enabled": True, "volatility": "HIGH", "precision": 3, "priority": 1},
    "CL=F": {"symbol": "CL=F", "display_name": "Crude Oil", "market": "COMMODITIES", "enabled": True, "volatility": "HIGH", "precision": 2, "priority": 1},
}

FOREX = ["EURUSD=X"]
CRYPTO = ["BTC-USD", "ETH-USD"]
COMMODITIES = ["GC=F", "SI=F", "CL=F"]
INDICES = []

SUPPORTED_ASSETS = {
    "FOREX": FOREX,
    "CRYPTO": CRYPTO,
    "COMMODITIES": COMMODITIES,
    "INDICES": INDICES,
}
