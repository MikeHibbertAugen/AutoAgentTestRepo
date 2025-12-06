"""
Unit tests for the Counter class.

This module contains comprehensive pytest tests covering all scenarios
for the Counter class including initialization, increment operations,
reset functionality, boundary conditions, edge cases, and display/output
functionality.
"""

import pytest
from src.counter import Counter


@pytest.fixture
def counter() -> Counter:
    """
    Pytest fixture that provides a fresh Counter instance for each test.
    
    Returns:
        Counter: A new Counter instance initialized with default values.
    """
    return Counter()


def test_default_initialization() -> None:
    """Test counter initializes with default start=1 and end=10."""
    counter = Counter()
    assert counter.current == 1
    assert counter.start == 1
    assert counter.end == 10


def test_custom_initialization() -> None:
    """Test counter initializes with custom start and end values."""
    counter = Counter(start=5, end=15)
    assert counter.current == 5
    assert counter.start == 5
    assert counter.end == 15


def test_initial_value_matches_start(counter: Counter) -> None:
    """
    Scenario 1: Initialize counter with default value.
    
    Given a new Counter instance is created
    When we check its initial value
    Then the counter should start at 1
    """
    assert counter.current == 1


def test_increment_counter_by_one(counter: Counter) -> None:
    """
    Scenario 2: Increment counter by one.
    
    Given a counter with value 1
    When we increment it once
    Then the counter should be 2
    """
    counter.increment()
    assert counter.current == 2


def test_increment_counter_multiple_times(counter: Counter) -> None:
    """
    Scenario 3: Increment counter multiple times.
    
    Given a counter with value 1
    When we increment it 3 times
    Then the counter should be 4
    """
    counter.increment()
    counter.increment()
    counter.increment()
    
    assert counter.current == 4


def test_counter_reaches_end_value(counter: Counter) -> None:
    """
    Scenario 5: Counter reaches end value.
    
    Given a counter with value 9
    When we increment it once
    Then the counter should be 10
    """
    # Increment from 1 to 9 (8 increments)
    for _ in range(8):
        counter.increment()
    
    assert counter.current == 9
    
    # Increment from 9 to 10
    counter.increment()
    
    assert counter.current == 10


def test_counter_prevents_exceeding_end(counter: Counter) -> None:
    """
    Scenario 6: Counter prevents exceeding end value.
    
    Given a counter at end value (10)
    When we attempt to increment it
    Then a ValueError should be raised
    """
    # Increment from 1 to 10 (9 increments)
    for _ in range(9):
        counter.increment()
    
    assert counter.current == 10
    
    # Attempt to increment beyond end should raise ValueError
    with pytest.raises(ValueError, match="Counter has reached its end value"):
        counter.increment()
    
    # Verify counter value hasn't changed
    assert counter.current == 10


def test_reset_counter(counter: Counter) -> None:
    """
    Scenario 7: Reset counter.
    
    Given a counter with value 5
    When we reset it
    Then the counter should return to 1
    """
    # Increment to 5
    for _ in range(4):
        counter.increment()
    
    assert counter.current == 5
    
    # Reset counter
    counter.reset()
    
    assert counter.current == 1


def test_has_reached_end_false(counter: Counter) -> None:
    """
    Scenario 8: Check if counter has reached end (not reached).
    
    Given a counter with value 5
    When we check if it has reached the end
    Then it should return False
    """
    # Increment to 5
    for _ in range(4):
        counter.increment()
    
    assert counter.has_reached_end() is False


def test_has_reached_end_true(counter: Counter) -> None:
    """
    Scenario 8: Check if counter has reached end (reached).
    
    Given a counter at value 10
    When we check if it has reached the end
    Then it should return True
    """
    # Increment to 10
    for _ in range(9):
        counter.increment()
    
    assert counter.has_reached_end() is True


def test_custom_range_increment() -> None:
    """Test counter with custom range increments correctly."""
    counter = Counter(start=100, end=105)
    assert counter.current == 100
    
    counter.increment()
    assert counter.current == 101
    
    for _ in range(4):
        counter.increment()
    
    assert counter.current == 105
    assert counter.has_reached_end() is True


def test_custom_range_exceeds_end() -> None:
    """Test counter with custom range raises error when exceeding end."""
    counter = Counter(start=0, end=3)
    
    for _ in range(3):
        counter.increment()
    
    assert counter.current == 3
    
    with pytest.raises(ValueError):
        counter.increment()


def test_reset_with_custom_start() -> None:
    """Test reset returns to custom start value."""
    counter = Counter(start=50, end=60)
    
    for _ in range(5):
        counter.increment()
    
    assert counter.current == 55
    
    counter.reset()
    
    assert counter.current == 50


def test_edge_case_start_equals_end() -> None:
    """Test counter where start equals end."""
    counter = Counter(start=5, end=5)
    assert counter.current == 5
    assert counter.has_reached_end() is True
    
    with pytest.raises(ValueError):
        counter.increment()


