from mercury_ai.providers.market_provider import MarketProvider

provider = MarketProvider()

data = provider.get_price("GC=F")

print(data)