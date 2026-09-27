from models import ViabilityScoreBreakdown, StartupProfile, SWOTAnalysis, MarketOpportunity, TechnicalFeasibility, RiskAssessment

def calculate_viability_score(
    profile: StartupProfile,
    swot: SWOTAnalysis,
    market: MarketOpportunity,
    tech: TechnicalFeasibility,
    risk: RiskAssessment
) -> ViabilityScoreBreakdown:
    problem_clarity = 15.0 if len(profile.problem_statement) > 40 and profile.is_valid else (8.0 if profile.is_valid else 0.0)
    
    if profile.target_audience_explicit:
        customer_need = 14.0
    elif profile.target_audience_assumptions:
        customer_need = 10.0
    else:
        customer_need = 5.0
        
    if "high" in market.market_summary.lower() or "strong" in market.market_summary.lower():
        market_opp = 13.5
    elif "moderate" in market.market_summary.lower():
        market_opp = 11.0
    else:
        market_opp = 8.0

    if len(swot.strengths) >= 3 and len(profile.known_competitors) > 0:
        differentiation = 12.5
    elif len(swot.strengths) >= 2:
        differentiation = 9.5
    else:
        differentiation = 6.0

    if profile.provided_revenue_model:
        revenue_model = 9.0
    elif profile.suggested_revenue_models:
        revenue_model = 7.0
    else:
        revenue_model = 4.0

    rating_lower = tech.feasibility_rating.lower()
    if "high" in rating_lower and "moderate" not in rating_lower:
        tech_feat = 9.5
    elif "moderate" in rating_lower:
        tech_feat = 8.0
    else:
        tech_feat = 5.0

    if "high" in market.scalability_assessment.lower() or "scalable" in market.scalability_assessment.lower():
        scalability = 8.5
    else:
        scalability = 6.5

    risk_count = len(risk.risks)
    high_risks = sum(1 for r in risk.risks if r.likelihood.lower() == "high")
    if high_risks >= 3:
        risk_profile = 4.0
    elif high_risks >= 1 or risk_count >= 4:
        risk_profile = 6.5
    else:
        risk_profile = 8.5

    total_score = round(
        problem_clarity + customer_need + market_opp + differentiation + revenue_model + tech_feat + scalability + risk_profile,
        1
    )
    total_score = min(100.0, max(0.0, total_score))

    explanation = (
        f"Viability score is {total_score}/100. Breakdown: Problem Clarity ({problem_clarity}/15), "
        f"Customer Need ({customer_need}/15), Market Opportunity ({market_opp}/15), "
        f"Differentiation ({differentiation}/15), Revenue Model ({revenue_model}/10), "
        f"Technical Feasibility ({tech_feat}/10), Scalability ({scalability}/10), "
        f"Risk Profile ({risk_profile}/10)."
    )

    return ViabilityScoreBreakdown(
        problem_clarity=problem_clarity,
        customer_need=customer_need,
        market_opportunity=market_opp,
        differentiation=differentiation,
        revenue_model=revenue_model,
        technical_feasibility=tech_feat,
        scalability=scalability,
        risk_profile=risk_profile,
        overall_viability_score=total_score,
        scoring_explanation=explanation
    )
