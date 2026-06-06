import os
import re

from dotenv import load_dotenv

from prompts.gherkin_template import (
    GHERKIN_PROMPT_TEMPLATE,
    GHERKIN_SYSTEM_INSTRUCTION,
    MIN_EDGE,
    MIN_NEGATIVE,
    MIN_POSITIVE,
    RETRY_PROMPT_TEMPLATE,
)
from services.llm_client import call_llm, configure_genai

load_dotenv()

MIN_POSITIVE = int(os.getenv("MIN_POSITIVE_SCENARIOS", MIN_POSITIVE))
MIN_NEGATIVE = int(os.getenv("MIN_NEGATIVE_SCENARIOS", MIN_NEGATIVE))
MIN_EDGE = int(os.getenv("MIN_EDGE_SCENARIOS", MIN_EDGE))


def _clean_gherkin_output(raw_text: str) -> str:
    text = raw_text.strip()
    fence_match = re.search(r"```(?:gherkin|feature)?\s*\n?(.*?)\n?```", text, re.DOTALL | re.IGNORECASE)
    if fence_match:
        text = fence_match.group(1).strip()
    return text


def _extract_feature_name(gherkin: str) -> str:
    match = re.search(r"^Feature:\s*(.+)$", gherkin, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "generated_feature"


def _count_scenarios(gherkin: str) -> dict[str, int]:
    return {
        "positive": len(re.findall(r"Scenario:\s*\[Positive\]", gherkin, re.IGNORECASE)),
        "negative": len(re.findall(r"Scenario:\s*\[Negative\]", gherkin, re.IGNORECASE)),
        "edge": len(re.findall(r"Scenario:\s*\[Edge\]", gherkin, re.IGNORECASE)),
    }


def _meets_minimums(counts: dict[str, int]) -> bool:
    return (
        counts["positive"] >= MIN_POSITIVE
        and counts["negative"] >= MIN_NEGATIVE
        and counts["edge"] >= MIN_EDGE
    )


def _build_prompt(user_story: str, requirements_context: str = "") -> str:
    story_block = user_story
    if requirements_context:
        story_block = f"{user_story}\n{requirements_context}"
    return GHERKIN_PROMPT_TEMPLATE.format(
        user_story=story_block,
        min_positive=MIN_POSITIVE,
        min_negative=MIN_NEGATIVE,
        min_edge=MIN_EDGE,
    )


def _build_retry_prompt(user_story: str, counts: dict[str, int]) -> str:
    return RETRY_PROMPT_TEMPLATE.format(
        user_story=user_story,
        positive_count=counts["positive"],
        negative_count=counts["negative"],
        edge_count=counts["edge"],
        min_positive=MIN_POSITIVE,
        min_negative=MIN_NEGATIVE,
        min_edge=MIN_EDGE,
    )


def _call_llm_gherkin(prompt: str) -> tuple[str, str]:
    raw, model_used = call_llm(prompt, GHERKIN_SYSTEM_INSTRUCTION)
    return _clean_gherkin_output(raw), model_used


def generate_test_cases(user_story: str, requirements_context: str = "") -> dict:
    user_story = user_story.strip()
    if not user_story:
        raise ValueError("User story cannot be empty")

    configure_genai()

    gherkin, model_used = _call_llm_gherkin(_build_prompt(user_story, requirements_context))
    counts = _count_scenarios(gherkin)

    if not _meets_minimums(counts):
        gherkin, model_used = _call_llm_gherkin(_build_retry_prompt(user_story, counts))
        counts = _count_scenarios(gherkin)

    feature_name = _extract_feature_name(gherkin)

    return {
        "gherkin": gherkin,
        "feature_name": feature_name,
        "model_used": model_used,
        "scenario_counts": counts,
    }
