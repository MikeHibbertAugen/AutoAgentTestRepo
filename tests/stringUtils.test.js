const { capitalizeWords } = require('../src/stringUtils');

describe('capitalizeWords', () => {
  describe('Standard functionality', () => {
    test('should capitalize first letter of each word in a simple sentence', () => {
      expect(capitalizeWords('hello world')).toBe('Hello World');
    });

    test('should handle empty string', () => {
      expect(capitalizeWords('')).toBe('');
    });

    test('should handle single word', () => {
      expect(capitalizeWords('hello')).toBe('Hello');
    });

    test('should handle already capitalized words', () => {
      expect(capitalizeWords('Hello World')).toBe('Hello World');
    });

    test('should handle mixed case words', () => {
      expect(capitalizeWords('hELLo wORLd')).toBe('HELLo WORLd');
    });

    test('should preserve multiple spaces between words', () => {
      expect(capitalizeWords('hello  world')).toBe('Hello  World');
      expect(capitalizeWords('hello   world   test')).toBe('Hello   World   Test');
    });

    test('should handle leading and trailing spaces', () => {
      expect(capitalizeWords('  hello world  ')).toBe('  Hello World  ');
    });

    test('should handle tabs and mixed whitespace', () => {
      expect(capitalizeWords('hello\tworld')).toBe('Hello\tWorld');
      expect(capitalizeWords('hello \t world')).toBe('Hello \t World');
    });
  });

  describe('Punctuation and special cases', () => {
    test('should handle punctuation', () => {
      expect(capitalizeWords('hello, world!')).toBe('Hello, World!');
      expect(capitalizeWords('hello; world?')).toBe('Hello; World?');
    });

    test('should handle apostrophes correctly', () => {
      expect(capitalizeWords("don't stop")).toBe("Don't Stop");
      expect(capitalizeWords("it's amazing")).toBe("It's Amazing");
    });

    test('should handle hyphens', () => {
      expect(capitalizeWords('state-of-the-art')).toBe('State-of-the-art');
      expect(capitalizeWords('well-known example')).toBe('Well-known Example');
    });

    test('should handle numbers', () => {
      expect(capitalizeWords('test 123 abc')).toBe('Test 123 Abc');
      expect(capitalizeWords('room 42b floor 3')).toBe('Room 42b Floor 3');
    });

    test('should handle strings with only numbers', () => {
      expect(capitalizeWords('123 456')).toBe('123 456');
    });

    test('should handle strings with special characters', () => {
      expect(capitalizeWords('hello@world.com')).toBe('Hello@world.com');
      expect(capitalizeWords('price: $100')).toBe('Price: $100');
    });
  });

  describe('Unicode and international characters', () => {
    test('should handle accented characters', () => {
      expect(capitalizeWords('café naïve')).toBe('Café Naïve');
      expect(capitalizeWords('résumé über')).toBe('Résumé Über');
    });

    test('should handle non-Latin scripts', () => {
      expect(capitalizeWords('hello мир')).toBe('Hello Мир');
    });

    test('should handle mixed scripts', () => {
      expect(capitalizeWords('test 测试')).toBe('Test 测试');
    });
  });

  describe('Input validation and error handling', () => {
    test('should handle null input', () => {
      expect(capitalizeWords(null)).toBe('');
    });

    test('should handle undefined input', () => {
      expect(capitalizeWords(undefined)).toBe('');
    });

    test('should throw error for non-string, non-null inputs', () => {
      expect(() => capitalizeWords(123)).toThrow('Input must be a string');
      expect(() => capitalizeWords({})).toThrow('Input must be a string');
      expect(() => capitalizeWords([])).toThrow('Input must be a string');
      expect(() => capitalizeWords(true)).toThrow('Input must be a string');
    });

    test('should handle very long strings', () => {
      const longString = 'word '.repeat(10000).trim();
      const result = capitalizeWords(longString);
      expect(result).toMatch(/^Word( Word)*$/);
      expect(result.split(' ').length).toBe(10000);
    });

    test('should reject strings exceeding maximum length', () => {
      const maxLength = 10 * 1024 * 1024; // 10MB
      const tooLongString = 'a'.repeat(maxLength + 1);
      expect(() => capitalizeWords(tooLongString)).toThrow('Input string exceeds maximum length');
    });
  });

  describe('Security tests', () => {
    test('should handle script tags without executing', () => {
      const maliciousInput = '<script>alert("xss")</script>';
      const result = capitalizeWords(maliciousInput);
      expect(result).toBe('<script>Alert("xss")</script>');
      expect(typeof result).toBe('string');
    });

    test('should handle SQL injection patterns', () => {
      const sqlInjection = "'; DROP TABLE users; --";
      const result = capitalizeWords(sqlInjection);
      expect(result).toBe("'; DROP TABLE Users; --");
      expect(typeof result).toBe('string');
    });

    test('should handle null byte injection', () => {
      const nullByteInput = 'hello\0world';
      const result = capitalizeWords(nullByteInput);
      expect(result).toMatch(/^Hello\0World$/);
    });

    test('should handle control characters safely', () => {
      const controlChars = 'hello\x01\x02world';
      expect(() => {
        const result = capitalizeWords(controlChars);
        expect(typeof result).toBe('string');
      }).not.toThrow();
    });

    test('should handle newlines and carriage returns', () => {
      expect(capitalizeWords('hello\nworld')).toBe('Hello\nWorld');
      expect(capitalizeWords('hello\r\nworld')).toBe('Hello\r\nWorld');
    });

    test('should handle HTML entities', () => {
      const htmlEntities = '&lt;hello&gt; &amp;world';
      const result = capitalizeWords(htmlEntities);
      expect(result).toBe('&lt;Hello&gt; &amp;world');
    });

    test('should not evaluate code-like strings', () => {
      const codeString = 'eval("malicious code")';
      const result = capitalizeWords(codeString);
      expect(result).toBe('Eval("malicious Code")');
      expect(typeof result).toBe('string');
    });
  });

  describe('Edge cases', () => {
    test('should handle single character', () => {
      expect(capitalizeWords('a')).toBe('A');
      expect(capitalizeWords('z')).toBe('Z');
    });

    test('should handle only whitespace', () => {
      expect(capitalizeWords('   ')).toBe('   ');
      expect(capitalizeWords('\t\t')).toBe('\t\t');
    });

    test('should handle only punctuation', () => {
      expect(capitalizeWords('!!!')).toBe('!!!');
      expect(capitalizeWords('...')).toBe('...');
    });

    test('should handle emoji', () => {
      expect(capitalizeWords('hello 😊 world')).toBe('Hello 😊 World');
    });

    test('should handle repeated punctuation', () => {
      expect(capitalizeWords('hello!!! world???')).toBe('Hello!!! World???');
    });

    test('should preserve original string type', () => {
      const result = capitalizeWords('test');
      expect(typeof result).toBe('string');
      expect(result).not.toBe(null);
      expect(result).not.toBe(undefined);
    });
  });

  describe('Performance tests', () => {
    test('should handle large strings efficiently', () => {
      const largeString = 'word '.repeat(50000).trim();
      const startTime = Date.now();
      const result = capitalizeWords(largeString);
      const endTime = Date.now();
      
      expect(result).toBeDefined();
      expect(endTime - startTime).toBeLessThan(5000); // Should complete within 5 seconds
    });

    test('should handle many small words', () => {
      const manyWords = Array.from({ length: 10000 }, (_, i) => `w${i}`).join(' ');
      const result = capitalizeWords(manyWords);
      expect(result).toMatch(/^W0 W1/);
    });
  });
});