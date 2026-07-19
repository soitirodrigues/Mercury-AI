from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.analysis.evidence_query import EvidenceQuery
from mercury_ai.core.asset_registry import AssetRegistry
from mercury_ai.config.configuration_center import MercuryConfigCenter

from mercury_ai.providers.mercury_data_provider import MercuryDataProvider

from mercury_ai.analysis.ranking_engine import RankingEngine
from mercury_ai.brain.institutional_brain import InstitutionalBrain
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.analysis.notification_center import NotificationCenter


class MercuryScanner:

    def __init__(self, min_quality_score=40.0):

        # Provider central V1
        self.provider = MercuryDataProvider()

        # Pipeline institucional
        self.pipeline = AnalysisPipeline(
            market_service=MarketDataService(
                provider=self.provider
            ),
            providers=[
                self.provider
            ]
        )

        self.ranking_engine = RankingEngine()
        self.brain = InstitutionalBrain()

        self.min_quality_score = min_quality_score

        self.asset_registry = AssetRegistry()

        self.config = MercuryConfigCenter()

        self.notification_center = NotificationCenter()


    def scan(self):

        print()
        print("=" * 60)
        print("MERCURY AI SCANNER")
        print("=" * 60)


        analyses = []


        active_profile = self.config.get(
            "OPERATIONAL_PROFILE",
            "active",
            "Demo"
        )

        active_broker = self.config.get(
            "OPERATIONAL_PROFILE",
            "broker",
            "XP"
        )


        authorized_symbols = (
            self.asset_registry
            .get_assets_for_broker(active_broker)
        )


        enabled_assets = [
            a
            for a in self.asset_registry.assets.values()
            if (
                a.enabled
                and a.profile == active_profile
                and a.symbol in authorized_symbols
            )
        ]


        enabled_assets.sort(
            key=lambda a: (
                -a.favorite,
                -a.last_operated,
                -a.previous_score,
                -a.priority,
                -a.liquidity,
                a.spread
            )
        )


        symbols = [
            a.symbol
            for a in enabled_assets
        ]


        for symbol in symbols:

            try:

                print(
                    f"\nAnalisando {symbol}..."
                )


                # Analise pelo provider V1
                analysis = self.pipeline.analyze(symbol)


                score = analysis.decision.score


                self.asset_registry.update_asset_stats(
                    symbol,
                    score
                )


                if score < self.min_quality_score:
                    continue


                analyses.append(
                    analysis
                )


                self._print_report(
                    analysis
                )


            except Exception as e:

                print(
                    f"{symbol} ERROR -> {e}"
                )



        ranked = self.ranking_engine.rank(
            analyses
        )


        self._print_ranking(
            ranked
        )


        print("=" * 60)


        return ranked



    def _print_ranking(self, ranked):

        print()
        print("=" * 60)
        print(
            "RANKING INSTITUCIONAL DE OPORTUNIDADES"
        )
        print("=" * 60)


        for index, analysis in enumerate(ranked):

            score = analysis.decision.score


            print(
                f"{index+1}. "
                f"{analysis.market.symbol:<10}"
                f" | Score: {score:.2f}"
                f" | {analysis.decision.decision}"
            )


            print(
                self.brain
                .explain(analysis)
                .replace("\n", " ")
            )


        print("=" * 60)




    def _print_report(self, analysis):

        market = analysis.market
        decision = analysis.decision
        regime = analysis.market_regime


        print()
        print("=" * 60)

        print(
            f"RELATÓRIO MERCURY AI | {market.symbol}"
        )

        print("=" * 60)


        self._print_line(
            "Ativo",
            market.symbol
        )


        self._print_line(
            "Decisão",
            decision.decision
        )


        self._print_line(
            "Confiança",
            f"{decision.confidence*100:.1f}%"
        )


        self._print_line(
            "Probabilidades",
            (
                f"BUY {decision.buy_probability:.1f}% | "
                f"SELL {decision.sell_probability:.1f}% | "
                f"WAIT {decision.wait_probability:.1f}%"
            )
        )


        self._print_line(
            "Regime",
            regime.regime if regime else "N/A"
        )


        self._print_line(
            "Score",
            decision.score
        )


        print("=" * 60)



    def _print_line(self, label, value):

        print(
            f"{label:<20}: {self._value(value)}"
        )



    def _value(self, value):

        if value is None:
            return "N/A"

        if isinstance(value, float):
            return f"{value:.2f}"

        return value