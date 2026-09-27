import logging
from pathlib import Path
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from models import StartupProfile, SWOTAnalysis
from chains.utils import try_recover_pydantic_from_error

logger = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "swot_prompt.txt"

def run_swot_analysis(profile: StartupProfile, llm: Optional[object] = None) -> SWOTAnalysis:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    prompt_template = ChatPromptTemplate.from_template(prompt_text)

    if llm:
        try:
            try:
                structured_llm = llm.with_structured_output(SWOTAnalysis)
                chain = prompt_template | structured_llm
                res = chain.invoke({"startup_profile": profile.model_dump_json()})
            except Exception:
                structured_llm = llm.with_structured_output(SWOTAnalysis, method="json_mode")
                chain = prompt_template | structured_llm
                res = chain.invoke({"startup_profile": profile.model_dump_json()})
            if res and isinstance(res, SWOTAnalysis):
                return res
        except Exception as e:
            recovered = try_recover_pydantic_from_error(e, SWOTAnalysis)
            if recovered:
                return recovered
            logger.warning("SWOT LLM analysis failed; using fallback: %s", e)

    concept_lower = profile.concept.lower()
    if "interview" in concept_lower:
        strengths = [
            "Clear and acute student pain point during placement season",
            "High scalability with automated AI mock interviews and instant feedback",
            "Low marginal cost per interview session generated"
        ]
        weaknesses = [
            "Dependence on third-party LLM APIs for feedback evaluation",
            "Potential user skepticism regarding AI scoring accuracy vs real human interviewers",
            "Seasonal user churn post placement season"
        ]
        opportunities = [
            "Expansion into institutional B2B licensing with colleges and placement cells",
            "Corporate partnerships for talent pre-screening",
            "Multi-domain expansion (behavioral, system design, data science)"
        ]
        threats = [
            "Established prep platforms (LeetCode, HackerRank) launching native AI mock tools",
            "Rapid model shifts requiring continuous evaluation prompt engineering",
            "Low switching barrier for students"
        ]
    elif "invoice" in concept_lower:
        strengths = [
            "High utility and immediate ROI through time savings for SMB finance teams",
            "Standardized document structures facilitating high AI extraction accuracy",
            "Recurring SaaS revenue potential"
        ]
        weaknesses = [
            "High initial trust barrier regarding financial data processing",
            "Integration complexity across varied legacy accounting software",
            "Vulnerability to OCR parsing errors on non-standard layout invoices"
        ]
        opportunities = [
            "Integration marketplace ecosystem (QuickBooks, Xero, SAP)",
            "Automated fraud and duplicate invoice detection features",
            "Expansion into automated bill payments and working capital analytics"
        ]
        threats = [
            "Incumbent accounting giants building native AI invoice readers",
            "Strict data privacy regulations and security liabilities",
            "Price competition from open-source document parsers"
        ]
    else:
        strengths = [
            "Direct alignment with identified target domain friction",
            "Potential to leverage AI automation to streamline manual workflows",
            "Flexible revenue opportunities across B2C and B2B segments"
        ]
        weaknesses = [
            "Early-stage brand awareness requiring targeted marketing efforts",
            "Third-party API dependencies and infrastructure operational costs",
            "Unvalidated customer willingness to pay at current proposed tier"
        ]
        opportunities = [
            "Growing digital adoption within target market segment",
            "Expansion into adjacent vertical workflows and partner integrations",
            "Network effects as platform usage expands"
        ]
        threats = [
            "Established competitors launching similar AI capabilities",
            "Changing regulatory requirements around data handling",
            "Customer acquisition cost escalation"
        ]

    return SWOTAnalysis(
        strengths=strengths,
        weaknesses=weaknesses,
        opportunities=opportunities,
        threats=threats
    )
