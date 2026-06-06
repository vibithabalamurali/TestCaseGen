from prompts.analysis_templates import STORY_ANALYSIS_PROMPT, STORY_ANALYSIS_SYSTEM
from services.llm_client import call_llm, parse_json_response


def analyze_user_story(user_story: str) -> dict:
    prompt = STORY_ANALYSIS_PROMPT.format(user_story=user_story.strip())
    raw, model_used = call_llm(prompt, STORY_ANALYSIS_SYSTEM)

    try:
        data = parse_json_response(raw)
    except (ValueError, TypeError) as exc:
        raise RuntimeError(f"Failed to parse story analysis: {exc}") from exc

    data["model_used"] = model_used
    return data


def format_requirements_for_prompt(analysis: dict) -> str:
    from prompts.analysis_templates import REQUIREMENTS_CONTEXT_TEMPLATE

    def join_items(key: str) -> str:
        items = analysis.get(key) or []
        return ", ".join(items) if items else "Not specified"

    return REQUIREMENTS_CONTEXT_TEMPLATE.format(
        actors=join_items("actors"),
        actions=join_items("actions"),
        inputs=join_items("inputs"),
        preconditions=join_items("preconditions"),
        acceptance_criteria=join_items("acceptance_criteria"),
    )
