"""
Comprehensive test suite for the Pi calculator module.

Tests the calculate_pi() function for accuracy, precision, output format,
and performance. Validates against known Pi value to 12 decimal places.
"""

import pytest
from decimal import Decimal
from src.pi_calculator import calculate_pi, _arctan, PI_PRECISION


class TestCalculatePi:
    """Test suite for the calculate_pi() function."""

    def test_calculate_pi_returns_string(self):
        """Test that calculate_pi() returns a string."""
        result = calculate_pi()
        assert isinstance(result, str)

    def test_calculate_pi_correct_value(self):
        """Test that calculate_pi() returns the correct value of Pi to 12 decimal places."""
        result = calculate_pi()
        expected = "3.141592653589"
        assert result == expected

    def test_calculate_pi_exact_precision(self):
        """Test that the result has exactly 12 decimal places."""
        result = calculate_pi()
        # Split by decimal point and check decimal places
        parts = result.split(".")
        assert len(parts) == 2
        assert len(parts[1]) == PI_PRECISION

    def test_calculate_pi_format(self):
        """Test that the result is properly formatted."""
        result = calculate_pi()
        # Should be able to convert back to Decimal
        decimal_result = Decimal(result)
        assert decimal_result > 3
        assert decimal_result < 4

    def test_calculate_pi_consistency(self):
        """Test that multiple calls return the same result (deterministic)."""
        result1 = calculate_pi()
        result2 = calculate_pi()
        result3 = calculate_pi()
        assert result1 == result2 == result3

    def test_calculate_pi_starts_with_3(self):
        """Test that Pi starts with 3."""
        result = calculate_pi()
        assert result.startswith("3.")

    def test_calculate_pi_performance(self):
        """Test that calculation completes in reasonable time (< 1 second)."""
        import time
        start = time.time()
        calculate_pi()
        end = time.time()
        elapsed = end - start
        assert elapsed < 1.0, f"Calculation took {elapsed} seconds, expected < 1 second"


class TestArctanHelper:
    """Test suite for the _arctan() helper function."""

    def test_arctan_one_fifth(self):
        """Test arctan(1/5) calculation."""
        result = _arctan(Decimal(1) / Decimal(5))
        # arctan(1/5) ≈ 0.197395559849881
        assert isinstance(result, Decimal)
        assert abs(result - Decimal("0.197395559849881")) < Decimal("1e-12")

    def test_arctan_one_239th(self):
        """Test arctan(1/239) calculation."""
        result = _arctan(Decimal(1) / Decimal(239))
        # arctan(1/239) ≈ 0.004184076886089
        assert isinstance(result, Decimal)
        assert abs(result - Decimal("0.004184076886089")) < Decimal("1e-12")

    def test_arctan_zero(self):
        """Test arctan(0) = 0."""
        result = _arctan(Decimal(0))
        assert result == Decimal(0)

    def test_arctan_small_value(self):
        """Test arctan with very small value."""
        result = _arctan(Decimal("0.001"))
        # For small x, arctan(x) ≈ x
        assert abs(result - Decimal("0.001")) < Decimal("0.0001")

    def test_arctan_returns_decimal(self):
        """Test that _arctan returns a Decimal type."""
        result = _arctan(Decimal("0.5"))
        assert isinstance(result, Decimal)


class TestPiPrecisionConstant:
    """Test suite for module-level constants."""

    def test_pi_precision_constant_exists(self):
        """Test that PI_PRECISION constant is defined."""
        assert PI_PRECISION is not None

    def test_pi_precision_value(self):
        """Test that PI_PRECISION equals 12."""
        assert PI_PRECISION == 12

    def test_pi_precision_type(self):
        """Test that PI_PRECISION is an integer."""
        assert isinstance(PI_PRECISION, int)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_calculate_pi_no_parameters(self):
        """Test that calculate_pi() works without parameters."""
        result = calculate_pi()
        assert result is not None

    def test_result_decimal_conversion(self):
        """Test that result can be converted to various numeric types."""
        result = calculate_pi()
        # Should be convertible to Decimal
        as_decimal = Decimal(result)
        assert as_decimal > 0
        # Should be convertible to float
        as_float = float(result)
        assert as_float > 3.14
        assert as_float < 3.15

    def test_known_digits_verification(self):
        """Test specific known digits of Pi."""
        result = calculate_pi()
        # First 12 decimal places: 3.141592653589
        assert result[0] == "3"
        assert result[2] == "1"  # First digit after decimal
        assert result[3] == "4"
        assert result[4] == "1"
        assert result[5] == "5"
        assert result[6] == "9"
        assert result[7] == "2"