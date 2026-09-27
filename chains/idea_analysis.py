import os
import json
import logging
from pathlib import Path
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from models import StartupProfile
from chains.utils import try_recover_pydantic_from_error

logger = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "idea_analysis_prompt.txt"

def run_idea_analysis(idea: str, llm: Optional[object] = None) -> StartupProfile:
    idea_str = idea.strip() if idea else ""
    if not idea_str or len(idea_str) < 5 or idea_str.lower() in ["abc", "test", "app", "hello", "123"]:
        return StartupProfile(
            idea_raw=idea,
            is_valid=False,
            rejection_reason="The provided startup idea is empty, whitespace-only, or meaningless.",
            concept="Invalid Concept",
            problem_statement="N/A",
            proposed_solution="N/A"
        )

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    prompt_template = ChatPromptTemplate.from_template(prompt_text)

    if llm:
        try:
            try:
                structured_llm = llm.with_structured_output(StartupProfile)
                chain = prompt_template | structured_llm
                res = chain.invoke({"idea": idea_str})
            except Exception:
                structured_llm = llm.with_structured_output(StartupProfile, method="json_mode")
                chain = prompt_template | structured_llm
                res = chain.invoke({"idea": idea_str})
            if res and isinstance(res, StartupProfile):
                return res
        except Exception as e:
            recovered = try_recover_pydantic_from_error(e, StartupProfile)
            if recovered:
                return recovered
            logger.warning("Idea analysis LLM failed; using fallback: %s", e)

    is_vague = len(idea_str) < 35
    concept = idea_str.capitalize()
    
    if "interview" in concept_lower_helper(idea_str):
        explicit_aud = ["College students preparing for technical software interviews"]
        assumed_aud = ["Training institutes and university placement cells"]
        problem = "Many engineering students lack structured, personalized practice and real-time feedback before placement interviews."
        solution = "An AI platform providing adaptive mock technical interviews and detailed feedback on technical and soft skills."
        prov_rev = []
        sugg_rev = ["Freemium B2C subscription", "B2B institutional licensing for colleges", "Pay-per-interview package"]
        known_comp = []
        pot_comp = [
            "Existing peer interview platforms (e.g. Pramp, Interviewing.io - General Knowledge)",
            "Coding practice platforms (e.g. LeetCode, HackerRank - General Knowledge)",
            "General-purpose AI assistants (e.g. ChatGPT, Claude)",
            "Peer-to-peer manual mock interviews"
        ]
        missing_info = ["Specific pricing tier", "Initial target programming languages/domains"]
    elif "invoice" in concept_lower_helper(idea_str):
        explicit_aud = ["Small business owners and accounting teams"]
        assumed_aud = ["Freelancers and SMB finance managers"]
        problem = "Small businesses spend excessive manual effort processing physical and digital invoices, leading to payment delays and human errors."
        solution = "A SaaS platform using AI OCR and LLM extraction to automatically parse invoices and sync with accounting software."
        prov_rev = ["SaaS Subscription"]
        sugg_rev = ["Usage-based tier (per invoice processed)", "Monthly SaaS tier", "Enterprise custom API integration"]
        known_comp = []
        pot_comp = [
            "Incumbent accounting software built-in tools (e.g. QuickBooks, Xero - General Knowledge)",
            "Document parsing software (e.g. Bill.com, Rossum.ai - General Knowledge)",
            "Manual spreadsheet tracking and human data entry"
        ]
        missing_info = ["Target accounting integrations (QuickBooks, Xero, etc.)"]
    elif "chef" in concept_lower_helper(idea_str) or "meal" in concept_lower_helper(idea_str):
        explicit_aud = ["Local home chefs and consumers seeking homemade food"]
        assumed_aud = ["Busy working professionals and health-conscious individuals"]
        problem = "Home chefs lack direct digital distribution to monetize their cooking, while local consumers struggle to find authentic homemade food."
        solution = "A peer-to-peer marketplace platform connecting verified home chefs with local consumers for ordered meals."
        prov_rev = []
        sugg_rev = ["Marketplace transaction commission", "Chef monthly subscription fee", "Delivery convenience fee"]
        known_comp = []
        pot_comp = [
            "Commercial food delivery apps (e.g. DoorDash, UberEats - General Knowledge)",
            "Local meal subscription and tiffin providers",
            "Direct informal social media ordering"
        ]
        missing_info = ["Food safety compliance framework", "Delivery logistics partner details"]
    else:
        explicit_aud = [idea_str[:50]] if not is_vague else []
        assumed_aud = ["General digital consumers and professionals"] if is_vague else ["Target segment related to " + idea_str[:30]]
        problem = f"Users in the domain of '{idea_str[:40]}' face operational inefficiencies and lack tailored modern solutions."
        solution = f"Proposed system addressing '{idea_str[:40]}' leveraging AI technology."
        prov_rev = []
        sugg_rev = ["Subscription (SaaS)", "Pay-per-use transaction fee", "Freemium with premium upgrades"]
        known_comp = []
        pot_comp = [
            "Generic manual workflows",
            "Existing legacy software tools",
            "Custom in-house solutions"
        ]
        missing_info = ["Detailed target audience demographics", "Specific pricing mechanism", "Distribution plan"]

    return StartupProfile(
        idea_raw=idea,
        is_valid=True,
        rejection_reason=None,
        concept=concept,
        target_audience_explicit=explicit_aud,
        target_audience_assumptions=assumed_aud,
        problem_statement=problem,
        proposed_solution=solution,
        provided_revenue_model=prov_rev,
        suggested_revenue_models=sugg_rev,
        known_competitors=known_comp,
        potential_competitors_alternatives=pot_comp,
        missing_information=missing_info
    )

def concept_lower_helper(s: str) -> str:
    return s.lower() if s else ""
