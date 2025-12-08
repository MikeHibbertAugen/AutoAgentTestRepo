"""
Unit tests for the Pi calculator module.

Tests the calculate_pi() function for accuracy, precision, type correctness,
and performance characteristics.
"""

import pytest
from decimal import Decimal
import time
from src.pi_calculator import calculate_pi, DEFAULT_PRECISION


def test_calculate_pi_accuracy():
    """Test that calculate_pi returns Pi accurate to 10 decimal places."""
    result = calculate_pi()
    expected = 3.1415926536
    
    # Check accuracy to 10 decimal places
    assert round(result, 10) == expected
    
    # Verify it's close to the actual value of Pi
    actual_pi = 3.141592653589793
    assert abs(result - actual_pi) < 1e-10


def test_calculate_pi_return_type():
    """Test that calculate_pi returns a float type."""
    result = calculate_pi()
    assert isinstance(result, float)


def test_calculate_pi_precision_parameter():
    """Test calculate_pi with different precision values."""
    # Test with lower precision
    result_5 = calculate_pi(precision=5)
    assert round(result_5, 5) == 3.14159
    
    # Test with higher precision
    result_15 = calculate_pi(precision=15)
    expected_15 = 3.141592653589793
    assert abs(result_15 - expected_15) < 1e-15


def test_calculate_pi_default_precision():
    """Test that default precision is used when not specified."""
    result = calculate_pi()
    result_with_default = calculate_pi(precision=DEFAULT_PRECISION)
    assert result == result_with_default


def test_calculate_pi_performance():
    """Test that calculate_pi executes within reasonable time."""
    start_time = time.time()
    calculate_pi()
    end_time = time.time()
    
    execution_time = end_time - start_time
    # Should complete in less than 100ms
    assert execution_time < 0.1


def test_calculate_pi_consistency():
    """Test that calculate_pi returns consistent results across multiple calls."""
    result1 = calculate_pi()
    result2 = calculate_pi()
    result3 = calculate_pi()
    
    assert result1 == result2 == result3


def test_calculate_pi_precision_validation():
    """Test that invalid precision values are handled appropriately."""
    # Test with precision of 1 (minimum reasonable value)
    result = calculate_pi(precision=1)
    assert round(result, 1) == 3.1
    
    # Test with very high precision
    result_high = calculate_pi(precision=30)
    assert isinstance(result_high, float)


def test_calculate_pi_matches_known_digits():
    """Test that the result matches known digits of Pi."""
    result = calculate_pi(precision=20)
    
    # Known value of Pi to 20+ decimal places
    known_pi = 3.14159265358979323846
    
    # Check that result is very close
    assert abs(result - known_pi) < 1e-20