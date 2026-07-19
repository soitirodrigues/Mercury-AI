from mercury_ai.providers.market_provider import MercuryDataProvider

provider = MercuryDataProvider()

data = provider.get_data("GC=F")

print(data)