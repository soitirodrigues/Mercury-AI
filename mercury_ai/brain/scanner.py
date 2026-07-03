from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.database.history_logger import HistoryLogger


class MercuryScanner:

    def __init__(self):

        self.pipeline = AnalysisPipeline()
        self.logger = HistoryLogger()

        self.symbols = [
            "GC=F",
            "SI=F",
            "CL=F",
            "BTC-USD",
            "ETH-USD",
            "EURUSD=X"
        ]

    def scan(self):

        print()
        print("=" * 60)
        print("MERCURY AI SCANNER")
        print("=" * 60)

        analyses = []

        for symbol in self.symbols:

            try:

                analysis = self.pipeline.analyze(symbol)

                analyses.append(analysis)

                self.logger.save(analysis)

                print(
                    f"{symbol:<10} "
                    f"{analysis.confluence.decision:<5} "
                    f"Score:{analysis.confluence.score:>4} "
                    f"Conf:{analysis.confluence.confidence}%"
                )

            except Exception as e:

                print(f"{symbol:<10} ERROR -> {e}")

        print("=" * 60)

        return analyses