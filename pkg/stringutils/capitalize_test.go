package stringutils

import (
	"strings"
	"testing"
	"unicode/utf8"
)

func TestCapitalizeWords(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{
			name:     "standard case",
			input:    "hello world",
			expected: "Hello World",
		},
		{
			name:     "empty string",
			input:    "",
			expected: "",
		},
		{
			name:     "single word",
			input:    "hello",
			expected: "Hello",
		},
		{
			name:     "multiple spaces",
			input:    "hello  world",
			expected: "Hello  World",
		},
		{
			name:     "leading and trailing spaces",
			input:    "  hello world  ",
			expected: "  Hello World  ",
		},
		{
			name:     "punctuation",
			input:    "hello, world!",
			expected: "Hello, World!",
		},
		{
			name:     "mixed with numbers",
			input:    "test 123 abc",
			expected: "Test 123 Abc",
		},
		{
			name:     "numbers only",
			input:    "123 456",
			expected: "123 456",
		},
		{
			name:     "unicode characters",
			input:    "café naïve",
			expected: "Café Naïve",
		},
		{
			name:     "unicode mixed case",
			input:    "ñoño año",
			expected: "Ñoño Año",
		},
		{
			name:     "apostrophes",
			input:    "don't",
			expected: "Don't",
		},
		{
			name:     "multiple apostrophes",
			input:    "it's john's book",
			expected: "It's John's Book",
		},
		{
			name:     "all caps input",
			input:    "HELLO WORLD",
			expected: "HELLO WORLD",
		},
		{
			name:     "mixed case input",
			input:    "HeLLo WoRLd",
			expected: "HeLLo WoRLd",
		},
		{
			name:     "tab separated",
			input:    "hello\tworld",
			expected: "Hello\tWorld",
		},
		{
			name:     "newline separated",
			input:    "hello\nworld",
			expected: "Hello\nWorld",
		},
		{
			name:     "mixed whitespace",
			input:    "hello \t\n world",
			expected: "Hello \t\n World",
		},
		{
			name:     "hyphenated words",
			input:    "self-service",
			expected: "Self-Service",
		},
		{
			name:     "single character",
			input:    "a",
			expected: "A",
		},
		{
			name:     "single character word with space",
			input:    "a b c",
			expected: "A B C",
		},
		{
			name:     "special characters only",
			input:    "!@#$%",
			expected: "!@#$%",
		},
		{
			name:     "mixed special and words",
			input:    "!hello @world",
			expected: "!Hello @World",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CapitalizeWords(tt.input)
			if result != tt.expected {
				t.Errorf("CapitalizeWords(%q) = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func TestCapitalizeWordsLargeInput(t *testing.T) {
	// Test with large string (performance test)
	largeInput := strings.Repeat("hello world ", 10000)
	result := CapitalizeWords(largeInput)
	
	// Verify the string starts correctly
	if !strings.HasPrefix(result, "Hello World ") {
		t.Errorf("Large string capitalization failed, got prefix: %q", result[:20])
	}
	
	// Verify the length is preserved
	if len(result) != len(largeInput) {
		t.Errorf("Length mismatch: got %d, want %d", len(result), len(largeInput))
	}
}

func TestCapitalizeWordsUnicode(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{
			name:     "german umlaut",
			input:    "über das",
			expected: "Über Das",
		},
		{
			name:     "french accents",
			input:    "école été",
			expected: "École Été",
		},
		{
			name:     "greek letters",
			input:    "αλφα βήτα",
			expected: "Αλφα Βήτα",
		},
		{
			name:     "cyrillic",
			input:    "привет мир",
			expected: "Привет Мир",
		},
		{
			name:     "mixed scripts",
			input:    "hello мир café",
			expected: "Hello Мир Café",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CapitalizeWords(tt.input)
			if result != tt.expected {
				t.Errorf("CapitalizeWords(%q) = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func TestCapitalizeWordsSecurityCases(t *testing.T) {
	tests := []struct {
		name  string
		input string
	}{
		{
			name:  "html tags",
			input: "<script>alert('xss')</script>",
		},
		{
			name:  "sql injection attempt",
			input: "'; DROP TABLE users; --",
		},
		{
			name:  "null byte",
			input: "hello\x00world",
		},
		{
			name:  "control characters",
			input: "hello\x01\x02\x03world",
		},
		{
			name:  "unicode zero width characters",
			input: "hello\u200Bworld",
		},
		{
			name:  "rtl override",
			input: "hello\u202Eworld",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Should not panic or cause issues
			result := CapitalizeWords(tt.input)
			
			// Verify result is valid UTF-8
			if !utf8.ValidString(result) {
				t.Errorf("Result is not valid UTF-8: %q", result)
			}
			
			// Verify length doesn't change unexpectedly
			if len(result) > len(tt.input)*2 {
				t.Errorf("Result length suspiciously large: %d vs input %d", len(result), len(tt.input))
			}
		})
	}
}

func TestCapitalizeWordsEdgeCases(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{
			name:     "only spaces",
			input:    "     ",
			expected: "     ",
		},
		{
			name:     "only tabs",
			input:    "\t\t\t",
			expected: "\t\t\t",
		},
		{
			name:     "only newlines",
			input:    "\n\n\n",
			expected: "\n\n\n",
		},
		{
			name:     "mixed whitespace only",
			input:    " \t\n ",
			expected: " \t\n ",
		},
		{
			name:     "word followed by punctuation",
			input:    "hello!world",
			expected: "Hello!World",
		},
		{
			name:     "numbers at start",
			input:    "123abc 456def",
			expected: "123Abc 456Def",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CapitalizeWords(tt.input)
			if result != tt.expected {
				t.Errorf("CapitalizeWords(%q) = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func BenchmarkCapitalizeWords(b *testing.B) {
	input := "hello world this is a test string"
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		CapitalizeWords(input)
	}
}

func BenchmarkCapitalizeWordsLarge(b *testing.B) {
	input := strings.Repeat("hello world ", 1000)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		CapitalizeWords(input)
	}
}

func BenchmarkCapitalizeWordsUnicode(b *testing.B) {
	input := "café naïve über école αλφα привет"
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		CapitalizeWords(input)
	}
}