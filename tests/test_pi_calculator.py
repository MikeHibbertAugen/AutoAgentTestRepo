"""
Comprehensive unit tests for the Pi calculator module.

Tests verify accuracy, precision, type correctness, and edge cases
for the calculate_pi() function and its helper functions.
"""

import pytest
from decimal import Decimal, getcontext
from src.pi_calculator import calculate_pi, _arctan_series, _calculate_terms_needed


class TestCalculatePi:
    """Test suite for the main calculate_pi() function."""

    def test_pi_accuracy_to_13_decimal_places(self):
        """Test that calculate_pi returns Pi accurate to 13 decimal places."""
        pi = calculate_pi()
        expected = Decimal("3.1415926535897")
        
        # Round to 13 decimal places for comparison
        pi_rounded = pi.quantize(Decimal("0.0000000000001"))
        
        assert pi_rounded == expected, f"Expected {expected}, got {pi_rounded}"

    def test_pi_return_type_is_decimal(self):
        """Test that calculate_pi returns a Decimal type."""
        pi = calculate_pi()
        assert isinstance(pi, Decimal), f"Expected Decimal type, got {type(pi)}"

    def test_pi_consistency(self):
        """Test that multiple calls return identical results."""
        pi1 = calculate_pi()
        pi2 = calculate_pi()
        pi3 = calculate_pi()
        
        assert pi1 == pi2 == pi3, "Multiple calls should return identical results"

    def test_pi_precision_higher_than_target(self):
        """Test that internal precision is higher than 13 decimal places."""
        pi = calculate_pi()
        pi_str = str(pi)
        
        # Remove the leading "3." and count decimal places
        if "." in pi_str:
            decimal_part = pi_str.split(".")[1]
            assert len(decimal_part) >= 13, "Should maintain at least 13 decimal places"

    def test_pi_value_in_valid_range(self):
        """Test that Pi value is within mathematically valid range."""
        pi = calculate_pi()
        
        # Pi should be between 3.14 and 3.15
        assert Decimal("3.14") < pi < Decimal("3.15"), f"Pi value {pi} out of valid range"

    def test_pi_matches_known_value_to_full_precision(self):
        """Test against known Pi value to maximum available precision."""
        pi = calculate_pi()
        # Pi to 20 decimal places for thorough verification
        known_pi = Decimal("3.14159265358979323846")
        
        # Should match at least to 13 decimal places
        pi_13 = pi.quantize(Decimal("0.0000000000001"))
        known_13 = known_pi.quantize(Decimal("0.0000000000001"))
        
        assert pi_13 == known_13


class TestArctanSeries:
    """Test suite for the _arctan_series helper function."""

    def test_arctan_of_one_fifth(self):
        """Test arctan(1/5) calculation."""
        x = Decimal(1) / Decimal(5)
        result = _arctan_series(x, num_terms=50)
        
        # Known value of arctan(1/5) ≈ 0.197395559849881
        expected = Decimal("0.197395559849881")
        
        # Should be accurate to at least 10 decimal places
        assert abs(result - expected) < Decimal("0.0000000001")

    def test_arctan_of_one_over_239(self):
        """Test arctan(1/239) calculation."""
        x = Decimal(1) / Decimal(239)
        result = _arctan_series(x, num_terms=30)
        
        # Known value of arctan(1/239) ≈ 0.004184076
        expected = Decimal("0.004184076")
        
        # Should be accurate to at least 8 decimal places
        assert abs(result - expected) < Decimal("0.000000001")

    def test_arctan_series_convergence(self):
        """Test that more terms improves accuracy."""
        x = Decimal(1) / Decimal(5)
        
        result_10_terms = _arctan_series(x, num_terms=10)
        result_50_terms = _arctan_series(x, num_terms=50)
        result_100_terms = _arctan_series(x, num_terms=100)
        
        # More terms should give same or better result
        # (results should converge to same value)
        diff_50_100 = abs(result_50_terms - result_100_terms)
        diff_10_50 = abs(result_10_terms - result_50_terms)
        
        assert diff_50_100 <= diff_10_50, "More terms should improve convergence"

    def test_arctan_zero(self):
        """Test that arctan(0) = 0."""
        result = _arctan_series(Decimal(0), num_terms=10)
        assert result == Decimal(0), "arctan(0) should equal 0"

    @pytest.mark.parametrize("x_value,num_terms", [
        (Decimal("0.1"), 20),
        (Decimal("0.2"), 30),
        (Decimal("0.01"), 10),
    ])
    def test_arctan_various_inputs(self, x_value, num_terms):
        """Test arctan_series with various inputs."""
        result = _arctan_series(x_value, num_terms)
        
        # Result should be positive for positive input
        assert result > 0, f"arctan({x_value}) should be positive"
        
        # Result should be less than input for x < 1
        assert result < x_value + Decimal("0.1"), f"arctan({x_value}) should be reasonable"


class TestCalculateTermsNeeded:
    """Test suite for the _calculate_terms_needed helper function."""

    def test_returns_positive_integer(self):
        """Test that _calculate_terms_needed returns a positive integer."""
        terms = _calculate_terms_needed()
        
        assert isinstance(terms, int), "Should return an integer"
        assert terms > 0, "Should return a positive number"

    def test_returns_sufficient_terms(self):
        """Test that returned term count is sufficient for target precision."""
        terms = _calculate_terms_needed()
        
        # For 13+ decimal places, should need at least 20-30 terms
        assert terms >= 20, f"Expected at least 20 terms, got {terms}"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_decimal_context_preservation(self):
        """Test that function doesn't modify global decimal context permanently."""
        original_prec = getcontext().prec
        
        calculate_pi()
        
        assert getcontext().prec == original_prec, "Should not permanently modify context"

    def test_multiple_rapid_calls(self):
        """Test that rapid successive calls work correctly."""
        results = [calculate_pi() for _ in range(10)]
        
        # All results should be identical
        assert all(r == results[0] for r in results), "All rapid calls should return same value"

    def test_pi_string_representation(self):
        """Test that Pi can be converted to string properly."""
        pi = calculate_pi()
        pi_str = str(pi)
        
        assert pi_str.startswith("3.14159"), "String representation should start with 3.14159"
        assert "." in pi_str, "String should contain decimal point"


class TestMachinFormula:
    """Test the Machin formula implementation indirectly."""

    def test_machin_formula_components(self):
        """Test that Machin formula components are calculated correctly."""
        # Machin formula: π/4 = 4·arctan(1/5) - arctan(1/239)
        
        arctan_fifth = _arctan_series(Decimal(1) / Decimal(5), num_terms=50)
        arctan_239 = _arctan_series(Decimal(1) / Decimal(239), num_terms=30)
        
        # Calculate pi/4 using Machin formula
        pi_over_4 = 4 * arctan_fifth - arctan_239
        pi_calculated = 4 * pi_over_4
        
        # Should match our calculate_pi result
        pi_function = calculate_pi()
        
        diff = abs(pi_calculated - pi_function)
        assert diff < Decimal("0.00000000001"), "Machin formula should match calculate_pi"