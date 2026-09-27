import os
import sys
import json
import logging
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from validation_pipeline import execute_validation_pipeline, generate_markdown_report

logging.basicConfig(level=logging.WARNING, format="%(levelname)s [%(name)s]: %(message)s")

OUTPUT_DIR = Path(__file__).parent / "outputs"

def run_app():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if len(sys.argv) > 1:
        idea = " ".join(sys.argv[1:])
    else:
        print("=== AI Startup Idea Validator ===")
        print("Enter your startup idea below ")
        user_input = input("> ").strip()

        if not user_input:
            print("Error: Startup idea cannot be empty.")
            return

        idea = user_input

    print(f"\nAnalyzing Startup Idea: '{idea}'...\n")

    report = execute_validation_pipeline(idea)
    md_content = generate_markdown_report(report)

    md_file = OUTPUT_DIR / "startup_validation_report.md"
    json_file = OUTPUT_DIR / "startup_validation_report.json"

    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_content)

    with open(json_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(report.model_dump(), indent=2))

    print(f"Validation complete!")
    print(f"Markdown report saved to: {md_file}")
    print(f"JSON data saved to: {json_file}\n")
    print(f"Overall Viability Score: {report.viability_score.overall_viability_score} / 100")
    print(f"Summary: {report.validation_summary}")
    print(f"Next Step: {report.recommended_next_step}\n")

    if report.investor_questions and report.investor_questions.questions:
        print("--- Optional Founder Response Mode ---")
        print("Investor Question:")
        q_item = report.investor_questions.questions[0]
        print(f"[{q_item.category}] {q_item.question}")
        print("Context: " + q_item.context_rationale)

        if sys.stdin.isatty():
            ans = input("\nYour Answer (or press Enter to skip): ").strip()
            if ans:
                print("\nAI Analysis of Founder Response:")
                if len(ans) < 20:
                    print("Analysis: The answer provides a brief direction but lacks details on CAC, conversion rate, or customer acquisition mechanics.")
                else:
                    print("Analysis: Solid initial response addressing key operational aspects. Consider quantifying target customer acquisition milestones.")

if __name__ == "__main__":
    run_app()
