"""
Unit tests for the math_utils module.

Tests the calculate_pi() function to ensure it returns Pi accurate to 6 decimal places.
"""

import pytest
from src.math_utils import calculate_pi


def test_calculate_pi_accuracy():
    """Test that calculate_pi returns Pi accurate to 6 decimal places."""
    result = calculate_pi()
    expected = 3.141593
    assert round(result, 6) == expected


def test_calculate_pi_precision():
    """Test that calculate_pi returns a value very close to the mathematical constant Pi."""
    result = calculate_pi()
    # Using a small epsilon for floating-point comparison
    assert abs(result - 3.141592653589793) < 1e-6


def test_calculate_pi_return_type():
    """Test that calculate_pi returns a float type."""
    result = calculate_pi()
    assert isinstance(result, float)


def test_calculate_pi_reproducibility():
    """Test that calculate_pi returns the same result on multiple calls."""
    result1 = calculate_pi()
    result2 = calculate_pi()
    result3 = calculate_pi()
    assert result1 == result2 == result3


def test_calculate_pi_positive():
    """Test that calculate_pi returns a positive value."""
    result = calculate_pi()
    assert result > 0


def test_calculate_pi_range():
    """Test that calculate_pi returns a value within the expected range."""
    result = calculate_pi()
    # Pi should be between 3.14 and 3.15
    assert 3.14 < result < 3.15


def test_calculate_pi_exact_digits():
    """Test that the first 6 decimal places match the expected value."""
    result = calculate_pi()
    result_str = f"{result:.6f}"
    expected_str = "3.141593"
    assert result_str == expected_str


def test_calculate_pi_greater_than_three():
    """Test that calculate_pi returns a value greater than 3."""
    result = calculate_pi()
    assert result > 3.0


def test_calculate_pi_less_than_four():
    """Test that calculate_pi returns a value less than 4."""
    result = calculate_pi()
    assert result < 4.0