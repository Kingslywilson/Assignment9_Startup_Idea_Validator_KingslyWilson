# 🚀 Assignment 9: AI Startup Idea Validator

## Project Overview

The **AI Startup Idea Validator** is a multi-stage startup validation framework built with Python, LangChain, Pydantic, and Groq compatible LLM.

The system transforms an initial startup idea into a structured business validation report by performing:

* Startup idea analysis
* Problem and customer analysis
* SWOT analysis
* Market opportunity analysis
* Technical feasibility assessment
* Risk assessment and mitigation planning
* Investor question generation
* Analytical viability scoring
* Go-to-market strategy generation
* Founder recommendation generation
* Final Markdown and JSON report generation

The application also includes error handling and heuristic fallback behavior for situations where an LLM API is unavailable.

---

# Technical Specifications

* **Python:** 3.12+
* **LangChain:** 0.3.x ecosystem
* **Structured Output:** Pydantic v2
* **LLM Provider:** Groq
* **Configured Model:** `openai/gpt-oss-20b`
* **Alternative Provider:** OpenAI-compatible configuration
* **Output Formats:** Markdown and JSON

---

# LangChain Concepts Used

## 1. ChatPromptTemplate and PromptTemplate

Prompt templates are stored as separate files inside the `prompts/` directory.

Each validation stage loads the appropriate prompt and dynamically injects the required startup context.

## 2. Multi-Stage Sequential Workflow

The application uses a sequential validation pipeline.

The output of one analysis stage is passed as structured context to subsequent stages.

The workflow includes:

```text
Startup Idea
     ↓
Idea Analysis
     ↓
SWOT Analysis
     ↓
Market Analysis
     ↓
Technical Feasibility
     ↓
Risk Analysis
     ↓
Investor Questions
     ↓
Viability Scoring
     ↓
GTM Strategy
     ↓
Final Validation Report
```

## 3. Structured Output Parsing

Pydantic models are used to define and validate structured application data.

The system uses structured LLM output where supported to maintain predictable data formats.

## 4. Dynamic Prompt Inputs

Each analysis stage receives the relevant information from previous stages through dynamically constructed prompts.

## 5. Error Handling and Hallucination Prevention

The prompts instruct the model to distinguish between:

* Information explicitly provided by the founder
* AI-generated assumptions
* Recommendations
* Information requiring further validation

The system avoids presenting unsupported market statistics, fabricated metrics, or unverified company information as established facts.

---

# Project Structure

