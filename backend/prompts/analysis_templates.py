STORY_ANALYSIS_SYSTEM = """You are a senior QA analyst and business analyst.
Analyze user stories for test readiness. Output ONLY valid JSON — no markdown, no explanation."""

STORY_ANALYSIS_PROMPT = """Analyze this user story before test case generation.

USER STORY:
{user_story}

Return ONLY this JSON structure:
{{
  "quality_score": <number 0-100>,
  "is_ready": <true if quality_score >= 70 else false>,
  "issues": [<list of clarity gaps, ambiguities, missing info>],
  "actors": [<users, admins, systems>],
  "actions": [<key user/system actions>],
  "inputs": [<form fields, data inputs, API params>],
  "preconditions": [<setup states required>],
  "acceptance_criteria": [<explicit or implied acceptance criteria>]
}}

Be specific. Flag missing acceptance criteria, vague verbs, unspecified error handling.
"""

COVERAGE_ANALYSIS_SYSTEM = """You are a QA coverage analyst specializing in BDD test design.
Compare requirements against generated Gherkin scenarios. Output ONLY valid JSON."""

COVERAGE_ANALYSIS_PROMPT = """Analyze test coverage: compare the user story against generated Gherkin test cases.

USER STORY:
{user_story}

GENERATED GHERKIN:
{gherkin}

Return ONLY this JSON structure:
{{
  "coverage_score": <number 0-100>,
  "covered": [<specific scenarios/requirements that ARE covered, e.g. "Login success with valid credentials">],
  "missing": [<important scenarios NOT covered, e.g. "Account lock after 5 failed attempts", "SQL injection">],
  "security_gaps": [<security tests missing: SQL injection, XSS, session hijacking, auth bypass, rate limiting>]
}}

Consider functional, negative, edge, and security coverage. Be practical for a QA POC demo.
"""

REQUIREMENTS_CONTEXT_TEMPLATE = """
EXTRACTED REQUIREMENTS (use these to ensure complete coverage):
- Actors: {actors}
- Actions: {actions}
- Inputs: {inputs}
- Preconditions: {preconditions}
- Acceptance criteria: {acceptance_criteria}
"""
