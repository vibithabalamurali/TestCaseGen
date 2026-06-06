import json
import os
import re

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
FALLBACK_MODELS = [
    m.strip()
    for m in os.getenv(
        "GEMINI_FALLBACK_MODELS",
        "gemini-2.5-flash-lite,gemini-flash-lite-latest,gemini-2.5-flash",
    ).split(",")
    if m.strip()
]


def configure_genai():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set. Add it to backend/.env")
    genai.configure(api_key=api_key)


def model_candidates() -> list[str]:
    seen = set()
    ordered = []
    for name in [DEFAULT_MODEL, *FALLBACK_MODELS]:
        if name and name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def is_quota_error(message: str) -> bool:
    lowered = message.lower()
    return "429" in message or "quota" in lowered or "resource exhausted" in lowered


def parse_json_response(text: str) -> dict:
    cleaned = text.strip()
    fence = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", cleaned, re.DOTALL | re.IGNORECASE)
    if fence:
        cleaned = fence.group(1).strip()
    return json.loads(cleaned)


def call_llm(prompt: str, system_instruction: str = "") -> tuple[str, str]:
    configure_genai()
    last_error = None

    for model_name in model_candidates():
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
            if is_quota_error(message):
                continue
            raise RuntimeError(f"LLM request failed ({model_name}): {message}") from exc

    raise RuntimeError(
        "Gemini API quota exceeded on all configured models. "
        "Check your API key at https://aistudio.google.com/apikey"
    ) from last_error
