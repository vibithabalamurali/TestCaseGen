import pytest

SAMPLE_GHERKIN = """
Feature: User Login
  Registered users can log in to access their dashboard.

  @positive
  Scenario: [Positive] Successful login with valid credentials
    Given I am on the login page
    When I enter "user@example.com" into the email field
    And I enter "Password123!" into the password field
    And I click the "Login" button
    Then I should be redirected to the account dashboard

  @negative
  Scenario: [Negative] Login with incorrect password
    Given I am on the login page
    When I enter "user@example.com" into the email field
    And I enter "WrongPassword" into the password field
    And I click the "Login" button
    Then I should see an error message "Invalid email or password."

  @edge
  Scenario: [Edge] Login with empty email field
    Given I am on the login page
    When I leave the email field empty
    And I click the "Login" button
    Then I should remain on the login page
""".strip()

SAMPLE_USER_STORY = (
    "As a registered user, I want to log in with my email and password, "
    "so that I can access my account dashboard."
)


@pytest.fixture
def client():
    from app import app

    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def mock_llm_response():
    return {
        "gherkin": SAMPLE_GHERKIN,
        "feature_name": "User Login",
        "model_used": "test-model",
        "scenario_counts": {"positive": 1, "negative": 1, "edge": 1},
    }
