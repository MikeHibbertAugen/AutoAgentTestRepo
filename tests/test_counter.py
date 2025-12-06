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


def test_counter_initializes_with_starting_value_one(counter: Counter) -> None:
    """
    Scenario 1: Counter initializes with starting value 1.
    
    Given a new Counter instance is created
    When we check its initial value
    Then the counter should start at 1
    """
    assert counter.get_value() == 1


def test_counter_increments_by_one(counter: Counter) -> None:
    """
    Scenario 2: Counter increments by one.
    
    Given a counter with value 1
    When we increment it once
    Then the counter should be 2
    """
    counter.increment()
    assert counter.get_value() == 2


def test_counter_increments_sequentially_multiple_times(counter: Counter) -> None:
    """
    Scenario 3: Counter increments sequentially multiple times.
    
    Given a counter with value 1
    When we increment it 5 times
    Then the counter should be 6
    """
    for _ in range(5):
        counter.increment()
    
    assert counter.get_value() == 6


def test_counter_reaches_maximum_value_of_ten(counter: Counter) -> None:
    """
    Scenario 4: Counter reaches maximum value of 10.
    
    Given a counter with value 1
    When we increment it 9 times
    Then the counter should be 10
    """
    for _ in range(9):
        counter.increment()
    
    assert counter.get_value() == 10


def test_get_current_counter_value(counter: Counter) -> None:
    """
    Scenario 5: Get current counter value.
    
    Given a counter with value 1
    When we increment it 3 times
    Then get_value() should return 4
    """
    counter.increment()
    counter.increment()
    counter.increment()
    
    assert counter.get_value() == 4