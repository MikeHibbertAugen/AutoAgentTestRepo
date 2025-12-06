"""
Unit tests for the Counter class.

This module contains comprehensive pytest tests covering all scenarios
for the Counter class including initialization, increment operations,
reset functionality, and boundary conditions.
"""

import pytest
from src.counter import Counter


@pytest.fixture
def counter() -> Counter:
    """
    Pytest fixture that provides a fresh Counter instance for each test.
    
    Returns:
        Counter: A new Counter instance initialized with default values (1 to 10).
    """
    return Counter()


def test_initialize_counter_default_values(counter: Counter) -> None:
    """
    Scenario 1: Initialize counter with default values.
    
    Given a new Counter instance is created with no arguments
    When we check its initial state
    Then the counter should start at 1
    And the end value should be 10
    """
    assert counter.current == 1
    assert counter.start == 1
    assert counter.end == 10
    assert counter.get_current() == 1


def test_initialize_counter_custom_range() -> None:
    """
    Scenario 2: Initialize counter with custom range.
    
    Given a new Counter instance is created with start=5 and end=15
    When we check its initial state
    Then the counter should start at 5
    And the end value should be 15
    """
    custom_counter = Counter(start=5, end=15)
    
    assert custom_counter.current == 5
    assert custom_counter.start == 5
    assert custom_counter.end == 15


def test_increment_counter_by_one(counter: Counter) -> None:
    """
    Scenario 3: Increment counter by one.
    
    Given a counter with value 1
    When we increment it once
    Then the counter should be 2
    """
    counter.increment()
    
    assert counter.get_current() == 2
    assert counter.current == 2


def test_get_current_counter_value(counter: Counter) -> None:
    """
    Scenario 4: Get current counter value.
    
    Given a counter that has been incremented twice
    When we get its value
    Then it should return 3
    """
    counter.increment()
    counter.increment()
    
    assert counter.get_current() == 3
    assert counter.current == 3


def test_increment_counter_multiple_times(counter: Counter) -> None:
    """
    Scenario 5: Increment counter multiple times.
    
    Given a counter with value 1
    When we increment it 5 times
    Then the counter should be 6
    """
    for _ in range(5):
        counter.increment()
    
    assert counter.get_current() == 6


def test_counter_reaches_maximum_value(counter: Counter) -> None:
    """
    Scenario 6: Counter reaches maximum value.
    
    Given a counter with value 9
    When we increment it once
    Then the counter should be 10
    And has_reached_end() should return True
    """
    # Increment from 1 to 9 (8 increments)
    for _ in range(8):
        counter.increment()
    
    assert counter.get_current() == 9
    assert counter.has_reached_end() is False
    
    # Increment from 9 to 10
    counter.increment()
    
    assert counter.get_current() == 10
    assert counter.has_reached_end() is True


def test_increment_beyond_maximum_raises_exception(counter: Counter) -> None:
    """
    Scenario 7: Increment beyond maximum raises exception.
    
    Given a counter at maximum value (10)
    When we attempt to increment it
    Then it should raise a ValueError
    And the error message should indicate the counter is at maximum
    """
    # Increment from 1 to 10 (9 increments)
    for _ in range(9):
        counter.increment()
    
    assert counter.get_current() == 10
    assert counter.has_reached_end() is True
    
    # Attempt to increment beyond maximum should raise ValueError
    with pytest.raises(ValueError, match="Cannot increment: counter has reached maximum value"):
        counter.increment()
    
    # Verify counter value remains unchanged
    assert counter.get_current() == 10


def test_reset_counter_to_initial_value(counter: Counter) -> None:
    """
    Scenario 8: Reset counter to initial value.
    
    Given a counter that has been incremented to 7
    When we reset the counter
    Then the counter should return to its initial value of 1
    And has_reached_end() should return False
    """
    # Increment counter to 7
    for _ in range(6):
        counter.increment()
    
    assert counter.get_current() == 7
    
    # Reset the counter
    counter.reset()
    
    assert counter.get_current() == 1
    assert counter.current == 1
    assert counter.has_reached_end() is False


def test_reset_counter_with_custom_range() -> None:
    """
    Additional test: Reset counter with custom range.
    
    Given a counter with custom start=5 and end=10
    When incremented and then reset
    Then it should return to start value of 5
    """
    custom_counter = Counter(start=5, end=10)
    
    custom_counter.increment()
    custom_counter.increment()
    
    assert custom_counter.get_current() == 7
    
    custom_counter.reset()
    
    assert custom_counter.get_current() == 5
    assert custom_counter.start == 5