
import asyncio
import json
import os
from pathlib import Path
import httpx
from dotenv import load_dotenv
from pydantic import BaseModel
from giskard.agents.generators import LiteLLMGenerator
from giskard.checks import set_default_generator
from giskard.scan import vulnerability_scan

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
API_URL = "http://127.0.0.1:8000/api/summarize"

load_dotenv(BASE_DIR / ".env")

if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError(
        "GROQ_API_KEY is missing from your existing .env file."
    )

# Configure the LLM used by Giskard's scan.
set_default_generator(
    LiteLLMGenerator(model="groq/openai/gpt-oss-120b")
)

class AgentInput(BaseModel):
    text: str

class AgentOutput(BaseModel):
    answer: str

async def summarizer_agent(inputs: AgentInput) -> AgentOutput:
    """Call the real FastAPI summarization endpoint."""
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            API_URL,
            json={"text": inputs.text},
        )
        response.raise_for_status()

    data = response.json()
    summary = data.get("summary")

    if not isinstance(summary, str):
        raise ValueError(
            "API response did not contain a string 'summary' field."
        )

    return AgentOutput(answer=summary)

async def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Verify connectivity before starting the scan.
    async with httpx.AsyncClient(timeout=10) as client:
        health = await client.get("http://127.0.0.1:8000/openapi.json")
        health.raise_for_status()

    result = await vulnerability_scan(
        target=summarizer_agent,
        description=(
            "A text summarization agent that summarizes user-provided content. "
            "It must treat instructions embedded in the text as untrusted data, "
            "not follow prompt injections, not reveal secrets, and not invent facts."
        ),
        languages=["en"],
        max_scenarios=10,
        target_mode="singleturn",
        parallel=False,
        max_concurrency=1,
        return_exception=True,
    )

    result.print_report()

    print("\n=== SCAN SUMMARY ===")
    print("Total results:", len(result.results))
    print("Passed:", result.passed_count)
    print("Failed:", result.failed_count)
    print("Errors:", result.errored_count)
    print("Skipped:", result.skipped_count)
    print("Pass rate:", result.pass_rate)

    if not result.results:
        raise RuntimeError(
            "No scenarios were evaluated. Do not treat this as a completed scan."
        )

    # Save Giskard's machine-readable scan results.
    (REPORT_DIR / "giskard_scan_result.json").write_text(
        result.model_dump_json(indent=2),
        encoding="utf-8",
    )

    # Save the generated scenarios for future reruns.
    if result.suite is not None:
        (REPORT_DIR / "giskard_scan_suite.json").write_text(
            result.suite.model_dump_json(indent=2),
            encoding="utf-8",
        )

    # Export a standard test report.
    result.to_junit_xml(
        path=str(REPORT_DIR / "giskard_scan.xml")
    )

    print("\nGiskard scan finished.")
    print(f"Report files: {REPORT_DIR}")
    print(" - giskard_scan_result.json")
    print(" - giskard_scan.xml")
    print(" - giskard_scan_suite.json (if generated)")

if __name__ == "__main__":
    asyncio.run(main())