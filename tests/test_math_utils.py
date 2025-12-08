"""
Comprehensive unit tests for the math_utils module.

This module tests the calculate_pi() function to ensure:
- Accuracy to 12 decimal places
- Correct return type (Decimal)
- Precision consistency
- Repeatability of results
"""

import pytest
from decimal import Decimal
from src.math_utils import calculate_pi


class TestCalculatePi:
    """Test suite for the calculate_pi function."""

    def test_pi_accuracy_12_decimals(self):
        """Test that Pi is calculated accurately to 12 decimal places."""
        result = calculate_pi()
        # Known value of Pi to 12 decimal places: 3.141592653589
        expected_str = "3.141592653589"
        result_str = str(result)[:14]  # Get first 14 characters (3.141592653589)
        assert result_str == expected_str, f"Expected {expected_str}, got {result_str}"

    def test_pi_return_type(self):
        """Test that the function returns a Decimal type."""
        result = calculate_pi()
        assert isinstance(result, Decimal), f"Expected Decimal type, got {type(result)}"

    def test_pi_consistency(self):
        """Test that multiple calls return identical results."""
        result1 = calculate_pi()
        result2 = calculate_pi()
        result3 = calculate_pi()
        assert result1 == result2 == result3, "Multiple calls should return identical results"

    def test_pi_precision_no_loss(self):
        """Test that precision is maintained through calculations."""
        result = calculate_pi()
        # Verify that we have at least 12 decimal places of precision
        result_str = str(result)
        # Remove the "3." prefix and check we have at least 12 digits
        decimal_part = result_str.split('.')[1]
        assert len(decimal_part) >= 12, f"Expected at least 12 decimal places, got {len(decimal_part)}"

    def test_pi_value_greater_than_3(self):
        """Test that Pi is greater than 3."""
        result = calculate_pi()
        assert result > Decimal('3'), "Pi should be greater than 3"

    def test_pi_value_less_than_4(self):
        """Test that Pi is less than 4."""
        result = calculate_pi()
        assert result < Decimal('4'), "Pi should be less than 4"

    def test_pi_specific_decimal_places(self):
        """Test specific decimal places against known Pi value."""
        result = calculate_pi()
        # Test against Pi = 3.141592653589793...
        # Check each decimal place individually
        result_str = str(result)
        assert result_str[0] == '3', "First digit should be 3"
        assert result_str[2] == '1', "First decimal place should be 1"
        assert result_str[3] == '4', "Second decimal place should be 4"
        assert result_str[4] == '1', "Third decimal place should be 1"
        assert result_str[5] == '5', "Fourth decimal place should be 5"
        assert result_str[6] == '9', "Fifth decimal place should be 9"
        assert result_str[7] == '2', "Sixth decimal place should be 2"
        assert result_str[8] == '6', "Seventh decimal place should be 6"
        assert result_str[9] == '5', "Eighth decimal place should be 5"
        assert result_str[10] == '3', "Ninth decimal place should be 3"
        assert result_str[11] == '5', "Tenth decimal place should be 5"
        assert result_str[12] == '8', "Eleventh decimal place should be 8"
        assert result_str[13] == '9', "Twelfth decimal place should be 9"

    def test_pi_performance(self):
        """Test that Pi calculation completes in reasonable time."""
        import time
        start_time = time.time()
        calculate_pi()
        end_time = time.time()
        elapsed = end_time - start_time
        # Should complete in less than 1 second
        assert elapsed < 1.0, f"Calculation took {elapsed}s, expected < 1.0s"

    def test_pi_immutability(self):
        """Test that the returned Decimal is a new object each time."""
        result1 = calculate_pi()
        result2 = calculate_pi()
        # Values should be equal but not the same object
        assert result1 == result2
        assert result1 is not result2, "Should return new Decimal objects"