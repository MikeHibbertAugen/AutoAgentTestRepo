"""
Unit tests for the Counter class.

This module contains comprehensive pytest tests covering all scenarios
for the Counter class including initialization, validation, counting logic,
boundary conditions, edge cases, and display/output functionality.
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
    assert counter.start == 1
    assert counter.end == 10


def test_custom_initialization() -> None:
    """Test counter initializes with custom start and end values."""
    counter = Counter(start=5, end=15)
    assert counter.start == 5
    assert counter.end == 15


def test_counter_custom_range() -> None:
    """Test counter with custom range generates correct sequence."""
    counter = Counter(start=5, end=8)
    values = list(counter.count())
    assert values == [5, 6, 7, 8]


def test_counter_validation_start_greater_than_end() -> None:
    """Test that ValueError is raised when start > end."""
    with pytest.raises(ValueError, match="Start value must be less than or equal to end value"):
        Counter(start=10, end=5)


def test_counter_validation_non_integer_start() -> None:
    """Test that TypeError is raised for non-integer start value."""
    with pytest.raises(TypeError):
        Counter(start="abc", end=10)


def test_counter_validation_non_integer_end() -> None:
    """Test that TypeError is raised for non-integer end value."""
    with pytest.raises(TypeError):
        Counter(start=1, end="xyz")


def test_counter_default_range() -> None:
    """Test counter with default range (1 to 10)."""
    counter = Counter()
    values = list(counter.count())
    assert values == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test_counter_single_value() -> None:
    """Test counter where start equals end."""
    counter = Counter(start=5, end=5)
    values = list(counter.count())
    assert values == [5]


def test_counter_negative_range() -> None:
    """Test counter with negative values."""
    counter = Counter(start=-5, end=-1)
    values = list(counter.count())
    assert values == [-5, -4, -3, -2, -1]


def test_counter_crossing_zero() -> None:
    """Test counter with range crossing zero."""
    counter = Counter(start=-2, end=2)
    values = list(counter.count())
    assert values == [-2, -1, 0, 1, 2]


def test_counter_execute_output(capsys: pytest.CaptureFixture) -> None:
    """Test counter execute method prints all values."""
    counter = Counter(start=1, end=5)
    counter.execute()
    
    captured = capsys.readouterr()
    lines = captured.out.strip().split('\n')
    
    assert len(lines) == 5
    assert lines == ["1", "2", "3", "4", "5"]


def test_counter_execute_default_output(capsys: pytest.CaptureFixture) -> None:
    """Test counter execute with default parameters (1 to 10)."""
    counter = Counter()
    counter.execute()
    
    captured = capsys.readouterr()
    lines = captured.out.strip().split('\n')
    
    assert len(lines) == 10
    for i, line in enumerate(lines, start=1):
        assert line.strip() == str(i)


def test_counter_execute_single_value(capsys: pytest.CaptureFixture) -> None:
    """Test counter execute with single value."""
    counter = Counter(start=7, end=7)
    counter.execute()
    
    captured = capsys.readouterr()
    assert captured.out.strip() == "7"


def test_counter_execute_negative_range(capsys: pytest.CaptureFixture) -> None:
    """Test counter execute with negative range."""
    counter = Counter(start=-3, end=-1)
    counter.execute()
    
    captured = capsys.readouterr()
    lines = captured.out.strip().split('\n')
    
    assert lines == ["-3", "-2", "-1"]


def test_counter_count_generator() -> None:
    """Test that count() returns a generator."""
    counter = Counter()
    result = counter.count()
    
    # Check it's a generator
    assert hasattr(result, '__iter__')
    assert hasattr(result, '__next__')


def test_counter_count_multiple_iterations() -> None:
    """Test that count() can be called multiple times."""
    counter = Counter(start=1, end=3)
    
    values1 = list(counter.count())
    values2 = list(counter.count())
    
    assert values1 == [1, 2, 3]
    assert values2 == [1, 2, 3]


def test_counter_large_range() -> None:
    """Test counter with large range."""
    counter = Counter(start=1, end=100)
    values = list(counter.count())
    
    assert len(values) == 100
    assert values[0] == 1
    assert values[-1] == 100


def test_counter_validation() -> None:
    """Test explicit validation method."""
    counter = Counter(start=1, end=10)
    # Should not raise any exception
    counter.validate()


def test_counter_str_representation() -> None:
    """Test string representation of counter."""
    counter = Counter(start=5, end=10)
    str_repr = str(counter)
    
    assert "5" in str_repr
    assert "10" in str_repr


def test_counter_repr() -> None:
    """Test repr representation of counter."""
    counter = Counter(start=5, end=10)
    repr_str = repr(counter)
    
    assert "Counter" in repr_str
    assert "5" in repr_str
    assert "10" in repr_str