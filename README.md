🚀 AI Test Case Generator from User Stories
📌 Overview

This project is an AI-powered Test Case Generator that converts user stories into structured BDD test cases in Gherkin format.

It helps QA engineers, developers, and testers automatically generate:

Positive test cases
Negative test cases
Edge cases
.feature files ready for automation frameworks like Cucumber and Behave
🧠 Problem Statement

Writing test cases manually from user stories is:

Time-consuming ⏱️
Inconsistent across teams ❌
Prone to missing edge cases ⚠️

This project solves that by using LLM-powered structured generation to automate the entire process.

🎯 Key Features
✨ Core Features (Completed)
📝 Web UI to paste user stories
💻 CLI support for quick generation
🤖 AI generates:
Positive test cases
Negative test cases
Edge cases
📄 Gherkin format output (Given / When / Then)
📁 .feature file generation
📦 Downloadable .feature file
🧪 Cucumber / Behave compatible output
🧠 Structured prompt engineering for consistent results
⚙️ How It Works
User Story Input
        ↓
LLM (Gemini / AI Model)
        ↓
Test Case Generation Engine
        ↓
Gherkin Formatter
        ↓
.feature File Generator
        ↓
Download / Export (ZIP supported)
🧪 Example
Input (User Story)
As a user, I want to log into the application using email and password so that I can access my dashboard.
Output (.feature file)
Feature: Login Functionality

Scenario: Successful login with valid credentials
Given user is on login page
When user enters valid email and password
Then user should be redirected to dashboard

Scenario: Login with invalid password
Given user is on login page
When user enters valid email and invalid password
Then error message should be displayed
🏗️ Tech Stack
🐍 Python (Flask / Backend API)
🤖 Gemini AI / LLM API
🌐 HTML / CSS / JavaScript (Frontend)
📦 Flask-CORS (API handling)
🧪 Gherkin (BDD format)
📂 Project Structure
ai-test-case-generator/
│
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── styles.css
├── utils/
│   ├── prompt_templates.py
│   ├── gherkin_formatter.py
│
├── output/
│   └── generated.feature
│
└── README.md
🚀 Getting Started
1️⃣ Clone the repository
git clone https://github.com/your-username/ai-test-case-generator.git
cd ai-test-case-generator
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Add API Key

Create a .env file:

GEMINI_API_KEY=your_api_key_here
4️⃣ Run the application
python app.py
5️⃣ Open in browser
http://localhost:5000
📦 Output Formats Supported
.feature file (Cucumber / Behave ready)
.zip export (full test suite package)
CLI output
Web UI output
🧠 AI Capability

The system uses structured prompt engineering to ensure:

Consistent Gherkin formatting
Coverage of edge cases
Separation of test types
Clean reusable scenarios
🔥 Future Enhancements
📊 AI Test Coverage Analyzer
🔐 Security test case generator (SQLi, XSS)
📄 PDF test report generator
🧪 Execution simulation dashboard
🤖 AI QA assistant chat mode
📈 Test case prioritization (P0/P1/P2)
💡 Real-World Use Cases
QA automation teams
Agile sprint planning
Test case documentation
BDD workflow integration
Software requirement validation
👨‍💻 Author

Vibitha Balamurali
🎓 AI & Software Development Enthusiast
💡 Focus: AI + QA Automation + Full Stack Projects

⭐ Support

If you like this project:

⭐ Star the repository
🍴 Fork it
🧪 Use it in your QA workflows