```text
Assignment9_Startup_Idea_Validator_Kingsly/

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

# Installation

## 1. Install Python

Use Python 3.12 or a compatible Python 3.x environment.

Verify the installation:

```bash
python --version
```

## 2. Install Dependencies

From the project directory:

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file using `.env.example` as a template.

Example:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

Alternatively, an OpenAI-compatible configuration can be used if supported by the installed application configuration.

### Security

API keys must not be committed to the repository.

The `.env` file should remain local and should not be included in the submitted ZIP file.

Only `.env.example` should be included for configuration reference.

---

# How to Run

## Interactive CLI Mode

Run:

```bash
python app.py
```

The application will prompt for a startup idea.

Example:

```text
I want to build an AI platform that helps college students prepare for technical interviews using personalized mock interviews and feedback.
```

---

## Command-Line Argument Mode

A startup idea can also be supplied directly:

```bash
python app.py "An AI-based platform that helps college students prepare for technical interviews using personalized mock interviews."
```

---

# Generated Outputs

After successful validation, the application generates:

```text
outputs/startup_validation_report.md
outputs/startup_validation_report.json
```

### Markdown Report

The Markdown report provides a human-readable startup validation report.

### JSON Report

The JSON file provides structured machine-readable validation results.

---

# Core System Architecture

## 1. Startup Idea Analysis

The first stage extracts and analyzes the submitted startup idea.

It identifies information such as:

* Problem
* Target customers
* Proposed solution
* Value proposition
* Revenue considerations
* Differentiation
* Explicit founder information
* AI assumptions
* Recommendations

When information is not provided by the founder, the system distinguishes assumptions and recommendations rather than presenting them as confirmed founder statements.

---

## 2. SWOT Analysis

The SWOT stage evaluates:

* Strengths
* Weaknesses
* Opportunities
* Threats

The analysis is based on the submitted startup context.

---

## 3. Market Opportunity Analysis

The market stage evaluates factors such as:

* Customer need
* Problem frequency
* Adoption considerations
* Differentiation
* Target segments
* Market validation requirements

The system is designed to avoid inventing unsupported market statistics or CAGR values.

---

## 4. Technical Feasibility

The technical analysis evaluates:

* Technology requirements
* AI/LLM dependencies
* External APIs
* Infrastructure requirements
* Latency considerations
* Scalability
* Implementation complexity

---

## 5. Risk Analysis

The risk stage identifies potential risks across areas including:

* Market
* Product
* Technical
* Financial
* Operational
* Adoption
* Competition
* Security
* External dependencies

Where appropriate, mitigation strategies are generated for identified risks.

---

# Analytical Viability Scoring

The application calculates an analytical viability score from **0–100** using eight evaluation components:

| Criterion             |   Weight |
| --------------------- | -------: |
| Problem Clarity       |      15% |
| Customer Need         |      15% |
| Market Opportunity    |      15% |
| Differentiation       |      15% |
| Revenue Model         |      10% |
| Technical Feasibility |      10% |
| Scalability           |      10% |
| Risk Profile          |      10% |
| **Total**             | **100%** |

The score is an analytical assessment of the startup information and business-model completeness.

It is **not a statistical prediction or guarantee of commercial success**.

---

# Investor Questions

The system generates challenging investor-oriented questions based on the startup analysis.

Questions can address areas such as:

* Customer validation
* Willingness to pay
* Revenue model
* Competitive differentiation
* Customer acquisition
* Unit economics
* Scalability
* Defensibility
* Technical risks

The founder can provide a response, after which the application can analyze the response and identify areas that require stronger evidence or clarification.

---

# Go-To-Market Strategy

The GTM stage develops a practical strategy covering areas such as:

* Initial target segment
* Positioning
* Acquisition channels
* Pilot strategy
* Pricing considerations
* Early customer validation
* Expansion opportunities

---

# Error Handling and Fallback Behavior

The application includes error handling for LLM/API failures.

If an API request fails or the configured LLM is unavailable, the application can use its configured fallback behavior where applicable instead of terminating with an unhandled exception.

This allows the application to maintain a controlled execution flow and report the affected stage.

The fallback output should be treated as an analytical fallback rather than a replacement for full LLM-powered analysis.

---

# Example Startup Ideas

## 1. AI Interview Preparation

```text
An AI-based platform that helps college students prepare for technical interviews using personalized mock interviews.
```

## 2. SMB Invoice Automation

```text
A SaaS platform for small businesses to automate invoice processing using AI.
```

## 3. Home Chef Marketplace

```text
A marketplace connecting local home chefs with customers looking for homemade meals.
```

---

# Testing

The project includes a dedicated:

```text
test_log.md
```

The test log covers:

* Startup idea analysis
* Problem analysis
* SWOT analysis
* Market analysis
* Technical feasibility
* Risk analysis
* Viability scoring
* Investor question generation
* Founder response analysis
* GTM strategy
* Markdown report generation
* JSON report generation
* Vague startup idea handling
* Incomplete business information
* Error handling
* API rate-limit handling
* Fallback execution
* Output verification
* Application stability

The tested workflow successfully generated both Markdown and JSON validation reports.

---

# Example Validation Result

For the following startup idea:

```text
I want to build an AI platform that helps college students prepare for technical interviews using personalized mock interviews and feedback.
```

The validation pipeline successfully produced:

```text
Overall Viability Score: 75.5 / 100
```

and generated:

```text
outputs/startup_validation_report.md
outputs/startup_validation_report.json
```

The report included startup analysis, market considerations, technical feasibility, risks, investor questions, scoring, GTM considerations, and recommended next steps.

---

# Known Limitations

1. The viability score is an analytical indicator and should not be interpreted as a guarantee of startup success.

2. Market analysis is primarily qualitative unless reliable external market data is explicitly provided.

3. The system does not perform real-time market research unless an external research capability is separately integrated.

4. AI-generated assumptions and recommendations require founder validation before being treated as business facts.

5. LLM availability and API rate limits can affect individual analysis stages.

6. Fallback execution provides resilience but may produce less detailed analysis than the full LLM pipeline.

7. API credentials and external service availability are required for full LLM-powered execution.

---

# Security Notes

* API keys must never be hard-coded into Python source files.
* API credentials should be stored in `.env`.
* `.env` should not be committed to version control.
* `.env.example` contains only placeholder credentials.
* Generated reports should be reviewed before sharing if they contain sensitive startup information.

---

# Conclusion

The **AI Startup Idea Validator** demonstrates a complete multi-stage LangChain workflow for transforming a startup idea into a structured business validation report.

The project demonstrates:

* Python application development
* LangChain prompt engineering
* Sequential AI workflows
* Pydantic structured outputs
* Business idea analysis
* SWOT analysis
* Market analysis
* Technical feasibility assessment
* Risk assessment
* Investor-question generation
* Analytical scoring
* GTM strategy generation
* Founder response analysis
* Error handling
* API fallback handling
* Markdown and JSON report generation

**Project Status: Ready for Submission**