def test_negative_range() -> None:
    """Test counter with negative values."""
    counter = Counter(start=-5, end=-1)
    assert counter.current == -5
    
    counter.increment()
    assert counter.current == -4
    
    for _ in range(3):
        counter.increment()
    
    assert counter.current == -1
    assert counter.has_reached_end() is True


def test_invalid_range_start_greater_than_end() -> None:
    """Test that ValueError is raised when start > end."""
    with pytest.raises(ValueError, match="Start value must be less than or equal to end value"):
        Counter(start=10, end=5)


def test_multiple_resets() -> None:
    """Test that reset can be called multiple times."""
    counter = Counter()
    
    counter.increment()
    counter.increment()
    assert counter.current == 3
    
    counter.reset()
    assert counter.current == 1
    
    counter.increment()
    assert counter.current == 2
    
    counter.reset()
    assert counter.current == 1


# Display and Output Functionality Tests


def test_get_all_values_as_list() -> None:
    """
    Scenario 1: Retrieve counter values as a list.
    
    Given a counter initialized from 1 to 10
    When I call get_all_values()
    Then I should receive a list [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    counter = Counter(start=1, end=10)
    values = counter.get_all_values()
    
    assert values == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert isinstance(values, list)
    assert len(values) == 10


def test_display_current_value(capsys: pytest.CaptureFixture) -> None:
    """
    Scenario 2: Display current counter value.
    
    Given a counter initialized from 1 to 10
    And the current value is 5
    When I call display_current()
    Then the output should show "5"
    """
    counter = Counter(start=1, end=10)
    # Increment to value 5
    for _ in range(4):
        counter.increment()
    
    assert counter.current == 5
    
    counter.display_current()
    captured = capsys.readouterr()
    
    assert "5" in captured.out


def test_print_all_sequentially(capsys: pytest.CaptureFixture) -> None:
    """
    Scenario 3: Print all counter values sequentially.
    
    Given a counter initialized from 1 to 10
    When I call print_all()
    Then each number from 1 to 10 should be printed on a separate line
    """
    counter = Counter(start=1, end=10)
    counter.print_all()
    
    captured = capsys.readouterr()
    lines = captured.out.strip().split('\n')
    
    assert len(lines) == 10
    for i, line in enumerate(lines, start=1):
        assert line.strip() == str(i)


def test_get_formatted_string() -> None:
    """
    Scenario 4: Get counter values as formatted string.
    
    Given a counter initialized from 1 to 10
    When I call to_string()
    Then I should receive "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
    """
    counter = Counter(start=1, end=10)
    result = counter.to_string()
    
    assert result == "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
    assert isinstance(result, str)


def test_get_current_value() -> None:
    """Test get_current_value() returns the current counter value."""
    counter = Counter(start=1, end=10)
    
    assert counter.get_current_value() == 1
    
    counter.increment()
    counter.increment()
    
    assert counter.get_current_value() == 3


def test_get_all_values_custom_range() -> None:
    """Test get_all_values() with custom range."""
    counter = Counter(start=5, end=10)
    values = counter.get_all_values()
    
    assert values == [5, 6, 7, 8, 9, 10]


def test_get_all_values_negative_range() -> None:
    """Test get_all_values() with negative range."""
    counter = Counter(start=-3, end=2)
    values = counter.get_all_values()
    
    assert values == [-3, -2, -1, 0, 1, 2]


def test_get_all_values_single_value() -> None:
    """Test get_all_values() when start equals end."""
    counter = Counter(start=7, end=7)
    values = counter.get_all_values()
    
    assert values == [7]
    assert len(values) == 1


def test_to_string_single_value() -> None:
    """Test to_string() with single value."""
    counter = Counter(start=5, end=5)
    result = counter.to_string()
    
    assert result == "5"


def test_to_string_custom_range() -> None:
    """Test to_string() with custom range."""
    counter = Counter(start=100, end=105)
    result = counter.to_string()
    
    assert result == "100, 101, 102, 103, 104, 105"


def test_print_all_custom_range(capsys: pytest.CaptureFixture) -> None:
    """Test print_all() with custom range."""
    counter = Counter(start=3, end=6)
    counter.print_all()
    
    captured = capsys.readouterr()
    lines = captured.out.strip().split('\n')
    
    assert lines == ["3", "4", "5", "6"]


def test_display_current_after_increment(capsys: pytest.CaptureFixture) -> None:
    """Test display_current() shows updated value after increment."""
    counter = Counter(start=1, end=10)
    
    counter.display_current()
    captured1 = capsys.readouterr()
    assert "1" in captured1.out
    
    counter.increment()
    counter.increment()
    
    counter.display_current()
    captured2 = capsys.readouterr()
    assert "3" in captured2.out