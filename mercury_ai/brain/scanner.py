import logging
import traceback

from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.core.asset_registry import AssetRegistry
from mercury_ai.config.configuration_center import MercuryConfigCenter

from mercury_ai.providers.mercury_data_provider import MercuryDataProvider

from mercury_ai.analysis.ranking_engine import RankingEngine
from mercury_ai.brain.institutional_brain import InstitutionalBrain
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.analysis.notification_center import NotificationCenter

logger = logging.getLogger(__name__)


class MercuryScanner:

    def __init__(self, min_quality_score=40.0):

        # Provider central V1
        self.provider = MercuryDataProvider()
        self.provider_manager = self.provider  # alias para compatibilidade com testes

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

        logger.info("=" * 60)
        logger.info("MERCURY AI SCANNER")
        logger.info("=" * 60)

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

                logger.info("Analisando %s...", symbol)

                # Analise pelo provider V1
                analysis = self.pipeline.analyze(symbol)

                logger.debug("=" * 80)
                logger.debug("DEBUG ANALYSIS")
                logger.debug("=" * 80)

                logger.debug("Decision : %s", analysis.decision.decision)
                logger.debug("Score    : %s", analysis.decision.score)
                logger.debug("Confidence: %s", analysis.decision.confidence)
                logger.debug("BUY      : %s", analysis.decision.buy_probability)
                logger.debug("SELL     : %s", analysis.decision.sell_probability)
                logger.debug("WAIT     : %s", analysis.decision.wait_probability)

                logger.debug("=" * 80)

                score = analysis.decision.score
                

                self.asset_registry.update_asset_stats(
                    symbol,
                    score
                )

                logger.info("Scanner Score........: %.2f", score)
                logger.info("Score mínimo.........: %.2f", self.min_quality_score)

                if score < self.min_quality_score:
                    logger.info(">>> DESCARTADO PELO SCANNER <<<")
                    continue

                logger.info(">>> ADICIONADO AO RANKING <<<")

                analyses.append(
                    analysis
                )

                self._print_report(
                    analysis
                )

<<<<<<< HEAD
            except (RuntimeError, ValueError, TypeError, KeyError, OSError, ConnectionError, TimeoutError) as e:
=======
            except Exception as e:
>>>>>>> 67cc5c60936ff914a76d6d94a09c6422d147e02a

                logger.error("=" * 80)
                logger.error("ERRO DURANTE A ANÁLISE DE %s", symbol)
                logger.error("=" * 80)

                traceback.print_exc()

                logger.error("Mensagem: %s", e)

                logger.error("=" * 80)

                # Trigger provider failover on failure
                if hasattr(self, 'provider_manager') and self.provider_manager is not None:
                    try:
                        self.provider_manager.trigger_failover()
                        self.notification_center.send(
                            "scanner_failover",
                            {"symbol": symbol, "error": str(e)}
                        )
                    except (RuntimeError, ConnectionError, OSError, AttributeError) as failover_error:
                        logger.error("Falha no failover: %s", failover_error)

        ranked = self.ranking_engine.rank(
            analyses
        )

        self._print_ranking(
            ranked
        )

        logger.info("=" * 60)

        return ranked

    def _print_ranking(self, ranked):

        logger.info("=" * 60)
        logger.info("RANKING INSTITUCIONAL DE OPORTUNIDADES")
        logger.info("=" * 60)

        for index, analysis in enumerate(ranked):

            score = analysis.decision.score

            logger.info(
                "%d. %-10s | Score: %.2f | %s",
                index + 1,
                analysis.market.symbol,
                score,
                analysis.decision.decision,
            )

            logger.info(
                "%s",
                self.brain
                .explain(analysis)
                .replace("\n", " "),
            )

        logger.info("=" * 60)

    def _print_report(self, analysis):

        market = analysis.market
        decision = analysis.decision
        regime = analysis.market_regime

        logger.info("=" * 60)
        logger.info("RELATÓRIO MERCURY AI | %s", market.symbol)
        logger.info("=" * 60)

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

        # =====================================================
        # DECISION EXPLAINABILITY
        # =====================================================
        if decision.explainability:
            exp = decision.explainability
            logger.info("-" * 40)
            logger.info("DECISION EXPLAINABILITY")
            logger.info("-" * 40)
            self._print_line("Decisão", exp.decision)
            self._print_line("Razão", exp.reason)
            self._print_line("Direção Dominante", exp.dominant_direction)
            self._print_line("Nota Oportunidade", exp.opportunity_grade)
            self._print_line("Sinais Conflitantes", str(exp.conflicting_signals))
            self._print_line("Score Institucional", f"{exp.institutional_score:.2f}")
            self._print_line("Confiança", f"{exp.confidence:.1f}%")
            self._print_line("Regra Disparada", exp.triggered_rule)
            if exp.contributions:
                logger.info("Contribuições por Engine:")
                for contrib in exp.contributions:
                    self._print_line(
                        f"  {contrib.engine_name}",
                        f"peso={contrib.weight} raw={contrib.raw_score:.2f} "
                        f"weighted={contrib.weighted_score:.2f} dir={contrib.direction} "
                        f"conf={contrib.confidence:.1f}%"
                    )
            if exp.decision_chain:
                logger.info("Cadeia de Decisão:")
                for i, step in enumerate(exp.decision_chain, 1):
                    logger.info("  %d. %s", i, step)

        logger.info("=" * 60)

    def _print_line(self, label, value):

        logger.info("%-20s: %s", label, self._value(value))

    def _value(self, value):

        if value is None:
            return "N/A"

        if isinstance(value, float):
            return f"{value:.2f}"

        return value