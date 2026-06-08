# 🚀 AI Test Case Generator from User Stories

## 👥 Team Information

### Team Name

**InfiniteMinds**

### Team Number

**Team 30**

### Team Members

* Vibitha B K
* Varun S
* Varsha S

---

## 🌐 Deliverable Links

### Demo Video

https://www.loom.com/share/277309bc610c49ba940f40a580c0fc94

### GitHub Repository

https://github.com/vibithabalamurali/TestCaseGen

### AI REFERENCE LINK

https://chatgpt.com/share/6a265385-4920-8320-a311-eb051e8861ab


---

## 📌 Overview

The AI Test Case Generator is a web-based application that automatically converts user stories into structured Behavior-Driven Development (BDD) test cases using Generative AI.

The system analyzes user requirements and generates comprehensive test scenarios in Gherkin format, including positive, negative, and edge-case scenarios. The generated output can be directly used with automation frameworks such as Cucumber and Behave.

This solution helps reduce manual effort, improve consistency, and increase test coverage during software testing activities.


# 🧠 Problem Statement

Software teams often spend significant time manually creating test cases from user stories. This process can be:

* Time-consuming
* Repetitive
* Error-prone
* Inconsistent across teams
* Likely to miss important edge cases

The AI Test Case Generator addresses these challenges by automatically generating structured test scenarios from natural language requirements.

---

# 🎯 Features

### Core Features

* User Story Input Interface
* AI-Powered Test Case Generation
* Positive Scenario Generation
* Negative Scenario Generation
* Edge Case Identification
* Gherkin Format Output
* Downloadable `.feature` Files
* Cucumber-Compatible Output
* Behave-Compatible Output
* Story Coverage Analysis
* Structured Prompt-Based Generation

---

# ⚙️ System Architecture

```text
User Story
     │
     ▼
AI Processing Engine
     │
     ▼
Coverage Analysis
     │
     ▼
Scenario Generation
     │
     ▼
Gherkin Formatter
     │
     ▼
Feature File Generator
     │
     ▼
Downloadable Output
```

---

# 🛠️ Technology Stack

## Frontend

* React.js
* JavaScript
* Tailwind CSS
* Axios

## Backend

* Python
* Flask
* Flask-CORS

## AI Integration

* Google Gemini API

## Testing

* Pytest

---

# 📂 Project Structure

```text
AI-Test-Case-Generator/

├── backend/
│   ├── tests/
│   ├── downloads/
│   ├── app.py
│   ├── requirements.txt
│   └── run_tests.bat
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── sample-data/
│   ├── input/
│   └── expected-output/
│
├── README.md
└── AI_USAGE_NOTE.md
```

---

# 🚀 Setup Instructions

## Backend Setup

Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Run the backend server:

```bash
python app.py
```

---

## Frontend Setup

Install dependencies:

```bash
cd frontend
npm install
```

Run the frontend:

```bash
npm run dev
```

Default frontend URL:

```text
http://localhost:5173
```

---

# ▶️ Run Instructions

### Start Backend

```bash
cd backend
python app.py
```

### Start Frontend

```bash
cd frontend
npm run dev
```

---

# 🔌 API Endpoints

| Endpoint               | Method | Description             |
| ---------------------- | ------ | ----------------------- |
| `/`                    | GET    | Home Route              |
| `/health`              | GET    | Health Check            |
| `/generate`            | POST   | Generate Test Cases     |
| `/download-package`    | POST   | Generate Behave Package |
| `/download/<filename>` | GET    | Download Feature File   |

---

# 🧪 Example

## Input User Story

```text
As a user, I want to log into the application using email and password so that I can access my dashboard.
```

## Generated Output

```gherkin
Feature: Login Functionality

Scenario: Successful login with valid credentials
Given user is on login page
When user enters valid email and password
Then user should be redirected to dashboard

Scenario: Login with invalid password
Given user is on login page
When user enters valid email and invalid password
Then error message should be displayed
```

---

# 📥 Download Features

The application supports generation of:

* Gherkin Feature Files
* Behave-Compatible Packages
* Cucumber-Compatible Packages

Generated package contents:

```text
project_package.zip

├── feature.feature
├── environment.py
├── common_steps.py
└── README.md
```

---

# 🧪 Testing & Quality Assurance

## Backend Test Coverage

The backend includes automated testing using **Pytest** to validate the application's core functionality and ensure reliable API behavior.

### Testing Framework

* Pytest (Python)

### Execute Tests

```bash
cd backend

run_tests.bat

# OR

pytest tests/ -v
```

### Covered Test Scenarios

#### Health & Routing Integrity

Validates:

* API availability
* Health endpoint functionality
* Route accessibility

#### AI Test Case Generation

Validates:

* User story submission
* AI processing workflow
* Gherkin generation
* Response structure validation

#### Behave Package Generation

Validates:

* ZIP archive creation
* Package structure generation
* Download readiness

#### Feature File Downloads

Validates:

* File availability
* Successful downloads
* Content integrity

### Coverage Summary

| Component           | Status   |
| ------------------- | -------- |
| Health Endpoint     | ✅ Tested |
| Route Validation    | ✅ Tested |
| AI Test Generation  | ✅ Tested |
| Response Validation | ✅ Tested |
| Package Generation  | ✅ Tested |
| File Downloads      | ✅ Tested |

---

## Frontend Quality Assurance

Frontend quality is maintained through ESLint validation.

Run lint checks:

```bash
npm run lint
```

### Validation Includes

* Code Quality Checks
* Syntax Validation
* React Best Practices
* Maintainability Standards

---

# 📂 Sample Data

Sample input and expected output files are included in:

```text
sample-data/

├── input/
└── expected-output/
```

These files can be used to validate application behavior and generated results.

---

# 📋 Assumptions

* User stories are provided in English.
* Gemini API credentials are configured correctly.
* Internet connectivity is available for AI processing.
* Generated test cases are reviewed before production use.
* Input user stories contain sufficient functional detail.

---

# ⚠️ Limitations

* Output quality depends on user story clarity.
* AI-generated scenarios may require manual refinement.
* Complex domain-specific requirements may need additional validation.
* Currently supports text-based user stories only.
* Generated test cases should be reviewed by QA professionals before automation.

---

# 🔮 Future Enhancements

* User Authentication
* Jira Integration
* Multi-Language Support
* Test Case Prioritization
* Export to PDF and Excel
* Advanced Coverage Analytics
* Automatic Step Definition Generation
* CI/CD Integration

---

# 👨‍💻 Author

Developed as part of an AI-powered software testing automation project focused on improving software quality assurance through automated test case generation.
