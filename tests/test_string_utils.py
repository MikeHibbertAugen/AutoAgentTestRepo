import unittest
from src.string_utils import capitalize_words


class TestCapitalizeWords(unittest.TestCase):
    """Comprehensive test suite for capitalize_words function."""

    # Standard test cases
    def test_standard_case(self):
        """Test standard multi-word string."""
        self.assertEqual(capitalize_words("hello world"), "Hello World")

    def test_empty_string(self):
        """Test empty string returns empty string."""
        self.assertEqual(capitalize_words(""), "")

    def test_none_input(self):
        """Test None input raises TypeError."""
        with self.assertRaises(TypeError):
            capitalize_words(None)

    def test_single_word(self):
        """Test single word capitalization."""
        self.assertEqual(capitalize_words("hello"), "Hello")

    def test_already_capitalized(self):
        """Test already capitalized string."""
        self.assertEqual(capitalize_words("Hello World"), "Hello World")

    def test_all_caps(self):
        """Test all uppercase string."""
        self.assertEqual(capitalize_words("HELLO WORLD"), "Hello World")

    def test_mixed_case(self):
        """Test mixed case string."""
        self.assertEqual(capitalize_words("hELLo WoRLd"), "Hello World")

    # Whitespace handling
    def test_multiple_spaces(self):
        """Test preservation of multiple spaces."""
        self.assertEqual(capitalize_words("hello  world"), "Hello  World")

    def test_leading_spaces(self):
        """Test string with leading spaces."""
        self.assertEqual(capitalize_words("  hello world"), "  Hello World")

    def test_trailing_spaces(self):
        """Test string with trailing spaces."""
        self.assertEqual(capitalize_words("hello world  "), "Hello World  ")

    def test_tabs_and_newlines(self):
        """Test string with tabs and newlines."""
        self.assertEqual(capitalize_words("hello\tworld"), "Hello\tWorld")
        self.assertEqual(capitalize_words("hello\nworld"), "Hello\nWorld")

    def test_multiple_whitespace_types(self):
        """Test string with various whitespace characters."""
        self.assertEqual(capitalize_words("hello \t\n world"), "Hello \t\n World")

    # Punctuation handling
    def test_punctuation(self):
        """Test string with punctuation."""
        self.assertEqual(capitalize_words("hello, world!"), "Hello, World!")

    def test_punctuation_start(self):
        """Test word starting with punctuation."""
        self.assertEqual(capitalize_words("'hello' \"world\""), "'hello' \"world\"")

    def test_apostrophes(self):
        """Test words with apostrophes."""
        self.assertEqual(capitalize_words("don't can't won't"), "Don't Can't Won't")

    def test_hyphens(self):
        """Test hyphenated words."""
        self.assertEqual(capitalize_words("well-known state-of-the-art"), "Well-known State-of-the-art")

    def test_periods(self):
        """Test multiple sentences."""
        self.assertEqual(capitalize_words("hello. world. test."), "Hello. World. Test.")

    # Numbers and special characters
    def test_numbers(self):
        """Test string with numbers."""
        self.assertEqual(capitalize_words("test 123 abc"), "Test 123 Abc")

    def test_numbers_start_word(self):
        """Test words starting with numbers."""
        self.assertEqual(capitalize_words("123abc test"), "123abc Test")

    def test_special_characters(self):
        """Test string with special characters."""
        self.assertEqual(capitalize_words("hello@world #test"), "Hello@world #test")

    # Unicode and international characters
    def test_unicode_basic(self):
        """Test basic Unicode characters."""
        self.assertEqual(capitalize_words("café naïve"), "Café Naïve")

    def test_unicode_accents(self):
        """Test accented characters."""
        self.assertEqual(capitalize_words("émile zürich"), "Émile Zürich")

    def test_unicode_german(self):
        """Test German characters."""
        self.assertEqual(capitalize_words("größe äpfel"), "Größe Äpfel")

    def test_unicode_spanish(self):
        """Test Spanish characters."""
        self.assertEqual(capitalize_words("señor niño"), "Señor Niño")

    def test_unicode_cyrillic(self):
        """Test Cyrillic characters."""
        self.assertEqual(capitalize_words("привет мир"), "Привет Мир")

    def test_unicode_greek(self):
        """Test Greek characters."""
        self.assertEqual(capitalize_words("γεια κόσμος"), "Γεια Κόσμος")

    # Edge cases
    def test_single_character(self):
        """Test single character."""
        self.assertEqual(capitalize_words("a"), "A")

    def test_single_space(self):
        """Test single space."""
        self.assertEqual(capitalize_words(" "), " ")

    def test_only_whitespace(self):
        """Test string with only whitespace."""
        self.assertEqual(capitalize_words("   "), "   ")

    def test_only_punctuation(self):
        """Test string with only punctuation."""
        self.assertEqual(capitalize_words("!!!"), "!!!")

    def test_numbers_only(self):
        """Test string with only numbers."""
        self.assertEqual(capitalize_words("123 456"), "123 456")

    # Type validation
    def test_non_string_int(self):
        """Test integer input raises TypeError."""
        with self.assertRaises(TypeError):
            capitalize_words(123)

    def test_non_string_list(self):
        """Test list input raises TypeError."""
        with self.assertRaises(TypeError):
            capitalize_words(["hello", "world"])

    def test_non_string_dict(self):
        """Test dict input raises TypeError."""
        with self.assertRaises(TypeError):
            capitalize_words({"key": "value"})

    # Security tests
    def test_script_tags(self):
        """Test handling of script tags (XSS prevention)."""
        result = capitalize_words("<script>alert('xss')</script>")
        self.assertEqual(result, "<script>alert('xss')</script>")
        # Ensures no code execution, just string manipulation

    def test_sql_injection_attempt(self):
        """Test handling of SQL injection patterns."""
        result = capitalize_words("hello'; DROP TABLE users; --")
        self.assertEqual(result, "Hello'; Drop Table Users; --")

    def test_control_characters(self):
        """Test handling of control characters."""
        result = capitalize_words("hello\x00world")
        # Should handle without crashing
        self.assertIsInstance(result, str)

    def test_null_byte(self):
        """Test null byte injection attempt."""
        result = capitalize_words("hello\x00world")
        self.assertIn("hello", result.lower())

    def test_very_long_string(self):
        """Test performance with very long string."""
        long_string = "word " * 10000
        result = capitalize_words(long_string)
        self.assertTrue(result.startswith("Word "))
        self.assertEqual(len(result), len(long_string))

    def test_maximum_length_handling(self):
        """Test string at maximum allowed length."""
        # 10MB limit test (assuming limit exists)
        large_string = "a" * 1000000  # 1MB test
        result = capitalize_words(large_string)
        self.assertEqual(result[0], "A")

    def test_unicode_overflow_attempt(self):
        """Test handling of potential unicode overflow."""
        result = capitalize_words("test " + "\U0001F600" + " emoji")
        self.assertIn("Test", result)

    # Real-world scenarios
    def test_sentence_case(self):
        """Test typical sentence."""
        self.assertEqual(
            capitalize_words("the quick brown fox jumps over the lazy dog"),
            "The Quick Brown Fox Jumps Over The Lazy Dog"
        )

    def test_title_with_articles(self):
        """Test title-like string."""
        self.assertEqual(
            capitalize_words("the lord of the rings"),
            "The Lord Of The Rings"
        )

    def test_email_address(self):
        """Test string containing email."""
        result = capitalize_words("contact john.doe@example.com today")
        self.assertEqual(result, "Contact John.doe@example.com Today")

    def test_url(self):
        """Test string containing URL."""
        result = capitalize_words("visit https://example.com now")
        self.assertEqual(result, "Visit Https://example.com Now")

    def test_file_path(self):
        """Test file path."""
        result = capitalize_words("path/to/my file.txt")
        self.assertEqual(result, "Path/to/my File.txt")

    def test_mixed_language(self):
        """Test mixed language content."""
        result = capitalize_words("hello мир café")
        self.assertEqual(result, "Hello Мир Café")


if __name__ == "__main__":
    unittest.main()