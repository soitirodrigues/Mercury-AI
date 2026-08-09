from dataclasses import replace
from typing import List

from mercury_ai.core.pipeline_executor import PipelineExecutor
from mercury_ai.core.pipeline_profiler import PipelineProfiler

from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_context import MarketContext


class ContextEngine:
    """
    Responsável apenas por enriquecer o MarketContext.

    O MarketContext oficial é criado exclusivamente pelo
    MarketContextBuilder.
    """

    def __init__(
        self,
        executor: PipelineExecutor,
        profiler: PipelineProfiler
    ):
        self.executor = executor
        self.profiler = profiler

    def analyze(
        self,
        context: MarketContext,
        evidences: List[Evidence]
    ) -> MarketContext:

        if not isinstance(context, MarketContext):
            raise TypeError(
                "ContextEngine expects MarketContext."
            )

        merged = self.executor.execute(
            "MergeEvidences",
            self._merge_evidences,
            list,
            evidences
        )

        deduped = self.executor.execute(
            "Deduplicate",
            self._deduplicate_evidences,
            list,
            merged
        )

        conflicts = self.executor.execute(
            "ConflictDetection",
            self._detect_conflicts,
            list,
            deduped
        )

        quality = self.executor.execute(
            "QualityCalculation",
            self._calculate_quality,
            float,
            conflicts
        )

        return self._refine_context(
            context=context,
            evidences=conflicts,
            quality=quality
        )

    def _merge_evidences(
        self,
        evidences: List[Evidence]
    ) -> List[Evidence]:

        return evidences

    def _deduplicate_evidences(
        self,
        evidences: List[Evidence]
    ) -> List[Evidence]:

        seen = set()
        unique = []

        for evidence in evidences:

            key = (
                evidence.engine_name,
                evidence.evidence_name
            )

            if key not in seen:

                seen.add(key)
                unique.append(evidence)

        return unique

    def _detect_conflicts(
        self,
        evidences: List[Evidence]
    ) -> List[Evidence]:

        result = list(evidences)

        trend = [
            e
            for e in evidences
            if e.engine_name == "Trend"
        ]

        momentum = [
            e
            for e in evidences
            if e.engine_name == "MomentumEngine"
        ]

        for t in trend:

            for m in momentum:

                if (
                    t.direction == "BULLISH"
                    and m.direction == "BEARISH"
                ) or (
                    t.direction == "BEARISH"
                    and m.direction == "BULLISH"
                ):

                    result.append(
                        Evidence(
                            engine_name="ConsistencyEngine",
                            evidence_name="TrendMomentumConflict",
                            direction="NEUTRAL",
                            strength=50.0,
                            quality_score=80.0,
                            description=(
                                f"Conflict: {t.direction} x {m.direction}"
                            ),
                            weight=-10.0,
                            contribution_score=-50.0
                        )
                    )

        return result

    def _calculate_quality(
        self,
        evidences: List[Evidence]
    ) -> float:

        if not evidences:
            return 0.0

        total = 0.0

        for evidence in evidences:

            total += getattr(
                evidence,
                "quality_score",
                100.0
            )

        return round(
            total / len(evidences),
            2
        )

    def _refine_context(
        self,
        context: MarketContext,
        evidences: List[Evidence],
        quality: float
    ) -> MarketContext:

        bullish = 0
        bearish = 0

        for evidence in evidences:

            if evidence.direction == "BULLISH":
                bullish += 1

            elif evidence.direction == "BEARISH":
                bearish += 1

        if bullish > bearish:
            bias = "BULLISH"

        elif bearish > bullish:
            bias = "BEARISH"

        else:
            bias = "NEUTRAL"

        new_context = replace(
            context,
            trend=list(evidences),
            market_regime=replace(
                context.market_regime,
                supporting_evidences=list(evidences)
            ),
            mtf_consensus=replace(
                context.mtf_consensus,
                global_bias=bias,
                local_bias=bias
            )
        )

        assert isinstance(new_context, MarketContext)

        return new_context