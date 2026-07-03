from mercury_ai.brain.mercury_brain import MercuryBrain

brain = MercuryBrain()

market = {
    "trend": "UP",
    "rsi": 28,
    "bollinger": "LOWER"
}

calendar = {
    "high_impact": False
}

news = {}

session = {
    "high_liquidity": True
}

result = brain.analyze(
    market,
    calendar,
    news,
    session
)

print(result)