# 🚀 Assignment 9: AI Startup Idea Validator (Python + LangChain)

## Project Overview
The **AI Startup Idea Validator** is a production-grade multi-stage startup validation framework implemented in Python using LangChain and Pydantic. It transforms an initial user startup idea into a comprehensive, structured business analysis report.

The system performs structured business extraction, qualitative market analysis, SWOT analysis, technical feasibility assessment, risk assessment with mitigations, tough investor question generation, analytical viability scoring (0-100), go-to-market strategy synthesis, and actionable founder recommendations.

---

## Technical Specifications
- **Python Version:** 3.12+
- **LangChain Version:** 0.3.x (`langchain-core`, `langchain-community`, `langchain-groq`, `langchain-openai`)
- **Structured Output Engine:** Pydantic v2 schemas
- **Supported LLM Providers:** Groq (`llama-3.3-70b-versatile`), OpenAI (`gpt-4o-mini`), with graceful heuristic offline fallback.

---

## LangChain Concepts Used
1. **ChatPromptTemplate & PromptTemplate:** Dynamic prompt construction loaded from file-based prompt templates in `prompts/`.
2. **Multi-Stage Sequential Workflows:** Chained analysis pipeline where each stage depends on structured Pydantic outputs from previous stages.
3. **Structured Output Parsing:** Enforces schema validation using Pydantic models (`with_structured_output`).
4. **Dynamic Prompt Inputs:** Dynamic context injection into separate prompt templates per stage.
5. **Error Handling & Hallucination Prevention:** Strict rules prohibiting fabricated metrics, CAGRs, or invented company names. Clear separation of explicit user inputs vs AI assumptions.

---

## Project Structure
```
Assignment9_Startup_Idea_Validator_Kingsly/
│
├── app.py
├── validation_pipeline.py
├── models.py
├── scoring.py
│
├── chains/
│   ├── idea_analysis.py
│   ├── swot_analysis.py
│   ├── market_analysis.py
│   ├── technical_feasibility.py
│   ├── risk_analysis.py
│   ├── investor_questions.py
│   ├── viability_scoring.py
│   ├── gtm_strategy.py
│   └── report_generator.py
│
├── prompts/
│   ├── idea_analysis_prompt.txt
│   ├── swot_prompt.txt
│   ├── market_opportunity_prompt.txt
│   ├── technical_feasibility_prompt.txt
│   ├── risk_analysis_prompt.txt
│   ├── investor_question_prompt.txt
│   ├── viability_scoring_prompt.txt
│   ├── gtm_strategy_prompt.txt
│   └── validation_report_prompt.txt
│
├── outputs/
│   ├── startup_validation_report.md
│   └── startup_validation_report.json
│
├── startup_validation_strategy.md
├── test_log.md
├── README.md
├── requirements.txt
└── .env.example
```

---

## Environment Configuration & Installation

### 1. Installation
Clone or unpack the project folder and install dependencies:
```bash
pip install -r requirements.txt
```

### 2. API Credentials Setup
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Populate either `GROQ_API_KEY` or `OPENAI_API_KEY`:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
# OR
OPENAI_API_KEY=sk-your_openai_api_key_here
```
*Note: Credentials must remain in `.env` and are never committed to version control.*

---

## How to Run the Application

### 1. Interactive CLI Mode
Run the main script without arguments to enter an interactive prompt:
```bash
python app.py
```

### 2. Command-Line Argument Mode
Pass a startup idea description directly via command-line arguments:
```bash
python app.py "An AI-based platform that helps college students prepare for technical interviews using personalized mock interviews."
```

Output files will be automatically generated in:
- `outputs/startup_validation_report.md`
- `outputs/startup_validation_report.json`

---

## Core System Architecture & Workflow

### 1. Idea Analysis & Assumption Handling
The input idea is parsed into explicit statements vs AI-generated assumptions. Unstated customer segments or pricing models are explicitly marked with `[Assumption]` or `[Recommendation]`. Vague or invalid inputs (e.g. "abc") are gracefully rejected with explanatory reasons.

### 2. SWOT & Market Analysis
SWOT analysis evaluates internal advantages and external threats specifically for the startup domain. Market analysis uses qualitative evaluation (need, frequency, adoption, differentiation) without fabricating fake numbers, CAGRs, or market size statistics.

### 3. Technical Feasibility & Risk Assessment
Evaluates tech stack complexity, AI dependencies, external APIs, latency, and cloud infrastructure. Risk assessment categorizes risks into Market, Product, Technical, Financial, Operational, Adoption, Competitive, Security, and Dependency with actionable mitigations.

### 4. Analytical Viability Scoring (0–100)
Calculates an explainable 8-component score:
- Problem Clarity (15%)
- Customer Need (15%)
- Market Opportunity (15%)
- Differentiation (15%)
- Revenue Model (10%)
- Technical Feasibility (10%)
- Scalability (10%)
- Risk Profile (10%)

### 5. Investor Question Generation & GTM Strategy
Generates 7 probing investor questions testing unit economics, defensibility, and scalability. Formulates a practical GTM strategy covering initial segment, positioning, acquisition channels, pilot testing, pricing, and expansion steps.

---

## Example Startup Ideas to Test
1. **AI Interview Prep Platform:** `"An AI-based platform that helps college students prepare for technical interviews using personalized mock interviews."`
2. **SMB Invoice Automation:** `"A SaaS platform for small businesses to automate invoice processing using AI."`
3. **Home Chef Marketplace:** `"A marketplace connecting local home chefs with customers looking for homemade meals."`

---

## Known Limitations
- The viability score is an analytical indicator of business model completeness, not a statistical guarantee of commercial success.
- Offline execution uses built-in heuristic parsing when API keys are absent.
