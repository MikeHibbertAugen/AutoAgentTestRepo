import unittest
from src.utils.string_operations import reverse_string


class TestReverseString(unittest.TestCase):
    """Comprehensive test suite for the reverse_string function."""

    def test_basic_string_reversal(self):
        """Test reversing a basic string."""
        self.assertEqual(reverse_string("hello"), "olleh")

    def test_empty_string(self):
        """Test reversing an empty string."""
        self.assertEqual(reverse_string(""), "")

    def test_single_character(self):
        """Test reversing a single character string."""
        self.assertEqual(reverse_string("a"), "a")

    def test_string_with_spaces(self):
        """Test reversing a string containing spaces."""
        self.assertEqual(reverse_string("hello world"), "dlrow olleh")

    def test_unicode_characters(self):
        """Test reversing a string with Unicode characters."""
        self.assertEqual(reverse_string("Hello 👋 World"), "dlroW 👋 olleH")

    def test_emoji_string(self):
        """Test reversing a string with multiple emojis."""
        self.assertEqual(reverse_string("😀😃😄"), "😄😃😀")

    def test_numbers_as_string(self):
        """Test reversing a string containing numbers."""
        self.assertEqual(reverse_string("12345"), "54321")

    def test_special_characters(self):
        """Test reversing a string with special characters."""
        self.assertEqual(reverse_string("!@#$%"), "%$#@!")

    def test_mixed_content(self):
        """Test reversing a string with mixed content."""
        self.assertEqual(reverse_string("Python 3.11"), "11.3 nohtyP")

    def test_palindrome(self):
        """Test reversing a palindrome string."""
        self.assertEqual(reverse_string("racecar"), "racecar")

    def test_string_with_newlines(self):
        """Test reversing a string with newline characters."""
        self.assertEqual(reverse_string("hello\nworld"), "dlrow\nolleh")

    def test_string_with_tabs(self):
        """Test reversing a string with tab characters."""
        self.assertEqual(reverse_string("hello\tworld"), "dlrow\tolleh")

    def test_string_with_multiple_spaces(self):
        """Test reversing a string with multiple consecutive spaces."""
        self.assertEqual(reverse_string("hello   world"), "dlrow   olleh")

    def test_long_string(self):
        """Test reversing a longer string."""
        input_str = "The quick brown fox jumps over the lazy dog"
        expected = "god yzal eht revo spmuj xof nworb kciuq ehT"
        self.assertEqual(reverse_string(input_str), expected)

    def test_type_error_with_none(self):
        """Test that TypeError is raised when None is passed."""
        with self.assertRaises(TypeError) as context:
            reverse_string(None)
        self.assertIn("must be a string", str(context.exception))

    def test_type_error_with_integer(self):
        """Test that TypeError is raised when an integer is passed."""
        with self.assertRaises(TypeError) as context:
            reverse_string(123)
        self.assertIn("must be a string", str(context.exception))

    def test_type_error_with_list(self):
        """Test that TypeError is raised when a list is passed."""
        with self.assertRaises(TypeError) as context:
            reverse_string(["h", "e", "l", "l", "o"])
        self.assertIn("must be a string", str(context.exception))

    def test_type_error_with_dict(self):
        """Test that TypeError is raised when a dict is passed."""
        with self.assertRaises(TypeError) as context:
            reverse_string({"key": "value"})
        self.assertIn("must be a string", str(context.exception))

    def test_type_error_with_float(self):
        """Test that TypeError is raised when a float is passed."""
        with self.assertRaises(TypeError) as context:
            reverse_string(3.14)
        self.assertIn("must be a string", str(context.exception))

    def test_type_error_with_boolean(self):
        """Test that TypeError is raised when a boolean is passed."""
        with self.assertRaises(TypeError) as context:
            reverse_string(True)
        self.assertIn("must be a string", str(context.exception))

    def test_accented_characters(self):
        """Test reversing a string with accented characters."""
        self.assertEqual(reverse_string("café"), "éfac")

    def test_chinese_characters(self):
        """Test reversing a string with Chinese characters."""
        self.assertEqual(reverse_string("你好世界"), "界世好你")

    def test_arabic_characters(self):
        """Test reversing a string with Arabic characters."""
        self.assertEqual(reverse_string("مرحبا"), "ابحرم")

    def test_mixed_languages(self):
        """Test reversing a string with mixed language characters."""
        self.assertEqual(reverse_string("Hello مرحبا 你好"), "好你 ابحرم olleH")


if __name__ == "__main__":
    unittest.main()