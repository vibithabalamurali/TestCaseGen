Feature: User Login
  As a registered user, I want to log in with email and password to access my dashboard.

  @positive
  Scenario: [Positive] Successful login with valid credentials
    Given I am on the login page
    And I have a registered account with email "user@example.com"
    When I enter "user@example.com" in the email field
    And I enter "ValidPass123!" in the password field
    And I click the "Login" button
    Then I should be redirected to the account dashboard
    And I should see a welcome message

  @positive
  Scenario: [Positive] Password field masks entered characters
    Given I am on the login page
    When I enter "secretpassword" in the password field
    Then the password field should display masked characters
    And the raw password should not be visible on screen

  @negative
  Scenario: [Negative] Login fails with invalid password
    Given I am on the login page
    And a registered account exists for "user@example.com"
    When I enter "user@example.com" in the email field
    And I enter "WrongPassword!" in the password field
    And I click the "Login" button
    Then I should remain on the login page
    And I should see the error message "Invalid email or password"

  @negative
  Scenario: [Negative] Login fails with empty email field
    Given I am on the login page
    When I leave the email field empty
    And I enter "SomePassword1!" in the password field
    And I click the "Login" button
    Then I should see an inline validation error for the email field
    And I should not be logged in

  @edge
  Scenario: [Edge] Account locks after five failed attempts in fifteen minutes
    Given I am on the login page
    And a registered account exists for "user@example.com"
    When I attempt to login with an invalid password 5 times within 15 minutes
    Then my account should be temporarily locked
    And I should see a message indicating the account is locked

  @edge
  Scenario: [Edge] Login with email at maximum allowed length
    Given I am on the login page
    And a registered account exists with a 254-character email address
    When I enter the maximum-length email in the email field
    And I enter the correct password
    And I click the "Login" button
    Then I should be redirected to the account dashboard
