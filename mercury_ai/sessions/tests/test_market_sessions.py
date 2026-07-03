from mercury_ai.sessions.market_sessions import MarketSessions

session = MarketSessions()

print("Sessão Atual:")
print(session.get_current_session())

print()

print("Alta Liquidez:")
print(session.is_high_liquidity())