Feature: Harmony Calculation
  As a cryptocurrency trader
  I want to calculate position harmony scores
  So that I can identify positions in alignment with market conditions

  Background:
    Given the position analyzer is configured
    And the exchange has the following positions:
      | symbol   | side | contracts | entry_price | mark_price | leverage | liquidation_price |
      | BTCUSDT  | long | 0.5       | 65000       | 68000      | 10       | 59000            |
      | ETHUSDT  | short| 2.0       | 3500        | 3400       | 5        | 3850             |

  @harmony
  Scenario: Calculate basic harmony score
    When I calculate the harmony score for "BTCUSDT"
    Then the harmony score should be between 0 and 1
    And the market alignment should be determined

  @harmony @fibonacci
  Scenario: Harmony score with Fibonacci alignment
    Given the market has the following Fibonacci levels for "BTCUSDT":
      | level | price |
      | 0     | 68000 |
      | 0.236 | 67200 |
      | 0.382 | 66700 |
      | 0.5   | 66000 |
      | 0.618 | 65300 |
      | 0.786 | 64600 |
      | 1     | 64000 |
    When I calculate the harmony score for "BTCUSDT"
    Then the fibonacci retracement harmony should be high
    And the position should be aligned with Fibonacci levels

  @harmony
  Scenario: Golden ratio harmony calculation
    When I calculate golden ratio harmony between prices "68000" and "42027"
    Then the golden ratio harmony should be high

  @harmony
  Scenario Outline: Harmony scores for different market conditions
    Given the exchange position "<symbol>" has mark price "<price>"
    And the market trend for "<symbol>" is "<trend>"
    When I calculate the harmony score for "<symbol>"
    Then the harmony score should be "<score_level>"
    And the market alignment should be "<alignment>"

    Examples:
      | symbol   | price | trend    | score_level | alignment |
      | BTCUSDT  | 70000 | bullish  | high        | ALIGNED   |
      | BTCUSDT  | 62000 | bearish  | low         | MISALIGNED|
      | ETHUSDT  | 3000  | bearish  | high        | ALIGNED   |
      | ETHUSDT  | 3700  | bullish  | low         | MISALIGNED|

  @harmony @portfolio
  Scenario: Portfolio-level harmony calculation
    Given the exchange has multiple positions
    When I calculate the portfolio harmony score
    Then the overall portfolio harmony should be calculated
    And the position correlation harmony should be calculated
    And the position harmony distribution should be calculated

  @harmony @visualization
  Scenario: Harmony score visualization
    When I calculate the harmony score for "BTCUSDT"
    And I request a harmony visualization
    Then a harmony chart should be generated
    And the chart should show alignment with market conditions

  @harmony @risk
  Scenario: Harmony impact on risk assessment
    Given the exchange position "BTCUSDT" has mark price "62000"
    When I calculate the harmony score for "BTCUSDT"
    And I analyze the "BTCUSDT" position
    Then the harmony score should affect the risk assessment
    And positions with low harmony should have higher risk 