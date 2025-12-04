package com.project.utils;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.NullAndEmptySource;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Comprehensive unit tests for StringUtils.capitalizeWords functionality.
 * Tests cover standard cases, edge cases, security scenarios, and performance.
 */
class StringUtilsTest {

    @Test
    @DisplayName("Should capitalize first letter of each word in standard case")
    void testCapitalizeWords_StandardCase() {
        String input = "hello world";
        String expected = "Hello World";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle null input gracefully")
    void testCapitalizeWords_NullInput() {
        assertThrows(IllegalArgumentException.class, () -> {
            StringUtils.capitalizeWords(null);
        });
    }

    @Test
    @DisplayName("Should handle empty string")
    void testCapitalizeWords_EmptyString() {
        String input = "";
        String expected = "";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle single word")
    void testCapitalizeWords_SingleWord() {
        String input = "hello";
        String expected = "Hello";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should preserve multiple spaces between words")
    void testCapitalizeWords_MultipleSpaces() {
        String input = "hello  world";
        String expected = "Hello  World";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle punctuation correctly")
    void testCapitalizeWords_WithPunctuation() {
        String input = "hello, world!";
        String expected = "Hello, World!";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle numbers in text")
    void testCapitalizeWords_WithNumbers() {
        String input = "test 123 abc";
        String expected = "Test 123 Abc";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle Unicode characters properly")
    void testCapitalizeWords_Unicode() {
        String input = "café naïve";
        String expected = "Café Naïve";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle apostrophes in contractions")
    void testCapitalizeWords_Apostrophes() {
        String input = "don't can't won't";
        String expected = "Don't Can't Won't";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle leading and trailing spaces")
    void testCapitalizeWords_LeadingTrailingSpaces() {
        String input = "  hello world  ";
        String expected = "  Hello World  ";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle only spaces")
    void testCapitalizeWords_OnlySpaces() {
        String input = "     ";
        String expected = "     ";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle mixed case input")
    void testCapitalizeWords_MixedCase() {
        String input = "hELLo WoRLd";
        String expected = "HELLo WoRLd";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle newlines and tabs")
    void testCapitalizeWords_NewlinesAndTabs() {
        String input = "hello\nworld\ttest";
        String expected = "Hello\nWorld\tTest";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @ParameterizedTest
    @CsvSource({
        "'a b c', 'A B C'",
        "'the quick brown fox', 'The Quick Brown Fox'",
        "'one two three four five', 'One Two Three Four Five'",
        "'test-case', 'Test-case'",
        "'hello.world', 'Hello.world'"
    })
    @DisplayName("Should handle various input patterns")
    void testCapitalizeWords_VariousPatterns(String input, String expected) {
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle already capitalized text")
    void testCapitalizeWords_AlreadyCapitalized() {
        String input = "Hello World";
        String expected = "Hello World";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle single character words")
    void testCapitalizeWords_SingleCharWords() {
        String input = "a b c d e";
        String expected = "A B C D E";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle special characters and symbols")
    void testCapitalizeWords_SpecialCharacters() {
        String input = "hello @world #test $money";
        String expected = "Hello @world #test $money";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    // Security-focused tests

    @Test
    @DisplayName("Security: Should handle script tags without execution")
    void testCapitalizeWords_SecurityScriptTags() {
        String input = "<script>alert('xss')</script>";
        String result = StringUtils.capitalizeWords(input);
        assertNotNull(result);
        assertFalse(result.contains("script>alert"));
        // Result should be capitalized but no execution
        assertTrue(result.startsWith("<script>"));
    }

    @Test
    @DisplayName("Security: Should handle SQL injection patterns")
    void testCapitalizeWords_SecuritySQLInjection() {
        String input = "'; DROP TABLE users; --";
        String result = StringUtils.capitalizeWords(input);
        assertNotNull(result);
        assertTrue(result.contains("DROP"));
        // Should just capitalize, not execute
    }

    @Test
    @DisplayName("Security: Should handle null byte injection attempts")
    void testCapitalizeWords_SecurityNullByte() {
        String input = "hello\0world";
        String result = StringUtils.capitalizeWords(input);
        assertNotNull(result);
    }

    @Test
    @DisplayName("Security: Should reject extremely large strings")
    void testCapitalizeWords_SecurityDOSPrevention() {
        // Create string larger than typical limit (e.g., 10MB)
        int size = 11 * 1024 * 1024; // 11 MB
        StringBuilder sb = new StringBuilder(size);
        for (int i = 0; i < size; i++) {
            sb.append('a');
        }
        String input = sb.toString();
        
        assertThrows(IllegalArgumentException.class, () -> {
            StringUtils.capitalizeWords(input);
        });
    }

    @Test
    @DisplayName("Security: Should handle control characters safely")
    void testCapitalizeWords_SecurityControlCharacters() {
        String input = "hello\u0001world\u0002test";
        String result = StringUtils.capitalizeWords(input);
        assertNotNull(result);
    }

    @Test
    @DisplayName("Security: Should handle Unicode direction override characters")
    void testCapitalizeWords_SecurityUnicodeOverride() {
        String input = "hello\u202Eworld";
        String result = StringUtils.capitalizeWords(input);
        assertNotNull(result);
    }

    // Performance tests

    @Test
    @DisplayName("Performance: Should handle moderately large strings efficiently")
    void testCapitalizeWords_PerformanceModerate() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 10000; i++) {
            sb.append("word ");
        }
        String input = sb.toString().trim();
        
        long startTime = System.currentTimeMillis();
        String result = StringUtils.capitalizeWords(input);
        long endTime = System.currentTimeMillis();
        
        assertNotNull(result);
        assertTrue(result.startsWith("Word"));
        assertTrue((endTime - startTime) < 5000, "Operation took too long");
    }

    @Test
    @DisplayName("Should handle strings with only special characters")
    void testCapitalizeWords_OnlySpecialChars() {
        String input = "!@#$%^&*()";
        String expected = "!@#$%^&*()";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle strings with repeated delimiters")
    void testCapitalizeWords_RepeatedDelimiters() {
        String input = "hello...world";
        String expected = "Hello...world";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle accented characters")
    void testCapitalizeWords_AccentedCharacters() {
        String input = "éclair résumé";
        String expected = "Éclair Résumé";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle hyphenated words")
    void testCapitalizeWords_HyphenatedWords() {
        String input = "well-known state-of-the-art";
        String expected = "Well-known State-of-the-art";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle all uppercase input")
    void testCapitalizeWords_AllUppercase() {
        String input = "HELLO WORLD";
        String expected = "HELLO WORLD";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle all lowercase input")
    void testCapitalizeWords_AllLowercase() {
        String input = "hello world test";
        String expected = "Hello World Test";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle words starting with numbers")
    void testCapitalizeWords_WordsStartingWithNumbers() {
        String input = "123abc 456def";
        String expected = "123abc 456def";
        assertEquals(expected, StringUtils.capitalizeWords(input));
    }

    @Test
    @DisplayName("Should handle whitespace string")
    void testCapitalizeWords_WhitespaceString() {
        String input = "\t\n\r ";
        String result = StringUtils.capitalizeWords(input);
        assertNotNull(result);
    }
}