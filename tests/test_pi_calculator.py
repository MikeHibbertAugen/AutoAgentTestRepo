"""
Comprehensive unit tests for the Pi calculator module.

This module tests the calculate_pi() function to ensure it returns Pi
accurate to 11 decimal places using Machin's formula.
"""

import math
import pytest
from src.pi_calculator import calculate_pi, _calculate_arctan, PI_PRECISION


class TestCalculatePi:
    """Test suite for the calculate_pi function."""

    def test_pi_accuracy_to_11_decimals(self):
        """Test that calculate_pi returns Pi accurate to 11 decimal places."""
        result = calculate_pi()
        expected = 3.14159265359
        assert f"{result:.11f}" == f"{expected:.11f}"

    def test_pi_precision_against_math_pi(self):
        """Test that the result is within acceptable tolerance of math.pi."""
        result = calculate_pi()
        tolerance = 1e-11
        assert abs(result - math.pi) < tolerance

    def test_return_type_is_float(self):
        """Test that calculate_pi returns a float type."""
        result = calculate_pi()
        assert isinstance(result, float)

    def test_consistency_across_calls(self):
        """Test that multiple calls return the same value."""
        result1 = calculate_pi()
        result2 = calculate_pi()
        result3 = calculate_pi()
        assert result1 == result2 == result3

    def test_pi_value_is_positive(self):
        """Test that the returned Pi value is positive."""
        result = calculate_pi()
        assert result > 0

    def test_pi_value_in_expected_range(self):
        """Test that Pi is in the expected range (3.14 to 3.15)."""
        result = calculate_pi()
        assert 3.14 < result < 3.15

    def test_pi_matches_known_digits(self):
        """Test that Pi matches known digits: 3.14159265358979..."""
        result = calculate_pi()
        # Check first 11 decimal places
        assert pytest.approx(result, abs=1e-11) == 3.14159265359


class TestCalculateArctan:
    """Test suite for the _calculate_arctan helper function."""

    def test_arctan_of_zero(self):
        """Test that arctan(0) returns 0."""
        result = _calculate_arctan(0, 50)
        assert pytest.approx(result, abs=1e-15) == 0.0

    def test_arctan_one_fifth(self):
        """Test arctan(1/5) against known value."""
        result = _calculate_arctan(1/5, 50)
        expected = math.atan(1/5)
        assert pytest.approx(result, abs=1e-11) == expected

    def test_arctan_one_over_239(self):
        """Test arctan(1/239) against known value."""
        result = _calculate_arctan(1/239, 50)
        expected = math.atan(1/239)
        assert pytest.approx(result, abs=1e-11) == expected

    def test_arctan_return_type(self):
        """Test that _calculate_arctan returns a float."""
        result = _calculate_arctan(0.5, 50)
        assert isinstance(result, float)

    def test_arctan_with_sufficient_terms(self):
        """Test that sufficient terms provide accurate results."""
        x = 0.2
        result = _calculate_arctan(x, 100)
        expected = math.atan(x)
        assert pytest.approx(result, abs=1e-12) == expected

    def test_arctan_negative_value(self):
        """Test arctan with negative value."""
        x = -0.5
        result = _calculate_arctan(x, 50)
        expected = math.atan(x)
        assert pytest.approx(result, abs=1e-11) == expected


class TestPiPrecisionConstant:
    """Test suite for the PI_PRECISION constant."""

    def test_precision_constant_exists(self):
        """Test that PI_PRECISION constant is defined."""
        assert PI_PRECISION is not None

    def test_precision_constant_value(self):
        """Test that PI_PRECISION has the expected value of 11."""
        assert PI_PRECISION == 11

    def test_precision_constant_type(self):
        """Test that PI_PRECISION is an integer."""
        assert isinstance(PI_PRECISION, int)


class TestMachinsFormula:
    """Test suite verifying Machin's formula implementation."""

    def test_machins_formula_components(self):
        """Test that Machin's formula components are calculated correctly."""
        # π/4 = 4*arctan(1/5) - arctan(1/239)
        arctan_1_5 = _calculate_arctan(1/5, 50)
        arctan_1_239 = _calculate_arctan(1/239, 50)
        
        pi_over_4 = 4 * arctan_1_5 - arctan_1_239
        calculated_pi = 4 * pi_over_4
        
        assert pytest.approx(calculated_pi, abs=1e-11) == math.pi

    def test_formula_matches_calculate_pi(self):
        """Test that manual formula calculation matches calculate_pi()."""
        result = calculate_pi()
        
        # Manual calculation using Machin's formula
        arctan_1_5 = _calculate_arctan(1/5, 50)
        arctan_1_239 = _calculate_arctan(1/239, 50)
        manual_pi = 4 * (4 * arctan_1_5 - arctan_1_239)
        
        assert pytest.approx(result, abs=1e-15) == manual_pi