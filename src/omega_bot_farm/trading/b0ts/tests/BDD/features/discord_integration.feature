Feature: Discord Bot Integration
  As a cryptocurrency trader
  I want to interact with the position analyzer through Discord
  So that I can monitor my positions and receive alerts

  Background:
    Given the position analyzer is configured
    And the Discord bot is running
    And the exchange has the following positions:
      | symbol   | side | contracts | entry_price | mark_price | leverage | liquidation_price |
      | BTCUSDT  | long | 0.5       | 65000       | 68000      | 10       | 59000            |
      | ETHUSDT  | short| 2.0       | 3500        | 3400       | 5        | 3850             |

  @discord
  Scenario: Process position command
    When a user sends "!position BTCUSDT" in Discord
    Then the bot should respond with the position details
    And the response should include PnL information
    And the response should include leverage information

  @discord @fibonacci
  Scenario: Process Fibonacci analysis command
    When a user sends "!fibonacci BTCUSDT" in Discord
    Then the bot should respond with Fibonacci analysis
    And the response should include key Fibonacci levels
    And the response should include the current price position

  @discord @harmony
  Scenario: Process harmony analysis command
    When a user sends "!harmony BTCUSDT" in Discord
    Then the bot should respond with harmony analysis
    And the response should include the harmony score
    And the response should include market alignment information

  @discord @risk
  Scenario: Process risk assessment command
    When a user sends "!risk BTCUSDT" in Discord
    Then the bot should respond with risk assessment
    And the response should include the risk level
    And the response should include liquidation distance

  @discord
  Scenario: Process recommendation command
    When a user sends "!recommend BTCUSDT" in Discord
    Then the bot should respond with a trading recommendation
    And the response should include an action
    And the response should include reasoning

  @discord @visualization
  Scenario: Process chart command
    When a user sends "!chart BTCUSDT" in Discord
    Then the bot should generate a position chart
    And the bot should send the chart as an attachment
    And the chart should include key levels and indicators

  @discord @notification
  Scenario: Send high risk alert notification
    Given the exchange position "BTCUSDT" has mark price "60500"
    When the risk level for "BTCUSDT" becomes "HIGH"
    Then the bot should send a risk alert to the notification channel
    And the alert should include the symbol and risk level
    And the alert should include liquidation proximity information

  @discord @notification
  Scenario: Send profit target notification
    Given the exchange position "BTCUSDT" has mark price "71500"
    When the PnL for "BTCUSDT" exceeds 10%
    Then the bot should send a profit target alert to the notification channel
    And the alert should include the symbol and PnL percentage
    And the alert should include a suggestion to consider taking profits

  @discord
  Scenario: Process help command
    When a user sends "!help" in Discord
    Then the bot should respond with available commands
    And the response should include command descriptions
    And the response should include command examples

  @discord
  Scenario: Process invalid command
    When a user sends "!invalid_command" in Discord
    Then the bot should respond with an error message
    And the response should suggest using !help

  @discord
  Scenario: Admin command authorization
    Given the user has admin role
    When the user sends "!admin refresh_markets" in Discord
    Then the bot should process the admin command
    And the bot should respond with confirmation

  @discord
  Scenario: Unauthorized admin command
    Given the user does not have admin role
    When the user sends "!admin refresh_markets" in Discord
    Then the bot should deny the admin command
    And the bot should respond with an authorization error 