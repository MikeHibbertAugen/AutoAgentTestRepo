"""
Unit tests for the Counter class.

This module contains comprehensive pytest tests covering all scenarios
for the Counter class including initialization, increment operations,
and boundary conditions.
"""

import pytest
from src.counter import Counter


@pytest.fixture
def counter() -> Counter:
    """
    Pytest fixture that provides a fresh Counter instance for each test.
    
    Returns:
        Counter: A new Counter instance initialized with default value.
    """
    return Counter()


def test_counter_initializes_with_default_value(counter: Counter) -> None:
    """
    Scenario 1: Initialize counter with default value.
    
    Given a new Counter instance is created
    When we check its initial value
    Then the counter should start at 1
    """
    assert counter.get_value() == 1


def test_counter_increments_to_next_value(counter: Counter) -> None:
    """
    Scenario 2: Increment counter to next value.
    
    Given a counter with value 1
    When we increment it once
    Then the counter should be 2
    And no limit message should be returned
    """
    result = counter.increment()
    assert result is None
    assert counter.get_value() == 2


def test_counter_increments_sequentially(counter: Counter) -> None:
    """
    Scenario 3: Counter increments sequentially.
    
    Given a counter with value 1
    When we increment it 5 times
    Then the counter should be 6
    And all increment operations should return None
    """
    for i in range(5):
        result = counter.increment()
        assert result is None
        assert counter.get_value() == i + 2


def test_counter_reaches_maximum_value(counter: Counter) -> None:
    """
    Scenario 4: Counter reaches maximum value.
    
    Given a counter with value 9
    When we increment it once
    Then the counter should be 10
    And no limit message should be returned
    """
    # Increment from 1 to 9 (8 increments)
    for _ in range(8):
        counter.increment()
    
    assert counter.get_value() == 9
    
    # Increment from 9 to 10
    result = counter.increment()
    
    assert result is None
    assert counter.get_value() == 10


def test_counter_does_not_exceed_maximum(counter: Counter) -> None:
    """
    Scenario 5: Counter does not exceed maximum value.
    
    Given a counter at maximum value (10)
    When we attempt to increment it
    Then the counter should remain at 10
    And an appropriate limit message should be returned
    """
    # Increment from 1 to 10 (9 increments)
    for _ in range(9):
        counter.increment()
    
    assert counter.get_value() == 10
    
    # Attempt to increment beyond maximum
    result = counter.increment()
    
    assert result is not None
    assert isinstance(result, str)
    assert "maximum" in result.lower() or "limit" in result.lower()
    assert counter.get_value() == 10
    
    # Verify multiple attempts still return message and value stays at 10
    result2 = counter.increment()
    
    assert result2 is not None
    assert isinstance(result2, str)
    assert counter.get_value() == 10