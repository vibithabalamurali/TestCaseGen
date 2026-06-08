# Test Cases - TestCaseGenerator

This document describes the happy-path test cases for the **Test Case Generator from User Story** project. It includes examples and specifications for:
1. **Pytest Happy Path Tests** (for Flask backend API endpoints)
2. **Python `unittest` style Tests** (for backend CLI and core LLM services)
3. **Vitest / Frontend Happy Path Tests** (for React frontend UI components)
4. **Happy Path Test Matrix**
5. **How to Run**

---

## 1. Pytest Happy Path Tests

### Backend API
These tests validate the primary Flask API endpoints under `backend/app.py`. They verify routing, requests, and structured response formats using `pytest`.

- `test_health_endpoint`
  - **Request**: `GET /health`
  - **Expected**: Status `200`
  - **Verify**: Response JSON is exactly `{"status": "ok"}`

- `test_home_page`
  - **Request**: `GET /`
  - **Expected**: Status `200`
  - **Verify**: Response contains a `"message"` and checks that `"/generate"` is listed in `"endpoints"`

- `test_generate_testcases`
  - **Request**: `POST /generate` with JSON payload:
    ```json
    {
      "userStory": "As a user, I want to login using email and password",
      "saveFile": false,
      "includeAnalysis": true
    }
    ```
  - **Expected**: Status `200`
  - **Verify**: 
    - The returned content-type is `application/json`
    - Response contains `"generated_test_cases"` with Gherkin tags (`Feature`, `Scenario`, `Given`, `When`, `Then`)
    - Response contains `"feature_name"`, `"scenario_counts"`, `"story_analysis"`, `"coverage_analysis"`, and `"execution_simulation"`

- `test_feature_package_download`
  - **Request**: `POST /download-package` with JSON payload:
    ```json
    {
      "gherkin": "Feature: Login ...",
      "feature_filename": "login.feature",
      "feature_name": "Login"
    }
    ```
  - **Expected**: Status `200`
  - **Verify**: Response `content_type` is `application/zip` and the file content binary length is greater than 100 bytes

- `test_feature_file_download`
  - **Request**: `GET /download/{filename}` (for a generated file name)
  - **Expected**: Status `200`
  - **Verify**: Response contains `"Feature:"` and serves the file as text/plain.

### Example Pytest Structure (`backend/tests/test_app.py`)

```python
import pytest
from unittest.mock import patch

class TestHealthAndHome:
    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.get_json() == {"status": "ok"}
```

---

## 2. Python `unittest` Style Tests (xUnit)

These tests target the internal command-line interface (`cli.py`) and background services (`llm_client.py` and `feature_writer.py`) using Python's standard `unittest` framework.

- `TestCLI.test_cli_generation`
  - **Setup**: Provide a temporary text file containing a valid user story
  - **Action**: Invoke `cli.py` passing the file path
  - **Expected**: Exit code `0` and a generated `.feature` file is written to the output directory

- `TestLLMClient.test_model_selection`
  - **Action**: Call `model_candidates()`
  - **Verify**: Replaces any malformed model name with a sanitized fallback model (e.g. `gemini-2.5-flash-lite`)

- `TestFeatureWriter.test_write_feature_file`
  - **Action**: Call `write_feature_file(gherkin_text, feature_name)`
  - **Verify**: Correctly formatted `.feature` file is saved with Gherkin scenarios to the target outputs folder

### Example xUnit / `unittest` Outline

```python
import unittest
from services.llm_client import get_default_model, sanitize_model_name

class TestLLMClient(unittest.TestCase):
    def test_sanitize_model_name(self):
        self.assertEqual(sanitize_model_name("models/gemini-2.5-flash"), "gemini-2.5-flash")
        self.assertEqual(sanitize_model_name("invalid-text"), "gemini-2.5-flash-lite")
```

---

## 3. Vitest / Frontend Happy Path Tests

These tests target the React client components (`App.jsx` and styling) in `frontend/src/` using `vitest` and `@testing-library/react`.

- `renders header title`
  - **Verify**: The component renders the main title `"Test Case Generator from User Story"` and badge `"POC · Infinite Computer Solutions"`.

- `loads sample story`
  - **Action**: Click the `"Load sample"` button.
  - **Verify**: The user story textarea is populated with the predefined template story text.

- `handles generation interaction`
  - **Action**: Paste a story, click `"Generate Test Cases"`, and check that the UI enters a loading state (`"Analyzing & Generating..."`).

- `renders panels after generation`
  - **Setup**: Mock a successful `/generate` response.
  - **Verify**:
    - **QA Intelligence Panel**: Shows the *Story Quality* score ring, *Test Coverage* list (Covered, Missing, and Security Gaps), and the *Execution Simulation* checklist.
    - **Generated Gherkin Panel**: Displays the counts (`positive`, `negative`, `edge`), Gherkin scenarios container, and action buttons (`Copy`, `Download .feature`, `Cucumber/Behave ZIP`).

### Example Vitest Test Outline

```jsx
import { render, screen, fireEvent } from "@testing-library/react";
import { expect, test } from "vitest";
import App from "../src/App";

test("renders title and load sample button", () => {
  render(<App />);
  expect(screen.getByText("Test Case Generator from User Story")).toBeInTheDocument();
  
  const sampleButton = screen.getByText("Load sample");
  fireEvent.click(sampleButton);
  expect(screen.getByPlaceholderText(/Paste your user story here/i).value).toContain("As a registered user");
});
```

---

## 4. Happy Path Test Matrix

| Test Layer | Framework | Target Component | Expected Outcome |
| --- | --- | --- | --- |
| Backend API | `pytest` | `GET /health` | Status `200`, JSON `{"status": "ok"}` |
| Backend API | `pytest` | `POST /generate` | Status `200`, JSON with Gherkin output & QA intelligence |
| Backend API | `pytest` | `POST /download-package` | Status `200`, returns Cucumber zip archive |
| Backend Services | `unittest` | `llm_client.py` | Gracefully falls back / sanitizes Gemini model config |
| Frontend UI | `vitest` | `App.jsx` (Header) | Renders project titles, branding badge |
| Frontend UI | `vitest` | `App.jsx` (QA Intelligence) | Displays Quality Score rings, checked test list, and simulated runs |

---

## 5. How to Run

### Run Backend Pytest
From the `backend/` directory:
```bash
pytest tests/ -v
```
Or execute the helper batch script:
```bash
backend\run_tests.bat
```

### Run Frontend Vitest
From the `frontend/` directory (after configuring test utilities):
```bash
npm run test
# or
npx vitest
```
