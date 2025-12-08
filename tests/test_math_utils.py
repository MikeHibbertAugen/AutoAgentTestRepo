"""
Comprehensive unit tests for math_utils module.

Tests the calculate_pi() function with various scenarios including
accuracy, precision, convergence, and performance.
"""

import math
import time
import pytest
from src.math_utils import calculate_pi, PI_PRECISION


class TestCalculatePi:
    """Test suite for the calculate_pi function."""

    def test_pi_accuracy_five_decimals(self):
        """Test that Pi is calculated accurately to 5 decimal places."""
        result = calculate_pi()
        expected = 3.14159
        assert round(result, 5) == expected, (
            f"Expected {expected}, but got {round(result, 5)}"
        )

    def test_pi_return_type(self):
        """Test that the function returns a float."""
        result = calculate_pi()
        assert isinstance(result, float), (
            f"Expected return type float, but got {type(result)}"
        )

    def test_pi_comparison_with_math_pi(self):
        """Test that calculated Pi is close to math.pi."""
        result = calculate_pi()
        # Should be within 0.000005 of math.pi (5 decimal precision)
        assert abs(result - math.pi) < 0.000005, (
            f"Calculated Pi {result} differs too much from math.pi {math.pi}"
        )

    def test_pi_value_range(self):
        """Test that Pi value is within expected range."""
        result = calculate_pi()
        assert 3.14159 <= result <= 3.14160, (
            f"Pi value {result} is outside expected range [3.14159, 3.14160]"
        )

    def test_pi_precision_constant(self):
        """Test that PI_PRECISION constant is correctly defined."""
        assert PI_PRECISION == 5, (
            f"Expected PI_PRECISION to be 5, but got {PI_PRECISION}"
        )

    def test_pi_calculation_performance(self):
        """Test that Pi calculation completes within reasonable time."""
        start_time = time.time()
        calculate_pi()
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Should complete within 2 seconds even on slower systems
        assert elapsed_time < 2.0, (
            f"Calculation took {elapsed_time:.2f}s, expected < 2.0s"
        )

    def test_pi_consistency(self):
        """Test that multiple calls return consistent results."""
        result1 = calculate_pi()
        result2 = calculate_pi()
        result3 = calculate_pi()
        
        assert result1 == result2 == result3, (
            "Multiple calls to calculate_pi() returned different results"
        )

    def test_pi_first_digit(self):
        """Test that the first digit of Pi is correct."""
        result = calculate_pi()
        first_digit = int(result)
        assert first_digit == 3, (
            f"Expected first digit to be 3, but got {first_digit}"
        )

    def test_pi_greater_than_three(self):
        """Test that Pi is greater than 3."""
        result = calculate_pi()
        assert result > 3.0, f"Pi should be greater than 3, but got {result}"

    def test_pi_less_than_four(self):
        """Test that Pi is less than 4."""
        result = calculate_pi()
        assert result < 4.0, f"Pi should be less than 4, but got {result}"


class TestPiCalculationDetails:
    """Detailed tests for Pi calculation algorithm behavior."""

    def test_pi_string_representation(self):
        """Test the string representation of calculated Pi."""
        result = calculate_pi()
        pi_str = f"{result:.5f}"
        assert pi_str == "3.14159", (
            f"Expected '3.14159', but got '{pi_str}'"
        )

    def test_pi_rounds_correctly(self):
        """Test that Pi rounds correctly at 5 decimal places."""
        result = calculate_pi()
        rounded = round(result, 5)
        # Verify individual decimal places
        rounded_str = f"{rounded:.5f}"
        assert rounded_str[0] == '3', "First digit should be 3"
        assert rounded_str[2] == '1', "First decimal should be 1"
        assert rounded_str[3] == '4', "Second decimal should be 4"
        assert rounded_str[4] == '1', "Third decimal should be 1"
        assert rounded_str[5] == '5', "Fourth decimal should be 5"
        assert rounded_str[6] == '9', "Fifth decimal should be 9"

    @pytest.mark.parametrize("decimal_places,expected_min,expected_max", [
        (1, 3.1, 3.2),
        (2, 3.14, 3.15),
        (3, 3.141, 3.142),
        (4, 3.1415, 3.1416),
        (5, 3.14159, 3.14160),
    ])
    def test_pi_at_various_precisions(
        self, decimal_places, expected_min, expected_max
    ):
        """Test Pi accuracy at various decimal precision levels."""
        result = calculate_pi()
        rounded = round(result, decimal_places)
        assert expected_min <= rounded <= expected_max, (
            f"At {decimal_places} decimals, expected Pi between "
            f"{expected_min} and {expected_max}, but got {rounded}"
        )

    def test_pi_not_nan(self):
        """Test that calculated Pi is not NaN."""
        result = calculate_pi()
        assert not math.isnan(result), "Calculated Pi should not be NaN"

    def test_pi_not_infinite(self):
        """Test that calculated Pi is not infinite."""
        result = calculate_pi()
        assert not math.isinf(result), "Calculated Pi should not be infinite"

    def test_pi_positive(self):
        """Test that calculated Pi is positive."""
        result = calculate_pi()
        assert result > 0, f"Pi should be positive, but got {result}"