import logging
from pathlib import Path
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from models import StartupProfile, TechnicalFeasibility, RiskAssessment, RiskAssessmentItem
from chains.utils import try_recover_pydantic_from_error

logger = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "risk_analysis_prompt.txt"

def run_risk_analysis(profile: StartupProfile, tech: TechnicalFeasibility, llm: Optional[object] = None) -> RiskAssessment:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    prompt_template = ChatPromptTemplate.from_template(prompt_text)

    if llm:
        try:
            try:
                structured_llm = llm.with_structured_output(RiskAssessment)
                chain = prompt_template | structured_llm
                res = chain.invoke({
                    "startup_profile": profile.model_dump_json(),
                    "technical_feasibility": tech.model_dump_json()
                })
            except Exception:
                structured_llm = llm.with_structured_output(RiskAssessment, method="json_mode")
                chain = prompt_template | structured_llm
                res = chain.invoke({
                    "startup_profile": profile.model_dump_json(),
                    "technical_feasibility": tech.model_dump_json()
                })
            if res and isinstance(res, RiskAssessment):
                return res
        except Exception as e:
            recovered = try_recover_pydantic_from_error(e, RiskAssessment)
            if recovered:
                return recovered
            logger.warning("Risk assessment LLM analysis failed; using fallback: %s", e)

    concept_lower = profile.concept.lower()
    risks = []
    
    if "interview" in concept_lower:
        risks = [
            RiskAssessmentItem(
                risk="High dependence on third-party LLM APIs for live interview evaluation",
                category="Dependency Risk",
                potential_impact="Operating costs may escalate rapidly as user volume and session length increase.",
                likelihood="High",
                suggested_mitigation="Implement prompt optimization, response caching, semantic compression, and routing simpler evaluation tasks to lower-cost open models."
            ),
            RiskAssessmentItem(
                risk="User skepticism regarding AI feedback credibility compared to human interviewers",
                category="Adoption Risk",
                potential_impact="Lower conversion rates from free mock sessions to paid subscriptions.",
                likelihood="Medium",
                suggested_mitigation="Benchmark AI feedback against official industry hiring rubrics and feature transparent scoring justifications."
            ),
            RiskAssessmentItem(
                risk="Seasonal demand fluctuation aligned with college placement cycles",
                category="Market Risk",
                potential_impact="Unpredictable monthly recurring revenue and severe off-season user churn.",
                likelihood="High",
                suggested_mitigation="Diversify into year-round enterprise B2B hiring assessment licensing and continuous skill improvement modules."
            ),
            RiskAssessmentItem(
                risk="Latency spikes during audio-to-text and AI evaluation streaming",
                category="Technical Risk",
                potential_impact="Degraded user experience during live interview practice.",
                likelihood="Medium",
                suggested_mitigation="Deploy WebSocket streaming with local audio buffering and edge-deployed speech recognition services."
            )
        ]
        summary = "Primary risks stem from API cost dependencies and seasonal demand cycles. Mitigations prioritize architectural cost controls and enterprise expansion."
    elif "invoice" in concept_lower:
        risks = [
            RiskAssessmentItem(
                risk="Inaccurate data extraction on complex or non-standard invoice formats",
                category="Product Risk",
                potential_impact="Financial discrepancies requiring manual correction, eroding customer trust.",
                likelihood="Medium",
                suggested_mitigation="Implement a human-in-the-loop review threshold for low-confidence extractions."
            ),
            RiskAssessmentItem(
                risk="Financial data privacy and security compliance liabilities",
                category="Security/Privacy Risk",
                potential_impact="Severe legal liabilities or customer loss in case of data breaches.",
                likelihood="Medium",
                suggested_mitigation="Enforce SOC2 compliance, end-to-end encryption, and zero-data-retention agreements with LLM vendors."
            ),
            RiskAssessmentItem(
                risk="High competition from incumbent accounting software adding native AI features",
                category="Competitive Risk",
                potential_impact="Decreased market share and pricing pressure.",
                likelihood="High",
                suggested_mitigation="Focus on deep custom workflow integrations and specialized multi-ERP synchronization."
            )
        ]
        summary = "Key risks involve data accuracy and incumbent competition. Mitigations emphasize security compliance and human-in-the-loop verification."
    else:
        risks = [
            RiskAssessmentItem(
                risk="Uncertain customer willingness to pay at projected price points",
                category="Financial Risk",
                potential_impact="Revenue shortfall and slow cash flow generation.",
                likelihood="Medium",
                suggested_mitigation="Run early pricing tests and offer limited pilot offerings to establish willingness to pay."
            ),
            RiskAssessmentItem(
                risk="Third-party AI service API dependency and price adjustments",
                category="Dependency Risk",
                potential_impact="Margin compression as usage scales.",
                likelihood="Medium",
                suggested_mitigation="Maintain model-agnostic architecture allowing seamless switching between LLM providers."
            ),
            RiskAssessmentItem(
                risk="Customer acquisition friction due to low brand awareness",
                category="Market Risk",
                potential_impact="Higher acquisition costs delaying profitability.",
                likelihood="High",
                suggested_mitigation="Leverage targeted organic marketing, community partnerships, and referral incentives."
            )
        ]
        summary = "Risks are focused around unit economics and market adoption. Mitigations prioritize lean validation and model-agnostic design."

    return RiskAssessment(risks=risks, overall_risk_summary=summary)
