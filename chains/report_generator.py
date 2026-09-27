import logging
from pathlib import Path
from typing import Optional, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from models import (
    StartupProfile, SWOTAnalysis, RiskAssessment, ViabilityScoreBreakdown,
    _coerce_list_of_strings, _coerce_str
)

logger = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "validation_report_prompt.txt"

def run_report_generator(
    profile: StartupProfile,
    swot: SWOTAnalysis,
    risk: RiskAssessment,
    score: ViabilityScoreBreakdown,
    llm: Optional[object] = None
) -> Dict[str, Any]:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    prompt_template = ChatPromptTemplate.from_template(prompt_text)

    if llm:
        try:
            chain = prompt_template | llm
            res = chain.invoke({
                "startup_profile": profile.model_dump_json(),
                "swot_analysis": swot.model_dump_json(),
                "risk_assessment": risk.model_dump_json(),
                "viability_score": score.model_dump_json()
            })
            if hasattr(res, "content"):
                import json
                content = str(res.content).strip()
                if content.startswith("```"):
                    lines = content.splitlines()
                    if lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].strip() == "```":
                        lines = lines[:-1]
                    content = "\n".join(lines).strip()
                parsed = json.loads(content)
                if isinstance(parsed, dict) and ("improvement_suggestions" in parsed or "validation_summary" in parsed):
                    return {
                        "improvement_suggestions": _coerce_list_of_strings(parsed.get("improvement_suggestions")),
                        "critical_assumptions": _coerce_list_of_strings(parsed.get("critical_assumptions")),
                        "validation_summary": _coerce_str(parsed.get("validation_summary")),
                        "recommended_next_step": _coerce_str(parsed.get("recommended_next_step"))
                    }
        except Exception as e:
            logger.warning("Report generator LLM failed; using fallback: %s", e)

    concept_lower = profile.concept.lower()
    if "interview" in concept_lower:
        suggs = [
            "Test willingness to pay early by offering a paid mock interview tier before heavy feature development.",
            "Form strategic pilot partnerships with 2-3 engineering college placement departments.",
            "Implement model routing and response caching to keep API operational costs low at scale.",
            "Benchmarking AI feedback against industry standards to build student trust."
        ]
        assump = [
            "Students are willing to pay for AI-generated interview feedback out-of-pocket.",
            "Colleges will purchase institutional-level software licenses for placement cells.",
            "AI-generated evaluation is perceived as credible and helpful by job seekers.",
            "LLM API unit costs will remain sustainable during high usage spikes."
        ]
        summary = "Validation Summary: The startup idea addresses a clear student pain point and is technically feasible using current AI technologies. However, user willingness to pay out-of-pocket, retention past recruitment season, and API operating unit economics require empirical validation before scaling."
        next_step = "Build a lightweight MVP with a 1-week student pilot in 2 target colleges to validate mock completion rates and user feedback credibility."
    elif "invoice" in concept_lower:
        suggs = [
            "Focus initially on a single accounting ecosystem (e.g. QuickBooks) before expanding integrations.",
            "Introduce a human-in-the-loop audit dashboard for low-confidence extraction scores.",
            "Highlight data privacy guarantees and SOC2 compliance to lower buyer trust barriers.",
            "Structure pricing on a per-invoice tier to directly match customer volume."
        ]
        assump = [
            "Small businesses process enough invoices monthly to justify dedicated software costs.",
            "OCR and vision LLM extraction achieves over 95% accuracy on non-standard invoice layouts.",
            "SMB finance managers will trust automated invoice parsing without mandatory manual double-checks."
        ]
        summary = "Validation Summary: Strong B2B SaaS proposition with high potential retention once embedded. Core risks center on accuracy guarantees and incumbent platform features."
        next_step = "Conduct a 14-day free trial pilot with 20 target small businesses to benchmark extraction accuracy and user workflow speedups."
    else:
        suggs = [
            "Sharpen value proposition by focusing on a specific narrow user segment.",
            "Validate pricing willingness to pay early using pre-orders or pilot commitments.",
            "Maintain a model-agnostic backend architecture to avoid vendor lock-in."
        ]
        assump = [
            "Target users experience high enough friction to adopt a new digital tool.",
            "Current AI technology can deliver consistent value without high error rates.",
            "Customer acquisition costs remain lower than projected lifetime value."
        ]
        summary = f"Validation Summary: The concept '{profile.concept[:50]}' presents a valid business foundation. Successful execution depends on clear market differentiation and tight unit economics control."
        next_step = "Construct a functional prototype and run a 30-day user validation experiment with early adopters."

    return {
        "improvement_suggestions": suggs,
        "critical_assumptions": assump,
        "validation_summary": summary,
        "recommended_next_step": next_step
    }
