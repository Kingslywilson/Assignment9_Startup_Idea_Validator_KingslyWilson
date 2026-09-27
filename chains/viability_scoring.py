from typing import Optional
from models import (
    StartupProfile, SWOTAnalysis, MarketOpportunity,
    TechnicalFeasibility, RiskAssessment, ViabilityScoreBreakdown
)
from scoring import calculate_viability_score

def run_viability_scoring(
    profile: StartupProfile,
    swot: SWOTAnalysis,
    market: MarketOpportunity,
    tech: TechnicalFeasibility,
    risk: RiskAssessment,
    llm: Optional[object] = None
) -> ViabilityScoreBreakdown:
    return calculate_viability_score(profile, swot, market, tech, risk)
