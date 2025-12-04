// Package stringutils provides utility functions for string manipulation.
package stringutils

import (
	"errors"
	"strings"
	"unicode"
	"unicode/utf8"
)

const (
	// MaxStringLength defines the maximum allowed string length (10MB)
	MaxStringLength = 10 * 1024 * 1024
)

var (
	// ErrNilInput is returned when a nil input is provided
	ErrNilInput = errors.New("input string cannot be nil")
	// ErrTooLarge is returned when input exceeds maximum allowed length
	ErrTooLarge = errors.New("input string exceeds maximum allowed length")
	// ErrInvalidInput is returned when input contains control characters
	ErrInvalidInput = errors.New("input string contains invalid control characters")
)

// CapitalizeWords capitalizes the first letter of each word in the input string.
// Words are separated by whitespace characters. The function preserves the original
// spacing and formatting of the input string.
//
// Parameters:
//   - input: The string to capitalize. Must not exceed MaxStringLength (10MB).
//
// Returns:
//   - The capitalized string with the first letter of each word in uppercase.
//   - An error if input validation fails.
//
// Security considerations:
//   - Input is validated for control characters to prevent injection attacks
//   - Maximum string length is enforced to prevent DoS attacks
//   - No logging of input data to prevent sensitive data exposure
//
// Examples:
//   CapitalizeWords("hello world")        // Returns: "Hello World"
//   CapitalizeWords("hello  world")       // Returns: "Hello  World" (preserves spacing)
//   CapitalizeWords("café naïve")         // Returns: "Café Naïve"
//   CapitalizeWords("don't stop")         // Returns: "Don't Stop"
func CapitalizeWords(input string) (string, error) {
	// Validate input length
	if len(input) > MaxStringLength {
		return "", ErrTooLarge
	}

	// Handle empty string
	if input == "" {
		return "", nil
	}

	// Validate input for control characters (except common whitespace)
	if err := validateInput(input); err != nil {
		return "", err
	}

	// Convert string to runes for proper Unicode handling
	runes := []rune(input)
	result := make([]rune, len(runes))
	capitalizeNext := true

	for i, r := range runes {
		if unicode.IsSpace(r) {
			// Preserve whitespace and mark next character for capitalization
			result[i] = r
			capitalizeNext = true
		} else if capitalizeNext && unicode.IsLetter(r) {
			// Capitalize the first letter of a word
			result[i] = unicode.ToUpper(r)
			capitalizeNext = false
		} else {
			// Keep character as-is
			result[i] = r
			// Don't reset capitalizeNext for non-letters (e.g., punctuation, numbers)
			if unicode.IsLetter(r) {
				capitalizeNext = false
			}
		}
	}

	return string(result), nil
}

// validateInput checks for dangerous control characters and invalid UTF-8 sequences.
// It allows common whitespace characters (space, tab, newline, carriage return)
// but rejects other control characters that could be used in injection attacks.
func validateInput(input string) error {
	// Check for valid UTF-8
	if !utf8.ValidString(input) {
		return ErrInvalidInput
	}

	// Check for dangerous control characters
	for _, r := range input {
		// Allow common whitespace: space, tab, newline, carriage return
		if r == ' ' || r == '\t' || r == '\n' || r == '\r' {
			continue
		}

		// Reject other control characters (ASCII 0-31 and 127)
		if r < 32 || r == 127 {
			return ErrInvalidInput
		}

		// Reject null bytes
		if r == 0 {
			return ErrInvalidInput
		}
	}

	return nil
}

// CapitalizeWordsWithDelimiters capitalizes the first letter of each word in the input string
// using custom delimiters. This function is useful when words are separated by characters
// other than whitespace.
//
// Parameters:
//   - input: The string to capitalize. Must not exceed MaxStringLength (10MB).
//   - delimiters: A string containing characters to treat as word separators.
//
// Returns:
//   - The capitalized string with the first letter of each word in uppercase.
//   - An error if input validation fails.
//
// Example:
//   CapitalizeWordsWithDelimiters("hello-world", "-") // Returns: "Hello-World"
func CapitalizeWordsWithDelimiters(input string, delimiters string) (string, error) {
	// Validate input length
	if len(input) > MaxStringLength {
		return "", ErrTooLarge
	}

	// Handle empty string
	if input == "" {
		return "", nil
	}

	// Validate input for control characters
	if err := validateInput(input); err != nil {
		return "", err
	}

	// Build delimiter map for O(1) lookup
	delimiterMap := make(map[rune]bool)
	for _, r := range delimiters {
		delimiterMap[r] = true
	}

	// Convert string to runes for proper Unicode handling
	runes := []rune(input)
	result := make([]rune, len(runes))
	capitalizeNext := true

	for i, r := range runes {
		if delimiterMap[r] || unicode.IsSpace(r) {
			// Preserve delimiter/whitespace and mark next character for capitalization
			result[i] = r
			capitalizeNext = true
		} else if capitalizeNext && unicode.IsLetter(r) {
			// Capitalize the first letter of a word
			result[i] = unicode.ToUpper(r)
			capitalizeNext = false
		} else {
			// Keep character as-is
			result[i] = r
			// Don't reset capitalizeNext for non-letters
			if unicode.IsLetter(r) {
				capitalizeNext = false
			}
		}
	}

	return string(result), nil
}