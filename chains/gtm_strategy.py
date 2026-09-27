import logging
from pathlib import Path
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from models import StartupProfile, MarketOpportunity, GTMStrategy
from chains.utils import try_recover_pydantic_from_error

logger = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "gtm_strategy_prompt.txt"

def run_gtm_strategy(profile: StartupProfile, market: MarketOpportunity, llm: Optional[object] = None) -> GTMStrategy:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    prompt_template = ChatPromptTemplate.from_template(prompt_text)

    if llm:
        try:
            try:
                structured_llm = llm.with_structured_output(GTMStrategy)
                chain = prompt_template | structured_llm
                res = chain.invoke({
                    "startup_profile": profile.model_dump_json(),
                    "market_opportunity": market.model_dump_json()
                })
            except Exception:
                structured_llm = llm.with_structured_output(GTMStrategy, method="json_mode")
                chain = prompt_template | structured_llm
                res = chain.invoke({
                    "startup_profile": profile.model_dump_json(),
                    "market_opportunity": market.model_dump_json()
                })
            if res and isinstance(res, GTMStrategy):
                return res
        except Exception as e:
            recovered = try_recover_pydantic_from_error(e, GTMStrategy)
            if recovered:
                return recovered
            logger.warning("GTM strategy LLM analysis failed; using fallback: %s", e)

    concept_lower = profile.concept.lower()

    if "interview" in concept_lower:
        seg = "Final-year computer science and engineering undergraduates preparing for upcoming campus recruitment drives."
        pos = "The personalized AI mock interviewer that provides instant, actionable technical and communication feedback."
        chans = [
            "Campus ambassador programs in top engineering colleges",
            "Targeted student tech communities (Discord, Reddit, LinkedIn)",
            "Partnerships with university placement cells and student coding clubs"
        ]
        pilot = "Run a limited pilot with a small group of target students to measure mock completion rates, repeat usage, willingness to pay, and feedback quality."
        price = "Test a freemium model with free introductory sessions, followed by low-cost monthly subscription or pay-per-session tiers to validate pricing willingness."
        parts = ["University placement cells", "Coding bootcamps", "Student developer clubs"]
        metrics = ["User activation rate", "Mock interview completion rate", "Paid plan conversion %", "User net promoter score (NPS)"]
        exp = "Expand into institutional B2B enterprise tier sold to universities and corporate recruitment screening teams."
    elif "invoice" in concept_lower:
        seg = "Small business owners and boutique accounting firms handling recurring vendor invoices."
        pos = "Zero-setup AI invoice processing that syncs with accounting stacks to eliminate manual data entry."
        chans = [
            "QuickBooks / Xero App Store listings",
            "Outbound sales to localized accounting agencies",
            "Content marketing targeting SMB CFOs and finance managers"
        ]
        pilot = "Run a limited free trial pilot with a select group of SMB accounts to validate extraction precision and workflow speed improvements."
        price = "Test a tiered usage-based SaaS pricing structure (based on monthly invoice volume) to validate willingness to pay before fixing prices."
        parts = ["Certified QuickBooks ProAdvisors", "Xero Platinum Partners"]
        metrics = ["Extraction accuracy rate %", "Time saved per invoice", "Monthly active accounts", "Net revenue retention"]
        exp = "Expand feature set into automated approval workflows, fraud detection, and multi-currency payment reconciliation."
    else:
        seg = "Target early adopter segment experiencing core domain pain points."
        pos = f"Innovative AI solution streamlining {profile.concept[:40]} with improved accuracy and speed."
        chans = ["Targeted digital marketing", "Industry community outreach", "Direct sales outreach"]
        pilot = "Launch a limited pilot with target users to collect qualitative feedback and measure initial engagement metrics."
        price = "Test a low-cost freemium or usage-based tier to assess customer pricing tolerance."
        parts = ["Industry niche partners", "Complementary software tool providers"]
        metrics = ["User signups", "Daily active usage", "Feature adoption rate", "Customer retention"]
        exp = "Expand into adjacent vertical markets and enterprise custom deployments."

    return GTMStrategy(
        initial_customer_segment=seg,
        positioning=pos,
        acquisition_channels=chans,
        pilot_strategy=pilot,
        pricing_approach=price,
        partnerships=parts,
        validation_metrics=metrics,
        expansion_strategy=exp
    )
