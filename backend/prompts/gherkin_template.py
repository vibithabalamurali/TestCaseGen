GHERKIN_SYSTEM_INSTRUCTION = """You are an expert QA engineer specializing in BDD and Gherkin test case design.
You write test cases for Cucumber (Java/JavaScript) and Behave (Python).
Output ONLY valid Gherkin syntax — no markdown fences, no explanations, no preamble."""

MIN_POSITIVE = 3
MIN_NEGATIVE = 3
MIN_EDGE = 3

GHERKIN_PROMPT_TEMPLATE = """Generate comprehensive test cases in Gherkin format for the user story below.

USER STORY:
{user_story}

REQUIREMENTS — ALL ARE MANDATORY:
1. Create ONE Feature block with a clear name derived from the user story.
2. Include a one-line feature description after the Feature title.
3. Generate EXACTLY {min_positive} or more positive (happy path) scenarios — each tagged @positive.
4. Generate EXACTLY {min_negative} or more negative (invalid input / error handling) scenarios — each tagged @negative.
5. Generate EXACTLY {min_edge} or more edge case scenarios (boundaries, limits, security, concurrency) — each tagged @edge.
6. You MUST include all three categories. Do NOT skip @negative or @edge scenarios.
7. Each scenario name MUST be prefixed with [Positive], [Negative], or [Edge].
8. Use Given, When, Then, And, But with 2-space indentation for steps.
9. Steps must be concrete and testable — avoid vague language like "works correctly".
10. Do NOT wrap output in markdown code blocks.

NEGATIVE scenario ideas (pick from user story acceptance criteria):
- Wrong credentials, invalid input format, empty fields, unauthorized access, expired session

EDGE scenario ideas:
- Account lockout after N failures, max field length, special characters, rate limiting, unverified account

STRICT OUTPUT FORMAT (repeat for every scenario):
Feature: <Feature Name>
  <one-line description>

  @positive
  Scenario: [Positive] <scenario title>
    Given <precondition>
    When <action>
    Then <expected result>

  @negative
  Scenario: [Negative] <scenario title>
    Given <precondition>
    When <action>
    Then <expected result>

  @edge
  Scenario: [Edge] <scenario title>
    Given <precondition>
    When <action>
    Then <expected result>
"""

RETRY_PROMPT_TEMPLATE = """Your previous Gherkin output was incomplete.

USER STORY:
{user_story}

PREVIOUS OUTPUT HAD:
- {positive_count} positive scenarios (need at least {min_positive})
- {negative_count} negative scenarios (need at least {min_negative})
- {edge_count} edge scenarios (need at least {min_edge})

Regenerate the COMPLETE Feature file from scratch with at least {min_positive} @positive,
{min_negative} @negative, and {min_edge} @edge scenarios. Include ALL three categories.
Output ONLY valid Gherkin — no markdown fences, no explanations.
"""
