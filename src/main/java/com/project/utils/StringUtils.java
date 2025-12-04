package com.project.utils;

import java.util.Objects;
import java.util.regex.Pattern;

/**
 * Utility class for string manipulation operations.
 * 
 * This class provides methods for common string operations with built-in
 * security safeguards and input validation.
 * 
 * @author Project Team
 * @version 1.0
 */
public class StringUtils {
    
    // Security constants
    private static final int MAX_STRING_LENGTH = 10 * 1024 * 1024; // 10MB
    private static final Pattern CONTROL_CHARS_PATTERN = Pattern.compile("[\\x00-\\x08\\x0B\\x0C\\x0E-\\x1F\\x7F]");
    
    /**
     * Private constructor to prevent instantiation of utility class.
     */
    private StringUtils() {
        throw new UnsupportedOperationException("Utility class cannot be instantiated");
    }
    
    /**
     * Capitalizes the first letter of each word in a string.
     * 
     * This method splits the input string by whitespace characters and capitalizes
     * the first letter of each word while preserving the original spacing and
     * formatting. It handles Unicode characters properly and includes security
     * safeguards against malicious input.
     * 
     * <p>Security considerations:
     * <ul>
     *   <li>Input is validated for null values and size limits</li>
     *   <li>Control characters are rejected to prevent injection attacks</li>
     *   <li>No dynamic code execution is performed</li>
     *   <li>Input strings are not logged to prevent sensitive data exposure</li>
     * </ul>
     * 
     * <p>Examples:
     * <pre>
     * capitalizeWords("hello world")      returns "Hello World"
     * capitalizeWords("hello  world")     returns "Hello  World"
     * capitalizeWords("hello, world!")    returns "Hello, World!"
     * capitalizeWords("don't stop")       returns "Don't Stop"
     * capitalizeWords("")                 returns ""
     * capitalizeWords(null)               throws IllegalArgumentException
     * </pre>
     * 
     * @param input the string to capitalize; may be empty but not null
     * @return a new string with the first letter of each word capitalized
     * @throws IllegalArgumentException if input is null, exceeds maximum length,
     *                                  or contains control characters
     */
    public static String capitalizeWords(String input) {
        // Input validation
        if (input == null) {
            throw new IllegalArgumentException("Input string cannot be null");
        }
        
        // Handle empty string
        if (input.isEmpty()) {
            return "";
        }
        
        // Security check: enforce maximum string length to prevent DoS
        if (input.length() > MAX_STRING_LENGTH) {
            throw new IllegalArgumentException(
                "Input string exceeds maximum allowed length of " + MAX_STRING_LENGTH + " characters"
            );
        }
        
        // Security check: reject control characters to prevent injection attacks
        if (CONTROL_CHARS_PATTERN.matcher(input).find()) {
            throw new IllegalArgumentException(
                "Input string contains invalid control characters"
            );
        }
        
        // Process the string
        StringBuilder result = new StringBuilder(input.length());
        boolean capitalizeNext = true;
        
        for (int i = 0; i < input.length(); i++) {
            char currentChar = input.charAt(i);
            
            if (Character.isWhitespace(currentChar)) {
                // Preserve whitespace and mark next character for capitalization
                result.append(currentChar);
                capitalizeNext = true;
            } else if (Character.isLetter(currentChar)) {
                // Capitalize if this is the start of a word
                if (capitalizeNext) {
                    result.append(Character.toUpperCase(currentChar));
                    capitalizeNext = false;
                } else {
                    result.append(Character.toLowerCase(currentChar));
                }
            } else {
                // Non-letter, non-whitespace character (punctuation, numbers, etc.)
                result.append(currentChar);
                // Don't reset capitalizeNext - allows for "don't" -> "Don't"
                // But do set it for certain punctuation
                if (currentChar == '.' || currentChar == '!' || currentChar == '?' || 
                    currentChar == '\n' || currentChar == '\r') {
                    capitalizeNext = true;
                }
            }
        }
        
        return result.toString();
    }
    
    /**
     * Checks if a string is null or empty.
     * 
     * @param str the string to check
     * @return true if the string is null or empty, false otherwise
     */
    public static boolean isEmpty(String str) {
        return str == null || str.isEmpty();
    }
    
    /**
     * Checks if a string is null, empty, or contains only whitespace.
     * 
     * @param str the string to check
     * @return true if the string is null, empty, or whitespace only, false otherwise
     */
    public static boolean isBlank(String str) {
        return str == null || str.trim().isEmpty();
    }
}