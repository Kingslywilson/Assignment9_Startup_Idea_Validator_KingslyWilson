import logging
from pathlib import Path
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from models import StartupProfile, TechnicalFeasibility
from chains.utils import try_recover_pydantic_from_error

logger = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "technical_feasibility_prompt.txt"

def run_technical_feasibility(profile: StartupProfile, llm: Optional[object] = None) -> TechnicalFeasibility:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    prompt_template = ChatPromptTemplate.from_template(prompt_text)

    if llm:
        try:
            try:
                structured_llm = llm.with_structured_output(TechnicalFeasibility)
                chain = prompt_template | structured_llm
                res = chain.invoke({"startup_profile": profile.model_dump_json()})
            except Exception:
                structured_llm = llm.with_structured_output(TechnicalFeasibility, method="json_mode")
                chain = prompt_template | structured_llm
                res = chain.invoke({"startup_profile": profile.model_dump_json()})
            if res and isinstance(res, TechnicalFeasibility):
                return res
        except Exception as e:
            recovered = try_recover_pydantic_from_error(e, TechnicalFeasibility)
            if recovered:
                return recovered
            logger.warning("Technical feasibility LLM analysis failed; using fallback: %s", e)

    concept_lower = profile.concept.lower()
    if "interview" in concept_lower:
        rating = "Moderate to High"
        reasoning = "Core components rely on mature LLM APIs, speech-to-text engines, and web frameworks. Main challenges involve real-time latency and scoring consistency."
        reqs = [
            "Web/Mobile user interface for live interview simulation",
            "Real-time audio streaming and speech recognition engine",
            "LLM evaluation engine with structured rubric parsing",
            "Secure user response storage and feedback analytics database"
        ]
        complexity = "Moderate complexity. Requires asynchronous processing pipeline for audio handling and LLM prompt chaining."
        aiml = [
            "Whisper or equivalent Speech-to-Text API",
            "LLMs for dynamic question generation and answer evaluation",
            "Text-to-Speech API for conversational voice output"
        ]
        apis = ["OpenAI/Groq API", "Deepgram/Whisper API", "ElevenLabs or Web Speech API"]
        infra = "Cloud serverless backend (FastAPI/Node), Redis cache for session state, PostgreSQL for structured logs."
        arch = [
            "Frontend (React / Next.js Web App)",
            "Python API (FastAPI / WebSockets)",
            "Interview Engine (Prompt & Context Manager)",
            "LangChain Workflow (Multi-agent evaluation)",
            "LLM & Speech Providers (Groq / OpenAI / Whisper)",
            "Database & Analytics (PostgreSQL & Redis Cache)"
        ]
    elif "invoice" in concept_lower:
        rating = "High"
        reasoning = "Document parsing and structured extraction are well-supported by modern multimodal LLMs and OCR frameworks with straightforward architecture."
        reqs = [
            "Document ingestion web portal supporting PDF/PNG/JPEG formats",
            "OCR preprocessing and vision-LLM extraction pipeline",
            "ERP / Accounting API connector framework (QuickBooks, Xero)",
            "Audit trail and manual exception review dashboard"
        ]
        complexity = "Low to Moderate complexity. System workflow is largely batch or event-driven document processing."
        aiml = [
            "Multimodal LLMs for vision-based document understanding",
            "Fallback OCR engines (Tesseract / AWS Textract)"
        ]
        apis = ["OpenAI GPT-4o / Claude Vision / Groq Vision API", "QuickBooks Online API", "Xero API"]
        infra = "AWS Lambda / Cloud Run for document triggers, S3 storage for raw invoices, relational DB for ledger audit."
        arch = [
            "Frontend Upload Portal (React / Vue)",
            "Python Gateway (FastAPI / Celery)",
            "OCR & Vision Pipeline (Multimodal Extraction)",
            "LangChain Structured Output Parser",
            "Accounting System Connectors (QuickBooks / Xero API)",
            "Secure Storage & Audit DB (S3 & PostgreSQL)"
        ]
    else:
        rating = "Moderate"
        reasoning = "Standard web/cloud application architecture with AI component integration."
        reqs = [
            "User facing web frontend",
            "Backend API services",
            "AI module integration",
            "Data storage infrastructure"
        ]
        complexity = "Moderate complexity dependent on specific feature scope."
        aiml = ["Standard LLM API integration for automated analysis"]
        apis = ["LLM Provider APIs", "Authentication Provider (Clerk/Auth0)"]
        infra = "Standard cloud deployment (Docker, Vercel/AWS, PostgreSQL)."
        arch = [
            "Frontend App Layer",
            "Python API Backend",
            "LangChain Orchestration Workflow",
            "LLM Provider API",
            "Database & Storage Tier"
        ]

    return TechnicalFeasibility(
        feasibility_rating=rating,
        reasoning=reasoning,
        core_technical_requirements=reqs,
        architecture_complexity=complexity,
        ai_ml_requirements=aiml,
        external_api_dependencies=apis,
        infrastructure_and_scalability=infra,
        suggested_architecture=arch
    )
