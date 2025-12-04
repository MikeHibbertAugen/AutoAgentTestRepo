/**
 * Text helper utilities for string manipulation
 */

/**
 * Maximum allowed string length to prevent DoS attacks (10MB of characters)
 */
const MAX_STRING_LENGTH = 10 * 1024 * 1024;

/**
 * Regular expression to detect control characters that could be used for injection
 */
const CONTROL_CHARS_REGEX = /[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]/;

/**
 * Capitalizes the first letter of each word in a string while preserving original spacing.
 * 
 * This function performs the following:
 * - Splits the input string by whitespace
 * - Capitalizes the first letter of each word
 * - Preserves original spacing and punctuation
 * - Handles Unicode characters properly
 * - Includes security validations to prevent injection attacks
 * 
 * @param input - The string to capitalize. Can be null, undefined, or empty.
 * @returns A new string with the first letter of each word capitalized
 * 
 * @throws {TypeError} If input is not a string (when not null/undefined)
 * @throws {RangeError} If input exceeds maximum allowed length
 * @throws {Error} If input contains control characters
 * 
 * @example
 * ```typescript
 * capitalizeWords("hello world") // Returns: "Hello World"
 * capitalizeWords("hello  world") // Returns: "Hello  World" (preserves spacing)
 * capitalizeWords("café naïve") // Returns: "Café Naïve"
 * capitalizeWords("don't stop") // Returns: "Don't Stop"
 * capitalizeWords("") // Returns: ""
 * capitalizeWords(null) // Returns: ""
 * ```
 * 
 * @security
 * - Validates input type to prevent injection attacks
 * - Rejects strings with control characters
 * - Enforces maximum string length to prevent DoS
 * - Does not use eval() or dynamic code execution
 * - No logging of input to prevent exposure of sensitive data
 */
export function capitalizeWords(input: string | null | undefined): string {
  // Handle null and undefined inputs gracefully
  if (input === null || input === undefined) {
    return '';
  }

  // Validate input type
  if (typeof input !== 'string') {
    throw new TypeError('Input must be a string');
  }

  // Handle empty string
  if (input.length === 0) {
    return '';
  }

  // Security: Check for maximum length to prevent DoS
  if (input.length > MAX_STRING_LENGTH) {
    throw new RangeError(`Input string exceeds maximum allowed length of ${MAX_STRING_LENGTH} characters`);
  }

  // Security: Reject strings with control characters
  if (CONTROL_CHARS_REGEX.test(input)) {
    throw new Error('Input contains invalid control characters');
  }

  // Split by spaces while preserving the original delimiters
  // This regex captures both words and the spaces between them
  const parts = input.split(/(\s+)/);

  // Process each part
  const result = parts.map(part => {
    // If this is a whitespace segment, preserve it as-is
    if (/^\s+$/.test(part)) {
      return part;
    }

    // If this is an empty part, return as-is
    if (part.length === 0) {
      return part;
    }

    // Capitalize the first character and append the rest
    // Use toLocaleUpperCase for proper Unicode handling
    const firstChar = part.charAt(0).toLocaleUpperCase();
    const restOfWord = part.slice(1);

    return firstChar + restOfWord;
  });

  return result.join('');
}

/**
 * Capitalizes the first letter of each word in a string with custom delimiter support.
 * 
 * This is an advanced version that allows specifying custom delimiters for word boundaries.
 * 
 * @param input - The string to capitalize
 * @param delimiters - Array of delimiter characters (default: whitespace only)
 * @returns A new string with the first letter of each word capitalized
 * 
 * @throws {TypeError} If input is not a string (when not null/undefined)
 * @throws {RangeError} If input exceeds maximum allowed length
 * @throws {Error} If input contains control characters
 * 
 * @example
 * ```typescript
 * capitalizeWordsWithDelimiters("hello-world", ["-"]) // Returns: "Hello-World"
 * capitalizeWordsWithDelimiters("hello_world_test", ["_"]) // Returns: "Hello_World_Test"
 * ```
 */
export function capitalizeWordsWithDelimiters(
  input: string | null | undefined,
  delimiters: string[] = []
): string {
  // Handle null and undefined inputs gracefully
  if (input === null || input === undefined) {
    return '';
  }

  // Validate input type
  if (typeof input !== 'string') {
    throw new TypeError('Input must be a string');
  }

  // Handle empty string
  if (input.length === 0) {
    return '';
  }

  // Security: Check for maximum length to prevent DoS
  if (input.length > MAX_STRING_LENGTH) {
    throw new RangeError(`Input string exceeds maximum allowed length of ${MAX_STRING_LENGTH} characters`);
  }

  // Security: Reject strings with control characters
  if (CONTROL_CHARS_REGEX.test(input)) {
    throw new Error('Input contains invalid control characters');
  }

  // If no custom delimiters, fall back to standard implementation
  if (delimiters.length === 0) {
    return capitalizeWords(input);
  }

  // Escape special regex characters in delimiters
  const escapedDelimiters = delimiters.map(d => d.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  
  // Create regex pattern that captures delimiters and words
  const pattern = new RegExp(`([${escapedDelimiters.join('')}\\s]+)`, 'g');
  
  // Split by delimiters while preserving them
  const parts = input.split(pattern);

  // Process each part
  const result = parts.map(part => {
    // If this is a delimiter segment or whitespace, preserve it as-is
    if (pattern.test(part) || part.length === 0) {
      return part;
    }

    // Capitalize the first character and append the rest
    const firstChar = part.charAt(0).toLocaleUpperCase();
    const restOfWord = part.slice(1);

    return firstChar + restOfWord;
  });

  return result.join('');
}