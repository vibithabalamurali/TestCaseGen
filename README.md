# 🚀 AI Test Case Generator from User Stories

## 📌 Overview

This project is an AI-powered Test Case Generator that converts user stories into structured BDD test cases in Gherkin format.

It helps QA engineers, developers, and testers automatically generate:
- Positive test cases  
- Negative test cases  
- Edge cases  
- `.feature` files ready for automation frameworks like Cucumber and Behave  

---

## 🧠 Problem Statement

Writing test cases manually from user stories is:
- Time-consuming  
- Inconsistent across teams  
- Prone to missing edge cases  

This project solves that using LLM-powered structured generation.

---

## 🎯 Features

### ✅ Core Features
- Web UI to paste user stories  
- CLI support for quick generation  
- AI generates:
  - Positive test cases  
  - Negative test cases  
  - Edge cases  
- Gherkin format output (Given/When/Then)  
- `.feature` file generation  
- Downloadable `.feature` file  
- Cucumber / Behave compatible output  
- Structured prompt templates for consistent AI responses  

---

## ⚙️ How It Works

User Story → AI Model → Test Case Generator → Gherkin Formatter → `.feature` File → Download

---

## 🧪 Example

### Input:
As a user, I want to log into the application using email and password so that I can access my dashboard.

### Output:
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
