"""
Unit tests for the Counter class.

This module contains pytest-based unit tests covering all BDD scenarios
for the Counter class implementation.
"""

import pytest
from src.counter import Counter


@pytest.fixture
def counter():
    """Fixture to provide a fresh Counter instance for each test."""
    return Counter()


def test_counter_initializes_with_starting_value_one(counter):
    """
    Test that a new counter starts at value 1.
    
    Given a new counter is created
    When the counter is initialized
    Then the counter value should be 1
    """
    assert counter.get_value() == 1


def test_counter_increments_by_one(counter):
    """
    Test that incrementing the counter increases its value by 1.
    
    Given a counter starting at 1
    When the counter is incremented once
    Then the counter value should be 2
    """
    counter.increment()
    assert counter.get_value() == 2


def test_counter_increments_sequentially_multiple_times(counter):
    """
    Test that the counter increments correctly through multiple increments.
    
    Given a counter starting at 1
    When the counter is incremented 5 times
    Then the counter value should be 6
    """
    for _ in range(5):
        counter.increment()
    assert counter.get_value() == 6


def test_counter_reaches_maximum_value_of_ten(counter):
    """
    Test that the counter can reach its maximum value of 10.
    
    Given a counter starting at 1
    When the counter is incremented 9 times
    Then the counter value should be 10 (the maximum value)
    """
    for _ in range(9):
        counter.increment()
    assert counter.get_value() == 10
    assert counter.get_value() == Counter.MAX_VALUE


def test_get_current_counter_value(counter):
    """
    Test that get_value() returns the correct current value after increments.
    
    Given a counter starting at 1
    When the counter is incremented 3 times
    Then get_value() should return 4
    """
    counter.increment()
    counter.increment()
    counter.increment()
    assert counter.get_value() == 4