import logging
from pathlib import Path
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from models import StartupProfile, RiskAssessment, InvestorQuestions, InvestorQuestion
from chains.utils import try_recover_pydantic_from_error

logger = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "investor_question_prompt.txt"

def run_investor_questions(profile: StartupProfile, risk: RiskAssessment, llm: Optional[object] = None) -> InvestorQuestions:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    prompt_template = ChatPromptTemplate.from_template(prompt_text)

    if llm:
        try:
            try:
                structured_llm = llm.with_structured_output(InvestorQuestions)
                chain = prompt_template | structured_llm
                res = chain.invoke({
                    "startup_profile": profile.model_dump_json(),
                    "risk_assessment": risk.model_dump_json()
                })
            except Exception:
                structured_llm = llm.with_structured_output(InvestorQuestions, method="json_mode")
                chain = prompt_template | structured_llm
                res = chain.invoke({
                    "startup_profile": profile.model_dump_json(),
                    "risk_assessment": risk.model_dump_json()
                })
            if res and isinstance(res, InvestorQuestions):
                return res
        except Exception as e:
            recovered = try_recover_pydantic_from_error(e, InvestorQuestions)
            if recovered:
                return recovered
            logger.warning("Investor questions LLM analysis failed; using fallback: %s", e)

    concept_lower = profile.concept.lower()
    questions = []

    if "interview" in concept_lower:
        questions = [
            InvestorQuestion(
                category="Problem",
                question="How have you empirically validated that students will pay out-of-pocket for AI mock interviews vs relying on free practice with peers?",
                context_rationale="Tests willingness to pay and market validation beyond free usage."
            ),
            InvestorQuestion(
                category="Customer",
                question="Who is your primary paying customer: individual students, university placement cells, or enterprise recruiters?",
                context_rationale="Clarifies customer persona, sales cycle length, and go-to-market motion."
            ),
            InvestorQuestion(
                category="Competition",
                question="Why would a computer science student choose your platform over LeetCode's ecosystem or general ChatGPT sessions?",
                context_rationale="Evaluates product defensibility and unique value proposition."
            ),
            InvestorQuestion(
                category="Revenue",
                question="Given the seasonal nature of college recruitment, how will you maintain steady cash flow during off-season months?",
                context_rationale="Assesses financial sustainability and seasonality mitigation."
            ),
            InvestorQuestion(
                category="Technology",
                question="How do you ensure AI interview evaluations remain consistently objective and free from hallucinations across complex coding prompts?",
                context_rationale="Tests technical robustness and quality assurance standards."
            ),
            InvestorQuestion(
                category="Scalability",
                question="What happens to unit economics when 50,000 students simultaneously run 30-minute voice/text mock interviews during peak hiring week?",
                context_rationale="Examines margin scalability and API operating cost structures."
            ),
            InvestorQuestion(
                category="Risk",
                question="What is the single biggest unproven business assumption in your deck, and what pilot test will prove or disprove it?",
                context_rationale="Evaluates founder self-awareness and lean hypothesis testing."
            )
        ]
    elif "invoice" in concept_lower:
        questions = [
            InvestorQuestion(
                category="Problem",
                question="What exact ROI metrics prove that small businesses will switch from their existing accounting software invoice features to your tool?",
                context_rationale="Tests value proposition clarity and customer switching motivation."
            ),
            InvestorQuestion(
                category="Customer",
                question="Are you targeting small business owners directly or accounting firms managing multiple client books?",
                context_rationale="Determines GTM efficiency and customer acquisition model."
            ),
            InvestorQuestion(
                category="Competition",
                question="How will you defend your business when QuickBooks or Xero launch an identical embedded AI invoice reader for free?",
                context_rationale="Tests long-term defensibility against platform incumbents."
            ),
            InvestorQuestion(
                category="Revenue",
                question="Is your pricing structured per-invoice or per-user seat, and how does that align with client volume scaling?",
                context_rationale="Evaluates pricing model alignment with customer usage."
            ),
            InvestorQuestion(
                category="Technology",
                question="What is your current error rate on poor-quality or handwritten invoices, and how does the system handle exceptions?",
                context_rationale="Tests product reliability and edge case handling."
            ),
            InvestorQuestion(
                category="Scalability",
                question="How seamlessly can your pipeline ingest and synchronize thousands of concurrent documents without API throttling?",
                context_rationale="Probes infrastructure throughput limits."
            ),
            InvestorQuestion(
                category="Risk",
                question="How do you handle data liability if an OCR error leads to an incorrect vendor payout?",
                context_rationale="Evaluates operational and legal risk exposure."
            )
        ]
    else:
        questions = [
            InvestorQuestion(
                category="Problem",
                question="What evidence demonstrates that this problem is severe enough to compel budget allocation from your target audience?",
                context_rationale="Validates customer pain intensity."
            ),
            InvestorQuestion(
                category="Customer",
                question="What is your projected Customer Acquisition Cost (CAC) compared to expected Lifetime Value (LTV)?",
                context_rationale="Evaluates unit economics and channel efficiency."
            ),
            InvestorQuestion(
                category="Competition",
                question="What prevents a well-funded competitor from cloning your core workflow within 60 days?",
                context_rationale="Tests competitive moat and defensibility."
            ),
            InvestorQuestion(
                category="Revenue",
                question="What pricing model has been tested with real users, and what was their response?",
                context_rationale="Assesses pricing validation."
            ),
            InvestorQuestion(
                category="Technology",
                question="What proprietary tech stack or data moat exists beyond standard wrapper calls to third-party LLMs?",
                context_rationale="Examines technical differentiation."
            ),
            InvestorQuestion(
                category="Scalability",
                question="How do gross margins evolve as server and API costs scale with active user volume?",
                context_rationale="Tests margin scalability."
            ),
            InvestorQuestion(
                category="Risk",
                question="What critical failure point would halt your business operations, and how are you mitigating it?",
                context_rationale="Evaluates risk mitigation readiness."
            )
        ]

    return InvestorQuestions(questions=questions)
