# 🚀 AI Test Case Generator from User Stories

## 👥 Team Information

### Team Name
**InfiniteMinds**

### Team Number
**Team 30**

### Team Members
* **Vibitha B K** - Full Stack & AI Integration Lead
* **Varun S** - Frontend & UI/UX Developer
* **Varsha S** - QA Engineer & CLI Development

---

## 🌐 Deliverable Links

### Deployed Links
* **Demo Video**: [Loom Demo Video](https://www.loom.com/share/277309bc610c49ba940f40a580c0fc94)
* **GitHub Repository**: [GitHub Repo](https://github.com/vibithabalamurali/TestCaseGen)
* **AI Reference Link**: [ChatGPT Reference Link](https://chatgpt.com/share/6a265385-4920-8320-a311-eb051e8861ab)

---

## 📌 Overview
The **AI Test Case Generator** is a web-based platform that automates the conversion of software user stories into structured Behavior-Driven Development (BDD) test scenarios using Generative Artificial Intelligence.

The system parses natural-language user stories and generates comprehensive test suites in Gherkin format, categorize them under positive, negative, and edge-case tags, and packages them as fully download-ready Cucumber/Behave frameworks.

---

## 🧠 Problem Statement
Software quality assurance teams spend massive manual effort translation user stories and acceptance criteria into test scripts. This manual approach presents several major bottlenecks:
* **Time-consuming manual drafting** of repetitive step scenarios.
* **Inconsistent test coverage** across diverse feature sets.
* **Overlooked edge cases** and negative input validations.
* **Long development-to-testing feedback loops**, slowing down CI/CD pipelines.

The AI Test Case Generator automates this translation layer, analyzing stories instantaneously and generating production-ready Gherkin test scenarios.

---

## 🎯 Features

### Core Features
* **Interactive Input Console**: Plain-text editor for user stories and acceptance criteria.
* **Gherkin Auto-Generation**: Instant generation of Cucumber/Behave feature scenarios.
* **Scenario Tagging**: Automatic categorizations with `@positive`, `@negative`, and `@edge` annotations.
* **QA Intelligence Analytics**:
  * **Story Quality**: Calculates a readiness score and points out missing requirements or actors.
  * **Test Coverage**: Highlights covered specifications, identifies missing test pathways, and flags security gaps.
  * **Execution Simulation**: Mock execution simulation mapping out step transitions.
* **Export Packages**: Downloads `.feature` files or ready-to-run Behave/Cucumber ZIP structures.

---

## ⚙️ Detailed System Architecture

### High-Level Architecture
```text
┌─────────────────────────────────────────────────────────────┐
│                        End Users                            │
│                     (QA / Developers)                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend                           │
│                                                             │
│  • User Story Editor                                        │
│  • QA Intelligence Console                                  │
│  • Interactive Gherkin Editor                               │
│  • Download & Package Manager                               │
│                                                             │
│ Technologies: React.js, Vite, Tailwind CSS, Axios           │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ HTTP / REST API
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask Backend API                        │
│                                                             │
│  API Layer                                                  │
│  ├── GET /health                                            │
│  ├── POST /generate                                         │
│  ├── POST /download-package                                 │
│  └── GET /download/<filename>                               │
│                                                             │
│  Business Logic Layer                                       │
│  ├── Story Analysis Service                                 │
│  ├── Coverage Mapping Engine                                │
│  ├── Execution Simulator                                    │
│  └── Behave ZIP Bundler                                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  AI Classification Engine                   │
│                                                             │
│  • Google Gemini API Client                                 │
│  • Structured Prompt Engineering Templates                  │
│  • Output Validation & Fallback Parser                      │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   Google Gemini API                         │
│                                                             │
│  • Story Comprehension                                      │
│  • Scenario Parsing & Gherkin Structuring                   │
│  • Edge-case & Security Gap Discovery                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Scenario Processing Workflow
```text
                  User Story & Acceptance Criteria
                                │
                                ▼
                  ┌───────────────────────────┐
                  │   Vite React Frontend     │
                  └─────────────┬─────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │    POST /generate API     │
                  └─────────────┬─────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │    Flask App Controller   │
                  └─────────────┬─────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │   Gemini Prompt Builder   │
                  └─────────────┬─────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │    Google Gemini API      │
                  └─────────────┬─────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │ JSON & Gherkin Validation │
                  └─────────────┬─────────────┘
                                │
         ┌──────────────────────┴──────────────────────┐
         ▼                                             ▼
┌───────────────────────────┐                 ┌───────────────────────────┐
│     QA Intelligence       │                 │     Gherkin Generator     │
│  • Quality Score          │                 │  • Positive Scenarios     │
│  • Coverage Analysis      │                 │  • Negative Scenarios     │
│  • Execution Simulator    │                 │  • Edge Cases Scenarios   │
└────────┬──────────────────┘                 └────────┬──────────────────┘
         │                                             │
         └──────────────────────┬──────────────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │   Render Frontend Panel   │
                  └───────────────────────────┘
```

---

## 📂 Project Structure

```text
TestCaseGenerator/
├── backend/
│   ├── tests/                  # Pytest unit & integration test files
│   │   ├── conftest.py
│   │   └── test_app.py
│   ├── services/               # Core background logic files
│   │   ├── feature_writer.py   # Formats and saves feature files
│   │   ├── llm_client.py       # Interacts with Gemini APIs
│   │   └── zip_package.py      # Combines scripts into Behave ZIPs
│   ├── output/                 # Storage for generated artifacts
│   ├── app.py                  # Main Flask API controllers and endpoints
│   ├── cli.py                  # CLI support for local test generation
│   ├── start.bat               # Fast launch batch script for backend
│   ├── run_tests.bat           # Run backend test suite quickly
│   └── requirements.txt        # Backend python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── assets/             # Assets and custom SVG graphics
│   │   ├── App.jsx             # Core application UI and layout
│   │   ├── App.css             # Main styling configurations
│   │   ├── index.css           # Global themes and CSS variables
│   │   └── main.jsx            # Vite DOM mounting entry point
│   ├── public/                 # Static assets
│   ├── eslint.config.js        # Lint settings
│   ├── vite.config.js          # Vite configuration
│   └── package.json            # Frontend package details
│
├── sample_data/                # Reference directories for input/output testing
│   ├── input/
│   └── expected-output/
│
├── README.md                   # This overview guide
└── AI_USAGE_NOTE.md            # Details of prompt development with AI
```

---

## 🚀 Setup Instructions

### Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `backend/` directory:
   ```env
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   ```
5. Run the backend server:
   ```bash
   python app.py
   ```

### Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Launch the development server:
   ```bash
   npm run dev
   ```
4. Access the frontend interface at:
   ```text
   http://localhost:5173
   ```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/health` | `GET` | API Health check endpoint |
| `/` | `GET` | Returns home documentation & active endpoints |
| `/generate` | `POST` | Processes user story, generates Gherkin & QA intelligence |
| `/download-package` | `POST` | Generates and zips a run-ready Behave package |
| `/download/<filename>` | `GET` | Fetches the raw `.feature` file for saving locally |

---

## 🧪 Example

### Input User Story
```text
As a registered user,
I want to log in with my email and password,
So that I can access my account dashboard.
```

### Generated Gherkin Scenarios
```gherkin
@positive
Scenario: Successful login with valid credentials
  Given user is on login page
  When user enters valid email "test@example.com" and password "Pass123"
  And clicks "Submit"
  Then user is redirected to account dashboard

@negative
Scenario: Login attempt with unregistered email
  Given user is on login page
  When user enters unregistered email "invalid@example.com" and password "Pass123"
  Then error message "User does not exist" should be displayed
```

---

## 🧪 Testing & Quality Assurance

### Backend Automated Testing
Backend stability and integration logic are validated using `pytest`.

Run tests:
```bash
cd backend
run_tests.bat
# OR
pytest tests/ -v
```

#### Coverage Matrix
| Module | Test Coverage | Status |
| --- | --- | --- |
| **Routing** | Checks `/`, `/health` accessibility and payloads | ✅ Passed |
| **Generation** | Mocks LLM client output and checks structured outputs | ✅ Passed |
| **Packages** | Generates valid Behave ZIP archives and payloads | ✅ Passed |
| **Downloads** | Ensures files write to the directory and stream correctly | ✅ Passed |

### Frontend Quality Control
Lints are managed using ESLint configurations.

Verify code styles:
```bash
cd frontend
npm run lint
```

---

## 📋 Assumptions & Limitations
* **Assumptions**:
  * Input user stories are provided in English.
  * Google Gemini API access credentials are validly set up.
  * Active internet connection is needed for processing.
* **Limitations**:
  * Generation quality relies closely on acceptance criteria clarity.
  * Complex business flows might need manual validation steps.
  * Sandbox is restricted to text format inputs.

---

## 🔮 Future Enhancements
* **Direct Jira Integration**: Automatically fetch stories and push back features.
* **Step Definition Stubber**: Write boilerplate testing classes in Python automatically.
* **Excel & PDF Exporters**: Generate shareable reports for stakeholders.
* **Multi-language Support**: Accept and write files in Spanish, German, French, etc.
