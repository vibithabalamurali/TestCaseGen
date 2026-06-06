"""Lightweight execution simulation — no real app needed, for demo purposes."""

import re


def simulate_execution(gherkin: str) -> list[dict]:
    scenarios = re.findall(
        r"^\s*Scenario:\s*(.+)$",
        gherkin,
        re.MULTILINE,
    )

    results = []
    for name in scenarios:
        lower = name.lower()
        if any(kw in lower for kw in ("sql injection", "xss", "injection", "auth bypass")):
            status = "passed"
            note = "Blocked by security controls"
        elif "[negative]" in lower or "invalid" in lower or "incorrect" in lower or "empty" in lower:
            status = "passed"
            note = "Error handling verified"
        elif "[edge]" in lower and ("lock" in lower or "rate" in lower):
            status = "passed"
            note = "Edge case handled"
        elif "[positive]" in lower or "successful" in lower:
            status = "passed"
            note = "Happy path verified"
        else:
            status = "passed"
            note = "Scenario validated"

        results.append({"scenario": name.strip(), "status": status, "note": note})

    passed = sum(1 for r in results if r["status"] == "passed")
    failed = sum(1 for r in results if r["status"] == "failed")

    return {
        "results": results,
        "summary": {"total": len(results), "passed": passed, "failed": failed},
    }
