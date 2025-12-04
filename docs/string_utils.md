# String Utils Module

## Overview
The `string_utils` module provides utility functions for string manipulation operations.

## Functions

### `capitalize_string`

Capitalizes the first character of a string and converts the rest to lowercase.

#### Signature
```python
def capitalize_string(text: str) -> str:
```

#### Parameters
- `text` (str): The input string to capitalize. Must be a string object.

#### Returns
- `str`: A new string with the first character capitalized and all other characters in lowercase.

#### Raises
- `TypeError`: If the input is not a string.

#### Description
This function takes a string and returns a new string where the first character is converted to uppercase and all subsequent characters are converted to lowercase. This differs from Python's built-in `str.capitalize()` method in that it provides additional validation and explicit type checking.

#### Behavior
- Empty strings return an empty string
- Single character strings are capitalized
- Already capitalized strings are processed normally (first char uppercase, rest lowercase)
- Strings with mixed case have all characters normalized
- Strings with leading/trailing whitespace preserve that whitespace
- Strings with numbers and special characters preserve those characters
- Unicode characters are handled according to their Unicode case properties

#### Examples

**Basic usage:**
```python
from src.string_utils import capitalize_string

result = capitalize_string("hello")
print(result)  # Output: "Hello"
```

**Empty string:**
```python
result = capitalize_string("")
print(result)  # Output: ""
```

**Already capitalized:**
```python
result = capitalize_string("Hello")
print(result)  # Output: "Hello"
```

**Mixed case:**
```python
result = capitalize_string("hELLO wORLD")
print(result)  # Output: "Hello world"
```

**With numbers:**
```python
result = capitalize_string("test123")
print(result)  # Output: "Test123"
```

**With special characters:**
```python
result = capitalize_string("hello-world!")
print(result)  # Output: "Hello-world!"
```

**With whitespace:**
```python
result = capitalize_string("  hello  ")
print(result)  # Output: "  hello  "
```

**With unicode:**
```python
result = capitalize_string("café")
print(result)  # Output: "Café"
```

#### Edge Cases and Limitations
- The function requires a string input; passing `None` or other types will raise a `TypeError`
- Whitespace characters (spaces, tabs, newlines) at the beginning of the string are preserved and not considered as the "first character"
- Non-alphabetic characters (numbers, punctuation) at the start of the string remain unchanged
- The function uses Python's built-in Unicode case mapping, which handles most international characters correctly

#### Type Checking
The function includes full type hints and can be validated with mypy:
```bash
mypy src/string_utils.py
```

#### Testing
Comprehensive tests are available in `tests/test_string_utils.py`. Run tests with:
```bash
pytest tests/test_string_utils.py -v
```

## See Also
- Python's built-in `str.capitalize()` method
- Python's built-in `str.title()` method for title-casing words