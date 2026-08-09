import pandas as pd
import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass, replace
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.liquidity_analysis import LiquidityAnalysis
from mercury_ai.models.swing_analysis import Swing
from mercury_ai.models.market_structure_profile import MarketStructureProfile
from mercury_ai.models.liquidity_result import LiquidityResult
from mercury_ai.core.pipeline_profiler import PipelineProfiler
from mercury_ai.core.pipeline_executor import PipelineExecutor


@dataclass(frozen=True)
class EqualHighGroup:
    touches: List[Swing]
    prices: List[float]
    timestamps: List[str]
    indices: List[int]
    strengths: List[float]
    ATRs: List[float]

@dataclass(frozen=True)
class EqualHighMetrics:
    touch_count: int
    average_price: float
    minimum_price: float
    maximum_price: float
    price_deviation: float
    average_strength: float
    minimum_strength: float
    maximum_strength: float
    average_ATR: float
    ATR_consistency: float 
    first_timestamp: str
    last_timestamp: str
    first_index: int
    last_index: int
    age_in_swings: int
    cluster_width: int

@dataclass(frozen=True)
class EqualHighScore:
    touch_score: float
    strength_score: float
    atr_score: float
    deviation_score: float
    density_score: float
    final_score: float
    touch_count: int
    average_price: float
    average_strength: float
    average_ATR: float
    age_in_swings: int
    cluster_density: float

