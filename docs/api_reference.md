# API Reference

## String Utilities Module

### `reverse_string(input_str: str) -> str`

Reverse the given string.

#### Parameters

- **input_str** (`str`): The string to reverse.

#### Returns

- `str`: The reversed string.

#### Raises

- **TypeError**: If the input is not a string.

#### Description

This function takes a string as input and returns a new string with all characters in reverse order. The original string remains unchanged. The function uses Python's slice notation with a step of -1 to efficiently reverse the string.

#### Examples

**Basic usage:**
```python
from src.string_utils import reverse_string

result = reverse_string("hello")
print(result)  # Output: "olleh"
```

**Empty string:**
```python
result = reverse_string("")
print(result)  # Output: ""
```

**Single character:**
```python
result = reverse_string("a")
print(result)  # Output: "a"
```

**String with spaces:**
```python
result = reverse_string("hello world")
print(result)  # Output: "dlrow olleh"
```

**Unicode characters:**
```python
result = reverse_string("Hello, 世界")
print(result)  # Output: "界世 ,olleH"
```

**Error handling:**
```python
try:
    result = reverse_string(123)
except TypeError as e:
    print(e)  # Output: "Input must be a string"
```

#### Notes

- The function preserves all characters including whitespace, punctuation, and unicode characters.
- Time complexity: O(n) where n is the length of the string.
- Space complexity: O(n) for the reversed string.