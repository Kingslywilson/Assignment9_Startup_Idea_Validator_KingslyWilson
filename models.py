from typing import List, Optional, Any
from pydantic import BaseModel, Field, field_validator

def _coerce_str(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        parts = [f"{k.replace('_', ' ').title()}: {val}" for k, val in v.items() if val]
        return "; ".join(parts)
    if isinstance(v, list):
        return ", ".join([_coerce_str(x) for x in v])
    return str(v)

def _coerce_list_of_strings(v: Any) -> List[str]:
    if v is None:
        return []
    if isinstance(v, list):
        res = []
        for item in v:
            if isinstance(item, str):
                res.append(item)
            elif isinstance(item, dict):
                values = [_coerce_str(val) for val in item.values() if val]
                if values:
                    res.append(" - ".join(values))
            else:
                res.append(str(item))
        return res
    if isinstance(v, str):
        return [v]
    if isinstance(v, dict):
        return [f"{k}: {val}" for k, val in v.items()]
    return []

class StartupProfile(BaseModel):
    idea_raw: str = Field(default="", description="Original user startup idea")
    is_valid: bool = Field(default=True, description="Whether the idea input is valid")
    rejection_reason: Optional[str] = Field(default=None, description="Reason if input is rejected")
    concept: str = Field(default="", description="Summary of startup/product concept")
    target_audience_explicit: Optional[List[str]] = Field(default_factory=list, description="Explicitly stated audience")
    target_audience_assumptions: Optional[List[str]] = Field(default_factory=list, description="Assumed audience segments")
    problem_statement: str = Field(default="", description="Clear problem statement detailing who, what, why", alias="problem")
    proposed_solution: str = Field(default="", description="Summary of proposed solution", alias="solution")
    provided_revenue_model: Optional[List[str]] = Field(default_factory=list, description="Explicitly provided revenue mechanisms")
    suggested_revenue_models: Optional[List[str]] = Field(default_factory=list, description="AI suggested revenue models")
    known_competitors: Optional[List[str]] = Field(default_factory=list, description="Stated or known competitors")
    potential_competitors_alternatives: Optional[List[str]] = Field(default_factory=list, description="Potential competitors or alternative solutions")
    missing_information: Optional[List[str]] = Field(default_factory=list, description="Key unstated details", alias="missing_details")

    model_config = {
        "populate_by_name": True
    }

    @field_validator(
        "concept", "problem_statement", "proposed_solution",
        "idea_raw", "rejection_reason", mode="before"
    )
    @classmethod
    def string_coercion(cls, v):
        return _coerce_str(v)

    @field_validator(
        "target_audience_explicit", "target_audience_assumptions",
        "provided_revenue_model", "suggested_revenue_models",
        "known_competitors", "potential_competitors_alternatives",
        "missing_information", mode="before"
    )
    @classmethod
    def list_coercion(cls, v):
        return _coerce_list_of_strings(v)

class SWOTAnalysis(BaseModel):
    strengths: Optional[List[str]] = Field(default_factory=list)
    weaknesses: Optional[List[str]] = Field(default_factory=list)
    opportunities: Optional[List[str]] = Field(default_factory=list)
    threats: Optional[List[str]] = Field(default_factory=list)

    model_config = {
        "populate_by_name": True
    }

    @field_validator("strengths", "weaknesses", "opportunities", "threats", mode="before")
    @classmethod
    def list_coercion(cls, v):
        return _coerce_list_of_strings(v)

class MarketOpportunity(BaseModel):
    customer_need_analysis: str = Field(default="", alias="customer_need")
    target_segment_evaluation: str = Field(default="", alias="target_segment")
    adoption_potential: str = Field(default="")
    problem_frequency: str = Field(default="")
    differentiation_opportunity: str = Field(default="", alias="differentiation")
    scalability_assessment: str = Field(default="", alias="scalability")
    market_summary: str = Field(default="", alias="summary")

    model_config = {
        "populate_by_name": True
    }

    @field_validator(
        "customer_need_analysis", "target_segment_evaluation", "adoption_potential",
        "problem_frequency", "differentiation_opportunity", "scalability_assessment",
        "market_summary", mode="before"
    )
    @classmethod
    def string_coercion(cls, v):
        return _coerce_str(v)

class TechnicalFeasibility(BaseModel):
    feasibility_rating: str = Field(default="Moderate", alias="rating")
    reasoning: str = Field(default="")
    core_technical_requirements: Optional[List[str]] = Field(default_factory=list, alias="technical_requirements")
    architecture_complexity: str = Field(default="Moderate")
    ai_ml_requirements: Optional[List[str]] = Field(default_factory=list, alias="ai_requirements")
    external_api_dependencies: Optional[List[str]] = Field(default_factory=list, alias="api_dependencies")
    infrastructure_and_scalability: str = Field(default="", alias="infrastructure")
    suggested_architecture: Optional[List[str]] = Field(default_factory=list, alias="architecture")

    model_config = {
        "populate_by_name": True
    }

    @field_validator(
        "feasibility_rating", "reasoning", "architecture_complexity",
        "infrastructure_and_scalability", mode="before"
    )
    @classmethod
    def string_coercion(cls, v):
        return _coerce_str(v)

    @field_validator(
        "core_technical_requirements", "ai_ml_requirements",
        "external_api_dependencies", "suggested_architecture", mode="before"
    )
    @classmethod
    def list_coercion(cls, v):
        return _coerce_list_of_strings(v)

class RiskAssessmentItem(BaseModel):
    risk: str = Field(default="Unspecified Risk", alias="description")
    category: str = Field(default="General Risk")
    potential_impact: str = Field(default="Moderate operational impact", alias="impact")
    likelihood: str = Field(default="Medium")
    suggested_mitigation: str = Field(default="Monitor and apply standard risk controls.", alias="mitigation")

    model_config = {
        "populate_by_name": True
    }

    @field_validator("risk", "category", "potential_impact", "likelihood", "suggested_mitigation", mode="before")
    @classmethod
    def string_coercion(cls, v):
        return _coerce_str(v)

class RiskAssessment(BaseModel):
    risks: Optional[List[RiskAssessmentItem]] = Field(default_factory=list, alias="risk_assessment")
    overall_risk_summary: str = Field(
        default="Overall risk profile requires structured mitigation across technical, financial, and operational vectors.",
        alias="summary"
    )

    model_config = {
        "populate_by_name": True
    }

    @field_validator("overall_risk_summary", mode="before")
    @classmethod
    def string_coercion(cls, v):
        return _coerce_str(v)

class InvestorQuestion(BaseModel):
    category: str = Field(default="General")
    question: str = Field(default="")
    context_rationale: str = Field(default="Validates strategic considerations.", alias="rationale")

    model_config = {
        "populate_by_name": True
    }

    @field_validator("category", "question", "context_rationale", mode="before")
    @classmethod
    def string_coercion(cls, v):
        return _coerce_str(v)

class InvestorQuestions(BaseModel):
    questions: Optional[List[InvestorQuestion]] = Field(default_factory=list)

    model_config = {
        "populate_by_name": True
    }

class ViabilityScoreBreakdown(BaseModel):
    problem_clarity: float = Field(default=10.0, ge=0, le=15)
    customer_need: float = Field(default=10.0, ge=0, le=15)
    market_opportunity: float = Field(default=10.0, ge=0, le=15)
    differentiation: float = Field(default=10.0, ge=0, le=15)
    revenue_model: float = Field(default=7.0, ge=0, le=10)
    technical_feasibility: float = Field(default=8.0, ge=0, le=10)
    scalability: float = Field(default=7.0, ge=0, le=10)
    risk_profile: float = Field(default=7.0, ge=0, le=10)
    overall_viability_score: float = Field(default=70.0, ge=0, le=100)
    scoring_explanation: str = Field(default="")

class GTMStrategy(BaseModel):
    initial_customer_segment: str = Field(
        default="Target early adopters seeking modern digital workflows.",
        alias="target_initial_customer_segment"
    )
    positioning: str = Field(
        default="AI-powered solution delivering operational efficiency.",
        alias="positioning_statement"
    )
    acquisition_channels: Optional[List[str]] = Field(default_factory=list, alias="channels")
    pilot_strategy: str = Field(
        default="Run targeted 30-day pilot with early adopter cohort.",
        alias="pilot"
    )
    pricing_approach: str = Field(
        default="Freemium with tiered paid subscription.",
        alias="pricing"
    )
    partnerships: Optional[List[str]] = Field(
        default_factory=list,
        alias="strategic_partnerships"
    )
    validation_metrics: Optional[List[str]] = Field(default_factory=list, alias="metrics")
    expansion_strategy: str = Field(
        default="Expand into adjacent verticals and institutional tiers.",
        alias="expansion"
    )

    model_config = {
        "populate_by_name": True
    }

    @field_validator(
        "initial_customer_segment", "positioning", "pilot_strategy",
        "pricing_approach", "expansion_strategy", mode="before"
    )
    @classmethod
    def string_coercion(cls, v):
        return _coerce_str(v)

    @field_validator("acquisition_channels", "partnerships", "validation_metrics", mode="before")
    @classmethod
    def list_coercion(cls, v):
        return _coerce_list_of_strings(v)

class ValidationReport(BaseModel):
    startup_profile: StartupProfile
    swot_analysis: SWOTAnalysis
    market_opportunity: MarketOpportunity
    technical_feasibility: TechnicalFeasibility
    risk_assessment: RiskAssessment
    investor_questions: InvestorQuestions
    viability_score: ViabilityScoreBreakdown
    improvement_suggestions: Optional[List[str]] = Field(default_factory=list)
    gtm_strategy: GTMStrategy
    critical_assumptions: Optional[List[str]] = Field(default_factory=list)
    validation_summary: str = Field(default="")
    recommended_next_step: str = Field(default="")

    @field_validator("improvement_suggestions", "critical_assumptions", mode="before")
    @classmethod
    def list_coercion(cls, v):
        return _coerce_list_of_strings(v)

    @field_validator("validation_summary", "recommended_next_step", mode="before")
    @classmethod
    def string_coercion(cls, v):
        return _coerce_str(v)
