# Test Case Generator from User Story

**POC for Infinite Computer Solutions — 4th Round Project**

Turn user stories into structured Gherkin test cases (positive, negative, edge) and export Cucumber/Behave-ready `.feature` files using Google Gemini.

## Business Problem

Writing test cases from user stories is slow and inconsistent. This tool automates BDD-style test design with LLM-powered structured generation.

## Features

| Capability | Status |
|---|---|
| Web UI — paste user story, view Gherkin output | ✅ |
| CLI — generate from stdin, file, or `--sample` | ✅ |
| Positive + Negative + Edge scenarios | ✅ |
| Gherkin format (Given/When/Then) | ✅ |
| Structured prompt templates | ✅ |
| Auto-write `.feature` file to `backend/output/` | ✅ |
| Download `.feature` from web UI | ✅ |
| Download **Cucumber/Behave ZIP** (feature + step defs + README) | ✅ |
| Gherkin validation & formatting for BDD runners | ✅ |

## Architecture

```
User Story  →  Prompt Template (Gherkin rules)  →  Gemini LLM  →  Clean Gherkin  →  .feature file
                     ↑                                    ↑
              backend/prompts/                   backend/services/
              gherkin_template.py                generator.py + feature_writer.py
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- [Google Gemini API key](https://aistudio.google.com/apikey)

## Setup

### 1. Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `backend/.env` and set your key:

```
GEMINI_API_KEY=your_actual_key_here
```

Start the API (use the virtual environment — required):

```powershell
cd backend
.\start.bat
```

Or manually:

```powershell
cd backend
.\venv\Scripts\activate
python app.py
```

> **Important:** Running `python app.py` without activating `venv` will fail with `No module named 'flask'` and the web UI will show "Failed to fetch".

API runs at `http://127.0.0.1:5000`.

### 2. Frontend (Web App)

```powershell
cd frontend
npm install
npm run dev
```

Open the URL shown in the terminal (usually `http://localhost:5173`).

## Usage

### Web App

1. Paste a user story (or click **Load sample**).
2. Click **Generate Test Cases**.
3. Review Gherkin output with `@positive`, `@negative`, `@edge` tags.
4. **Copy** or **Download .feature** (single Gherkin file)
5. **Download Cucumber/Behave ZIP** — full runnable Behave project (see below)

### Download for Cucumber or Behave

| Button | What you get | Use case |
|--------|--------------|----------|
| **Download .feature** | One formatted Gherkin file | Drop into existing Cucumber/Behave project |
| **Download Cucumber/Behave ZIP** | Complete test package | Run immediately with Behave |

**ZIP contents:**
```
behave.ini
features/
  your_feature.feature    ← formatted Gherkin (@positive, @negative, @edge)
  environment.py          ← Behave hooks
  steps/
    common_steps.py       ← step definition stubs
README_BEHAVE.md          ← how to run with Python Behave
README_CUCUMBER.md        ← how to use with Java/JS Cucumber
```

**Run the downloaded ZIP with Behave (Python):**
```powershell
# Unzip, then inside the folder:
python -m venv venv
.\venv\Scripts\activate
pip install behave
behave --dry-run          # verify steps match
behave --tags=@positive   # run positive scenarios
```

**Use with Cucumber (Java / JavaScript):**
- Copy only the `.feature` file from the ZIP into your Cucumber `features/` folder
- Implement step definitions in your language (see `README_CUCUMBER.md` in the ZIP)

### CLI

Run from the `backend` folder (with venv activated):

```powershell
# Built-in sample story
python cli.py --sample

# From a file
python cli.py --file ..\samples\login_user_story.txt

# Inline story
python cli.py --story "As a user, I want to reset my password..."

# Custom output path
python cli.py --sample -o ..\my_tests\login.feature

# Print only (no file write)
python cli.py --sample --no-save
```

Generated files are saved to `backend/output/` by default.

## Sample User Story

See [`samples/login_user_story.txt`](samples/login_user_story.txt).

## API

| Method | Endpoint | Body | Response |
|---|---|---|---|
| GET | `/health` | — | `{ "status": "ok" }` |
| POST | `/generate` | `{ "userStory": "...", "saveFile": true }` | Gherkin text + file path |
| GET | `/download/<filename>` | — | `.feature` file download |
| POST | `/download-package` | `{ "gherkin", "feature_filename", "feature_name" }` | ZIP with Behave project |
| GET | `/download-package/<filename>` | — | ZIP from saved `.feature` |

## Project Structure

```
TestCaseGenerator/
├── backend/
│   ├── app.py                 # Flask REST API
│   ├── cli.py                 # Command-line interface
│   ├── prompts/
│   │   └── gherkin_template.py
│   ├── services/
│   │   ├── generator.py       # LLM call + output cleanup
│   │   └── feature_writer.py  # Writes .feature files
│   └── output/                # Generated .feature files
├── frontend/
│   └── src/App.jsx            # React web UI
└── samples/
    └── login_user_story.txt
```

## Demo Script (Interview)

1. Show the business problem: manual test case writing from stories is slow.
2. Open web app → load sample login story → generate.
3. Point out `@positive`, `@negative`, `@edge` scenarios and Given/When/Then steps.
4. Download **Cucumber/Behave ZIP** → unzip → `pip install behave` → `behave --dry-run`
5. Run CLI: `python cli.py --file ..\samples\login_user_story.txt` for automation angle.
6. Explain structured templates in `backend/prompts/gherkin_template.py`.

## Tech Stack

- **Backend:** Python, Flask, Google Generative AI (Gemini)
- **Frontend:** React, Vite
- **Output:** Gherkin `.feature` (Cucumber / Behave compatible)

## License

MIT — for portfolio / interview demonstration.
