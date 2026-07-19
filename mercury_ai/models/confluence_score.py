from dataclasses import dataclass

@dataclass(frozen=True)
class ConfluenceScore:
    confluence_score: float
    clarity_score: float
    bullish_score: float
    bearish_score: float
    conflict_penalty: float
