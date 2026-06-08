import json
import os
import re
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
SAFE_DEFAULT_MODEL = "gemini-2.5-flash-lite"
DEFAULT_FALLBACKS = "gemini-flash-lite-latest,gemini-2.5-flash"


def _load_env():
    load_dotenv(ENV_PATH, override=True)


def sanitize_model_name(name: str) -> str:
    """Strip accidental pasted text (e.g. git commands) from model names."""
    name = (name or "").strip()
    match = re.match(r"^(?:models/)?(gemini[\w\-.]+)", name, re.IGNORECASE)
    if match:
        return match.group(1).lower().replace("models/", "")
    return SAFE_DEFAULT_MODEL


def get_default_model() -> str:
    _load_env()
    return sanitize_model_name(os.getenv("GEMINI_MODEL", SAFE_DEFAULT_MODEL))


def get_fallback_models() -> list[str]:
    _load_env()
    raw = os.getenv("GEMINI_FALLBACK_MODELS", DEFAULT_FALLBACKS)
    return [sanitize_model_name(m) for m in raw.split(",") if m.strip()]


def configure_genai():
    _load_env()
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set. Add it to backend/.env")
    genai.configure(api_key=api_key)


def model_candidates() -> list[str]:
    seen = set()
    ordered = []
    for name in [get_default_model(), *get_fallback_models()]:
        if name and name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def is_quota_error(message: str) -> bool:
    lowered = message.lower()
    return "429" in message or "quota" in lowered or "resource exhausted" in lowered


def is_model_error(message: str) -> bool:
    lowered = message.lower()
    return (
        "400" in message
        or "unexpected model name" in lowered
        or "not found" in lowered
        or "invalid model" in lowered
    )


def parse_json_response(text: str) -> dict:
    cleaned = text.strip()
    fence = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", cleaned, re.DOTALL | re.IGNORECASE)
    if fence:
        cleaned = fence.group(1).strip()
    return json.loads(cleaned)


def call_llm(prompt: str, system_instruction: str = "") -> tuple[str, str]:
    configure_genai()
    last_error = None
    models = model_candidates()

    for model_name in models:
        try:
            kwargs = {}
            if system_instruction:
                kwargs["system_instruction"] = system_instruction
            model = genai.GenerativeModel(model_name, **kwargs)
            response = model.generate_content(prompt)
            if not response.text:
                raise RuntimeError("LLM returned an empty response")
            return response.text.strip(), model_name
        except Exception as exc:
            message = str(exc)
            last_error = exc
            if is_quota_error(message) or is_model_error(message):
                continue
            raise RuntimeError(f"LLM request failed ({model_name}): {message}") from exc

    raise RuntimeError(
        f"All Gemini models failed. Tried: {', '.join(models)}. "
        "Check GEMINI_API_KEY and GEMINI_MODEL in backend/.env"
    ) from last_error
