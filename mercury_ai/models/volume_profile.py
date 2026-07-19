from dataclasses import dataclass

@dataclass(frozen=True)
class VolumeProfile:
    relative_volume: float = 1.0
    volume_spike: bool = False
    buying_climax: bool = False
    selling_climax: bool = False
    absorption: bool = False
    effort_vs_result: float = 0.0
    dry_volume: bool = False
    trend_confirmation: bool = False
    volume_divergence: bool = False
    institutional_participation: float = 0.0
    confidence_score: float = 0.0
    participation_quality: float = 0.0
    volume_consistency: float = 0.0
    exhaustion_volume: bool = False
