from prompts.analysis_templates import COVERAGE_ANALYSIS_PROMPT, COVERAGE_ANALYSIS_SYSTEM
from services.llm_client import call_llm, parse_json_response


def analyze_coverage(user_story: str, gherkin: str) -> dict:
    prompt = COVERAGE_ANALYSIS_PROMPT.format(
        user_story=user_story.strip(),
        gherkin=gherkin.strip(),
    )
    raw, model_used = call_llm(prompt, COVERAGE_ANALYSIS_SYSTEM)

    try:
        data = parse_json_response(raw)
    except (ValueError, TypeError) as exc:
        raise RuntimeError(f"Failed to parse coverage analysis: {exc}") from exc

    data["model_used"] = model_used
    return data