class LiquidityEngine:
    """
    Motor institucional para análise de liquidez baseado em histórico de swings confirmados.
    Responsabilidade: Orquestração do pipeline institucional de liquidez (Equal Highs) com camada de validação.
    Pipeline puramente funcional.
    """

    def __init__(self, 
                 executor: Optional[PipelineExecutor] = None,
                 profiler: Optional[PipelineProfiler] = None,
                 minimum_touches: int = 2,
                 maximum_touches: int = 10,
                 atr_multiplier: float = 0.75,
                 maximum_swing_distance: int = 50,
                 minimum_strength: float = 0.3,
                 touch_weight: float = 0.3,
                 strength_weight: float = 0.2,
                 atr_consistency_weight: float = 0.2,
                 deviation_weight: float = 0.1,
                 density_weight: float = 0.2,
                 maximum_score: float = 100.0,
                 minimum_score: float = 0.0,
                 evidence_weight: float = 30.0):
        self.executor = executor
        self.profiler = profiler
        self.minimum_touches = minimum_touches
        self.maximum_touches = maximum_touches
        self.atr_multiplier = atr_multiplier
        self.maximum_swing_distance = maximum_swing_distance
        self.minimum_strength = minimum_strength
        self.touch_weight = touch_weight
        self.strength_weight = strength_weight
        self.atr_consistency_weight = atr_consistency_weight
        self.deviation_weight = deviation_weight
        self.density_weight = density_weight
        self.maximum_score = maximum_score
        self.minimum_score = minimum_score
        self.evidence_weight = evidence_weight
        
    def _build_groups_for_type(self, swings: List[Swing], swing_type: str) -> List[EqualHighGroup]:
        """Build equal-level groups for a given swing type ('HIGH' or 'LOW')."""
        filtered = [s for s in swings if s.type == swing_type and s.confirmed and s.strength >= self.minimum_strength]
        if len(filtered) < self.minimum_touches:
            return []

        # 1. Global sort by price AND index for determinism
        filtered.sort(key=lambda s: (s.price, s.index))

        final_groups = []

        # 2. Global Sliding Price Window (optimized with cap to prevent O(n^3) blowup)
        n = len(filtered)
        # Cap cluster_candidate size to prevent pathological cases (e.g., identical prices)
        max_cluster_size = min(n, self.maximum_touches * 10)
        for i in range(n):
            cluster_candidate = [filtered[i]]
            for j in range(i + 1, min(i + max_cluster_size, n)):
                avg_atr = (filtered[i].atr + filtered[j].atr) / 2
                if (filtered[j].price - filtered[i].price) <= (avg_atr * self.atr_multiplier) or \
                   np.isclose(filtered[j].price, filtered[i].price, atol=avg_atr * self.atr_multiplier):
                    cluster_candidate.append(filtered[j])
                else:
                    break

            if len(cluster_candidate) >= self.minimum_touches:
                cluster_candidate.sort(key=lambda s: s.index)
                k = 0
                while k < len(cluster_candidate):
                    temp_cluster = [cluster_candidate[k]]
                    for l in range(k + 1, len(cluster_candidate)):
                        if cluster_candidate[l].index - cluster_candidate[k].index <= self.maximum_swing_distance:
                            temp_cluster.append(cluster_candidate[l])
                        else:
                            break
                    if len(temp_cluster) >= self.minimum_touches:
                        if len(temp_cluster) > self.maximum_touches:
                            temp_cluster = temp_cluster[-self.maximum_touches:]
                        final_groups.append(EqualHighGroup(
                            touches=list(temp_cluster), 
                            prices=list(s.price for s in temp_cluster),
                            timestamps=list(s.timestamp for s in temp_cluster), 
                            indices=list(s.index for s in temp_cluster),
                            strengths=list(s.strength for s in temp_cluster), 
                            ATRs=list(s.atr for s in temp_cluster)
                        ))
                    k += 1

        # 4. Deterministic Deduplication
        # Sort final_groups for deterministic order before deduplicating
        final_groups.sort(key=lambda g: tuple(sorted(g.indices)))
        
        unique_final_groups = []
        seen_group_ids = set()
        for g in final_groups:
            group_id = tuple(sorted(g.indices))
            if group_id not in seen_group_ids:
                unique_final_groups.append(g)
                seen_group_ids.add(group_id)
        return unique_final_groups

    def build_equal_high_groups(self, swings: List[Swing]) -> List[EqualHighGroup]:
        return self._build_groups_for_type(swings, 'HIGH')

    def build_equal_low_groups(self, swings: List[Swing]) -> List[EqualHighGroup]:
        return self._build_groups_for_type(swings, 'LOW')

    def validate_equal_high_groups(self, groups: List[EqualHighGroup]) -> Tuple[List[EqualHighGroup], List[str]]:
        valid_groups = []
        rejection_reasons = []  
        for g in groups:
            seen_swings = set()
            has_duplicates = False
            for s in g.touches:
                swing_id = (s.index, s.price, s.timestamp)
                if swing_id in seen_swings:
                    has_duplicates = True
                    break
                seen_swings.add(swing_id)
            if has_duplicates:
                rejection_reasons.append("DUPLICATE_SWINGS")
                continue
            if len(g.touches) < self.minimum_touches or len(g.touches) > self.maximum_touches:
                rejection_reasons.append("INVALID_TOUCH_COUNT")
                continue
            if not g.ATRs or np.mean(g.ATRs) <= 0:
                rejection_reasons.append("INVALID_ATR")
                continue
            if not g.strengths or np.mean(g.strengths) < self.minimum_strength:
                rejection_reasons.append("INVALID_STRENGTH")
                continue
            if len(g.indices) < 2 or g.indices[-1] - g.indices[0] <= 0:
                rejection_reasons.append("INVALID_CLUSTER_WIDTH")
                continue
            if any(not ts or not isinstance(ts, str) for ts in g.timestamps):
                rejection_reasons.append("INVALID_TIMESTAMP")
                continue
            if any(idx < 0 for idx in g.indices) or not all(g.indices[i] <= g.indices[i+1] for i in range(len(g.indices)-1)):
                rejection_reasons.append("INVALID_INDEX")
                continue
            valid_groups.append(g)
        return valid_groups, rejection_reasons

    def calculate_metrics(self, groups: List[EqualHighGroup], current_swing_index: int) -> List[EqualHighMetrics]:
        metrics = []
        for g in groups:
            atrs = np.array(g.ATRs)
            atr_mean = np.mean(atrs)
            atr_consistency = np.std(atrs) / atr_mean if atr_mean > 0 else 0.0
            metrics.append(EqualHighMetrics(touch_count=len(g.touches), average_price=float(np.mean(g.prices)), minimum_price=float(min(g.prices)), maximum_price=float(max(g.prices)), price_deviation=float(max(g.prices) - min(g.prices)), average_strength=float(np.mean(g.strengths)), minimum_strength=float(min(g.strengths)), maximum_strength=float(max(g.strengths)), average_ATR=float(atr_mean), ATR_consistency=float(atr_consistency), first_timestamp=g.timestamps[0], last_timestamp=g.timestamps[-1], first_index=g.indices[0], last_index=g.indices[-1], age_in_swings=current_swing_index - g.indices[-1], cluster_width=g.indices[-1] - g.indices[0]))
        return metrics

    def calculate_scores(self, metrics_list: List[EqualHighMetrics]) -> List[EqualHighScore]:
        scores = []
        for m in metrics_list:
            touch_score = min(100.0, (m.touch_count / self.maximum_touches) * 100)
            strength_score = m.average_strength * 100
            atr_score = max(0.0, min(100.0, (1.0 - m.ATR_consistency) * 100))
            epsilon = 1e-9
            # Deviation: normalize by atr_multiplier so high-volatility assets aren't over-penalized
            deviation_score = max(0.0, min(100.0, (1.0 - m.price_deviation / (m.average_ATR * self.atr_multiplier + epsilon)) * 100))
            # Density: use maximum_swing_distance as denominator (robust against age=0)
            density_score = max(0.0, min(100.0, (1.0 - m.cluster_width / (self.maximum_swing_distance + epsilon)) * 100))
            final = (touch_score * self.touch_weight + strength_score * self.strength_weight + atr_score * self.atr_consistency_weight + deviation_score * self.deviation_weight + density_score * self.density_weight)
            final_score = float(max(self.minimum_score, min(self.maximum_score, final)))
            scores.append(EqualHighScore(
                touch_score=float(touch_score), strength_score=float(strength_score), atr_score=float(atr_score), 
                deviation_score=float(deviation_score), density_score=float(density_score), final_score=final_score, 
                touch_count=m.touch_count, average_price=m.average_price, average_strength=m.average_strength, 
                average_ATR=m.average_ATR, age_in_swings=m.age_in_swings, cluster_density=float(density_score / 100.0)
            ))
        return scores

    def select_best_equal_high(self, scores: List[EqualHighScore]) -> Optional[EqualHighScore]:
        if not scores: return None
        return sorted(scores, key=lambda x: (x.final_score, x.touch_count, x.cluster_density, x.average_strength, -x.average_ATR, -x.age_in_swings), reverse=True)[0]
        
    def populate_profile(self, profile: MarketStructureProfile, selected_score: EqualHighScore) -> MarketStructureProfile:
        return replace(profile, equal_highs=True, buy_side_liquidity=selected_score.final_score, liquidity_cluster=selected_score.cluster_density)

    def generate_equal_high_evidence(self, selected_score: EqualHighScore) -> List[Evidence]:
        return [Evidence(
            engine_name="LiquidityEngine",
            evidence_name="Equal High Liquidity",
            direction="BULLISH",
            strength=selected_score.average_strength,
            confidence=selected_score.final_score,
            description=f"Equal High cluster detected: {selected_score.touch_count} touches at {selected_score.average_price:.2f}.",
            weight=self.evidence_weight,
            metadata={
                "touch_count": selected_score.touch_count,
                "average_price": selected_score.average_price,
                "average_strength": selected_score.average_strength,
                "average_ATR": selected_score.average_ATR,
                "age_in_swings": selected_score.age_in_swings,
                "cluster_density": selected_score.cluster_density,
                "final_score": selected_score.final_score
            }
        )]

    def generate_equal_low_evidence(self, selected_score: EqualHighScore) -> List[Evidence]:
        return [Evidence(
            engine_name="LiquidityEngine",
            evidence_name="Equal Low Liquidity",
            direction="BEARISH",
            strength=selected_score.average_strength,
            confidence=selected_score.final_score,
            description=f"Equal Low cluster detected: {selected_score.touch_count} touches at {selected_score.average_price:.2f}.",
            weight=self.evidence_weight,
            metadata={
                "touch_count": selected_score.touch_count,
                "average_price": selected_score.average_price,
                "average_strength": selected_score.average_strength,
                "average_ATR": selected_score.average_ATR,
                "age_in_swings": selected_score.age_in_swings,
                "cluster_density": selected_score.cluster_density,
                "final_score": selected_score.final_score
            }
        )]

    def analyze(self, df: pd.DataFrame, swings: List[Swing], profile: MarketStructureProfile, profiler: Optional[PipelineProfiler] = None) -> LiquidityResult:
        # Fix: use self.executor if available, otherwise create one with profiler
        if self.executor is not None:
            executor = self.executor
        else:
            executor = PipelineExecutor(profiler=profiler)
        
        # Contract Check: Inputs
        if not isinstance(swings, list) or (swings and not isinstance(swings[0], Swing)):
            raise TypeError("Input 'swings' must be a list of Swing objects.")

        current_swing_index = swings[-1].index if swings else 0
        
        # 1 Build Groups (Equal Highs + Equal Lows)
        high_groups = executor.execute("Build High Groups", self.build_equal_high_groups, list, swings)
        low_groups = executor.execute("Build Low Groups", self.build_equal_low_groups, list, swings)
        if not high_groups and not low_groups:
            return LiquidityResult(evidences=(), score=0.0, confidence=0.0, strength=0.0, metadata={})
        
        # 2 Validate Groups
        valid_highs, _ = executor.execute("Validation Highs", self.validate_equal_high_groups, tuple, high_groups) if high_groups else ([], [])
        valid_lows, _ = executor.execute("Validation Lows", self.validate_equal_high_groups, tuple, low_groups) if low_groups else ([], [])
        if not valid_highs and not valid_lows:
            return LiquidityResult(evidences=(), score=0.0, confidence=0.0, strength=0.0, metadata={})
        
        # 3 Build Metrics
        high_metrics = executor.execute("Metrics Highs", self.calculate_metrics, list, valid_highs, current_swing_index) if valid_highs else []
        low_metrics = executor.execute("Metrics Lows", self.calculate_metrics, list, valid_lows, current_swing_index) if valid_lows else []
        
        # 4 Build Scores
        high_scores = executor.execute("Scores Highs", self.calculate_scores, list, high_metrics) if high_metrics else []
        low_scores = executor.execute("Scores Lows", self.calculate_scores, list, low_metrics) if low_metrics else []
        
        # 5 Select Best Group (per type)
        selected_high = executor.execute("Selection Highs", self.select_best_equal_high, (EqualHighScore, type(None)), high_scores) if high_scores else None
        selected_low = executor.execute("Selection Lows", self.select_best_equal_high, (EqualHighScore, type(None)), low_scores) if low_scores else None
        if not selected_high and not selected_low:
            return LiquidityResult(evidences=(), score=0.0, confidence=0.0, strength=0.0, metadata={})
        
        # 6 Generate Evidence (both types)
        all_evidences = []
        best_score = 0.0
        best_strength = 0.0
        best_count = 0
        best_price = 0.0
        if selected_high:
            high_evidences = executor.execute("Evidence Highs", self.generate_equal_high_evidence, list, selected_high)
            all_evidences.extend(high_evidences)
            best_score = max(best_score, selected_high.final_score)
            best_strength = max(best_strength, selected_high.average_strength)
            best_count = max(best_count, selected_high.touch_count)
            best_price = selected_high.average_price
        if selected_low:
            low_evidences = executor.execute("Evidence Lows", self.generate_equal_low_evidence, list, selected_low)
            all_evidences.extend(low_evidences)
            if selected_low.final_score > best_score:
                best_score = selected_low.final_score
                best_strength = selected_low.average_strength
                best_count = selected_low.touch_count
                best_price = selected_low.average_price
        
        # 7 Populate Profile (use best score)
        best_selected = selected_high if (selected_high and (not selected_low or selected_high.final_score >= selected_low.final_score)) else selected_low
        if best_selected:
            new_profile = executor.execute("Profile", self.populate_profile, MarketStructureProfile, profile, best_selected)
        
        # 8 Build LiquidityResult
        return LiquidityResult(
            evidences=tuple(all_evidences),
            score=best_score,
            confidence=best_score / 100.0,
            strength=best_strength,
            metadata={
                "count": best_count, 
                "avg_price": best_price,
                "has_equal_highs": selected_high is not None,
                "has_equal_lows": selected_low is not None,
            }
        )

    def analyze_tuple(self, df: pd.DataFrame, swings: List[Swing], profile: MarketStructureProfile, profiler: Optional[PipelineProfiler] = None) -> Tuple[LiquidityAnalysis, List[Evidence], MarketStructureProfile]:
        # Backward compatibility shim
        res = self.analyze(df, swings, profile, profiler)
        # Fix: set has_equal_highs based on whether evidences were found, not always True
        has_equal_highs = len(res.evidences) > 0
        analysis = LiquidityAnalysis(has_equal_highs=has_equal_highs, 
                                     confidence=res.confidence, 
                                     quality=res.strength, 
                                     evidences=res.evidences)
        # Fix: populate the profile with equal_highs info and return the updated profile
        if has_equal_highs and res.score > 0:
            from mercury_ai.models.market_structure_profile import MarketStructureProfile as MSP
            from dataclasses import replace as dc_replace
            new_profile = dc_replace(profile, equal_highs=True, buy_side_liquidity=res.score, liquidity_cluster=res.strength)
            return analysis, list(res.evidences), new_profile
        return analysis, list(res.evidences), profile
