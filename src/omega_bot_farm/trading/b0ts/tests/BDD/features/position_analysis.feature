Feature: Position Analysis
  As a cryptocurrency trader
  I want to analyze my open positions
  So that I can make informed trading decisions

  Background:
    Given the position analyzer is configured
    And the exchange has the following positions:
      | symbol   | side | contracts | entry_price | mark_price | leverage | liquidation_price |
      | BTCUSDT  | long | 0.5       | 65000       | 68000      | 10       | 59000            |
      | ETHUSDT  | short| 2.0       | 3500        | 3400       | 5        | 3850             |

  @position
  Scenario: Analyze basic position details
    When I analyze the "BTCUSDT" position
    Then the analysis should include position details
    And the unrealized PnL should be calculated correctly
    And the position leverage should be 10

  @position @risk
  Scenario: Assess position risk level
    When I analyze the "BTCUSDT" position
    Then the risk assessment should be "LOW"
    And the liquidation distance percentage should be greater than 10%

  @position @risk
  Scenario: Detect high-risk position
    Given the exchange position "ETHUSDT" has mark price "3700"
    When I analyze the "ETHUSDT" position
    Then the risk assessment should be "HIGH"
    And the liquidation distance percentage should be less than 5%

  @position @fibonacci
  Scenario: Calculate Fibonacci levels for position
    When I analyze the "BTCUSDT" position with Fibonacci analysis
    Then the analysis should include Fibonacci levels
    And the current price should be at one of the Fibonacci levels
    And the next support level should be identified

  @position
  Scenario: Generate position recommendations
    When I analyze the "BTCUSDT" position
    Then the analysis should include a recommendation
    And the recommendation should have an action and reasoning

  @position @harmony
  Scenario: Calculate position harmony score
    When I analyze the "BTCUSDT" position with harmony calculations
    Then the analysis should include a harmony score between 0 and 1
    And the market alignment should be determined

  @position
  Scenario Outline: Analyze positions with different market conditions
    Given the exchange position "<symbol>" has mark price "<price>"
    When I analyze the "<symbol>" position
    Then the unrealized PnL direction should be "<pnl_direction>"
    And the risk assessment should be "<risk_level>"

    Examples:
      | symbol   | price | pnl_direction | risk_level |
      | BTCUSDT  | 70000 | positive      | LOW        |
      | BTCUSDT  | 62000 | negative      | MEDIUM     |
      | BTCUSDT  | 60000 | negative      | HIGH       |
      | ETHUSDT  | 3000  | positive      | LOW        |
      | ETHUSDT  | 3700  | negative      | HIGH       |

  @position @visualization
  Scenario: Generate position visualization
    When I analyze the "BTCUSDT" position
    And I request a visualization of the analysis
    Then a position chart should be generated
    And a risk gauge chart should be generated
    And a Fibonacci levels chart should be generated 