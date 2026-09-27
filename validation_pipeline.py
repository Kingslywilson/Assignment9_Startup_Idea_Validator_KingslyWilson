import os
import json
import logging
from typing import Optional, Tuple
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

from models import ValidationReport, StartupProfile, SWOTAnalysis, MarketOpportunity, TechnicalFeasibility, RiskAssessment, InvestorQuestions, ViabilityScoreBreakdown, GTMStrategy

from chains.idea_analysis import run_idea_analysis
from chains.swot_analysis import run_swot_analysis
from chains.market_analysis import run_market_analysis
from chains.technical_feasibility import run_technical_feasibility
from chains.risk_analysis import run_risk_analysis
from chains.investor_questions import run_investor_questions
from chains.viability_scoring import run_viability_scoring
from chains.gtm_strategy import run_gtm_strategy
from chains.report_generator import run_report_generator

def get_llm():
    load_dotenv()
    groq_key = os.getenv("GROQ_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if groq_key:
        try:
            from langchain_groq import ChatGroq
            return ChatGroq(model_name="openai/gpt-oss-20b", temperature=0.2, api_key=groq_key)
        except Exception as e:
            logger.warning("Failed to initialize ChatGroq: %s", e)

    return None

def execute_validation_pipeline(idea: str) -> ValidationReport:
    llm = get_llm()
    
    profile = run_idea_analysis(idea, llm=llm)
    if not profile.is_valid:
        empty_swot = SWOTAnalysis()
        empty_market = MarketOpportunity(
            customer_need_analysis="N/A", target_segment_evaluation="N/A",
            adoption_potential="N/A", problem_frequency="N/A",
            differentiation_opportunity="N/A", scalability_assessment="N/A",
            market_summary="Input idea rejected. Business analysis not applicable."
        )
        empty_tech = TechnicalFeasibility(
            feasibility_rating="N/A", reasoning=profile.rejection_reason or "Invalid input",
            core_technical_requirements=[], architecture_complexity="N/A",
            ai_ml_requirements=[], external_api_dependencies=[],
            infrastructure_and_scalability="N/A", suggested_architecture=[]
        )
        empty_risk = RiskAssessment(risks=[], overall_risk_summary="N/A")
        empty_questions = InvestorQuestions(questions=[])
        zero_score = ViabilityScoreBreakdown(
            problem_clarity=0, customer_need=0, market_opportunity=0,
            differentiation=0, revenue_model=0, technical_feasibility=0,
            scalability=0, risk_profile=0, overall_viability_score=0,
            scoring_explanation=f"Rejection: {profile.rejection_reason}"
        )
        empty_gtm = GTMStrategy(
            initial_customer_segment="N/A", positioning="N/A", acquisition_channels=[],
            pilot_strategy="N/A", pricing_approach="N/A", partnerships=[],
            validation_metrics=[], expansion_strategy="N/A"
        )
        return ValidationReport(
            startup_profile=profile,
            swot_analysis=empty_swot,
            market_opportunity=empty_market,
            technical_feasibility=empty_tech,
            risk_assessment=empty_risk,
            investor_questions=empty_questions,
            viability_score=zero_score,
            improvement_suggestions=["Provide a clear, detailed startup description."],
            gtm_strategy=empty_gtm,
            critical_assumptions=["N/A"],
            validation_summary=f"Input Rejected: {profile.rejection_reason}",
            recommended_next_step="Resubmit with a meaningful startup concept description."
        )

    swot = run_swot_analysis(profile, llm=llm)
    market = run_market_analysis(profile, swot, llm=llm)
    tech = run_technical_feasibility(profile, llm=llm)
    risk = run_risk_analysis(profile, tech, llm=llm)
    questions = run_investor_questions(profile, risk, llm=llm)
    score = run_viability_scoring(profile, swot, market, tech, risk, llm=llm)
    gtm = run_gtm_strategy(profile, market, llm=llm)
    rep_meta = run_report_generator(profile, swot, risk, score, llm=llm)

    return ValidationReport(
        startup_profile=profile,
        swot_analysis=swot,
        market_opportunity=market,
        technical_feasibility=tech,
        risk_assessment=risk,
        investor_questions=questions,
        viability_score=score,
        improvement_suggestions=rep_meta.get("improvement_suggestions", []),
        gtm_strategy=gtm,
        critical_assumptions=rep_meta.get("critical_assumptions", []),
        validation_summary=rep_meta.get("validation_summary", ""),
        recommended_next_step=rep_meta.get("recommended_next_step", "")
    )

def generate_markdown_report(report: ValidationReport) -> str:
    p = report.startup_profile
    s = report.swot_analysis
    m = report.market_opportunity
    t = report.technical_feasibility
    r = report.risk_assessment
    q = report.investor_questions
    v = report.viability_score
    g = report.gtm_strategy

    md = []
    md.append("# 🚀 AI Startup Idea Validation Report")
    md.append("")
    md.append("## 📌 1. Business Profile Extraction")
    md.append(f"**Startup / Product Concept:** {p.concept}")
    md.append("")
    md.append("### Target Audience")
    if p.target_audience_explicit:
        md.append("**Explicitly Stated Audience:**")
        for item in p.target_audience_explicit:
            md.append(f"- {item}")
    if p.target_audience_assumptions:
        md.append("**AI-Generated Assumptions:**")
        for item in p.target_audience_assumptions:
            md.append(f"- *[Assumption]* {item}")
    md.append("")
    md.append(f"**Problem Statement:** {p.problem_statement}")
    md.append(f"**Proposed Solution:** {p.proposed_solution}")
    md.append("")
    md.append("### Revenue Model Analysis")
    if p.provided_revenue_model:
        md.append("**Provided Revenue Model:**")
        for item in p.provided_revenue_model:
            md.append(f"- {item}")
    if p.suggested_revenue_models:
        md.append("**Suggested Revenue Models (Recommendations):**")
        for item in p.suggested_revenue_models:
            md.append(f"- *[Recommendation]* {item}")
    md.append("")
    md.append("### Competition Analysis")
    if p.known_competitors:
        md.append("**Known Competitors:**")
        for item in p.known_competitors:
            md.append(f"- {item}")
    if p.potential_competitors_alternatives:
        md.append("**Potential Competitors / Alternatives:**")
        for item in p.potential_competitors_alternatives:
            md.append(f"- *[Potential Competitor/Alternative]* {item}")
    if p.missing_information:
        md.append("")
        md.append("**Missing Information Identified:**")
        for item in p.missing_information:
            md.append(f"- {item}")

    md.append("")
    md.append("## 📊 2. SWOT Analysis")
    md.append("### Strengths")
    for item in s.strengths:
        md.append(f"- {item}")
    md.append("### Weaknesses")
    for item in s.weaknesses:
        md.append(f"- {item}")
    md.append("### Opportunities")
    for item in s.opportunities:
        md.append(f"- {item}")
    md.append("### Threats")
    for item in s.threats:
        md.append(f"- {item}")

    md.append("")
    md.append("## 📈 3. Market Opportunity Analysis")
    md.append(f"- **Customer Need:** {m.customer_need_analysis}")
    md.append(f"- **Target Segment Evaluation:** {m.target_segment_evaluation}")
    md.append(f"- **Adoption Potential:** {m.adoption_potential}")
    md.append(f"- **Problem Frequency:** {m.problem_frequency}")
    md.append(f"- **Differentiation Opportunity:** {m.differentiation_opportunity}")
    md.append(f"- **Scalability Assessment:** {m.scalability_assessment}")
    md.append(f"- **Market Summary:** {m.market_summary}")

    md.append("")
    md.append("## 🛠️ 4. Technical Feasibility & Architecture")
    md.append(f"**Feasibility Rating:** `{t.feasibility_rating}`")
    md.append(f"**Reasoning:** {t.reasoning}")
    md.append("### Core Technical Requirements")
    for item in t.core_technical_requirements:
        md.append(f"- {item}")
    md.append(f"**Architecture Complexity:** {t.architecture_complexity}")
    md.append("### AI/ML Requirements")
    for item in t.ai_ml_requirements:
        md.append(f"- {item}")
    md.append("### External API Dependencies")
    for item in t.external_api_dependencies:
        md.append(f"- {item}")
    md.append("### Suggested System Architecture")
    for step in t.suggested_architecture:
        md.append(f"- {step}")

    md.append("")
    md.append("## ⚠️ 5. Risk Assessment & Mitigations")
    md.append(f"**Overall Risk Summary:** {r.overall_risk_summary}")
    md.append("")
    for item in r.risks:
        md.append(f"### Risk: {item.risk}")
        md.append(f"- **Category:** {item.category}")
        md.append(f"- **Potential Impact:** {item.potential_impact}")
        md.append(f"- **Likelihood:** {item.likelihood}")
        md.append(f"- **Suggested Mitigation:** {item.suggested_mitigation}")
        md.append("")

    md.append("## ❓ 6. Investor Question Generator")
    for item in q.questions:
        md.append(f"- **[{item.category}]** {item.question}")
        md.append(f"  *Context:* {item.context_rationale}")

    md.append("")
    md.append("## 💯 7. Startup Viability Score & Breakdown")
    md.append(f"### **Overall Startup Viability Score: {v.overall_viability_score} / 100**")
    md.append("")
    md.append("| Evaluation Criteria | Score | Max Weight |")
    md.append("|---|---|---|")
    md.append(f"| Problem Clarity | {v.problem_clarity} | 15% |")
    md.append(f"| Customer Need | {v.customer_need} | 15% |")
    md.append(f"| Market Opportunity | {v.market_opportunity} | 15% |")
    md.append(f"| Differentiation | {v.differentiation} | 15% |")
    md.append(f"| Revenue Model | {v.revenue_model} | 10% |")
    md.append(f"| Technical Feasibility | {v.technical_feasibility} | 10% |")
    md.append(f"| Scalability | {v.scalability} | 10% |")
    md.append(f"| Risk Profile | {v.risk_profile} | 10% |")
    md.append("")
    md.append(f"**Explanation:** {v.scoring_explanation}")

    md.append("")
    md.append("## 🎯 8. Go-To-Market (GTM) Strategy")
    md.append(f"- **Initial Customer Segment:** {g.initial_customer_segment}")
    md.append(f"- **Positioning:** {g.positioning}")
    md.append("- **Acquisition Channels:**")
    for c in g.acquisition_channels:
        md.append(f"  - {c}")
    md.append(f"- **Pilot Strategy:** {g.pilot_strategy}")
    md.append(f"- **Pricing Approach:** {g.pricing_approach}")
    md.append("- **Partnerships:**")
    for part in g.partnerships:
        md.append(f"  - {part}")
    md.append("- **Validation Metrics:**")
    for vm in g.validation_metrics:
        md.append(f"  - {vm}")
    md.append(f"- **Expansion Strategy:** {g.expansion_strategy}")

    md.append("")
    md.append("## 💡 9. Recommendations & Validation Summary")
    md.append("### Improvement Suggestions")
    for item in report.improvement_suggestions:
        md.append(f"- {item}")
    md.append("")
    md.append("### Critical Assumptions to Validate")
    for item in report.critical_assumptions:
        md.append(f"- *[Assumption]* {item}")
    md.append("")
    md.append(f"### Final Validation Summary\n{report.validation_summary}")
    md.append("")
    md.append(f"### Recommended Next Step\n{report.recommended_next_step}")

    return "\n".join(md)
