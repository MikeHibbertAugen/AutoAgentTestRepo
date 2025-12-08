"""
Comprehensive unit tests for the Pi calculator module.

Tests cover accuracy, type validation, consistency, and precision of the
calculate_pi() function using pytest framework.
"""

import pytest
from decimal import Decimal
from src.pi_calculator import calculate_pi


class TestPiCalculator:
    """Test suite for Pi calculator functionality."""

    def test_basic_functionality(self):
        """Test that calculate_pi returns the correct value to 9 decimal places."""
        result = calculate_pi()
        expected = 3.141592654
        assert result == expected, f"Expected {expected}, got {result}"

    def test_return_type(self):
        """Test that calculate_pi returns a float type."""
        result = calculate_pi()
        assert isinstance(result, float), f"Expected float, got {type(result)}"

    def test_precision_nine_decimals(self):
        """Test that the result has exactly 9 decimal places."""
        result = calculate_pi()
        result_str = str(result)
        
        # Check format: should be 3.141592654
        assert result_str == "3.141592654", (
            f"Expected '3.141592654', got '{result_str}'"
        )
        
        # Verify decimal places
        if '.' in result_str:
            decimal_part = result_str.split('.')[1]
            assert len(decimal_part) == 9, (
                f"Expected 9 decimal places, got {len(decimal_part)}"
            )

    def test_consistency(self):
        """Test that multiple calls return the same result."""
        results = [calculate_pi() for _ in range(10)]
        assert all(r == results[0] for r in results), (
            "Multiple calls should return identical results"
        )

    def test_mathematical_accuracy(self):
        """Test accuracy against known value of Pi."""
        result = calculate_pi()
        # Pi to higher precision: 3.14159265358979323846...
        # Our result should be 3.141592654 (rounded to 9 decimals)
        assert abs(result - 3.141592654) < 1e-10, (
            "Result deviates from expected Pi value"
        )

    def test_value_range(self):
        """Test that Pi is within expected mathematical bounds."""
        result = calculate_pi()
        assert 3.14 < result < 3.15, (
            f"Pi should be between 3.14 and 3.15, got {result}"
        )

    def test_greater_than_three(self):
        """Test that Pi is greater than 3."""
        result = calculate_pi()
        assert result > 3.0, "Pi should be greater than 3"

    def test_less_than_four(self):
        """Test that Pi is less than 4."""
        result = calculate_pi()
        assert result < 4.0, "Pi should be less than 4"

    def test_not_equal_to_simple_fractions(self):
        """Test that Pi is not equal to common approximations."""
        result = calculate_pi()
        assert result != 22/7, "Pi should not equal 22/7"
        assert result != 3.14, "Pi should not equal 3.14"

    def test_specific_decimal_digits(self):
        """Test specific digits of Pi to ensure correctness."""
        result = calculate_pi()
        result_str = f"{result:.9f}"
        
        # Verify specific digits: 3.141592654
        assert result_str[0] == '3', "First digit should be 3"
        assert result_str[2] == '1', "First decimal should be 1"
        assert result_str[3] == '4', "Second decimal should be 4"
        assert result_str[4] == '1', "Third decimal should be 1"
        assert result_str[5] == '5', "Fourth decimal should be 5"
        assert result_str[6] == '9', "Fifth decimal should be 9"
        assert result_str[7] == '2', "Sixth decimal should be 2"
        assert result_str[8] == '6', "Seventh decimal should be 6"
        assert result_str[9] == '5', "Eighth decimal should be 5"
        assert result_str[10] == '4', "Ninth decimal should be 4"


class TestPiCalculatorPerformance:
    """Performance and edge case tests."""

    def test_performance_benchmark(self):
        """Test that calculation completes in reasonable time."""
        import time
        
        start_time = time.time()
        calculate_pi()
        elapsed_time = time.time() - start_time
        
        # Should complete in less than 1 second
        assert elapsed_time < 1.0, (
            f"Calculation took {elapsed_time:.3f}s, should be < 1.0s"
        )

    def test_repeated_calls_performance(self):
        """Test performance of multiple sequential calls."""
        import time
        
        start_time = time.time()
        for _ in range(100):
            calculate_pi()
        elapsed_time = time.time() - start_time
        
        # 100 calls should complete in less than 5 seconds
        assert elapsed_time < 5.0, (
            f"100 calls took {elapsed_time:.3f}s, should be < 5.0s"
        )