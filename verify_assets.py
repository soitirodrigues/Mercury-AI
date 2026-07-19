from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider

def verify_assets():
    pipeline = AnalysisPipeline(market_service=MarketDataService(providers=[YahooFinanceProvider()]), providers=[YahooFinanceProvider()])
    
    symbols = ["GC=F", "BTC-USD", "EURUSD=X"]
    
    print("Verifying assets...")
    
    for symbol in symbols:
        try:
            result = pipeline.analyze(symbol)
            print(f"Asset: {symbol:10} | Decision: {result.decision.decision} | Summary: {result.decision.summary}")
        except Exception as e:
            print(f"Asset: {symbol:10} | Error: {e}")

if __name__ == "__main__":
    verify_assets()
