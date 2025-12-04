/**
 * String utility functions for text manipulation
 * @module stringUtils
 */

/**
 * Maximum allowed string length to prevent DoS attacks (10MB)
 */
const MAX_STRING_LENGTH = 10 * 1024 * 1024;

/**
 * Regular expression to match control characters
 */
const CONTROL_CHARS_REGEX = /[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g;

/**
 * Capitalizes the first letter of each word in a string while preserving
 * original spacing and formatting.
 * 
 * Security considerations:
 * - Input validation prevents injection attacks
 * - Size limits prevent DoS attacks
 * - No dynamic code execution
 * - Control characters are sanitized
 * 
 * @param {string} input - The string to capitalize
 * @param {Object} options - Optional configuration
 * @param {boolean} options.sanitizeControlChars - Remove control characters (default: true)
 * @returns {string} The capitalized string
 * @throws {TypeError} If input is not a string
 * @throws {RangeError} If input exceeds maximum length
 * 
 * @example
 * capitalizeWords('hello world')
 * // Returns: 'Hello World'
 * 
 * @example
 * capitalizeWords('hello,  world!')
 * // Returns: 'Hello,  World!'
 * 
 * @example
 * capitalizeWords("don't stop")
 * // Returns: "Don't Stop"
 */
function capitalizeWords(input, options = {}) {
  // Input validation
  if (input === null || input === undefined) {
    return '';
  }

  if (typeof input !== 'string') {
    throw new TypeError(`Expected string, got ${typeof input}`);
  }

  // Handle empty string
  if (input.length === 0) {
    return '';
  }

  // Security: Prevent DoS with very large strings
  if (input.length > MAX_STRING_LENGTH) {
    throw new RangeError(`String length exceeds maximum allowed length of ${MAX_STRING_LENGTH} characters`);
  }

  // Security: Sanitize control characters if enabled (default)
  const sanitizeControlChars = options.sanitizeControlChars !== false;
  let processedInput = input;
  
  if (sanitizeControlChars) {
    processedInput = input.replace(CONTROL_CHARS_REGEX, '');
  }

  // Capitalize first letter of each word while preserving spacing
  // This regex captures:
  // - Start of string or any whitespace followed by a word character
  // - Unicode letters are properly handled
  const result = processedInput.replace(/(^|\s)(\p{L})/gu, (match, whitespace, letter) => {
    return whitespace + letter.toUpperCase();
  });

  return result;
}

/**
 * Capitalizes the first letter of each word in a string with custom delimiter support.
 * 
 * @param {string} input - The string to capitalize
 * @param {string|RegExp} delimiter - Custom delimiter pattern (default: whitespace)
 * @returns {string} The capitalized string
 * 
 * @example
 * capitalizeWordsWithDelimiter('hello-world-example', '-')
 * // Returns: 'Hello-World-Example'
 */
function capitalizeWordsWithDelimiter(input, delimiter = /\s+/) {
  // Input validation
  if (input === null || input === undefined) {
    return '';
  }

  if (typeof input !== 'string') {
    throw new TypeError(`Expected string, got ${typeof input}`);
  }

  if (input.length === 0) {
    return '';
  }

  if (input.length > MAX_STRING_LENGTH) {
    throw new RangeError(`String length exceeds maximum allowed length of ${MAX_STRING_LENGTH} characters`);
  }

  // Split by delimiter, capitalize each word, and rejoin
  const delimiterRegex = typeof delimiter === 'string' 
    ? new RegExp(`(${delimiter.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'g')
    : delimiter;

  // Split while preserving delimiters
  const parts = input.split(delimiterRegex);
  
  const capitalizedParts = parts.map(part => {
    if (part && part.length > 0 && /\p{L}/u.test(part[0])) {
      return part[0].toUpperCase() + part.slice(1);
    }
    return part;
  });

  return capitalizedParts.join('');
}

/**
 * Checks if a string contains only safe characters (no control characters)
 * 
 * @param {string} input - The string to check
 * @returns {boolean} True if string is safe, false otherwise
 */
function isSafeString(input) {
  if (typeof input !== 'string') {
    return false;
  }
  
  return !CONTROL_CHARS_REGEX.test(input);
}

// Export functions
module.exports = {
  capitalizeWords,
  capitalizeWordsWithDelimiter,
  isSafeString,
  MAX_STRING_LENGTH
};