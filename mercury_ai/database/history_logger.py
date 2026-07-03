from pathlib import Path
import csv
from datetime import datetime


class HistoryLogger:

    def __init__(self):

        self.file = Path("mercury_ai/database/analysis_history.csv")

        # Cria a pasta caso ela não exista
        self.file.parent.mkdir(parents=True, exist_ok=True)

        if not self.file.exists():

            with open(self.file, "w", newline="", encoding="utf8") as f:

                writer = csv.writer(f)

                writer.writerow([
                    "datetime",
                    "symbol",
                    "decision",
                    "score",
                    "confidence"
                ])

    def save(self, analysis):

        with open(self.file, "a", newline="", encoding="utf8") as f:

            writer = csv.writer(f)

            writer.writerow([
                datetime.now(),
                analysis.market.symbol,
                analysis.confluence.decision,
                analysis.confluence.score,
                analysis.confluence.confidence
            ])